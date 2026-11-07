import bpy, math, json, os
from math import sin, cos, pi
from mathutils import Vector, Euler
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-action'
s=bpy.context.scene;r=bpy.data.objects['ENKIDU_RIG']
old=r.animation_data.action
if old:old.use_fake_user=True
r.animation_data.action=None
for track in r.animation_data.nla_tracks:track.mute=True
for side in ['L','R']:r['Leg IK '+side]=1.;r['Arm IK '+side]=0.
def smooth(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)
def mix(a,b,q):return a+(b-a)*q
def herm(a,b,ma,mb,q):return (2*q**3-3*q*q+1)*a+(q**3-2*q*q+q)*ma+(-2*q**3+3*q*q)*b+(q**3-q*q)*mb
def phase(t):
 if t<=65:return (t-1)/64
 if t<101:return herm(1,2.2,36/64,36/20,(t-65)/36)
 return 2.2+(t-101)/20

def inv_phase(p):
 if p<=1:return 1+64*p
 if p>=2.2:return 101+20*(p-2.2)
 lo,hi=65.,101.
 for _ in range(30):
  mid=(lo+hi)/2
  if phase(mid)<p:lo=mid
  else:hi=mid
 return (lo+hi)/2

def runmix(t):return smooth((t-65)/36)
def stride(t):return .34+.44*runmix(t)
# Integrate travel from cadence and stride, rather than sliding the planted feet.
DT=.125;dist=[0.]
for i in range(1,1601):
 t=1+i*DT;prev=t-DT;dist.append(dist[-1]+stride((prev+t)/2)*(phase(t)-phase(prev)))
def firstdist(t):
 if t<1:return (t-1)*.34/64
 ix=(t-1)/DT;i=int(ix)
 return mix(dist[i],dist[i+1],ix-i)
D137=firstdist(137);D145=D137+.13;D153=D145+.02;D169=D153+.36;D185=D169+.075

def rootdist(t):
 if t<=137:return firstdist(t)
 if t<=145:return D137+.13*(2*(t-137)/8-((t-137)/8)**2)
 if t<=149:return D145
 if t<=153:return D145+.02*((t-149)/4)**2
 if t<=169:return mix(D153,D169,(t-153)/16)
 if t<=185:return herm(D169,D185,.075,.34/64*16,(t-169)/16)
 return D185+.34*(t-185)/64

def gait(t,final=False):
 p=(t-185)/64 if final else phase(t);theta=2*pi*p
 k=0 if final else runmix(t);C=.34+.44*k;duty=.62-.22*k;D=rootdist(t)
 out={'pelvis':(.009*sin(theta),0,-.026-.0045*cos(2*theta)+k*(-.026+.022*cos(2*theta))),
 'angles':{'pelvis':(2.5*k,1*sin(theta),-2*cos(theta)), 'spine':(1.3+4*k,-.6*sin(theta),1.1*cos(theta)), 'chest':(.6+2*k,-.5*sin(theta),1*cos(theta)), 'neck':(-.6-2*k,.2*sin(theta),-.3*cos(theta)), 'head':(-.5-2*k,.2*sin(theta),-.25*cos(theta)), 'backpack':((.65+1.2*k)*sin(2*theta-.35),(.4+.5*k)*sin(theta-.4),.4*sin(theta-.5))}, 'feet':{},'bagz':(.0015+.002*k)*sin(2*theta-.3)}
 def t_for_phase(pp):return 185+64*pp if final else inv_phase(pp)
 def D_at(tt):return D185+.34*(tt-185)/64 if final else firstdist(tt)
 def C_at(tt):return .34 if final else stride(tt)
 def duty_at(tt):return .62 if final else .62-.22*runmix(tt)
 for side,offset in [('L',0),('R',.5)]:
  pp=p+offset;n=math.floor(pp);q=pp-n;tc=t_for_phase(n-offset);tn=t_for_phase(n+1-offset)
  cy=-D_at(tc)-.5*C_at(tc)*duty_at(tc);ny=-D_at(tn)-.5*C_at(tn)*duty_at(tn)
  if q<duty:
   v=q/duty;fy=cy;lift=0.;pitch=-5*(1-smooth(v/.18)) if v<.18 else (10+8*k)*smooth((v-.7)/.3) if v>.7 else 0
  else:
   v=(q-duty)/(1-duty);fy=mix(cy,ny,smooth(v));lift=(.042+.10*k)*sin(pi*v)**2;pitch=mix(10+8*k,-5,smooth(v))
  out['feet'][side]=(fy,lift,pitch)
  arm=(8.5+22*k)*cos(theta+offset*2*pi)
  out['angles']['upper_arm.'+side]=(arm,0,(-1 if side=='L' else 1)*3*k)
  out['angles']['forearm.'+side]=(-7-45*k-(2+6*k)*sin(theta+offset*2*pi),0,0)
  out['angles']['hand.'+side]=(-2-3*k,0,0)
 return out

start=gait(137);end=gait(185,True)
leftplant=start['feet']['L'][0];rightplant=leftplant+.045
landing={side:end['feet'][side][0] for side in ['L','R']}
def jump_pose(t):
 # A short braking gather, compression, push-off, flight, absorption and recovery.
 keys=[(137,start['pelvis'][2],7,0,0),(143,-.065,10,22,-28),(149,-.115,14,28,-45),(153,-.025,4,-48,-38),(161,-.055,1,-34,-52),(169,-.040,6,-22,-35),(175,-.115,15,-8,-50),(185,end['pelvis'][2],1.9,0,-7)]
 for j in range(len(keys)-1):
  if keys[j][0]<=t<=keys[j+1][0]:break
 a,b=keys[j],keys[j+1];w=smooth((t-a[0])/(b[0]-a[0]));z,lean,arm,elbow=[mix(a[i],b[i],w) for i in range(1,5)]
 out={'pelvis':(0,0,z),'angles':{'pelvis':(lean*.12,0,0),'spine':(lean*.50,0,0),'chest':(lean*.38,0,0),'neck':(-lean*.25,0,0),'head':(-lean*.25,0,0),'backpack':(1.8*sin((t-149)*pi/12)*math.exp(-max(0,t-169)/12),0,0)},'bagz':.002*sin((t-149)*pi/8),'feet':{}}
 for side in ['L','R']:
  out['angles']['upper_arm.'+side]=(arm,0,-3 if side=='L' else 3);out['angles']['forearm.'+side]=(elbow,0,0);out['angles']['hand.'+side]=(-3,0,0)
  fy0,li0,pi0=start['feet'][side];plant=leftplant if side=='L' else rightplant
  if t<=143:
   w=smooth((t-137)/6);fy=mix(fy0,plant,w);lift=li0*(1-w);pitch=pi0*(1-w)
  elif t<=149:fy=plant;lift=0;pitch=0
  elif t<=153:fy=plant;lift=0;pitch=15*smooth((t-149)/4)
  elif t<169:
   q=(t-153)/16;fy=mix(plant,landing[side],smooth(q));lift=.34*4*q*(1-q)+.055*sin(pi*q)**2;pitch=mix(15,-6,smooth(q))
  else:fy=landing[side];lift=0;pitch=-6*(1-smooth((t-169)/6))
  out['feet'][side]=(fy,lift,pitch)
 # Seamlessly match the complete gait pose at both ends.
 boundary=None;bw=0
 if t<143:boundary=start;bw=1-smooth((t-137)/6)
 if t>179:boundary=end;bw=smooth((t-179)/6)
 if boundary:
  out['pelvis']=tuple(mix(out['pelvis'][i],boundary['pelvis'][i],bw) for i in range(3))
  for name,angles in out['angles'].items():out['angles'][name]=tuple(mix(angles[i],boundary['angles'][name][i],bw) for i in range(3))
  out['bagz']=mix(out['bagz'],boundary['bagz'],bw)
  if t>179:
   for side in ['L','R']:
    fy,lift,pitch=out['feet'][side];out['feet'][side]=(fy,lift,mix(pitch,end['feet'][side][2],bw))
 return out

def move(name,delta):r.pose.bones[name].location=r.data.bones[name].matrix_local.to_3x3().inverted()@Vector(delta)
def rotate(name,angles):
 basis=r.data.bones[name].matrix_local.to_3x3();world=Euler(tuple(math.radians(a) for a in angles),'XYZ').to_matrix();r.pose.bones[name].rotation_euler=(basis.inverted()@world@basis).to_euler('XYZ')
# A dedicated camera leaves the earlier inspection views intact.
cam=bpy.data.objects['Camera • character and rig'].copy();cam.data=cam.data.copy();cam.name='Camera • walk run jump follow';s.collection.objects.link(cam)
cam.location=(1.8,-3,.97);target=Vector((0,0,.92));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=2.15;s.camera=cam
lights=[o for o in s.objects if o.type=='LIGHT'];light_orig={o.name:o.location.copy() for o in lights}
N=313;validation=[]
for frame in range(1,N+1):
 s.frame_set(frame)
 for pb in r.pose.bones:pb.rotation_mode='XYZ';pb.location=(0,0,0);pb.rotation_euler=(0,0,0);pb.scale=(1,1,1)
 D=rootdist(frame);q=(frame-153)/16;air=.34*4*q*(1-q) if 153<frame<169 else 0.
 pose=gait(frame) if frame<=137 else jump_pose(frame) if frame<185 else gait(frame,True)
 move('root',(0,-D,air));move('pelvis',pose['pelvis'])
 for name,ang in pose['angles'].items():rotate(name,ang)
 move('backpack',(0,0,pose['bagz']))
 for side in ['L','R']:
  fy,lift,pitch=pose['feet'][side];move('foot_ik.'+side,(0,fy+D,lift-air));rotate('foot_ik.'+side,(pitch,0,0));rotate('toe.'+side,(-max(0,pitch)*.8,0,0))
  for finger in ['index','middle','ring','pinky']:
   for j,deg in [(1,5),(2,9),(3,6)]:r.pose.bones[f'{finger}.{j:02d}.{side}'].rotation_euler.x=math.radians(deg)
  r.pose.bones['thumb.01.'+side].rotation_euler.x=.06
 # Correct sole contact using the actual evaluated shoe geometry.
 for iteration in range(3):
  bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
  for side,sign in [('L',1),('R',-1)]:
   ob=bpy.data.objects['ANIM • V09 • layered sneaker rubber sole '+str(sign)];eo=ob.evaluated_get(deps);me=eo.to_mesh();lowest=min((eo.matrix_world@v.co).z for v in me.vertices);eo.to_mesh_clear()
   correction=.008+pose['feet'][side][1]-lowest;pb=r.pose.bones['foot_ik.'+side];pb.location+=r.data.bones[pb.name].matrix_local.to_3x3().inverted()@Vector((0,0,correction))
 for pb in r.pose.bones:
  pb.keyframe_insert(data_path='location',frame=frame,group=pb.name);pb.keyframe_insert(data_path='rotation_euler',frame=frame,group=pb.name)
 cam.location.y=-3-D;cam.keyframe_insert(data_path='location',frame=frame)
 for ob in lights:
  ob.location=light_orig[ob.name]+Vector((0,-D,0));ob.keyframe_insert(data_path='location',frame=frame)
 if frame%24==1:print('Authored frame',frame,flush=True)
a=r.animation_data.action;a.name='Enkidu • Walk Run Jump Land Walk • 13 seconds';a.use_fake_user=True
for owner in [r,cam]+lights:
 action=owner.animation_data.action
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for kp in fc.keyframe_points:kp.interpolation='BEZIER';kp.handle_left_type='AUTO_CLAMPED';kp.handle_right_type='AUTO_CLAMPED'
     fc.extrapolation='CONSTANT'
s.render.fps=24;s.frame_start=1;s.frame_end=312;s.use_preview_range=True;s.frame_preview_start=1;s.frame_preview_end=312;s.sync_mode='FRAME_DROP'
for m in list(s.timeline_markers):s.timeline_markers.remove(m)
for frame,name in [(1,'01 • Slow step left'),(33,'02 • Slow step right'),(65,'03 • Accelerate'),(101,'04 • Faster run'),(137,'05 • Gather'),(149,'06 • Push off'),(153,'07 • Takeoff'),(161,'08 • Jump apex'),(169,'09 • Touchdown'),(175,'10 • Absorb landing'),(185,'11 • Walk again')]:s.timeline_markers.new(name,frame=frame)
s['Animation']='Two slow steps, accelerate into a run, gather, forward jump, soft landing, walk. Frames 1–312 at 24 fps. Root moves forward; following camera. Replay resets the route.'
r['Active sequence frames']=312;r['Active sequence seconds']=13;r['Root travel metres']=rootdist(313)
notes='ENKIDU — WALK / RUN / JUMP / LAND / WALK\n\n13 seconds, 24 fps, frames 1–312.\n1–64: two slow steps. 65–100: accelerate. 101–136: faster running.\n137–152: gather, crouch, push off. 153–168: jump.\n169–184: touchdown and soft knee compression/recovery. 185–312: return to walking.\n\nCharacter travels forward along -Y; follow camera and studio lights move with him.\nThe timeline repeats the whole sequence, returning to the route start on replay.\nSpace plays/pauses. The original slow walk action is preserved, as is the original v14 file.\nNo facial animation or cloth simulation is added. This is an editable body animation on the existing character rig.\n'
text=bpy.data.texts.new('ACTION SEQUENCE • playback notes');text.write(notes)
open(ROOT+'/PLAYBACK.txt','w').write(notes)
s.frame_set(1);bpy.context.view_layer.update()
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_walk_run_jump_v15.blend')
print(json.dumps({'file':bpy.data.filepath,'action':a.name,'frames':312,'root_travel':rootdist(313)}),flush=True)
