import bpy,math,sys
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-backpack'
p=bpy.context.preferences.addons['cycles'].preferences
try:
 p.compute_device_type='METAL';p.get_devices()
 for d in p.devices:d.use=d.type=='METAL'
except Exception:pass
s=bpy.data.scenes['BACKPACK • isolated construction review'];s.cycles.device='GPU';s.cycles.samples=40
names=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['hero','outer','body','side','open','worn']
for name in names:
 if name=='worn':
  sc=bpy.data.scenes['BACKPACK • worn fit review'];sc.camera=bpy.data.objects['V12 • worn backpack review'];sc.cycles.device='GPU';sc.cycles.samples=40
 else:
  sc=s;sc.camera=bpy.data.objects['V12 • bag '+name]
 bpy.data.objects['V12 • FLAP CONTROL — rotate local X to open'].rotation_euler.x=math.radians(120) if name=='open' else 0
 sc.render.resolution_x=1000;sc.render.resolution_y=1100;sc.render.resolution_percentage=100;sc.render.filepath=root+'/enkidu-backpack-'+name+'-v12.png'
 bpy.ops.render.render(write_still=True,scene=sc.name)
