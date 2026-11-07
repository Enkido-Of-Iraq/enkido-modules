# Tasks

## 1. Project Context

- [ ] 1.1 Add the approved Enkidu narrative, 7+ content-rating, desktop/mobile, Unity, Blender, and Iraqi Arabic–influenced dialogue constraints to `openspec/config.yaml`; verify `openspec context --json` resolves from the Unity root.
- [ ] 1.2 Add a concise project-context document that distinguishes historically informed setting guidance from final historical claims; verify it is linked from the project documentation or OpenSpec context.

## 2. Asset Pipeline

- [ ] 2.1 Create the Blender-source and Unity-runtime asset folder convention, including a documented naming rule for matching source and export files; verify a sample asset pair can be located by its shared base name.
- [ ] 2.2 Add an asset manifest format that records source file, exported Unity asset, owner, and import status; verify the existing Iraq marshland kit can be represented without ambiguous paths.
- [ ] 2.3 Document Unity 6 import expectations for Blender-derived assets, including scale, axis, materials, and mobile performance review; verify the guidance is usable for a new FBX import.

## 3. Source Control and GitHub

- [ ] 3.1 Initialize Git at the Enkidu Unity-project root and add a Unity-appropriate `.gitignore` that tracks `Assets`, `Packages`, `ProjectSettings`, OpenSpec artifacts, and approved source assets while excluding generated folders; verify `git status --ignored` excludes `Library`, `Temp`, and `Logs`.
- [ ] 3.2 Connect the user-confirmed owner URL for the `AnkiDo` GitHub repository as `origin`; verify `git remote -v` reports the intended fetch and push URL.
- [ ] 3.3 Create the initial source-control commit containing the project context, asset-pipeline documentation, and required Unity project files; verify the commit has no unintended generated files.

## 4. Integration Review

- [ ] 4.1 Validate that OpenSpec context, the asset manifest, and Git tracking agree on the first Blender-to-Unity asset pair; verify with `openspec validate add-game-context --strict` and a clean Git status after the planned files are committed.

## Workflow follow-up

- Archive the change after the context and source-control setup has been reviewed and applied.
