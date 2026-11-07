# Proposal

## Why

Enkidu needs an agreed gameplay foundation before individual scenes, characters, and assets are built. The project is already a Unity 6 Universal Render Pipeline project with Cinemachine and the Input System available, but it does not yet define the core player experience, mission structure, or safe-save behavior.

## What Changes

- Define Enkidu as a single-player, mission-based third-person survival journey for desktop and mobile; it is not an open-world game.
- Establish an over-the-shoulder, behind-and-above camera with cinematic framing that supports exploration, danger, hiding, and interaction.
- Define the player action baseline: careful movement, running, jumping, hiding, grabbing and collecting usable items.
- Define inventory, crafting, and level-to-level character progression for practical survival solutions such as fire-making, repairing radios and engines, vehicle repair, simple traps, and abstract game-safe defensive tools.
- Define automatic checkpoint saving and a resume rule that never places the player directly into immediate danger.
- Establish the visual direction: accessible, high-quality stylized presentation of 1990s southern Iraq using restrained geometry and a strong focus on color, materials, textures, lighting, and atmosphere.
- Establish desktop keyboard/controller and mobile touch controls as equal supported inputs.

## Capabilities

### New Capabilities

- `mission-progression`: Linear mission structure, objectives, gated challenges, and level-to-level player development.
- `third-person-player`: Single-player movement, hiding, jumping, interaction, and camera behavior.
- `inventory-crafting`: Item collection, inventory management, recipes, crafted survival tools, and skill-gated repairs.
- `checkpoint-save`: Automatic checkpoint saving, safe resume placement, and cross-platform save expectations.
- `platform-controls`: Desktop and mobile input support for the core player actions.
- `visual-direction`: Art-direction constraints for a recognizable, performance-aware 1990s southern-Iraq setting.

### Modified Capabilities

- None.

## Impact

- Affects future Unity scenes, player prefabs, Input System action maps, Cinemachine camera setup, save-data services, UI, animation, and gameplay tests.
- Guides Blender asset production and the Unity import pipeline; no Unity implementation is included in this planning change.
- Uses already-installed Unity packages: Universal Render Pipeline, Cinemachine, Input System, and Accessibility modules.
