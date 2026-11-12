# Tasks

## 1. Deterministic Mounted Baseline

- [ ] 1.1 Preserve the current `AnzuDesert` scene, mounted prefab, controller settings, and visual reference as a rollback baseline; verify the preserved scene opens and the current keyboard traversal still runs.
- [ ] 1.2 Replace reliance on load-time setup markers with explicitly serialized scene and prefab references; verify a clean Unity checkout opens `AnzuDesert` without requiring an `InitializeOnLoad` mutation to create the mounted player or camera.
- [ ] 1.3 Add a repeatable traversal fixture that can supply forward, steering, run, release, brake, and reverse inputs; verify it reports position, signed speed, locomotion state, and elapsed transition times.

## 2. Shared Input

- [ ] 2.1 Select one authoritative Unity Input System action asset and connect logical Move, Look, and Run actions to the mounted player; verify movement no longer reads `Keyboard.current` or legacy axes directly.
- [ ] 2.2 Bind WASD/arrows and the desktop run control to the shared actions; verify both keyboard layouts produce matching Move values and releasing run while moving returns the target state to Walking.
- [ ] 2.3 Add mobile virtual movement and camera controls plus a hold-to-run button bound to the same actions; verify Run remains active only while the button is held and releases immediately when the press ends.
- [ ] 2.4 Add input-adapter tests using deterministic values for desktop and mobile paths; verify equivalent action values produce identical locomotion intent.

## 3. Locomotion State and Movement

- [ ] 3.1 Introduce the authoritative Idle, Walking, Running, Stopping, and Reversing state owner with threshold hysteresis; verify the traversal fixture covers every permitted transition without frame-to-frame state flicker.
- [ ] 3.2 Implement signed forward speed with independently configurable acceleration, deceleration, active braking, walk speed, run speed, and reverse speed; verify forward input, reduced input, release, braking, and reverse meet the spec scenarios.
- [ ] 3.3 Implement creature-style yaw steering with separate moving and low-speed turn rates and no lateral strafe; verify forward turns follow Anzu's changing facing direction and rest turns produce negligible translation.
- [ ] 3.4 Integrate gravity and `CharacterController` grounding without changing the signed horizontal state; verify the mounted pair remains grounded and can traverse the test surface without accumulating vertical drift.
- [ ] 3.5 Add play-mode movement tests for acceleration, proportional input, run release, stopping, forward-to-reverse braking, reverse limit, and steering; verify all movement tests pass in a non-interactive Unity test run.

## 4. Mounted Animation Presentation

- [ ] 4.1 Connect one animation presentation adapter to the authoritative locomotion state and actual signed speed while keeping Enkidu and Anzu on one playback clock; verify each state produces an observable animation response.
- [ ] 4.2 Neutralize imported animated-root displacement so gameplay translation remains on the controller root; verify the animated hierarchy does not separate from the collider during the traversal fixture.
- [ ] 4.3 Bound gait cadence changes during acceleration, stopping, and reverse and preserve the idle pose at rest; verify playback has no sudden cadence jumps and the rider remains aligned for a sixty-second mixed traversal.
- [ ] 4.4 Document the visual limitations of the single prototype gait and the required future idle, walk, run, stop, and reverse clips; verify the review notes distinguish first-slice acceptance from final animation quality.

## 5. Third-Person Mounted Camera

- [ ] 5.1 Add a stable mounted camera target on the gameplay root and configure Cinemachine follow damping and full-pair framing; verify acceleration, turning, stopping, and reverse keep Enkidu and Anzu visible together.
- [ ] 5.2 Connect Look input to independent camera orbit with configured pitch limits; verify camera orbit does not change Anzu's steering and cannot exceed its vertical bounds.
- [ ] 5.3 Add delayed smooth recentering toward Anzu's travel direction and suspend it during active Look input; verify the camera does not fight continuous player orbit and recenters after release.
- [ ] 5.4 Add camera play-mode coverage for damping, orbit independence, pitch clamping, and recenter delay; verify the camera tests pass in a non-interactive Unity test run.

## 6. Desktop and Mobile Performance Gate

- [ ] 6.1 Define the sixty-second traversal sequence and evidence template with build, device, median frame rate, frame time, memory where available, and dominant CPU/GPU or rendering cost; verify desktop and mobile runs use the same route and input timing.
- [ ] 6.2 Profile the unchanged mounted asset in a desktop development build; verify the evidence records whether the median reaches 60 FPS and identifies the dominant cost.
- [ ] 6.3 Select and document the representative midrange mobile device, then profile a device build; verify the evidence records whether the median reaches 30 FPS plus frame time, memory, and dominant rendering cost.
- [ ] 6.4 If either target is missed, apply bounded first-slice cleanup to duplicate or hidden renderers, equivalent materials, shadow participation, or mounted LOD usage; verify before/after evidence and visual review show the target improvement without breaking rider/creature appearance.
- [ ] 6.5 Re-run the desktop and mobile traversal after cleanup; verify both target results and any remaining asset-reduction blocker are recorded without weakening the acceptance thresholds.

## 7. Integrated Acceptance

- [ ] 7.1 Run the complete mounted-traversal scenario in `AnzuDesert` with keyboard controls; verify walk, run, steering, stopping, reverse, animation, and camera satisfy every desktop scenario in the spec.
- [ ] 7.2 Run the same scenario with the mobile control UI on the selected device; verify virtual movement, camera orbit, and hold-to-run satisfy every mobile scenario in the spec.
- [ ] 7.3 Verify a clean checkout imports and opens the serialized playable slice, all Unity tests pass, the performance evidence is present, and `openspec validate add-anzu-mounted-movement --strict` succeeds.

## Workflow follow-up

- Archive `add-anzu-mounted-movement` after implementation, performance evidence, and visual review are accepted.
- Sync the mounted-traversal capability into the durable project specs during archive.
