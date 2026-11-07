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
s.camera=bpy.data.objects['V09 • shoe detail']
s.render.resolution_x=1100;s.render.resolution_y=800
s.render.filepath=root+'/enkidu-body-shoes-v11.png'
bpy.ops.render.render(write_still=True)
