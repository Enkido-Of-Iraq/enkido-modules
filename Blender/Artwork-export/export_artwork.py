import bpy,os,json,shutil
from mathutils import Vector
OUT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/Artwork-export'
s=bpy.context.scene;r=bpy.data.objects['ENKIDU_RIG'];s.frame_set(1)
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
# Preserve the native project and its original procedural materials without conversion.
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/Artwork.blend',copy=True)
shutil.copy2('/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-action/Enkidu_walk_run_jump_preview_v15.mp4',OUT+'/Artwork.mp4')
selected=[o for o in s.objects if o.name.startswith('ANIM') and not o.hide_render and o.type in {'MESH','CURVE'}]
# FBX represents the small curve details as polygon geometry.
bpy.ops.object.select_all(action='DESELECT')
for o in selected:
 if o.type=='CURVE':
  o.hide_set(False);o.select_set(True);bpy.context.view_layer.objects.active=o
  bpy.ops.object.convert(target='MESH');o.select_set(False)
# Make simple, coloured exchange materials explicit. Detailed Blender shaders remain in Artwork.blend.
used={m for o in selected for m in o.data.materials if m}
mat_notes=[]
for m in used:
 if not m.use_nodes:continue
 p=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
 if not p:continue
 if p.inputs['Base Color'].is_linked:
  mat_notes.append(m.name)
  for link in list(p.inputs['Base Color'].links):m.node_tree.links.remove(link)
  p.inputs['Base Color'].default_value=m.diffuse_color
  if 'reference coloured eyes' in m.name:p.inputs['Base Color'].default_value=(.075,.035,.012,1)
# Include the following camera and simple stage lighting alongside the animated character.
selected += [r,s.camera,bpy.data.objects['Ground • contact plane']]+[o for o in s.objects if o.type=='LIGHT']
for o in selected:o.hide_set(False);o.select_set(True)
bpy.context.view_layer.objects.active=r
# Bake the evaluated rig and constraints into ordinary FBX keyframes.
frames=[1,33,65,101,137,149,153,161,169,175,185,249,312]
bones=['root','pelvis','head','foot.L','foot.R','backpack']
reference={}
for f in frames:
 s.frame_set(f);bpy.context.view_layer.update()
 reference[str(f)]={n:list(r.matrix_world@r.pose.bones[n].head) for n in bones}
s.frame_set(1)
bpy.ops.export_scene.fbx(filepath=OUT+'/Artwork.fbx',use_selection=True,object_types={'ARMATURE','MESH','CAMERA','LIGHT'},global_scale=1.0,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_mesh_modifiers=True,mesh_smooth_type='FACE',add_leaf_bones=False,use_armature_deform_only=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_force_startend_keying=True,bake_anim_step=1.0,bake_anim_simplify_factor=0.0,path_mode='COPY',embed_textures=True)
export_count=len([o for o in selected if o.type=='MESH'])
# Import into a fresh scene and check that the animation survived the file exchange.
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.render.fps=24
bpy.ops.import_scene.fbx(filepath=OUT+'/Artwork.fbx',use_anim=True,anim_offset=0.0)
ir=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
errors=[]
for f in frames:
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update()
 for n in bones:errors.append((ir.matrix_world@ir.pose.bones[n].head-Vector(reference[str(f)][n])).length)
report={'fbx':OUT+'/Artwork.fbx','fps':24,'frames':[1,312],'duration_seconds':13,'export_meshes':export_count,'import_meshes':len([o for o in bpy.context.scene.objects if o.type=='MESH']),'import_bones':len(ir.data.bones),'has_animation':bool(ir.animation_data and ir.animation_data.action),'sampled_frames':frames,'maximum_bone_position_error_metres':max(errors),'procedural_materials_approximated':mat_notes}
open(OUT+'/export-verification.json','w').write(json.dumps(report,indent=2))
assert report['has_animation'],'Animation missing after FBX import'
assert report['import_meshes']==export_count,'Meshes missing after FBX import'
assert max(errors)<.002,'Animation positions changed after FBX import'
open(OUT+'/Artwork_README.txt','w').write('ARTWORK — ENKIDU ANIMATION\n\nArtwork.fbx: animated 3D character, backpack, skeleton, following camera and studio stage. Standard baked keyframes, 24 fps, 312 frames / 13 seconds. Includes forward travel. Import animation in your application and set playback to 24 fps.\n\nArtwork.mp4: the rendered 13-second video, 480 x 640, H.264, 24 fps. Use directly in video editors.\n\nArtwork.blend: complete editable Blender source, including original procedural cloth, skin and hair materials.\n\nSequence: two slow steps, accelerate, run, jump, cushioned landing, return to walking.\n\nFBX uses simplified coloured materials. Blender procedural surface textures do not transfer through FBX; recreate or bake materials for matching rendering in another 3D application. The MP4 preserves the rendered look. No single editable 3D format is supported by every application.\n\nVerification: FBX was imported into a fresh Blender scene; mesh count, skeleton, animation and sampled bone positions were checked.\n')
print(json.dumps(report),flush=True)
