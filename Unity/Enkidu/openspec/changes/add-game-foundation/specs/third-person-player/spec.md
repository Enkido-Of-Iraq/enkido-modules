# Spec Delta

## Purpose

Defines the single-player third-person view and the core actions used to explore, evade danger, and interact with the world.

## ADDED Requirements

### Requirement: Third-person cinematic camera
The game SHALL use a camera positioned behind and above the player, following the player's travel direction while preserving the character and nearby hazards in view. The camera MUST avoid obstructing geometry where a clear view can be maintained.

#### Scenario: Player travels through a narrow space
- **WHEN** scenery would block the default behind-the-player view
- **THEN** the camera adjusts its position or framing to keep the player visible

### Requirement: Locomotion actions
The player SHALL be able to move carefully, run, and jump where level rules permit. Running MUST produce a meaningfully faster traversal state than careful movement.

#### Scenario: Player switches from careful movement to running
- **WHEN** the player activates run while movement is allowed
- **THEN** the character changes to the faster traversal state until the player cancels it or a mission rule prevents it

### Requirement: Hiding and cover
The player SHALL be able to enter designated hiding or cover spaces and receive clear feedback when the character is concealed or exposed.

#### Scenario: Player hides behind valid cover
- **WHEN** the player uses a designated hiding space
- **THEN** the game enters the concealed state and communicates that state without relying only on color

### Requirement: World interaction
The player SHALL be able to grab, collect, and inspect mission-relevant items when within the interaction range defined by the mission.

#### Scenario: Player collects a usable material
- **WHEN** the player interacts with an available crafting material
- **THEN** the material is removed from the world and added to the player's inventory with confirmation
