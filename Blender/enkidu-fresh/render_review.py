import bpy,sys
from mathutils import Vector
s=bpy.context.scene
s.camera=next(o for o in s.objects if o.name.startswith('Camera • full character'))
s.camera.location=(.13,-3,.80);s.camera.rotation_euler=(Vector((0,0,.73))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=1.55
s.render.resolution_x=1000;s.render.resolution_y=1250;s.cycles.samples=80
s.render.filepath='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh/enkidu-full-v03.png'
bpy.ops.render.render(write_still=True)
