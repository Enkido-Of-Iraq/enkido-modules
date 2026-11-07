import bpy,sys
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-rig'
s=bpy.data.scenes['ENKIDU • animation stage'];bpy.context.window.scene=s
p=bpy.context.preferences.addons['cycles'].preferences
try:
 p.compute_device_type='METAL';p.get_devices()
 for d in p.devices:d.use=d.type=='METAL'
 s.cycles.device='GPU'
except Exception:s.cycles.device='CPU'
s.cycles.samples=32;s.render.resolution_x=850;s.render.resolution_y=1100;s.render.resolution_percentage=100
jobs=[('neutral',1,'Camera • character and rig'),('step',24,'Camera • character and rig'),('reach',48,'Camera • character and rig'),('backpack',48,'Camera • backpack fit')]
if '--' in sys.argv:jobs=[j for j in jobs if j[0] in sys.argv[sys.argv.index('--')+1:]]
for name,frame,cam in jobs:
 s.frame_set(frame);s.camera=bpy.data.objects[cam];s.render.filepath=root+'/enkidu-rig-'+name+'-v13.png';bpy.ops.render.render(write_still=True,scene=s.name)
