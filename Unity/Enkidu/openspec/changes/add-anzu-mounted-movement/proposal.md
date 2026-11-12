# Proposal

## Why

The existing Anzu scene proves that the combined rider-and-creature asset can move, but its controller is a keyboard-only prototype with one gait clip, a fixed camera, and no mobile input or explicit locomotion contract. The project needs a small, testable mounted-traversal slice before expanding into mounting, combat, flight, or larger environments.

## What Changes

- Make `AnzuDesert` a playable mounted-movement test scene with Enkidu already riding Anzu.
- Add forward movement, braking and slow reverse, left/right creature steering, walking, running, stopping, and return to idle.
- Give acceleration, deceleration, reverse speed, and turning independently configurable values so Anzu carries believable weight.
- Route keyboard and mobile controls through shared Unity Input System actions; support WASD and run input on desktop plus a virtual movement stick and run button on mobile.
- Add an orbiting third-person camera with damping, vertical limits, and recentering around the mounted pair.
- Establish one authoritative locomotion state used by movement, the synchronized rider-and-creature animation, sound hooks, camera behavior, and UI.
- Measure the test scene on desktop and a representative midrange mobile device, recording frame rate and the dominant rendering costs.
- Keep mounting/dismounting, jumping, flight, combat, stamina, networking, advanced terrain traversal, and final production animation or asset optimization outside this first slice.

## Capabilities

### New Capabilities

- `mounted-traversal`: Player-controlled traversal while Enkidu is mounted on Anzu, including locomotion states, steering, desktop/mobile input, synchronized animation, third-person camera behavior, and performance acceptance for the playable test slice.

### Modified Capabilities

None.

## Impact

- Replaces the direct keyboard polling and fixed camera behavior in the mounted movement prototype.
- Affects the `AnzuDesert` scene, the mounted controller, Unity Input System assets, mobile UI, mounted animation playback, camera configuration, and movement validation.
- Uses the existing combined Enkidu/Anzu FBX as the first-slice animated asset; distinct production-quality idle, walk, run, and transition clips remain follow-up art work.
- Requires performance profiling because the current mounted asset is approximately 223 MB and contains hundreds of renderers and materials, making mobile viability an explicit risk.
