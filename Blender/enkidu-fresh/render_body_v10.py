import bpy
s=bpy.context.scene
p=bpy.context.preferences.addons['cycles'].preferences
try:
 p.compute_device_type='METAL';p.get_devices()
 for d in p.devices:d.use=d.type=='METAL'
 s.cycles.device='GPU'
except Exception:s.cycles.device='CPU'
s.cycles.samples=48
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
for cam,suffix,w,h in [('V09 • full body','full',900,1200),('V09 • shoe detail','shoes',1100,800),('V09 • clothing repair detail','repairs',900,1000),('V09 • full profile','profile',900,1200)]:
 s.camera=bpy.data.objects[cam];s.render.resolution_x=w;s.render.resolution_y=h;s.render.filepath=root+'/enkidu-body-'+suffix+'-v10.png';bpy.ops.render.render(write_still=True)
