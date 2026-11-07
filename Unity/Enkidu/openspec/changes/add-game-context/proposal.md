# Proposal

## Why

Enkidu needs a durable project context before gameplay, environment, and character work expands. The Unity project currently has a starter scene and assets but no documented narrative, platform, asset-pipeline, or source-control constraints to guide future changes.

## What Changes

- Define Enkidu as a desktop and mobile survival-journey game about an 11-year-old boy travelling through southern Iraq in the 1990s, in the aftermath of the Gulf War.
- Establish tone and visual-direction guidance: a grounded, empathetic child-led journey in a historically informed southern Iraqi environment.
- Establish Unity as the game runtime and Blender as the authoring tool for 3D environment and character assets.
- Define an asset-pipeline expectation that Blender source assets and Unity-imported assets remain traceable to one another.
- Record GitHub synchronization as a project requirement. The current Unity folder is not a Git repository, so Git initialization and remote connection remain a prerequisite before synchronization can occur.

## Capabilities

### New Capabilities

None. This is project-context and workflow documentation only; it does not add runtime behavior.

### Modified Capabilities

None.

## Impact

- `openspec/config.yaml` will gain project guidance for future plans and implementation.
- Future Unity scenes, scripts, and Blender assets will use the defined setting, platform targets, and source-asset traceability rules.
- Git/GitHub setup is required before the stated synchronization workflow can be enforced.
