import bpy,math,json
from math import pi,sin,cos
from mathutils import Vector,Quaternion,Euler
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-walk'
s=bpy.context.scene;r=bpy.data.objects['ENKIDU_RIG'];N=64
old=r.animation_data.action
if old:old.use_fake_user=True
r.animation_data.action=None
if r.animation_data.nla_tracks:
 for track in r.animation_data.nla_tracks:track.mute=True
r['Leg IK L']=1.;r['Leg IK R']=1.;r['Arm IK L']=0.;r['Arm IK R']=0.
# Store transforms in the fitted rig's local bone axes, authored in world axes.
def move(name,delta):r.pose.bones[name].location=r.data.bones[name].matrix_local.to_3x3().inverted()@Vector(delta)
def rotate(name,angles):
 basis=r.data.bones[name].matrix_local.to_3x3();world=Euler(tuple(math.radians(a) for a in angles),'XYZ').to_matrix();r.pose.bones[name].rotation_euler=(basis.inverted()@world@basis).to_euler('XYZ')
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def foot_motion(p):
 duty=.62;A=.105
 if p<duty:
  q=p/duty;y=-A+2*A*q;lift=0
  pitch=-5*(1-smooth(q/.14)) if q<.14 else 10*smooth((q-.76)/.24) if q>.76 else 0
 else:
  q=(p-duty)/(1-duty);m=2*A/duty*(1-duty)
  y=(2*q**3-3*q*q+1)*A+(q**3-2*q*q+q)*m+(-2*q**3+3*q*q)*(-A)+(q**3-q*q)*m
  lift=.042*sin(pi*q)**2;pitch=10-15*smooth(q)
 return y,lift,pitch
animated=[]
for frame in range(1,N+2):
 s.frame_set(frame);phase=(frame-1)/N;theta=2*pi*phase
 for pb in r.pose.bones:pb.location=(0,0,0);pb.rotation_euler=(0,0,0);pb.scale=(1,1,1)
 move('pelvis',(.009*sin(theta),0,-.026-.0045*cos(2*theta)))
 rotate('pelvis',(0,1.0*sin(theta),-2.0*cos(theta)))
 rotate('spine',(1.3,-.6*sin(theta),1.1*cos(theta)))
 rotate('chest',(.6,-.5*sin(theta),1.0*cos(theta)))
 rotate('neck',(-.6,.2*sin(theta),-.3*cos(theta)))
 rotate('head',(-.5,.2*sin(theta),-.25*cos(theta)))
 for side,offset in [('L',0),('R',.5)]:
  p=(phase+offset)%1;y,lift,pitch=foot_motion(p)
  move('foot_ik.'+side,(0,y,lift));rotate('foot_ik.'+side,(pitch,0,0))
  rotate('toe.'+side,(-max(0,pitch)*.8,0,0))
  arm=8.5*cos(theta+offset*2*pi)
  rotate('upper_arm.'+side,(arm,0,0));rotate('forearm.'+side,(-7-2*sin(theta+offset*2*pi),0,0));rotate('hand.'+side,(-2,0,0))
  for finger in ['index','middle','ring','pinky']:
   for j,deg in [(1,5),(2,9),(3,6)]:r.pose.bones[f'{finger}.{j:02d}.{side}'].rotation_euler.x=math.radians(deg)
  r.pose.bones['thumb.01.'+side].rotation_euler.x=.06
 rotate('backpack',(.65*sin(2*theta-.35),.4*sin(theta-.4),.4*sin(theta-.5)))
 move('backpack',(0,0,.0015*sin(2*theta-.3)))
 # Ground the actual deforming soles after heel/toe rotation. Swing clearance is added above this baseline.
 for iteration in range(2):
  bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
  for side,sign,offset in [('L',1,0),('R',-1,.5)]:
   p=(phase+offset)%1;lift=foot_motion(p)[1]
   ob=bpy.data.objects['ANIM • V09 • layered sneaker rubber sole '+str(sign)];eo=ob.evaluated_get(deps);me=eo.to_mesh();lowest=min((eo.matrix_world@v.co).z for v in me.vertices);eo.to_mesh_clear()
   correction=.006+lift-lowest;pb=r.pose.bones['foot_ik.'+side];pb.location+=r.data.bones[pb.name].matrix_local.to_3x3().inverted()@Vector((0,0,correction))
 for pb in r.pose.bones:
  pb.keyframe_insert(data_path='location',frame=frame,group=pb.name);pb.keyframe_insert(data_path='rotation_euler',frame=frame,group=pb.name)
a=r.animation_data.action;a.name='Enkidu • Slow Walk • Seamless 64f';a.use_fake_user=True
curves=[fc for layer in a.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
for fc in curves:
 for kp in fc.keyframe_points:kp.interpolation='BEZIER';kp.handle_left_type='AUTO_CLAMPED';kp.handle_right_type='AUTO_CLAMPED'
 mod=fc.modifiers.new('CYCLES');mod.mode_before='REPEAT';mod.mode_after='REPEAT'
# The endpoint duplicates frame 1 but sits outside the playback range, avoiding a held seam.
s.render.fps=24;s.frame_start=1;s.frame_end=N;s.use_preview_range=True;s.frame_preview_start=1;s.frame_preview_end=N;s.sync_mode='FRAME_DROP'
for marker in list(s.timeline_markers):s.timeline_markers.remove(marker)
for frame,name in [(1,'Left contact'),(17,'Left support / right swing'),(33,'Right contact'),(49,'Right support / left swing')]:s.timeline_markers.new(name,frame=frame)
s['Animation']='Slow walk in place; 64 frames at 24 fps; seamless repeat; 48 steps per minute approximately.'
r['Walk cycle frames']=64;r['Walk cycle seconds']=64/24;r['Walk type']='In place. Animate root separately for forward travel.'
s.frame_set(1);bpy.context.view_layer.update()
# Keep final render detail while making the detailed mesh lighter in the viewport.
s.render.use_simplify=True;s.render.simplify_subdivision=0;s.render.simplify_subdivision_render=2
s.camera=bpy.data.objects['Camera • character and rig']
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.overlay.show_overlays=False;area.spaces.active.shading.type='MATERIAL';area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.region_3d.view_camera_zoom=-10
text=bpy.data.texts.new('SLOW WALK • playback notes');text.write('SLOW WALK V14\n\nActive action: Enkidu • Slow Walk • Seamless 64f\n64 frames at 24 fps (2.67 seconds), approximately 45 steps per minute.\nThe animation walks in place and loops continuously. Animate root for travel.\nFrame 65 matches frame 1; playback ends at 64 to avoid a doubled endpoint. Every channel has repeat cycles before and after the keyed range.\nPress Space over the viewport or timeline to play/pause.\nThe previous rig verification action is preserved.\n\nFoot positions include evaluated sole-contact correction; body sway, opposite arm swing, slight heel/toe roll and small backpack lag are keyed. This remains a starter character rig; larger motion may need corrective skinning.\n')
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_slow_walk_v14.blend')
result={'file':bpy.data.filepath,'action':a.name,'curves':len(curves),'cycle_frames':64,'seconds':64/24}
