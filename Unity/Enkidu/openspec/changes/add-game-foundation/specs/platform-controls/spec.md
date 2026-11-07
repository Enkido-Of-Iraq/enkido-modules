# Spec Delta

## Purpose

Defines equivalent core gameplay controls for desktop and mobile versions of Enkidu.

## ADDED Requirements

### Requirement: Desktop control support
The desktop version SHALL support keyboard-and-mouse controls and controller controls for movement, camera, running, jumping, hiding, interaction, inventory, and pause.

#### Scenario: Player uses a controller on desktop
- **WHEN** a supported controller is active on desktop
- **THEN** the player can perform every required core action without switching to keyboard or mouse

### Requirement: Mobile control support
The mobile version SHALL provide touch controls for movement, camera, running, jumping, hiding, interaction, inventory, and pause. Controls MUST remain reachable on common portrait and landscape safe areas used by supported devices.

#### Scenario: Player performs a core action on mobile
- **WHEN** the player uses the configured touch controls
- **THEN** the corresponding core gameplay action is available without an external controller

### Requirement: Shared action semantics
The game SHALL preserve the same action meanings, mission outcomes, and save behavior across desktop and mobile, even where the control presentation differs.

#### Scenario: Player completes an interaction on either platform
- **WHEN** the player activates an available world interaction using desktop or mobile controls
- **THEN** the game produces the same interaction result
