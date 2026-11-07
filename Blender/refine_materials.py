import bpy, math, os
from mathutils import Vector
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d'
sc=bpy.context.scene
image=bpy.data.images.get('Enkidu | original full concept and portrait')
if not image:raise RuntimeError('Packed concept image missing')
image.pack()
# Freeze the starter shirt's remesh modifier before adding UVs: voxel remesh discards UV data.
shirt_obj=bpy.data.objects.get('Shirt | main cloth shell')
if shirt_obj:
 bpy.ops.object.select_all(action='DESELECT');shirt_obj.select_set(True);bpy.context.view_layer.objects.active=shirt_obj;bpy.ops.object.convert(target='MESH')

# All references remain packed; projected UVs are editable and are an initial texture pass.
def uv_project(o,kind):
 if o.type!='MESH':return
 layer=o.data.uv_layers.new(name='Concept front projection')
 for poly in o.data.polygons:
  for li in poly.loop_indices:
   v=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
   if kind=='face':px=1118+v.x*1950;py=600-(v.z-1.235)*2000
   else:px=380+v.x*720;py=1020-v.z*700
   layer.data[li].uv=(px/1536,1-py/1024)
 return layer.name

def texmat(name,base,skin=False,fabric=False,projection=False,front=False):
 m=bpy.data.materials.new(name);m.use_nodes=True;nodes=m.node_tree.nodes;links=m.node_tree.links
 p=nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*base,1)
 p.inputs['Roughness'].default_value=.52 if skin else .82
 if skin:
  p.inputs['Subsurface Weight'].default_value=.12
  p.inputs['Subsurface Radius'].default_value=(1,.40,.22)
  p.inputs['Subsurface Scale'].default_value=.025
  p.inputs['Specular IOR Level'].default_value=.32
 if fabric:
  p.inputs['Sheen Weight'].default_value=.20;p.inputs['Sheen Roughness'].default_value=.8
 tc=nodes.new('ShaderNodeTexCoord')
 noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=550 if skin else 320;noise.inputs['Detail'].default_value=3
 links.new(tc.outputs['Object'],noise.inputs['Vector'])
 bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18 if skin else .30;bump.inputs['Distance'].default_value=.00012 if skin else .00032
 links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],p.inputs['Normal'])
 ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.38,.38,.38,1) if skin else (.68,.68,.68,1);ramp.color_ramp.elements[1].color=(.65,.65,.65,1) if skin else (.95,.95,.95,1)
 links.new(noise.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],p.inputs['Roughness'])
 if projection:
  im=nodes.new('ShaderNodeTexImage');im.name='Original concept colour | editable UV projection';im.image=image;im.extension='EXTEND';uvnode=nodes.new('ShaderNodeUVMap');uvnode.uv_map='Concept front projection';links.new(uvnode.outputs['UV'],im.inputs['Vector'])
  mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[1].default_value=(*base,1);links.new(im.outputs['Color'],mix.inputs[2])
  geo=nodes.new('ShaderNodeNewGeometry');sep=nodes.new('ShaderNodeSeparateXYZ');links.new(geo.outputs['Normal'],sep.inputs[0])
  remap=nodes.new('ShaderNodeMapRange');remap.inputs['From Min'].default_value=-.12;remap.inputs['From Max'].default_value=-.80;remap.inputs['To Min'].default_value=0;remap.inputs['To Max'].default_value=1;remap.clamp=True
  links.new(sep.outputs['Y'],remap.inputs['Value'])
  if fabric and 'blue cotton' in name:
   rgb=nodes.new('ShaderNodeSeparateColor');rgb.mode='RGB';links.new(im.outputs['Color'],rgb.inputs['Color'])
   delta=nodes.new('ShaderNodeMath');delta.operation='SUBTRACT';links.new(rgb.outputs['Blue'],delta.inputs[0]);links.new(rgb.outputs['Red'],delta.inputs[1])
   key=nodes.new('ShaderNodeMapRange');key.inputs['From Min'].default_value=-.005;key.inputs['From Max'].default_value=.018;key.inputs['To Min'].default_value=0;key.inputs['To Max'].default_value=1;key.clamp=True;links.new(delta.outputs[0],key.inputs['Value'])
   mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';links.new(remap.outputs[0],mul.inputs[0]);links.new(key.outputs[0],mul.inputs[1]);links.new(mul.outputs[0],mix.inputs[0])
  else:links.new(remap.outputs[0],mix.inputs[0])
  links.new(mix.outputs[0],p.inputs['Base Color'])
 else:
  color=nodes.new('ShaderNodeValToRGB');color.color_ramp.elements[0].color=(*[v*.78 for v in base],1);color.color_ramp.elements[1].color=(*[min(v*1.12,1) for v in base],1)
  links.new(noise.outputs['Fac'],color.inputs[0]);links.new(color.outputs[0],p.inputs['Base Color'])
 return m
skin=texmat('REALISM | skin • subsurface • microtexture',(.32,.155,.075),skin=True)
face=texmat('REALISM | face • concept colour • subsurface',(.32,.155,.075),skin=True,projection=True)
shirt=texmat('REALISM | faded blue cotton • woven fibres',(.085,.123,.165),fabric=True,projection=True)
pants=texmat('REALISM | worn brown cotton • reference colour',(.17,.095,.048),fabric=True,projection=True)
bag=texmat('REALISM | weathered canvas • fibre relief',(.21,.125,.057),fabric=True)
shoes=texmat('REALISM | grey canvas uppers',(.23,.20,.15),fabric=True)
rubber=texmat('REALISM | worn rubber soles',(.34,.28,.19))
for o in sc.objects:
 if o.type not in {'MESH','CURVE'} or not o.data.materials:continue
 old=o.data.materials[0].name
 new=None
 if old.startswith('Skin'):
  if o.name.startswith(('Head','Nose','Ear')) and o.type=='MESH':uv_project(o,'face');new=face
  else:new=skin
 elif old.startswith('Shirt'):
  if o.type=='MESH':uv_project(o,'body');new=shirt
 elif old.startswith('Trousers'):
  if o.type=='MESH':uv_project(o,'body');new=pants
 elif old.startswith('Bag'):new=bag
 elif old.startswith('Shoes'):new=shoes
 elif old.startswith('Soles'):new=rubber
 if new:o.data.materials[0]=new
# Real eye response: warm sclera, detailed radial iris, glossy corneal surface.
for m in bpy.data.materials:
 if m.name.startswith('Eye |'):
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.46,.39,.28,1);p.inputs['Roughness'].default_value=.23;p.inputs['Coat Weight'].default_value=.45;p.inputs['Coat Roughness'].default_value=.12
 if m.name.startswith('Iris |'):
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.20;p.inputs['Coat Weight'].default_value=.7
  ns=m.node_tree.nodes;ls=m.node_tree.links;tc=ns.new('ShaderNodeTexCoord');noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=25;noise.inputs['Detail'].default_value=5;ls.new(tc.outputs['Generated'],noise.inputs['Vector'])
  ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.009,.004,.001,1);ramp.color_ramp.elements[1].color=(.14,.055,.012,1);ls.new(noise.outputs['Fac'],ramp.inputs[0]);ls.new(ramp.outputs[0],p.inputs['Base Color'])
 if m.name.startswith('Buckles'):
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Metallic'].default_value=.8;p.inputs['Roughness'].default_value=.48
 if m.name.startswith('Hair |'):
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.012,.007,.004,1);p.inputs['Roughness'].default_value=.74;p.inputs['Specular IOR Level'].default_value=.13
  tex=m.node_tree.nodes.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=210;tex.inputs['Detail'].default_value=2;b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.21;b.inputs['Distance'].default_value=.00035;m.node_tree.links.new(tex.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs[0],p.inputs['Normal'])
# Tame blockout strand ridges into one cohesive hair volume; retain originals hidden for editing.
hair_col=bpy.data.collections.get('03 Hair')
source=bpy.data.collections.new('03b Original hair forms | hidden backup');sc.collection.children.link(source)
parts=list(hair_col.objects)
for o in parts:
 clone=o.copy();clone.data=o.data.copy();source.objects.link(clone);clone.hide_set(True);clone.hide_render=True
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.convert(target='MESH');bpy.ops.object.join();hair=bpy.context.object;hair.name='Hair | unified volume for sculpt refinement'
rem=hair.modifiers.new('Merge hair forms','REMESH');rem.mode='VOXEL';rem.voxel_size=.0012;rem.use_smooth_shade=True
sm=hair.modifiers.new('Soften lock transitions','SMOOTH');sm.factor=.65;sm.iterations=4
# More flattering, less toy-like portrait lighting and close-up camera.
sc.cycles.samples=64;sc.cycles.use_denoising=True
for a in bpy.data.screens:
 for area in a.areas:
  if area.type=='VIEW_3D':area.spaces.active.overlay.show_extras=False
notes=bpy.data.texts.get('START HERE | Enkidu development notes')
notes.write('\n\nMATERIAL STUDY v06: Skin now uses subsurface scattering, variable roughness and pores, with front colour projection from the packed concept. Cotton clothing has reference colour and procedural fibre relief. Canvas, rubber, aged brass and wet eyes have distinct shaders. Hair masses merged for sculpt refinement; source forms retained hidden. Projection is a first texture pass, not final UV unwrapping: side/back colours are inferred, seams may need painted cleanup. Original concept is painterly rather than a real photograph. Geometry remains a starter; realism still requires detailed anatomy, cloth and strand grooming.\n')
sc.render.filepath=ROOT+'/enkidu-material-study-v06.png'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_character_materials_v06.blend')
bpy.ops.render.render(write_still=True)
# Extra portrait for evaluating skin and eye materials.
cam=sc.camera;cam.location=(.35,-2.8,1.47);cam.rotation_euler=(Vector((0,-.015,1.32))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.43
sc.render.resolution_x=1000;sc.render.resolution_y=1000;sc.render.filepath=ROOT+'/enkidu-face-materials-v06.png'
bpy.ops.render.render(write_still=True)
print('MATERIAL_PASS_COMPLETE')
