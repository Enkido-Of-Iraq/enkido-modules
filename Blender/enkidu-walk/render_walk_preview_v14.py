import bpy,os
s=bpy.context.scene
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-walk'
s.render.engine='BLENDER_EEVEE'
if hasattr(s,'eevee'):
 for prop,value in [('taa_render_samples',16),('taa_samples',16),('use_gtao',True)]:
  if hasattr(s.eevee,prop):setattr(s.eevee,prop,value)
s.render.resolution_x=480;s.render.resolution_y=640;s.render.resolution_percentage=100
os.makedirs(root+'/frames',exist_ok=True)
s.render.image_settings.file_format='PNG';s.frame_start=1;s.frame_end=64;s.use_preview_range=False;s.render.fps=24;s.render.filepath=root+'/frames/walk_';s.frame_set(1)
bpy.ops.render.render(animation=True)
