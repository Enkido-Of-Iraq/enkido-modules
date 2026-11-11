Enkidu / Anzu mounted walk, v04
Source models: Enkidu character/backpack rig v13 and Anzu wings-only v10.
Reference: exec-a780294b-ee61-4f89-9934-dbeedb4aef51.png.
Animation specification: openspec/specs/3d-animation/spec.md.
192 frames, 24 fps, 8 seconds, 1000 x 1000.
Forward axis -Y. Root Z remains exactly 0. Travel 3.438 scene units.
Foot stance uses world-space cancellation; swing lifts ankle about 0.24 units.
Legacy IK constraints are muted in the seated pose.
Rider is bone-parented to rider_mount with a seated pose and backpack.
Camera tracks from a three-quarter view. Head/wings/tail have restrained motion.
LIMITATIONS: This is a stylized animation prototype. Existing Anzu geometry
is simplified, with two walking legs and talon arms. It does not yet match
the four-legged anatomy, realistic sculpt, or detailed feathers of the supplied
concept. Anzu uses rigid part bone attachments; Enkidu uses weighted clothing
and rigid head/hair attachments. Not a production-ready deforming creature.
Original models are preserved.

Video is a Workbench material-color motion preview, not a final textured render.
The Blender source retains Eevee materials. Spec visual acceptance remains open.
Review: start, middle and final frames inspected. Motion passes forward-axis
and root-height checks. Visual acceptance FAILS: joint gaps from rigid parts,
simplified biped creature anatomy, stylized head, rider and feather likeness.
This delivery is a working draft, not a completed match to the reference.
