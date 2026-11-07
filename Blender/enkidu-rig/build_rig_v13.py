import bpy, math, json, os
from mathutils import Vector, Matrix, Quaternion
from math import pi, sin, cos
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-rig'
source_scene=bpy.data.scenes['Enkidu • sketch-fitted head']
bpy.context.window.scene=source_scene
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.update()
scene=bpy.data.scenes.new('ENKIDU • animation stage');scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.fps=24;scene.frame_start=1;scene.frame_end=72
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
COL={}
for name in ['01 • Animation rig','02 • Body and hands','03 • Head and eyes','04 • Hair groom','05 • Clothing and repairs','06 • Canvas shoes','07 • Backpack','08 • Stage','09 • Rig shapes','10 • References']:
 c=bpy.data.collections.new(name);scene.collection.children.link(c);COL[name]=c
COL['09 • Rig shapes'].hide_render=True;COL['09 • Rig shapes'].hide_viewport=True
# Copy the latest visible components into a clean scene; do not alter previous studies.
sources=[('Anatomy.001','02 • Body and hands'),('V05 • head and neck','03 • Head and eyes'),('V05 • cartilage','03 • Head and eyes'),('V05 • eyes lids and brows','03 • Head and eyes'),('V05 • groom','04 • Hair groom'),('V09 • clothing','05 • Clothing and repairs'),('V09 • repairs and stitching','05 • Clothing and repairs'),('V09 • sneakers','06 • Canvas shoes'),('V12 • Enkidu reference backpack','07 • Backpack')]
objects=[];source_names={};types={}
deps=bpy.context.evaluated_depsgraph_get()
for cname,dest in sources:
 for src in list(bpy.data.collections[cname].objects):
  if src.type not in ['MESH','CURVE'] or src.hide_render or src.hide_viewport:continue
  rigid_curve=src.type=='CURVE' and dest in ['03 • Head and eyes','04 • Hair groom']
  if src.type=='CURVE' and not rigid_curve:
   me=bpy.data.meshes.new_from_object(src.evaluated_get(deps),preserve_all_data_layers=True,depsgraph=deps);o=bpy.data.objects.new('ANIM • '+src.name,me)
  else:o=src.copy();o.data=src.data.copy();o.name='ANIM • '+src.name
  COL[dest].objects.link(o);world=src.matrix_world.copy();o.parent=None;o.matrix_world=world;o.hide_render=False;o.hide_viewport=False
  source_names[o.name]=src.name;types[o.name]=dest;objects.append(o)
# Skeleton fitted to measured body joints. X positive = anatomical left, facing -Y.
bpy.context.window.scene=scene
arm=bpy.data.armatures.new('Enkidu • animation skeleton');rig=bpy.data.objects.new('ENKIDU_RIG',arm);COL['01 • Animation rig'].objects.link(rig);rig.show_in_front=True;arm.display_type='OCTAHEDRAL'
bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def bone(name,head,tail,parent=None,deform=True,connect=False):
 b=arm.edit_bones.new(name);b.head=head;b.tail=tail;b.use_deform=deform
 if parent:b.parent=arm.edit_bones[parent];b.use_connect=connect
 if abs((Vector(tail)-Vector(head)).normalized().dot(Vector((0,1,0))))<.95:b.align_roll(Vector((0,1,0)))
 else:b.align_roll(Vector((0,0,1)))
 return b
bone('root',(0,0,.015),(0,0,.13),deform=False)
bone('pelvis',(0,0,.735),(0,0,.855),'root')
bone('spine',(0,0,.855),(0,0,.98),'pelvis',connect=True)
bone('chest',(0,0,.98),(0,0,1.115),'spine',connect=True)
bone('neck',(0,0,1.115),(0,0,1.22),'chest',connect=True)
bone('head',(0,0,1.22),(0,0,1.399),'neck',connect=True)
bone('backpack',(0,.13,.99),(0,.13,1.12),'chest')
bone('backpack_flap',(0,.078,1.139),(0,.18,1.139),'backpack')
finger_map={}
for side,suf in [(1,'L'),(-1,'R')]:
 def P(x,y,z):return(side*x,y,z)
 bone('clavicle.'+suf,P(.015,0,1.105),P(.135,0,1.095),'chest')
 bone('upper_arm.'+suf,P(.135,0,1.095),P(.211,-.005,.85),'clavicle.'+suf,connect=True)
 bone('forearm.'+suf,P(.211,-.005,.85),P(.232,-.024,.674),'upper_arm.'+suf,connect=True)
 bone('hand.'+suf,P(.232,-.024,.674),P(.234,-.028,.625),'forearm.'+suf,connect=True)
 fingers=[o for o in objects if source_names[o.name].startswith('Finger') and (o.matrix_world@o.data.vertices[0].co).x*side>0]
 fingers.sort(key=lambda o:abs(sum((o.matrix_world@v.co).x for v in o.data.vertices)/len(o.data.vertices)))
 for name,ob in zip(['index','middle','ring','pinky'],fingers):
  points=[ob.matrix_world@v.co for v in ob.data.vertices];cx=sum(p.x for p in points)/len(points);z0=max(p.z for p in points);z1=min(p.z for p in points)
  joints=[Vector((cx,-.027-(k/3)*.004,z0+(z1-z0)*k/3)) for k in range(4)]
  names=[]
  for j in range(3):
   nm=f'{name}.{j+1:02d}.{suf}';bone(nm,joints[j],joints[j+1],names[-1] if names else 'hand.'+suf,connect=bool(names));names.append(nm)
  finger_map[ob.name]=(names,z0,z1)
 thumb=next(o for o in objects if source_names[o.name].startswith('Thumb') and (o.matrix_world@o.data.vertices[0].co).x*side>0)
 points=[P(.216,-.029,.655),P(.208,-.036,.642),P(.200,-.043,.625)]
 bone('thumb.01.'+suf,points[0],points[1],'hand.'+suf);bone('thumb.02.'+suf,points[1],points[2],'thumb.01.'+suf,connect=True)
 finger_map[thumb.name]=(['thumb.01.'+suf,'thumb.02.'+suf],.655,.625)
 bone('thigh.'+suf,P(.071,.006,.715),P(.073,-.024,.405),'pelvis')
 bone('shin.'+suf,P(.073,-.024,.405),P(.078,.005,.102),'thigh.'+suf,connect=True)
 bone('foot.'+suf,P(.078,.005,.102),P(.078,-.075,.035),'shin.'+suf,connect=True)
 bone('toe.'+suf,P(.078,-.075,.035),P(.078,-.135,.035),'foot.'+suf,connect=True)
 bone('foot_ik.'+suf,P(.078,.005,.102),P(.078,-.075,.035),'root',False)
 bone('knee_pole.'+suf,P(.073,-.36,.405),P(.073,-.36,.46),'root',False)
 bone('hand_ik.'+suf,P(.232,-.024,.674),P(.234,-.028,.625),'root',False)
 bone('elbow_pole.'+suf,P(.23,.28,.86),P(.23,.28,.92),'root',False)
bpy.ops.object.mode_set(mode='POSE')
for pb in rig.pose.bones:pb.rotation_mode='XYZ'
def driver_influence(c,prop):
 d=c.driver_add('influence').driver;d.type='SCRIPTED';d.expression='blend';v=d.variables.new();v.name='blend';v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["'+prop+'"]'
for suf in ['L','R']:
 for label,value in [('Leg IK ',1.),('Arm IK ',0.)]:rig[label+suf]=value;rig.id_properties_ui(label+suf).update(min=0,max=1,description='0 = rotate FK bones; 1 = move the IK target and pole control')
 for limb,target,pole,prop in [('shin','foot_ik','knee_pole','Leg IK '),('forearm','hand_ik','elbow_pole','Arm IK ')]:
  c=rig.pose.bones[limb+'.'+suf].constraints.new('IK');c.name='Two bone '+limb+' IK';c.target=rig;c.subtarget=target+'.'+suf;c.pole_target=rig;c.pole_subtarget=pole+'.'+suf;c.chain_count=2;c.use_stretch=False;driver_influence(c,prop+suf)
  rig.pose.bones[limb+'.'+suf].ik_stretch=0
 for part,target,prop in [('foot','foot_ik','Leg IK '),('hand','hand_ik','Arm IK ')]:
  c=rig.pose.bones[part+'.'+suf].constraints.new('COPY_ROTATION');c.name='Match IK target orientation';c.target=rig;c.subtarget=target+'.'+suf;c.target_space='POSE';c.owner_space='POSE';driver_influence(c,prop+suf)
# Calibrate leg pole angles against the measured neutral knee position.
for suf in ['L','R']:
 c=rig.pose.bones['shin.'+suf].constraints[0];best=(100,0)
 for angle in [0,pi/2,-pi/2,pi]:
  c.pole_angle=angle;bpy.context.view_layer.update();err=(rig.pose.bones['shin.'+suf].head-arm.bones['shin.'+suf].head_local).length
  if err<best[0]:best=(err,angle)
 c.pole_angle=best[1]
# Arms default to FK, calibrate IK for optional hand placement.
for suf in ['L','R']:
 rig['Arm IK '+suf]=1.;rig.update_tag();bpy.context.view_layer.update();c=rig.pose.bones['forearm.'+suf].constraints[0];best=(100,0)
 for angle in [0,pi/2,-pi/2,pi]:
  c.pole_angle=angle;bpy.context.view_layer.update();err=(rig.pose.bones['forearm.'+suf].head-arm.bones['forearm.'+suf].head_local).length
  if err<best[0]:best=(err,angle)
 c.pole_angle=best[1];rig['Arm IK '+suf]=0.;rig.update_tag()
bpy.ops.object.mode_set(mode='OBJECT');bpy.context.view_layer.update()
# Bone collections make the skeleton readable.
groups={n:arm.collections.new(n) for n in ['Body FK','Arms and hands','Legs and feet','IK targets and poles','Backpack']}
for b in arm.bones:
 group='Backpack' if b.name.startswith('backpack') else 'IK targets and poles' if '_ik.' in b.name or '_pole.' in b.name else 'Legs and feet' if b.name.startswith(('thigh','shin','foot','toe')) else 'Arms and hands' if '.' in b.name else 'Body FK'
 groups[group].assign(b);b.color.palette='THEME04' if b.name.endswith('.L') else 'THEME03' if b.name.endswith('.R') else 'THEME02'
# Deterministic normalized skinning for separated clothing / anatomy pieces.
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def mix(a,b,t):
 out={k:v*(1-t) for k,v in a.items()}
 for k,v in b.items():out[k]=out.get(k,0)+v*t
 return out
def torso(p):
 z=p.z
 knots=[(.76,'pelvis'),(.90,'spine'),(1.075,'chest'),(1.19,'neck')]
 if z<=knots[0][0]:return {'pelvis':1}
 for (a,n),(b,m) in zip(knots,knots[1:]):
  if z<=b:return {n:1-smooth(a,b,z),m:smooth(a,b,z)}
 return {'neck':1}
def shirt_weight(p):
 w=torso(p);suf='L' if p.x>0 else 'R';a=smooth(.108,.183,abs(p.x))*smooth(.94,.99,p.z)
 if p.z>1.13:a*=1-smooth(1.13,1.17,p.z)
 w=mix(w,{'upper_arm.'+suf:1},a)
 clav=smooth(.055,.11,abs(p.x))*smooth(1.10,1.15,p.z)*.55
 return mix(w,{'clavicle.'+suf:1},clav)
def arm_weight(p,suf):
 if p.z>.85:return mix({'forearm.'+suf:1},{'upper_arm.'+suf:1},smooth(.815,.905,p.z))
 return mix({'hand.'+suf:1},{'forearm.'+suf:1},smooth(.655,.704,p.z))
def leg_weight(p,suf):
 w=mix({'shin.'+suf:1},{'thigh.'+suf:1},smooth(.365,.45,p.z))
 w=mix({'foot.'+suf:1},w,smooth(.09,.17,p.z));return mix(w,{'pelvis':1},smooth(.64,.725,p.z))
def shoe_weight(p,suf):return mix({'foot.'+suf:1},{'toe.'+suf:1},1-smooth(-.10,-.055,p.y))
def strap_weight(p):
 suf='L' if p.x>0 else 'R';w=torso(p);cl=.45*smooth(1.07,1.14,p.z);w=mix(w,{'clavicle.'+suf:1},cl)
 back=smooth(.032,.075,p.y)
 if p.z<.92:back=max(back,smooth(.94,.87,p.z))
 return mix(w,{'backpack':1},back)
def parent_bone(o,name):
 world=o.matrix_world.copy();o.parent=rig;o.parent_type='BONE';o.parent_bone=name;bpy.context.view_layer.update();o.matrix_world=world;o['Rig binding']='Rigid attachment: '+name
# Materials use stored rest coordinates so dust/pores do not slide during poses.
mat_cache={}
def fix_materials(o):
 if o.type!='MESH':return
 attr=o.data.attributes.get('rig_rest_position') or o.data.attributes.new('rig_rest_position','FLOAT_VECTOR','POINT')
 for i,v in enumerate(o.data.vertices):attr.data[i].vector=o.matrix_world@v.co
 for i,m in enumerate(list(o.data.materials)):
  if not m or not m.use_nodes:continue
  if m.name not in mat_cache:
   new=m.copy();new.name='ANIM • '+m.name;n=new.node_tree.nodes;l=new.node_tree.links
   links=[li for li in l if li.from_node.type=='NEW_GEOMETRY' and li.from_socket.name=='Position']
   if links:
    a=n.new('ShaderNodeAttribute');a.attribute_name='rig_rest_position';a.name='Stable rest-space texture coordinates'
    for li in links:dest=li.to_socket;l.remove(li);l.new(a.outputs['Vector'],dest)
   mat_cache[m.name]=new
  o.data.materials[i]=mat_cache[m.name]
weighted=0;rigid=0;totalverts=0
for o in objects:
 name=source_names[o.name];cat=types[o.name];fix_materials(o)
 points=[o.matrix_world@v.co for v in o.data.vertices] if o.type=='MESH' else []
 center=sum(points,Vector())/len(points) if points else o.matrix_world.translation;suf='L' if center.x>0 else 'R'
 fixed=None;fn=None
 if cat=='04 • Hair groom':fixed='head'
 elif cat=='03 • Head and eyes':
  if 'face skull neck' in name:fn=lambda p:mix({'neck':1},{'head':1},smooth(1.175,1.235,p.z))
  else:fixed='head'
 elif cat=='02 • Body and hands':
  if o.name in finger_map:
   names,z0,z1=finger_map[o.name]
   def finger_fn(p,names=names,z0=z0,z1=z1):
    t=max(0,min(.999,(z0-p.z)/(z0-z1)))*len(names);i=min(len(names)-1,int(t));fraction=t-i
    if i==len(names)-1:return {names[i]:1}
    blend=smooth(.65,1.0,fraction);return{names[i]:1-blend,names[i+1]:blend}
   fn=finger_fn
  elif name.startswith('Palm'):fn=lambda p,suf=suf:mix({'hand.'+suf:1},{'forearm.'+suf:1},smooth(.665,.689,p.z))
  else:fn=lambda p,suf=suf:arm_weight(p,suf)
 elif cat=='05 • Clothing and repairs':
  if any(k in name for k in ['trouser','ankle cuff','knee']):fn=lambda p,suf=suf:leg_weight(p,suf)
  elif 'underlying' in name:fn=torso
  else:fn=shirt_weight
 elif cat=='06 • Canvas shoes':fn=lambda p,suf=suf:shoe_weight(p,suf)
 elif cat=='07 • Backpack':
  if name.startswith(('V12 • 02 ','V12 • 03 rounded closure','V12 • 03 closure tab')):fixed='backpack_flap'
  elif any(k in name for k in ['04 ','05 ']):fn=strap_weight
  else:fixed='backpack'
 if fixed:parent_bone(o,fixed);rigid+=1;continue
 if not fn:raise RuntimeError('No binding for '+o.name)
 if o.type!='MESH':raise RuntimeError('Weighted object must be mesh: '+o.name)
 for g in list(o.vertex_groups):o.vertex_groups.remove(g)
 groups_by_name={}
 for i,p in enumerate(points):
  w={k:v for k,v in fn(p).items() if v>1e-5};w=dict(sorted(w.items(),key=lambda kv:kv[1],reverse=True)[:4]);den=sum(w.values())
  if not den:raise RuntimeError('Zero weight '+o.name)
  for k,v in w.items():
   if k not in groups_by_name:groups_by_name[k]=o.vertex_groups.new(name=k)
   groups_by_name[k].add([i],v/den,'REPLACE')
 mod=o.modifiers.new('Enkidu skeleton • preserve joint volume','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
 o.modifiers.move(len(o.modifiers)-1,0)
 world=o.matrix_world.copy();o.parent=rig;o.matrix_world=world;o['Rig binding']='Normalized deform weights';weighted+=1;totalverts+=len(points)
# Hand-drawn controller outlines; stored in hidden collection, visible as bone shapes.
def shape(name,verts,edges):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,edges,[]);ob=bpy.data.objects.new(name,me);COL['09 • Rig shapes'].objects.link(ob);return ob
ring=shape('WGT • ring',[(.09*cos(2*pi*i/48),0,.09*sin(2*pi*i/48)) for i in range(48)],[(i,(i+1)%48) for i in range(48)])
rootshape=shape('WGT • root',[(.27*cos(2*pi*i/64),0,.27*sin(2*pi*i/64)) for i in range(64)],[(i,(i+1)%64) for i in range(64)])
footshape=shape('WGT • foot',[(x,y,0) for x,y in [(-.055,-.045),(.055,-.045),(.055,.15),(.035,.18),(-.035,.18),(-.055,.15)]],[(i,(i+1)%6) for i in range(6)])
diamond=shape('WGT • pole',[(.035,0,0),(0,0,.035),(-.035,0,0),(0,0,-.035)],[(0,1),(1,2),(2,3),(3,0)])
for pb in rig.pose.bones:
 if pb.name=='root':pb.custom_shape=rootshape
 elif pb.name.startswith('foot_ik'):pb.custom_shape=footshape
 elif '_pole.' in pb.name:pb.custom_shape=diamond
 elif pb.name in ['pelvis','spine','chest','neck','head','backpack'] or pb.name.startswith('hand_ik'):pb.custom_shape=ring
 if pb.custom_shape:pb.use_custom_shape_bone_size=False
# Simple neutral stage with floor, lighting and front / rear review cameras.
def material(name,col):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=.85;return m
floor=material('Stage • warm grey',(.16,.145,.125));me=bpy.data.meshes.new('Animation ground');me.from_pydata([(-200,-200,.004),(200,-200,.004),(200,200,.004),(-200,200,.004)],[],[(0,1,2,3)]);o=bpy.data.objects.new('Ground • contact plane',me);COL['08 • Stage'].objects.link(o);me.materials.append(floor)
world=bpy.data.worlds.new('Animation stage environment');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.22,.22,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35;scene.world=world
for name,loc,power,size in [('Key',(-2,-3,3.5),260,3),('Fill',(2,-1,2.3),140,2.5),('Backpack rim',(0,2.5,2.7),210,2.0)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.size=size;o=bpy.data.objects.new(name,d);COL['08 • Stage'].objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.85))-o.location).to_track_quat('-Z','Y').to_euler()
def camera(name,loc,target,scale):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);COL['08 • Stage'].objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=scale;return o
scene.camera=camera('Camera • character and rig',(.95,-3,1.05),(0,0,.73),1.65)
camera('Camera • backpack fit',(.85,2.8,1.05),(0,.05,.73),1.65)
camera('Camera • side rig',(3,-.08,.9),(0,0,.73),1.65)
scene.render.resolution_x=1000;scene.render.resolution_y=1200;scene.render.resolution_percentage=100;scene.view_settings.view_transform='AgX'
# Reusable pose-check action, separate from a production walk cycle.
def reset():
 for pb in rig.pose.bones:pb.location=(0,0,0);pb.rotation_euler=(0,0,0);pb.scale=(1,1,1)
def move_world(name,delta):rig.pose.bones[name].location=arm.bones[name].matrix_local.to_3x3().inverted()@Vector(delta)
def rotate_world(name,axis,angle):
 local=arm.bones[name].matrix_local.to_3x3().inverted()@Vector(axis);rig.pose.bones[name].rotation_euler=Quaternion(local,math.radians(angle)).to_euler()
for frame,label in [(1,'Neutral / bind review'),(24,'Step / knee and backpack check'),(48,'Reach / head and finger check'),(72,'Return to neutral')]:
 scene.frame_set(frame);reset()
 if frame==24:
  move_world('pelvis',(0,0,-.025));move_world('foot_ik.L',(0,-.12,.04));move_world('foot_ik.R',(0,.045,0));rotate_world('upper_arm.L',(1,0,0),14);rotate_world('upper_arm.R',(1,0,0),-14);rotate_world('head',(0,0,1),-10)
 if frame==48:
  rotate_world('upper_arm.L',(1,0,0),-28);rotate_world('forearm.L',(1,0,0),-32);rotate_world('clavicle.L',(0,1,0),-5);rotate_world('chest',(0,0,1),8);rotate_world('head',(0,0,1),18)
  for name in ['index','middle','ring','pinky']:
   for j in [1,2,3]:rig.pose.bones[f'{name}.{j:02d}.L'].rotation_euler.x=math.radians(12+j*4)
 for pb in rig.pose.bones:
  pb.keyframe_insert(data_path='location',frame=frame,group=pb.name);pb.keyframe_insert(data_path='rotation_euler',frame=frame,group=pb.name)
 marker=scene.timeline_markers.new(label,frame=frame)
rig.animation_data.action.name='Enkidu • rig verification poses';rig.animation_data.action.use_fake_user=True
scene.frame_set(1);bpy.context.view_layer.update()
# Rig documentation travels with the asset.
text=bpy.data.texts.new('START HERE • Enkidu animation rig')
text.write('ENKIDU / RIG V13\n\nLatest head V08, body/clothes V11 and backpack V12 assembled in one scene.\n\nSelect ENKIDU_RIG and enter Pose Mode.\nroot moves the entire character; pelvis/spine/chest/neck/head rotate the torso.\nfoot_ik.L/R place the feet; knee_pole.L/R steer the knee bend. Leg IK properties default to 1.\nArms default to FK: clavicle, upper_arm, forearm, hand. Arm IK properties can be set to 1 for hand_ik and elbow_pole controls. Switch at the neutral pose; automatic IK/FK matching is not provided.\nFinger bones rotate individually. Backpack follows the chest; backpack and backpack_flap allow additional motion.\n\nTimeline: 1 neutral, 24 step test, 48 reach/look/fingers, 72 neutral. This action is a deformation test, not a finished walk cycle.\n\nAll visible components are attached. Clothes and straps use deformation weights; hair, face details and backpack panels use rigid bone attachments where appropriate. Procedural mesh textures use rest-space coordinates.\n\nLimitations: no facial expression rig, no cloth simulation or automatic secondary motion. Existing segmented anatomy and clothing topology remain; extreme poses may need corrective sculpting and weights. Game-engine textures are not baked.\n')
scene['Source versions']='Head V08 / body V11 / backpack V12';scene['Rig version']='V13';scene['Animation notes']='Pose Mode; use rig custom properties for IK/FK. See START HERE text.'
rig['Purpose']='Full body deformation rig with finger joints, IK feet, optional IK hands, backpack and flap controls.'
rig['Not included']='Facial expressions, automatic IK/FK matching, cloth simulation.'
# Verification data, including normalized weights and complete binding coverage.
report={'weighted_objects':weighted,'rigid_objects':rigid,'weighted_vertices':totalverts,'bones':len(arm.bones),'deform_bones':sum(b.use_deform for b in arm.bones),'unbound':[],'weight_errors':0,'neutral_joint_error':{}}
for o in objects:
 if not o.parent:report['unbound'].append(o.name)
 if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers):
  for v in o.data.vertices:
   total=sum(g.weight for g in v.groups)
   if abs(total-1)>1e-4:report['weight_errors']+=1
for suf in ['L','R']:report['neutral_joint_error'][suf]=(rig.pose.bones['shin.'+suf].head-arm.bones['shin.'+suf].head_local).length
with open(ROOT+'/rig-validation-v13.json','w') as f:json.dump(report,f,indent=2)
# Save a clean file containing this scene and its dependencies only.
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='POSE')
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.shading.type='MATERIAL';a.spaces.active.overlay.show_overlays=True;a.spaces.active.region_3d.view_perspective='CAMERA'
bpy.data.libraries.write(ROOT+'/Enkidu_character_backpack_rig_v13.blend',{scene,text},fake_user=True,compress=True)
result={'file':ROOT+'/Enkidu_character_backpack_rig_v13.blend','validation':report}
