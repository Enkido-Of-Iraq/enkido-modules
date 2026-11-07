# Design

## Context

The Unity project is set up for URP, Cinemachine, the Input System, and mobile/desktop work, but it has no approved player-character production package or authored narrative structure. The existing foundation proposal defines shared movement, crafting, safe save, camera, and mission systems. This design connects those systems to the boy and his father-search story.

## Goals / Non-Goals

**Goals:**

- Give artists, animators, level designers, writers, and programmers one consistent protagonist reference.
- Make the boy's age, physique, emotional range, and learned competence visible in both artwork and gameplay.
- Turn story information into playable goals, environmental clues, travel sequences, and recovery moments.
- Protect the 7+ tone while preserving emotional weight and historical atmosphere.

**Non-Goals:**

- Finalize the father's fate, the complete number of chapters, voice casting, or all supporting characters.
- Produce Blender meshes, Unity scenes, final dialogue, cinematics, or gameplay code during this planning change.
- Recreate a particular reference image or real person's likeness; all approved production art will be original.

## Decisions

### Maintain one character production packet

Create a versioned production packet that contains approved turnaround art, silhouette notes, costume states, expression sheet, materials palette, scale reference, animation list, and Unity import checklist. Blender and Unity changes must trace back to this packet.

Alternative considered: letting each asset or scene define its own visual interpretation. Rejected because the boy's readability and emotional continuity would drift.

### Tie skill unlocks to witnessed learning

Each new practical ability is introduced through a situation, guide, found note, or observed action, then reinforced with a player-controlled use shortly afterward. Mission design records the narrative source of the ability alongside the gameplay unlock.

Alternative considered: granting abilities only through a generic progression menu. Rejected because it weakens the boy's intelligence and the story's emotional logic.

### Tell the journey through a playable chapter graph

Story beats are represented as chapters with an entry goal, a place, key encounter types, a clue or emotional shift, a safe checkpoint, and an exit transition. Buses, towns, and other travel segments connect chapters without turning the game into an open world.

Alternative considered: a linear film sequence between missions. Rejected because travel and encounters are central to the player's relationship with Iraq and the boy.

### Use suspense grammar instead of direct depiction

Threats are communicated through spatial design, dialogue cues, off-screen sound, expression, lighting, trusted adults, and escape routes. The player responds with agency—observe, hide, flee, seek help, or solve an environmental obstacle.

Alternative considered: direct depictions of violence or adult exploitation. Rejected because it conflicts with the 7+ rating and the protagonist's intended emotional safety.

### Preserve a growing visual story in the costume

The boy's base silhouette remains consistent, while reversible costume wear, dust, small repairs, backpack contents, and posture changes show the length of the journey. Changes must not make him look ill or impede readability.

Alternative considered: a completely different design per chapter. Rejected because it obscures character recognition and complicates production.

## Risks / Trade-offs

- [A child protagonist may feel passive] → Tie every tense story beat to a clear observation, choice, escape, or practical solution controlled by the player.
- [Historical subject matter can be oversimplified] → Use research review and cultural consultation before final writing or asset approval.
- [Dark themes may exceed the stated age rating] → Review scripts, cinematics, audio, and failure states against the age-appropriate tension spec before acceptance.
- [High-quality facial emotion costs performance] → Define LODs and animation budgets early; preserve eyes, brows, silhouette, and key gesture readability first.
- [Narrative scope may become too large] → Treat the initial game as a vertical chapter sequence and write later regions as separate changes.

## Migration Plan

1. Approve the character production packet and create an original Blender blockout before detailed modeling.
2. Produce a Unity test prefab with placeholder materials, rig, and a short emotional-motion set.
3. Build one travel-and-clue vertical slice that tests a helper encounter, a danger escape, a learned skill, and a safe recovery checkpoint.
4. Review the slice for visual consistency, cultural care, age suitability, and performance before adding later chapters.
