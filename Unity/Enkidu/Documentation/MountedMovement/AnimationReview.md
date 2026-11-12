# Mounted animation review

The first playable slice intentionally uses the existing single combined Enkidu-and-Anzu animation take. Both characters share one legacy `Animation` clock, so the rider cannot drift out of phase with the creature. Gameplay movement stays on the `CharacterController` root, while the imported animated root is restored to its initial local position and rotation every frame.

This is acceptable for testing movement synchronization, cadence smoothing, and mounted alignment. It is not final animation quality: idle currently holds the gait at rest, reverse plays the prototype take backward, and walking, running, stopping, and reversing do not have distinct authored transitions.

Production follow-up requires dedicated idle, walk, run, stop, and reverse clips on the combined rig (or a validated paired-rig solution), including transition poses and foot-contact review.
