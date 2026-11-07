# Design

## Context

See `proposal.md` for motivation. Enkidu is a Unity 6 project with URP, the Input System, and Cinemachine available. It currently contains `GetStarted_Scene`, imported art and prefab assets, and no Git repository or GitHub remote. OpenSpec is now initialized at the Unity-project root.

## Goals / Non-Goals

**Goals:**

- Make the narrative, setting, technical targets, and asset-pipeline constraints available to all future OpenSpec changes.
- Keep Unity source assets and Blender source files traceable through a predictable naming and folder convention.
- Establish the source-control work needed to synchronize the Unity project with a user-selected GitHub repository.

**Non-Goals:**

- Implement player movement, combat, survival systems, story content, or final levels.
- Produce final character or environment artwork.
- Create a GitHub repository, push commits, or configure credentials without the user providing the intended repository and authorization.

## Decisions

### Store enduring project constraints in `openspec/config.yaml`

The OpenSpec context will identify Enkidu, its southern-Iraq 1990s survival-journey setting, supported platforms, Unity/Blender responsibilities, and GitHub synchronization requirement. This makes the facts available to future proposals without coupling them to a single feature.

Alternative considered: maintain a standalone design brief only. Rejected because OpenSpec workflows would not automatically apply it to subsequent planning.

### Keep source and runtime art traceable by name

Blender source files will be stored in a dedicated source-art location and exported runtime assets will live under Unity `Assets/Art`. Matching base names and a small asset manifest will identify each Blender source and Unity import. Unity-ready exports will use formats suitable for the target asset type, such as FBX for static meshes.

Alternative considered: store only Unity imports. Rejected because it prevents non-destructive revisions to 3D assets.

### Treat desktop and mobile as first-class targets

Future gameplay and scene proposals must state input, performance, and UI implications for both desktop and mobile. Shared gameplay systems should use Unity's Input System rather than device-specific direct input.

Alternative considered: target desktop first and port later. Rejected because late mobile constraints would reshape controls, performance budgets, and UI.

### Establish GitHub synchronization through Git at the Unity-project root

The Unity root will become the repository root, with a Unity-appropriate `.gitignore`. Versioned content will include `Assets`, `Packages`, `ProjectSettings`, OpenSpec artifacts, and Blender source assets. Generated folders such as `Library`, `Temp`, `Logs`, and build outputs will be excluded. The intended GitHub host is the `AnkiDo` repository; its exact owner and remote URL must be confirmed before a remote is added.

Alternative considered: synchronize generated Unity folders or store the project outside Git. Rejected because generated files create noisy, non-portable history and undermine collaboration.

### Use a child-safe Iraqi Arabic–influenced dialogue style

The game will target ages 7+ and use strong, emotionally direct language without adult profanity or adult themes. Dialogue and localization planning will retain an Iraqi Arabic–influenced voice where appropriate, while UI and support text must remain understandable for the selected release languages.

Alternative considered: treat dialogue tone as an unbounded artistic decision. Rejected because content-rating constraints need to shape narrative work from the outset.

## Risks / Trade-offs

- [A single reference image can lead to historically or geographically inaccurate art] → Research references and review visual decisions before finalizing environments, clothing, dialogue, or cultural details.
- [Desktop/mobile parity can constrain visual fidelity] → Set mobile performance budgets before adding high-cost shaders, scenes, or asset density.
- [Blender files are large and binary] → Keep source assets organized, avoid duplicate exports, and adopt Git LFS only when file size or collaboration needs justify it.
- [No GitHub remote is currently configured] → Obtain the AnkiDo repository URL and access before attempting synchronization.
- [Iraqi Arabic–influenced dialogue may be misunderstood outside its intended audience] → Have native-speaker review and localization checks before release.

## Migration Plan

1. Add the approved game context to `openspec/config.yaml`.
2. Establish the source-art/export convention and document the asset manifest format.
3. Initialize Git at the Unity root, add the Unity `.gitignore`, and connect the user-selected GitHub remote.
4. Validate the first synchronized Unity scene and Blender asset pair before expanding the game.

