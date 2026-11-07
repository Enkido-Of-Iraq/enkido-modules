# Spec Delta

## Purpose

Defines Enkidu's linear mission structure and how survival abilities unlock across the boy's journey.

## ADDED Requirements

### Requirement: Linear mission structure
The game SHALL present a sequence of authored missions rather than an open world. Each mission MUST have a start state, player-readable objective, completion condition, and a transition to the next mission or hub.

#### Scenario: Player begins a mission
- **WHEN** the player starts a new mission
- **THEN** the game presents its immediate objective and confines progress to that mission's authored playable area

### Requirement: Challenge-gated progression
The game SHALL gate selected paths and objectives behind learned survival abilities or acquired tools, while clearly indicating the needed capability without requiring hidden knowledge.

#### Scenario: Player encounters a broken radio challenge
- **WHEN** the player interacts with a radio that requires repair
- **THEN** the game identifies the required repair capability or missing material and retains the objective for later completion

### Requirement: Persistent character development
The game SHALL retain unlocked practical abilities and earned crafting knowledge across mission transitions and safe checkpoint resumes.

#### Scenario: Player enters a later mission
- **WHEN** a player has unlocked fire-making in an earlier completed mission
- **THEN** fire-making remains available in later missions where it is permitted
