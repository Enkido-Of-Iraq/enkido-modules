import bpy,json
from mathutils import Vector
OUT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/Artwork-export'
r=bpy.data.objects['ENKIDU_RIG'];frames=[1,33,101,153,161,169,175,185,312];bones=['root','pelvis','head','foot.L','foot.R','backpack'];ref={}
for f in frames:
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update();ref[f]={n:list(r.matrix_world@r.pose.bones[n].head) for n in bones}
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=24;bpy.ops.import_scene.fbx(filepath=OUT+'/Artwork.fbx',use_anim=True,anim_offset=0.)
r=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');errors=[];rows=[]
for f in frames:
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update();d={n:(r.matrix_world@r.pose.bones[n].head-Vector(ref[f][n])).length for n in bones};errors+=list(d.values());rows.append({'frame':f,'error':d})
report={'range':list(r.animation_data.action.frame_range),'max_error':max(errors),'rows':rows};open(OUT+'/timing-check.json','w').write(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
