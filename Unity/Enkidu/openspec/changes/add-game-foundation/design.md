# Design

## Context

The project is a Unity 6.0.5 URP project. Its installed packages already include Cinemachine 3.1.6, Input System 1.20.0, and Accessibility modules; the present Assets structure contains imported environment art and a starter scene but no dedicated game-runtime architecture. See `proposal.md` for motivation and the capability specs for required behavior.

## Goals / Non-Goals

**Goals:**

- Create a reusable foundation that lets each authored mission share the same player, input, inventory, save, and visual-quality rules.
- Make desktop and mobile first-class while allowing platform-specific control layouts and scalable visual detail.
- Keep the initial runtime modular enough for future scene, NPC, dialogue, accessibility, and quest specifications.

**Non-Goals:**

- Build the opening mission, combat, enemy AI, final UI art, final character assets, or final platform/device matrix in this change.
- Promise photorealism or recreate a specific commercial game's camera behavior; the reference is cinematic intent, not copied content.
- Provide real-world weapon or explosive construction guidance. Crafted defensive tools remain abstract, game-safe interactions.

## Decisions

### Mission scenes use a shared runtime layer

Each mission will load its authored scene content with a shared persistent runtime layer for player state, mission state, save data, input, and UI services. This avoids each scene rebuilding foundations or losing progress during transitions.

Alternative considered: put all systems in every scene. Rejected because it risks duplicated configuration and inconsistent saves.

### Cinemachine owns framing; player movement owns travel

Use Cinemachine for a configurable behind-and-above follow camera with obstruction handling. Player movement exposes camera targets and state but does not contain camera policy, allowing the same player to work in confined interiors and wide environments.

Alternative considered: a fixed camera or custom camera code embedded in the player. Rejected because it cannot consistently support cinematic framing and mission-specific tuning.

### One semantic action map, platform-specific bindings

Define actions such as Move, Look, Run, Jump, Hide, Interact, Inventory, and Pause once, then bind them to keyboard/mouse, controller, and touch layouts. Missions consume actions rather than device inputs.

Alternative considered: separate desktop and mobile gameplay controllers. Rejected because it would create divergent outcomes and duplicate testing.

### Data-driven progression, inventory, and recipes

Items, recipes, learned abilities, mission locks, and interaction requirements will be data assets or serializable data, not hard-coded scene behavior. A mission declares what it needs; the shared systems decide whether the player qualifies.

Alternative considered: bespoke scripts for every puzzle. Rejected because reused repair, crafting, and skill conditions would become difficult to maintain.

### Safe checkpoint snapshots are authoritative

The save model records the latest explicitly safe checkpoint plus persistent player state: completed mission state, inventory, learned abilities, recipes, and completed repairs. Temporary threat state is not a resume point. Save writes are atomic: a last-known-good save stays usable if a newer write fails.

Alternative considered: saving the exact location whenever the application closes. Rejected because it can return a player to unavoidable danger.

### Art direction is defined by readable atmosphere

Blender-authored assets and Unity materials will prioritize silhouette, surface texture, palette, directional light, fog, particles, and environmental storytelling. Quality levels can reduce secondary density, shadows, or post-processing, but never obscure navigation or interactions.

Alternative considered: high-density asset detail as the main quality target. Rejected because it compromises mobile performance and is not the intended visual priority.

## Risks / Trade-offs

- [Desktop and mobile performance needs differ] → Establish quality tiers and profile representative missions before producing large asset batches.
- [Cinematic camera can hide hazards in small spaces] → Test all mission routes with obstruction and player-visibility scenarios.
- [Automatic saves can be corrupted by interrupted writes] → Keep versioned, validated last-known-good checkpoint data.
- [Crafting can distract from the story] → Keep recipes limited to mission-relevant survival choices and surface requirements clearly.
- [A 7+ audience needs tension without distressing detail] → Use implication, framing, audio restraint, and non-graphic failure feedback; review individual scenes before production.

## Migration Plan

1. Add the shared runtime foundation alongside the existing starter content.
2. Build a small vertical-slice mission that exercises movement, camera, interaction, inventory, a gated repair, and safe checkpoint resume.
3. Profile that slice on representative desktop and mobile hardware before converting further art and mission content.
4. Roll back a foundation subsystem by retaining the previous valid scene and checkpoint data format until migration is verified.

## Open Questions

- Which operating systems, mobile device tiers, target frame rates, and offline/cloud-save policy define the first release? These are deferred until the foundation is ready to be implemented and profiled.
