# Design

## Context

See `proposal.md` for motivation and `specs/mounted-traversal/spec.md` for behavior. The current `AnzuDesert` prototype uses a `CharacterController`, directly polls the keyboard, drives a fixed-offset `Camera`, and labels locomotion state while speed-scaling one combined legacy animation take. The synchronized mounted FBX is approximately 223 MB and the scene contains hundreds of renderers and materials, so mobile performance is a first-order constraint.

The repository also contains two existing Input System assets and Cinemachine. The implementation should use those installed systems rather than adding another input or camera dependency.

## Goals / Non-Goals

**Goals:**

- Separate input intent, locomotion simulation, locomotion state, animation presentation, and camera presentation while keeping one authoritative state.
- Make desktop and mobile controls interchangeable through the same action values.
- Preserve the combined rider-and-creature asset so Enkidu cannot drift from Anzu during the first slice.
- Produce deterministic scene and prefab assets that do not depend on one-shot editor scripts running on load.
- Establish a repeatable performance sequence and evidence format for desktop and mobile.

**Non-Goals:**

- Build a general mount framework or support switching between mounted and unmounted controllers.
- Replace the creature rig, author final animation clips, or solve every mobile asset cost in this change.
- Add gameplay systems beyond traversal or support arbitrary steep terrain and airborne movement.

## Decisions

### Use signed forward speed with creature-style steering

The controller will maintain a signed scalar speed along Anzu's forward axis. Forward input selects a positive walk or run target; backward input first drives positive speed toward zero and then selects a limited negative target. Horizontal input changes yaw and never creates lateral translation.

This matches the weight and anatomy of a ridden creature and avoids requiring strafe animations. Camera-relative omnidirectional movement was considered but rejected because it would make Anzu slide sideways and would couple camera orbit to steering.

### Separate acceleration, deceleration, braking, and turn tuning

Movement will expose distinct tuning values for acceleration, passive deceleration, active braking, reverse speed, moving turn rate, and low-speed turn rate. Speed will approach its target continuously, and small dead zones plus stop/run thresholds will prevent state flicker.

A single acceleration value was considered but rejected because starting, releasing input, and actively braking need different weight and responsiveness.

### Derive one locomotion state from intent and actual motion

One state owner will resolve `Idle`, `Walking`, `Running`, `Stopping`, and `Reversing` from input intent, signed actual speed, and thresholds. Animation, sound hooks, camera tuning, UI, and automated validation will read this state rather than deriving parallel states.

State transitions will use speed thresholds with hysteresis so a value near zero or the run boundary cannot alternate every frame. A collection of independent booleans was considered but rejected because contradictory combinations such as running and stopping would remain possible.

```text
                       +---------+
                +----->| Walking |-----+
                |      +---------+     |
                |          |           |
                |          v           |
+------+        |      +---------+     |       +----------+
| Idle |--------+      | Running |     +------>| Stopping |
+------+               +---------+             +----------+
   ^                        |                       |   |
   |                        +-----------------------+   |
   |                                                    v
   +--------------------------------------------+  +-----------+
                                                +--| Reversing |
                                                   +-----------+
```

### Consume Unity Input System actions through one input adapter

The mounted controller will consume logical Move, Look, and Run values supplied by one input adapter. Desktop bindings and mobile on-screen controls will feed those same actions. Automated tests may substitute deterministic action values without introducing a second movement implementation.

The mobile run control will be hold-to-run, matching the momentary desktop run input. Releasing it while forward movement continues returns the target state to Walking rather than retaining a toggle state.

Direct `Keyboard.current` polling was considered but rejected because it excludes mobile controls and makes simulation tests a special case. A separate mobile controller was considered but rejected because it would duplicate locomotion behavior.

### Use Cinemachine for mounted camera presentation

A mounted camera target will be attached to the gameplay root, not to an animated bone. Cinemachine will provide orbit, follow damping, pitch limits, and recentering while Look input controls orbit independently from locomotion. Camera configuration will keep the full rider-and-creature silhouette framed across idle, acceleration, turning, and stopping.

Continuing the custom `LateUpdate` camera was considered but rejected because it lacks orbit, vertical limits, collision extension points, and consistent damping controls already available in the installed camera package.

### Keep the combined FBX as one animation authority for the first slice

Animation presentation will operate on the combined Enkidu-and-Anzu hierarchy so both subjects share the same playback clock and mount relationship. The adapter will respond to locomotion state and actual speed, hold an idle pose at rest, and bound cadence changes during acceleration and deceleration. Gameplay translation remains on the controller root; animated root displacement is neutralized to prevent double movement.

Splitting rider and creature animation in this slice was rejected because it creates phase and mount-point drift risk. Converting the entire art pipeline to a new rig or Animator setup is deferred until distinct production idle, walk, run, stop, and reverse clips exist.

### Treat performance as a measured gate with bounded asset cleanup

The same scripted sixty-second traversal will be captured on desktop and the selected mobile device. The evidence will include build/device identity, median frame rate, frame time, memory on mobile, and dominant CPU/GPU or rendering cost.

The current asset will first be measured unchanged. If it misses the target, this change may consolidate equivalent materials, disable non-gameplay duplicate or hidden renderers, adjust shadow participation, and add a first-slice LOD or simplified mounted prefab. Full production retopology and final texture atlasing remain separate art work.

Assuming the current asset is acceptable without measurement was rejected because its file size, renderer count, and material count already indicate a high mobile risk.

### Replace load-time scene mutation with explicit serialized setup

The completed scene, mounted prefab, input references, camera, and validation fixtures will be saved explicitly. Existing one-shot `InitializeOnLoad` setup scripts and marker files may be used only to understand the prototype; the playable slice will not depend on them mutating the scene when the editor opens.

Keeping automatic setup scripts active was rejected because their behavior depends on editor timing and local marker files, which makes a clean checkout difficult to reproduce.

## Risks / Trade-offs

- [The single current gait cannot convincingly represent idle, walk, run, stop, and reverse] -> Bound playback behavior for the first slice, document visual limitations, and keep distinct production clips as required follow-up art.
- [The mounted FBX may miss the mobile frame and memory target even after bounded cleanup] -> Record the failed profile honestly and create a separate asset-reduction change rather than weakening the target silently.
- [Braking and steering can feel correct numerically but wrong at creature scale] -> Keep movement values serialized and validate them with repeated controller tests plus hands-on play review.
- [Camera recentering can fight the player's orbit input] -> Apply a delay after Look input, use smooth recentering, and suspend recentering while input remains active.
- [Legacy animation and gameplay translation can both move the root] -> Keep gameplay motion on the controller root and neutralize imported root displacement in the presentation layer.
- [Two existing input assets can create binding confusion] -> Select one authoritative action asset for the mounted slice and reference it explicitly from the scene and mobile UI.

## Migration Plan

1. Capture the current `AnzuDesert` scene and mounted prefab as the baseline and preserve the existing controller for rollback.
2. Add the shared input adapter and locomotion state owner, then replace direct keyboard polling while keeping keyboard behavior available.
3. Move gameplay translation and steering to the signed-speed controller and validate state transitions before connecting presentation.
4. Attach animation and Cinemachine presentation to the authoritative gameplay root and state.
5. Add mobile on-screen controls and run the same movement validation through desktop and mobile action paths.
6. Measure the unchanged asset, apply only the bounded first-slice optimizations needed, and record final desktop/mobile evidence.
7. Remove the scene's dependency on load-time mutation scripts after the serialized setup is verified in a clean checkout.

Rollback consists of restoring the preserved scene/prefab and previous controller component; no saved-game or network data migration is involved.

## Open Questions

- Which physical midrange mobile device will serve as the first acceptance target?
