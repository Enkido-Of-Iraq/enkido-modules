import bpy, math, os
from mathutils import Vector, Matrix
from math import sin,cos,pi
s=bpy.context.scene
s.name='Enkidu riding Anzu • slow walk'
a=bpy.data.objects['ANZU_RIG • rideable creature'];r=bpy.data.objects['ENKIDU_RIG']
for o in [a,r,s.camera]:
 o.animation_data_clear()
for rig in [a,r]:
 for p in rig.pose.bones:p.matrix_basis.identity()
a.location=(0,0,0)
s.frame_set(1);bpy.context.view_layer.update()
# All edits are a new version; original files remain unchanged.
def bind(o,b,rig=a):
 w=o.matrix_world.copy();o.parent=rig;o.parent_type='BONE';o.parent_bone=b;bpy.context.view_layer.update();o.matrix_world=w
# Repair unmatched legacy name patterns.
for o in list(s.objects):
 if o.parent!=a:continue
 for side in ['L','R']:
  if '• '+side+' primary feather' in o.name or '• '+side+' secondary feather' in o.name:bind(o,'wing.'+side)
# Build coherent walking chains fitted to actual mesh joints.
bpy.context.view_layer.objects.active=a;a.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for side,x in [('L',-.63),('R',.63)]:
 for name,h,t,parent in [('walk_thigh',(x,.7,2.15),(x,.10,1.05),'root'),('walk_shin',(x,.10,1.05),(x,-.35,.20),'walk_thigh.'+side),('walk_foot',(x,-.35,.20),(x,-.9,.20),'walk_shin.'+side)]:
  b=a.data.edit_bones.new(name+'.'+side);b.head=h;b.tail=t;b.parent=a.data.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
for o in list(s.objects):
 if o.parent!=a:continue
 for side in ['L','R']:
  for pattern,bone in [('thigh','walk_thigh'),('shin','walk_shin'),('foot toe','walk_foot'),('claw','walk_foot')]:
   if '• '+side+' '+pattern in o.name:bind(o,bone+'.'+side)
# Real material colors, sculptural lion muzzle, compact horns and beard.
def mat(n,c,metal=0,rough=.55):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
gold=mat('Lion • warm tawny gold',(.36,.18,.055),.18)
dark=mat('Lion • nose and mouth',(.025,.012,.008),0,.38)
ivory=mat('Lion • aged ivory',(.72,.59,.34),0,.3)
horn=mat('Lion • horn keratin',(.13,.065,.024),.1)
leather=mat('Mounted harness • leather',(.09,.029,.012),0,.67)
def uv(n,loc,scale,m,b='head'):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=loc);o=bpy.context.object;o.name=n;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 for p in o.data.polygons:p.use_smooth=True
 bind(o,b);return o
def tube(n,points,radius,m,b='head',radii=None):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=radius;c.bevel_resolution=3;c.resolution_u=16
 sp=c.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for i,(p,co) in enumerate(zip(sp.bezier_points,points)):
  p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO';p.radius=radii[i] if radii else 1
 o=bpy.data.objects.new(n,c);s.collection.objects.link(o);c.materials.append(m);bind(o,b);return o
for o in s.objects:
 if any(k in o.name for k in ['hooked beak','lower mandible','nostril','swept crest']):o.hide_render=True;o.hide_set(True)
uv('Lion • dark mouth',(0,-1.64,4.60),(.35,.28,.23),dark)
uv('Lion • lower jaw',(0,-1.57,4.37),(.36,.35,.17),gold)
for sg in [-1,1]:
 uv('Lion • muzzle',(.17*sg,-1.68,4.83),(.23,.32,.21),gold)
 uv('Lion • cheek',(.40*sg,-1.32,4.83),(.27,.3,.4),gold)
 tube('Lion • forward horn',[(sg*.38,-.95,5.45),(sg*.43,-1.05,5.76),(sg*.42,-1.45,5.94)],.13,horn,radii=[1,.7,.015])
 tube('Lion • upper fang',[(sg*.26,-1.82,4.73),(sg*.28,-1.91,4.60),(sg*.22,-1.94,4.44)],.065,ivory,radii=[1,.8,.01])
for x in [-.14,-.07,0,.07,.14]:uv('Lion • incisor',(x,-1.94,4.70),(.035,.048,.07),ivory)
uv('Lion • broad nose',(0,-1.97,4.90),(.19,.09,.10),dark)
for j in range(17):
 x=(j-8)*.035
 tube('Lion • flowing beard',[(x,-1.65,4.38),(x*1.15,-1.71,4.10),(x*.7,-1.48,3.80+.12*abs(x))],.055,gold,radii=[1,.75,.01])
# Harness girth encircles body, with a visible buckle and reins.
pts=[(1.26*cos(t),.3,2.65+1.29*sin(t)) for t in [i*2*pi/24 for i in range(25)]]
tube('Harness • continuous girth',pts,.075,leather,'spine')
tube('Harness • brass buckle',[(1.30,.22,2.9),(1.30,.22,3.13),(1.30,.43,3.13),(1.30,.43,2.9),(1.30,.22,2.9)],.035,ivory,'spine')
# Seat boy with joint directions set in armature coordinates.
for side in ['L','R']:r['Leg IK '+side]=0.;r['Arm IK '+side]=0.
r.update_tag();bpy.context.view_layer.update()
def aim(rig,n,h,t):
 p=rig.pose.bones[n];q=(Vector(t)-Vector(h)).to_track_quat('Y','Z');p.matrix=Matrix.Translation(Vector(h))@q.to_matrix().to_4x4();bpy.context.view_layer.update()
for side,sg in [('L',1),('R',-1)]:
 hip=(sg*.071,.006,.715);knee=(sg*.32,-.18,.55);ankle=(sg*.34,-.12,.25)
 aim(r,'thigh.'+side,hip,knee);aim(r,'shin.'+side,knee,ankle);aim(r,'foot.'+side,ankle,(sg*.34,-.23,.19))
 sh=(sg*.135,0,1.095);el=(sg*.22,-.13,.89);hand=(sg*.16,-.29,.87)
 aim(r,'upper_arm.'+side,sh,el);aim(r,'forearm.'+side,el,hand)
r.scale=(1.8,1.8,1.8);r.location=(0,.65,2.53)
bpy.context.view_layer.update();bind(r,'rider_mount')
for sg in [-1,1]:tube('Harness • rein',[(sg*.29,.12,4.10),(sg*.45,-.35,3.85),(sg*.5,-1.05,3.7)],.028,leather,'spine')
# Analytic two-link gait: feet remain fixed in world during stance.
# Keys are baked per frame; world forward is -Y. No root vertical travel.
rest={n:a.data.bones[n].matrix_local.copy() for n in a.data.bones.keys()}
N=192;period=72;speed=.018
for f in range(1,N+1):
 t=f-1;a.location=(0,-speed*t,0);a.keyframe_insert('location',frame=f)
 for side,offset,sg in [('L',0,-1),('R',.5,1)]:
  phase=(t/period+offset)%1;cycle=math.floor(t/period+offset)
  # stance 65%, swing 35%; exact stance cancellation of root movement
  stride=speed*period
  if phase<.65:fy=-.35-stride*.325+stride*phase;fz=.20
  else:
   u=(phase-.65)/.35;sm=u*u*(3-2*u);fy=-.35+stride*.325-stride*.65*sm;fz=.20+.24*sin(pi*u)
  hip=Vector((sg*.63,.7,2.15));foot=Vector((sg*.63,fy,fz));d=(foot-hip);dist=d.length;L1=1.253;L2=.962
  direction=d.normalized();along=(L1*L1-L2*L2+dist*dist)/(2*dist);height=math.sqrt(max(.01,L1*L1-along*along));bend=Vector((0,-direction.z,direction.y));knee=hip+direction*along+bend*height
  for name,h,ta in [('walk_thigh',hip,knee),('walk_shin',knee,foot),('walk_foot',foot,foot+Vector((0,-.55,0)))]:
   p=a.pose.bones[name+'.'+side];p.rotation_mode='QUATERNION';aim(a,p.name,h,ta);p.keyframe_insert('location',frame=f);p.keyframe_insert('rotation_quaternion',frame=f);p.keyframe_insert('scale',frame=f)
 for name,ang in [('head',.018*sin(t*.035)),('wing.L',.018*sin(t*.05)),('wing.R',-.018*sin(t*.05)),('tail',.025*sin(t*.04))]:
  p=a.pose.bones[name];p.rotation_mode='XYZ';p.rotation_euler=(0,ang,0);p.keyframe_insert('rotation_euler',frame=f)
# Camera follows slowly, preserving feet and rider in frame.
cam=s.camera;cam.animation_data_clear();cam.data.type='PERSP';cam.data.lens=48
for f in [1,N]:
 y=-speed*(f-1);cam.location=(10.8,y-12.0,7.2);target=Vector((0,y,2.9));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
s.frame_start=1;s.frame_end=N;s.render.fps=24;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.frame_set(1)
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
a['Animation notes']='Slow -Y travel; two-link planted-foot gait; rigid Anzu pieces, weighted Enkidu rider. Stylized assembly, not final sculpt.'
bpy.ops.wm.save_as_mainfile(filepath='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/riding/Enkidu_Anzu_mounted_walk_v01.blend')
s.render.filepath='/private/tmp/mounted_preview.png';bpy.ops.render.render(write_still=True)
