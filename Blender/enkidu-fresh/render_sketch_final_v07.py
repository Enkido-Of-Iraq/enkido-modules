import bpy
s=bpy.context.scene
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
p=bpy.context.preferences.addons['cycles'].preferences
gpu=False
try:
 p.compute_device_type='METAL';p.get_devices()
 for d in p.devices:
  d.use=(d.type=='METAL')
  gpu|=d.use
except Exception as e:print('CPU fallback',str(e),flush=True)
s.cycles.device='GPU' if gpu else 'CPU'
print('Render device',s.cycles.device,flush=True)
s.render.resolution_x=1100;s.render.resolution_y=1100;s.cycles.samples=96
for name,suffix in [('V05 • front comparison','front'),('V05 • left-facing profile','left-profile'),('V05 • right-facing profile','right-profile'),('V05 • three-quarter review','three-quarter')]:
 s.camera=bpy.data.objects[name];s.render.filepath=root+'/enkidu-sketch-head-'+suffix+'-v07.png'
 try:bpy.ops.render.render(write_still=True)
 except RuntimeError:
  s.cycles.device='CPU';bpy.ops.render.render(write_still=True)
print('All four reference views rendered',flush=True)
