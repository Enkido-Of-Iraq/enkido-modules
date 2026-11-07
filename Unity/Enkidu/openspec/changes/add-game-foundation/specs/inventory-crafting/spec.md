# Spec Delta

## Purpose

Defines the player's inventory and practical crafting loop for solving survival and traversal challenges.

## ADDED Requirements

### Requirement: Inventory visibility
The game SHALL maintain an inventory of collected usable items and display each item's identity, available quantity when stackable, and relevant purpose when the player opens the inventory.

#### Scenario: Player reviews collected materials
- **WHEN** the player opens the inventory after gathering items
- **THEN** the game displays the materials available for mission use and crafting

### Requirement: Recipe-based crafting
The game SHALL allow the player to craft an available recipe only when its materials and any required learned ability are present. The crafting interface MUST explain unmet requirements.

#### Scenario: Player lacks a recipe material
- **WHEN** the player selects a recipe without all required materials
- **THEN** crafting does not occur and the missing materials are identified

### Requirement: Practical survival solutions
The crafting and progression system SHALL support non-graphic, context-appropriate survival solutions including fire-making, repairs to radios or engines, vehicle maintenance, and simple environmental traps or abstract defensive tools.

#### Scenario: Player repairs a mission vehicle
- **WHEN** the player has the required repair capability and materials at a repair objective
- **THEN** the game allows completion of the repair and updates the mission state

### Requirement: Persistent inventory state
The game SHALL preserve player inventory, learned recipes, and completed repair states in automatic saves and across mission transitions.

#### Scenario: Player resumes after a checkpoint
- **WHEN** the game resumes a saved checkpoint
- **THEN** the inventory and learned recipes match the saved checkpoint state
