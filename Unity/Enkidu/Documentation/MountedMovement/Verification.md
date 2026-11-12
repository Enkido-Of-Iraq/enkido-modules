# Verification — 2026-11-12

Unity 6000.5.10f1 compiled and executed MountedSliceSetup.Configure successfully. The saved scene references the mounted player prefab, shared input, mobile controls and Cinemachine camera.

Automated results: 7/7 EditMode tests passed; 4/4 PlayMode tests passed. Coverage includes acceleration, proportional target speed, run release, stopping, braking before reverse, reverse limit, state hysteresis, injected input equivalence, rest steering, basic horizontal state during grounding, orbit independence, pitch limits and recenter delay. These small tests do not establish full scene acceptance or real touch-device behavior.

Strict OpenSpec validation passed. The large scene diff moves the mounted hierarchy into Assets/Prefabs/MountedAnzuPlayer.prefab.

Outstanding acceptance: preserved baseline visual/keyboard review; clean-checkout import; complete scene traversal and 60-second rider alignment review; real keyboard/mobile action delivery; camera damping/framing review; desktop development-build performance and physical midrange mobile performance. No measured FPS or mobile acceptance is claimed. Task checkboxes remain open where their full verification criteria have not been met.

Known follow-up checks: review camera recenter direction with the selected Cinemachine binding mode, pointer-delta versus stick-rate sensitivity, input execution order and touch control switching. The traversal fixture currently exercises a shorter functional route; the documented 60-second performance sequence still needs automated capture.
