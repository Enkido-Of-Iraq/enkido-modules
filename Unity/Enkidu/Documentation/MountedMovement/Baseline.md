# Mounted traversal rollback baseline

The pre-change `AnzuDesert` scene, mounted hierarchy, controller settings, and combined rider/creature visual are preserved in Git commit `8d78593`.

Baseline controller values were walk speed `0.7`, run speed `9`, acceleration `4`, and turn speed `150`. The controller used a `CharacterController`, read WASD/arrows plus Shift directly, and kept the existing combined FBX animation and fixed-offset camera together in `AnzuDesert`.

Rollback is performed by restoring the scene, `EnkiduRidingAnzu.prefab`, and `MountedAnzuController.cs` from that commit. Do not overwrite the source FBX or artwork when comparing the new slice.
