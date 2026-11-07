import bpy
from mathutils import Vector
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-backpack'
main=bpy.data.scenes['Enkidu • sketch-fitted head'];study=bpy.data.scenes['BACKPACK • isolated construction review']
review=bpy.data.scenes.new('BACKPACK • worn fit review');review.render.engine='CYCLES';review.cycles.samples=48;review.cycles.use_denoising=True;review.world=study.world
for c in main.collection.children:
 if not c.name.startswith('Studio'):review.collection.children.link(c)
cam=bpy.data.objects['V12 • worn backpack review'];review.collection.objects.link(cam);review.camera=cam
for name,loc,power,size in [('worn key',(-1,1.7,2.6),160,2),('worn fill',(1.6,1.1,1.7),85,1.5),('worn rim',(-.8,-1,2.0),95,1.5)]:
 d=bpy.data.lights.new('V12 • '+name,'AREA');d.energy=power;d.size=size;o=bpy.data.objects.new(d.name,d);review.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,.1,1))-o.location).to_track_quat('-Z','Y').to_euler()
base=bpy.data.objects['V12 • isolated studio floor'];floor=base.copy();floor.name='V12 • worn review floor';floor.location.z=-.824;review.collection.objects.link(floor)
review.render.resolution_x=1000;review.render.resolution_y=1100;review.render.resolution_percentage=100;review.view_settings.view_transform='AgX'
main.camera=bpy.data.objects['V09 • full body']
# Convenient startup view: the isolated, textured backpack with character scenes accessible.
if bpy.context.window:bpy.context.window.scene=study
study.camera=bpy.data.objects['V12 • bag hero']
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.shading.type='MATERIAL';a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.overlay.show_overlays=False
bpy.ops.wm.save_as_mainfile(filepath=root+'/Enkidu_backpack_sketch_v12.blend')
ref=bpy.data.images.get('exec-a2165755-2984-43f5-bf48-4672c7e39661.png')
assets={study}
if ref:assets.add(ref)
bpy.data.libraries.write(root+'/Enkidu_backpack_standalone_v12.blend',assets,fake_user=True,compress=True)
result={'character_file':bpy.data.filepath,'standalone':root+'/Enkidu_backpack_standalone_v12.blend','active_scene':bpy.context.scene.name}
