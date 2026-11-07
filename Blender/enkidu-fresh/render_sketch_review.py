import bpy
s=bpy.context.scene
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
s.render.resolution_x=800;s.render.resolution_y=800;s.cycles.samples=40
for name,suffix in [('V05 • front comparison','front'),('V05 • left-facing profile','profile'),('V05 • three-quarter review','three-quarter')]:
 s.camera=bpy.data.objects[name];s.render.filepath=root+'/review-v05-'+suffix+'.png'
 bpy.ops.render.render(write_still=True)
