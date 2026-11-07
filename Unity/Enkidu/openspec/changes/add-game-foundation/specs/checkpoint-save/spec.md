# Spec Delta

## Purpose

Defines automatic checkpoint saving so players can safely leave and resume Enkidu on desktop or mobile.

## ADDED Requirements

### Requirement: Automatic checkpoint saves
The game SHALL automatically save progress at designated checkpoints and when the player exits through a supported exit or backgrounding path. The player MUST not need to manually save to preserve the latest valid checkpoint.

#### Scenario: Player exits after reaching a checkpoint
- **WHEN** the player exits the game after a valid checkpoint is recorded
- **THEN** the next launch offers or performs a resume from that checkpoint

### Requirement: Safe resume placement
The game SHALL resume the player at a checkpoint location that is not inside immediate lethal or unavoidable danger. If the most recent transient state is unsafe, the game MUST fall back to the latest safe checkpoint.

#### Scenario: Player leaves while being pursued
- **WHEN** the player exits during a dangerous pursuit after a prior safe checkpoint
- **THEN** the next session resumes at the prior safe checkpoint rather than inside the active threat

### Requirement: Save integrity feedback
The game SHALL confirm successful automatic saves through an unobtrusive, accessible indicator and MUST retain the last valid save if a new save cannot complete.

#### Scenario: Save operation fails
- **WHEN** an automatic save cannot complete
- **THEN** the game preserves the last valid checkpoint and informs the player without corrupting it
