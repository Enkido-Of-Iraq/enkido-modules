import bpy,math,random,os
from mathutils import Vector,Matrix
from math import sin,cos,pi
random.seed(7)
s=bpy.context.scene;s.frame_set(1);boy=bpy.data.objects['ENKIDU_RIG'];old=bpy.data.objects['ANZU_RIG • rideable creature']
w=boy.matrix_world.copy();boy.parent=None;boy.matrix_world=w
for o in list(s.objects):
 p=o
 while p.parent:p=p.parent
 if p==old:o.hide_render=True;o.hide_set(True)
col=bpy.data.collections.new('ANZU V05 • quadruped rebuild');s.collection.children.link(col)
def move(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);return o
def mat(n,c,rough=.6,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 noise=m.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=85
 bump=m.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.025;m.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);m.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal']);return m
skin=mat('V05 • tawny hide',(.32,.16,.055));gold=mat('V05 • ochre feathers',(.46,.255,.085),.5,.15);edge=mat('V05 • pale feather edges',(.64,.38,.13),.48,.18);brown=mat('V05 • dark flight feathers',(.15,.075,.026));black=mat('V05 • keratin nose claws',(.025,.015,.009),.35);ivory=mat('V05 • teeth',(.72,.62,.40),.3);amber=mat('V05 • amber iris',(.72,.30,.025),.23);leather=mat('V05 • aged leather',(.10,.035,.013));mouth=mat('V05 • mouth',(.055,.012,.009))
def uv(n,p,sc,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=p);o=move(bpy.context.object);o.name=n;o.scale=sc;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=True
 return o
def tube(n,pts,rad,m,radii=None):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=rad;c.bevel_resolution=3;sp=c.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for i,(p,co) in enumerate(zip(sp.bezier_points,pts)):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO';p.radius=radii[i] if radii else 1
 o=bpy.data.objects.new(n,c);col.objects.link(o);c.materials.append(m);return o
# Smooth continuous trunk and rising neck, not a spherical belly.
parts=[uv('body',p,sc,skin) for p,sc in [((0,.1,2.1),(.69,1.45,.69)),((0,.95,2.0),(.73,.68,.72)),((0,-.95,2.25),(.66,.63,.85)),((0,-1.25,2.85),(.46,.48,.83)),((0,-1.48,3.30),(.39,.42,.53))]]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();body=bpy.context.object;body.name='V05 • seamless trunk neck'
mod=body.modifiers.new('Unified anatomy','REMESH');mod.mode='VOXEL';mod.voxel_size=.055;bpy.ops.object.modifier_apply(modifier=mod.name)
mod=body.modifiers.new('Organic smoothing','SMOOTH');mod.factor=1;mod.iterations=5;bpy.ops.object.modifier_apply(modifier=mod.name)
for p in body.data.polygons:p.use_smooth=True
# Lioness skull and muzzle unified into one sculptural surface.
parts=[uv('head',p,sc,skin) for p,sc in [((0,-1.55,3.50),(.43,.46,.43)),((-.25,-1.75,3.39),(.26,.32,.27)),((.25,-1.75,3.39),(.26,.32,.27)),((-.14,-1.99,3.36),(.19,.24,.145)),((.14,-1.99,3.36),(.19,.24,.145)),((0,-1.88,3.13),(.28,.28,.13))]]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();head=bpy.context.object;head.name='V05 • sculpted lioness face'
mod=head.modifiers.new('Unified muzzle','REMESH');mod.mode='VOXEL';mod.voxel_size=.025;bpy.ops.object.modifier_apply(modifier=mod.name)
mod=head.modifiers.new('Smooth face','SMOOTH');mod.factor=.6;mod.iterations=4;bpy.ops.object.modifier_apply(modifier=mod.name)
headparts=[head,uv('V05 • nose',(0,-2.205,3.42),(.145,.065,.075),black),uv('V05 • mouth opening',(0,-2.10,3.225),(.27,.08,.085),mouth)]
for sg in [-1,1]:
 headparts += [uv('V05 • recessed eye',(.30*sg,-1.92,3.59),(.092,.045,.065),black),uv('V05 • amber gaze',(.30*sg,-1.958,3.59),(.046,.018,.046),amber),uv('V05 • pupil',(.30*sg,-1.975,3.59),(.014,.008,.038),black)]
 headparts.append(tube('V05 • angry brow',[(sg*.13,-1.92,3.65),(sg*.28,-1.96,3.69),(sg*.43,-1.80,3.68)],.065,skin,[.65,1,.3]))
 headparts.append(tube('V05 • forward pointed horn',[(sg*.27,-1.40,3.80),(sg*.31,-1.50,4.07),(sg*.29,-1.87,4.19)],.105,black,[1,.65,.01]))
 headparts.append(tube('V05 • canine',[(sg*.21,-2.14,3.29),(sg*.21,-2.18,3.18),(sg*.18,-2.15,3.13)],.045,ivory,[1,.65,.01]))
for x in [-.12,-.06,0,.06,.12]:headparts.append(uv('V05 • upper tooth',(x,-2.175,3.26),(.026,.024,.04),ivory))
for j in range(17):
 x=(j-8)*.028;headparts.append(tube('V05 • tapered beard',[(x,-1.97,3.13),(x*1.1,-1.97,2.94),(x*.55,-1.79,2.71+abs(x)*.3)],.035,gold,[1,.8,.01]))
# Feather vanes: broad face directed outward, overlapping layered silhouette.
def feather(n,base,tip,width,normal,m):
 a=Vector(base);d=Vector(tip)-a;normal=Vector(normal).normalized();u=d.normalized().cross(normal).normalized();vs=[]
 for i in range(11):
  t=i/10;c=a+d*t+normal*.045*sin(pi*t);w=width*sin(pi*t)**.7
  vs.extend([c-u*w,c+normal*.025,c+u*w])
 fs=[]
 for i in range(10):
  k=i*3;fs += [(k,k+3,k+4,k+1),(k+1,k+4,k+5,k+2)]
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.materials.append(m);o=bpy.data.objects.new(n,me);col.objects.link(o)
 for p in me.polygons:p.use_smooth=True
 mod=o.modifiers.new('Vane thickness','SOLIDIFY');mod.thickness=.012
 return o
bodyfeathers=[];wingparts={'L':[],'R':[]}
for sg,side in [(-1,'L'),(1,'R')]:
 for row in range(4):
  for i in range(12):
   y=-1.05+i*.18;z=2.65-row*.18;x=sg*(.52+.11*sin(row*pi/4))
   bodyfeathers.append(feather('V05 • body contour',(x,y,z),(x*1.08,y+.35,z-.24),.105,(sg,0,.2),gold if i%3 else edge))
 for row in range(3):
  for i in range(14):
   base=(sg*(.53+row*.10),-.70+i*.10,2.75-row*.11)
   tip=(sg*(.83+row*.1),.60+i*.105,2.15-row*.12)
   wingparts[side].append(feather('V05 • layered folded wing',base,tip,.16,(sg,0,.25),brown if row==2 else gold))
 for row in range(4):
  for i in range(8):
   y=-1.72+i*.11;z=3.78-row*.18;x=sg*(.30+.06*row)
   headparts.append(feather('V05 • swept lion feather ruff',(x,y,z),(x+sg*.20,y+.31,z-.30),.095,(sg,-.2,.1),gold if i%3 else edge))
# Rig with four genuine weight-bearing limbs.
arm=bpy.data.armatures.new('Anzu V05 • quadruped skeleton');rig=bpy.data.objects.new('ANZU_V05_RIG',arm);col.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def bone(n,h,t,parent=None):
 b=arm.edit_bones.new(n);b.head=h;b.tail=t
 if parent:b.parent=arm.edit_bones[parent]
bone('root',(0,0,0),(0,0,.3));bone('spine',(0,.8,2),(0,-.5,2.3),'root');bone('head',(0,-1.1,2.8),(0,-1.55,3.6),'spine');bone('seat',(0,.2,2.78),(0,.2,3),'spine');bone('tail',(0,1.3,2.1),(0,2.3,2.2),'spine')
joints={}
for sg,side in [(-1,'L'),(1,'R')]:
 bone('wing.'+side,(sg*.45,-.55,2.55),(sg*.8,.9,2.5),'spine')
 for kind,y in [('front',-.98),('hind',1.02)]:
  key=kind+'.'+side;h=Vector((sg*.52,y,2.07));k=Vector((sg*.58,y+(.18 if kind=='hind' else -.08),1.12));f=Vector((sg*.60,y-.10,.18));joints[key]=(h,k,f)
  bone(key+'.upper',h,k,'root');bone(key+'.lower',k,f,key+'.upper');bone(key+'.foot',f,f+Vector((0,-.4,0)),key+'.lower')
bpy.ops.object.mode_set(mode='OBJECT')
def bind(o,b):
 w=o.matrix_world.copy();o.parent=rig;o.parent_type='BONE';o.parent_bone=b;bpy.context.view_layer.update();o.matrix_world=w
bind(body,'spine')
for o in bodyfeathers:bind(o,'spine')
for o in headparts:bind(o,'head')
for side,obs in wingparts.items():
 for o in obs:bind(o,'wing.'+side)
# Continuous skinned limbs; knee rings blend between upper/lower bones.
for key,(h,k,f) in joints.items():
 vs=[];weights=[];fs=[]
 for i in range(21):
  t=i/20;p=h.lerp(k,t*2) if t<=.5 else k.lerp(f,(t-.5)*2)
  rad=(.28*(1-t)+.105*t)*(1+.1*sin(t*pi*4));blend=max(0,min(1,(t-.38)/.24))
  for j in range(16):
   ang=j*2*pi/16;vs.append(p+Vector((rad*cos(ang),rad*sin(ang),0)));weights.append(blend)
 for i in range(20):
  for j in range(16):a=i*16+j;b=i*16+(j+1)%16;fs.append((a,b,b+16,a+16))
 fs.extend([tuple(reversed(range(16))),tuple(range(320,336))])
 me=bpy.data.meshes.new(key);me.from_pydata(vs,[],fs);me.materials.append(skin);o=bpy.data.objects.new('V05 • continuous '+key,me);col.objects.link(o)
 for p in me.polygons:p.use_smooth=True
 gu=o.vertex_groups.new(name=key+'.upper');gl=o.vertex_groups.new(name=key+'.lower')
 for i,t in enumerate(weights):gu.add([i],1-t,'REPLACE');gl.add([i],t,'REPLACE')
 m=o.modifiers.new('Continuous skin deformation','ARMATURE');m.object=rig;o.parent=rig
 joint=uv('V05 • shoulder/haunch',h,(.30,.32,.37),skin);bind(joint,key+'.upper')
 for j in range(3):
  x=f.x+(j-1)*.115;p=(x,f.y-.18,.13);o=uv('V05 • articulated toe',p,(.10,.30,.12),skin);bind(o,key+'.foot')
  o=tube('V05 • curved claw',[(x,f.y-.36,.14),(x,f.y-.50,.10),(x,f.y-.56,.05)],.065,black,[1,.6,.01]);bind(o,key+'.foot')
for i in range(9):
 o=feather('V05 • fan tail',((i-4)*.05,1.3,2.25),((i-4)*.14,2.6,2.05),.13,(0,0,1),gold if i%2 else brown);bind(o,'tail')
# Saddle, continuous leather belt and reins.
saddle=uv('V05 • soft saddle',(0,.28,2.77),(.40,.48,.12),leather);bind(saddle,'seat')
for y in [.15,.48]:
 o=tube('V05 • girth belt',[(.72*cos(t),y,2.1+.73*sin(t)) for t in [i*2*pi/24 for i in range(25)]],.045,leather);bind(o,'spine')
# Boy seated naturally with bent knees, feet beside flanks.
for p in boy.pose.bones:
 for c in p.constraints:c.mute=True
boy.animation_data_clear()
def aim(r,n,h,t):
 p=r.pose.bones[n];p.matrix=Matrix.Translation(Vector(h))@(Vector(t)-Vector(h)).to_track_quat('Y','Z').to_matrix().to_4x4();bpy.context.view_layer.update()
for side,sg in [('L',1),('R',-1)]:
 aim(boy,'thigh.'+side,(sg*.071,.006,.715),(sg*.34,-.13,.64));aim(boy,'shin.'+side,(sg*.34,-.13,.64),(sg*.38,-.08,.34));aim(boy,'foot.'+side,(sg*.38,-.08,.34),(sg*.38,-.19,.29))
 aim(boy,'upper_arm.'+side,(sg*.135,0,1.095),(sg*.20,-.13,.89));aim(boy,'forearm.'+side,(sg*.20,-.13,.89),(sg*.15,-.29,.86))
boy.matrix_world=Matrix.Translation((0,.30,1.50))@Matrix.Diagonal((1.85,1.85,1.85,1));bind(boy,'seat')
for sg in [-1,1]:
 o=tube('V05 • hand reins',[(sg*.28,-.24,3.09),(sg*.38,-.65,2.92),(sg*.4,-1.35,2.85)],.022,leather);bind(o,'seat')
# Slow quadruped walk with three-foot support and horizontal root motion.
N=192;period=96;speed=.010
for frame in range(1,N+1):
 t=frame-1;rig.location=(0,-t*speed,0);rig.keyframe_insert('location',frame=frame)
 for key,(h,k,f) in joints.items():
  offset={'hind.L':0,'front.L':.25,'hind.R':.5,'front.R':.75}[key];ph=(t/period+offset)%1;stride=speed*period
  target=f.copy()
  if ph<.75:target.y+=stride*(ph-.375)
  else:
   u=(ph-.75)/.25;target.y+=stride*.375-stride*.75*(u*u*(3-2*u));target.z+=.18*sin(pi*u)
  d=target-h;dist=d.length;L1=(k-h).length;L2=(f-k).length;along=(L1*L1-L2*L2+dist*dist)/(2*dist);bend=Vector((0,-d.z,d.y)).normalized();knee=h+d.normalized()*along+bend*math.sqrt(max(.0001,L1*L1-along*along))
  for part,aa,bb in [('upper',h,knee),('lower',knee,target),('foot',target,target+Vector((0,-.4,0)))]:
   p=rig.pose.bones[key+'.'+part];p.rotation_mode='QUATERNION';aim(rig,p.name,aa,bb)
   for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(prop,frame=frame)
 for n,ang in [('head',.013*sin(t*.04)),('tail',.025*sin(t*.035)),('wing.L',.012*sin(t*.045)),('wing.R',-.012*sin(t*.045))]:
  p=rig.pose.bones[n];p.rotation_mode='XYZ';p.rotation_euler=(0,ang,0);p.keyframe_insert('rotation_euler',frame=frame)
cam=s.camera;cam.animation_data_clear();cam.data.lens=52
for f in [1,N]:
 y=-speed*(f-1);cam.location=(8,y-9,5.5);cam.rotation_euler=(Vector((0,y,2))-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
s.frame_start=1;s.frame_end=N;s.render.fps=24;s.frame_set(1);s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=8
bpy.ops.wm.save_as_mainfile(filepath='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/riding/Enkidu_Anzu_quadruped_v05.blend')
s.render.engine='BLENDER_WORKBENCH';s.display.shading.color_type='MATERIAL';s.display.shading.light='STUDIO';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.render_aa='8';s.render.filepath='/private/tmp/anzu_v05_preview.png';bpy.ops.render.render(write_still=True)
