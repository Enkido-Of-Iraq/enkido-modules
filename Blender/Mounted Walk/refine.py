import bpy,math,random
from mathutils import Vector
from math import sin,cos,pi
s=bpy.context.scene;a=bpy.data.objects['ANZU_RIG • rideable creature'];r=bpy.data.objects['ENKIDU_RIG'];s.frame_set(1)
def bind(o,b):
 w=o.matrix_world.copy();o.parent=a;o.parent_type='BONE';o.parent_bone=b;bpy.context.view_layer.update();o.matrix_world=w
# Remove stage obstacles from this shot only.
for o in s.objects:
 if o.type in ['MESH','CURVE'] and not o.parent and not o.name.startswith('ANIM'):
  if any(w in o.name.lower() for w in ['column','wall','brazier','step','rubble','plinth','pedestal']):o.hide_render=True;o.hide_set(True)
 if o.parent==a and any(w in o.name for w in ['primary feather','secondary feather','wing arm','cheek feather','heavy brow','swept crest']):o.hide_render=True;o.hide_set(True)
gold=bpy.data.materials['Lion • warm tawny gold'];dark=bpy.data.materials['Lion • horn keratin']
def feather(n,base,tip,width,ma,b):
 base=Vector(base);tip=Vector(tip);d=tip-base;u=d.normalized().cross(Vector((0,0,1)))
 if u.length<.1:u=Vector((1,0,0))
 u.normalize();v=u.cross(d.normalized()).normalized();verts=[]
 for i in range(9):
  t=i/8;w=width*(sin(pi*t)**.65+.015);center=base+d*t+v*.05*sin(pi*t)
  verts.extend([center-u*w,center+v*.035,center+u*w])
 faces=[]
 for i in range(8):
  j=i*3;faces.extend([(j,j+3,j+4,j+1),(j+1,j+4,j+5,j+2)])
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.materials.append(ma);o=bpy.data.objects.new(n,me);s.collection.objects.link(o)
 for p in me.polygons:p.use_smooth=True
 sol=o.modifiers.new('Feather thickness','SOLIDIFY');sol.thickness=.015
 bind(o,b)
for side,sg in [('L',-1),('R',1)]:
 for row in range(3):
  for i in range(13):
   base=(sg*(.73+row*.18),-.25+i*.09,3.65-row*.12)
   tip=(sg*(1.20+row*.18+i*.035),.95+i*.13,2.75-row*.10+i*.018)
   feather('Folded wing • '+side,base,tip,.14,gold if (i+row)%3 else dark,'wing.'+side)
# Mantle overlapping rows around body, keeping saddle clear.
for row in range(6):
 z=3.45-row*.27
 for i in range(23):
  t=2*pi*i/23;rx=1.18*math.sqrt(max(.15,1-((z-2.65)/1.4)**2));ry=1.82*math.sqrt(max(.15,1-((z-2.65)/1.4)**2))
  base=(rx*cos(t),ry*sin(t),z);tip=(rx*1.02*cos(t),ry*1.02*sin(t)+.16,z-.44)
  feather('Mantle • overlapping feather',base,tip,.12,gold if i%4 else dark,'spine')
for row in range(4):
 for i in range(13):
  t=-pi*.1+pi*1.2*i/12
  base=(.57*cos(t),-.85+.57*sin(t),5.35-row*.22)
  tip=(.88*cos(t),-.65+.83*sin(t),4.90-row*.25)
  feather('Head • swept feather ruff',base,tip,.11,gold,'head')
# Wider camera side angle reveals rider. Clear arena floor.
cam=s.camera;cam.animation_data_clear()
for f in [1,192]:
 y=-.018*(f-1);cam.location=(11.5,y-8.0,6.5);target=Vector((0,y,2.8));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
cam.data.lens=48
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/riding/Enkidu_Anzu_mounted_walk_v02.blend')
s.render.filepath='/private/tmp/mounted_preview2.png';bpy.ops.render.render(write_still=True)
