import bpy,math,json,os
s=bpy.context.scene;r=bpy.data.objects['ENKIDU_RIG'];root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-action'
report={'frames':312,'fps':24,'frames_checked':[]};minimum=999;maxik=0
for f in range(1,314):
 s.frame_set(f);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();row={'frame':f,'soles':{},'ik_error':{}}
 for side,sign in [('L',1),('R',-1)]:
  o=bpy.data.objects['ANIM • V09 • layered sneaker rubber sole '+str(sign)];eo=o.evaluated_get(dep);m=eo.to_mesh();z=min((eo.matrix_world@v.co).z for v in m.vertices);eo.to_mesh_clear();minimum=min(minimum,z);row['soles'][side]=z
  err=(r.pose.bones['shin.'+side].tail-r.pose.bones['foot_ik.'+side].head).length;maxik=max(maxik,err);row['ik_error'][side]=err
 if f in [1,33,65,85,101,112,121,137,143,149,153,157,161,165,169,172,175,185,217,249,313]:report['frames_checked'].append(row)
report.update(minimum_sole_z=minimum,maximum_ik_error=maxik,all_frames_checked=True)
open(root+'/animation-validation-v15.json','w').write(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
s.render.engine='BLENDER_EEVEE'
if hasattr(s,'eevee'):
 for prop,value in [('taa_render_samples',16),('taa_samples',16)]:
  if hasattr(s.eevee,prop):setattr(s.eevee,prop,value)
s.render.resolution_x=480;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.use_preview_range=False
# Inspect takeoff, apex, landing, and running before the complete preview export.
for f in [1,112,149,161,169,175,201]:
 s.frame_set(f);s.render.filepath=root+'/review_%04d.png'%f;bpy.ops.render.render(write_still=True)
