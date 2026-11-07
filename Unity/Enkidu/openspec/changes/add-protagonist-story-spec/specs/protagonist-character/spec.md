# Spec Delta

## Purpose

Defines Enkidu's 11-year-old protagonist as a visually memorable, emotionally credible, and playable child at the center of the journey.

## ADDED Requirements

### Requirement: Character artwork identity
The protagonist SHALL be depicted as an 11-year-old Iraqi boy with a thin, small, healthy body and an expressive face. His artwork MUST communicate alertness, curiosity, resilience, and vulnerability without depicting illness or physical incapacity.

#### Scenario: Character is reviewed in a neutral pose
- **WHEN** the protagonist is viewed in character art or a Unity model preview
- **THEN** he reads as a healthy child with a modest build, childlike proportions, and a distinctive, readable silhouette

### Requirement: Emotionally readable performance
The character SHALL communicate fear, hope, grief, concentration, curiosity, relief, and determination through facial expression, pose, idle motion, and animation without relying only on dialogue.

#### Scenario: Character discovers a lead about his father
- **WHEN** the player finds credible information about the father
- **THEN** the character performance visibly communicates renewed attention and determination

### Requirement: Child-scaled traversal
The protagonist SHALL use his smaller body as a gameplay strength: he can move quickly, hide in child-sized safe spaces, and reach routes unavailable to larger characters. This MUST not imply superhuman strength.

#### Scenario: Player approaches a narrow hiding route
- **WHEN** the player enters a route designated for the child
- **THEN** the character can use it while larger adult characters cannot follow through that route

### Requirement: Learned practical competence
The protagonist SHALL gain practical abilities through observation, helping others, collected clues, and mission experiences. Growth MUST reflect quick learning and intelligence rather than sudden unexplained mastery.

#### Scenario: Player completes a guided repair encounter
- **WHEN** the character learns a repair method from a mission encounter
- **THEN** that skill becomes available for later compatible challenges

### Requirement: Cohesive production artwork
The Blender character source, rig, animation set, Unity model import, materials, and LODs SHALL preserve the approved silhouette, facial readability, and key costume details across supported quality settings.

#### Scenario: Character runs on mobile quality settings
- **WHEN** the protagonist is rendered on the mobile quality tier
- **THEN** his face, silhouette, movement state, and interaction cues remain recognizable
