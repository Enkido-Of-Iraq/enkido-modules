import bpy,math,random
from math import sin,cos,pi
from mathutils import Vector
random.seed(155)
s=bpy.context.scene
# Remove only the generated failed setup scene, leave user's original default scene intact.
for sc in list(bpy.data.scenes):
 if sc!=s and sc.name.startswith('Enkidu • fresh character'):bpy.data.scenes.remove(sc)
s.name='Enkidu • fresh rebuild'
# Bring whites behind orbital rims, retaining actual 3D irises.
for o in s.objects:
 if o.name.startswith(('Eyeball','Iris','Pupil')):o.location.y+=.010
 if o.type=='CURVE' and o.name.startswith(('Upper eyelid','Lower eyelid','Individual upper lashes')):
  for sp in o.data.splines:
   for p in sp.points:p.co.y+=.009
# Open garment necks and cuffs instead of primitive end caps.
import bmesh
for o in s.objects:
 if o.type=='MESH' and o.name.startswith(('Oversized cotton','Short sleeve','Trouser leg')):
  bm=bmesh.new();bm.from_mesh(o.data)
  bmesh.ops.delete(bm,geom=[f for f in bm.faces if len(f.verts)>20],context='FACES_ONLY')
  bm.to_mesh(o.data);bm.free()
  sol=o.modifiers.new('Cloth thickness','SOLIDIFY');sol.thickness=.0015
  if o.name.startswith('Trouser leg'):
   for v in o.data.vertices:
    if v.co.z<.24:v.co.z-=.045*(.24-v.co.z)/.105
    if v.co.z<.35:
     v.co.x+=(.003*sin(v.co.z*220)+.002*sin(v.co.z*125))*(1 if v.co.x>0 else -1)
  if o.name.startswith('Short sleeve'):
   for v in o.data.vertices:
    if v.co.z>1.06:v.co.z+=.022*(v.co.z-1.06)/.055
# Reference cotton and twill colour; true 3D normal / roughness retained.
ref=next(i for i in bpy.data.images if 'exec-400a2b28' in i.filepath)
for o in s.objects:
 if o.type!='MESH' or not o.name.startswith(('Oversized cotton','Short sleeve','Trouser leg','Canvas shoe upper')):continue
 ma=o.data.materials[0].copy();o.data.materials[0]=ma;n=ma.node_tree.nodes;l=ma.node_tree.links;p=n.get('Principled BSDF')
 old=p.inputs['Base Color'].links[0].from_socket if p.inputs['Base Color'].is_linked else None
 tex=n.new('ShaderNodeTexImage');tex.image=ref;tex.extension='EXTEND'
 a=n.new('ShaderNodeAttribute');a.attribute_name='FrontColour'
 mix=n.new('ShaderNodeMixRGB');l.new(a.outputs['Fac'],mix.inputs[0]);l.new(tex.outputs[0],mix.inputs[2])
 if old:l.new(old,mix.inputs[1])
 l.new(mix.outputs[0],p.inputs['Base Color'])
 at=o.data.attributes.new('FrontColour','FLOAT','POINT')
 for i,v in enumerate(o.data.vertices):at.data[i].value=max(0,min(1,-v.co.y/.025))*.92
 uv=o.data.uv_layers.new(name='Garment front reference')
 for lo in o.data.loops:
  x,y,z=o.data.vertices[lo.vertex_index].co
  if o.name.startswith('Trouser'):py=917-(z-.09)*650
  elif o.name.startswith('Canvas shoe'):py=990-z*650
  else:py=516-(z-.744)*720
  uv.data[lo.index].uv=((382+x*650)/1536,1-py/1024)
# Replace entire upright groom with irregular, swept waves around the skull.
coll=next(c for c in s.collection.children if c.name.startswith('Hair groom'))
ma=next(o.data.materials[0] for o in coll.objects if o.name.startswith('Wavy groom'))
for o in list(coll.objects):
 if o.name.startswith('Wavy groom'):bpy.data.objects.remove(o,do_unlink=True)
cap=next(o for o in coll.objects if o.name.startswith('Hair underlayer'));cap.scale=(.084,.077,.062)
cu=bpy.data.curves.new('Swept wavy strand groom','CURVE');cu.dimensions='3D';cu.bevel_depth=.00036;cu.bevel_resolution=2
for k in range(5200):
 a=random.uniform(-pi,pi);polar=random.uniform(.05,2.08)
 # keep hairline clear of eyes while adding falling fringe
 if cos(a)>.3:polar=min(polar,1.86)
 ph=random.uniform(0,2*pi);dr=random.uniform(.0,.008);sweep=random.uniform(.28,.65)
 pts=[]
 for j in range(24):
  t=j/23;aa=a+sweep*t+.07*sin(ph+6*t);pp=polar+.24*t
  radius=1+.07*sin(t*pi)+.03*sin(t*8+ph)
  x=(.097+dr)*sin(pp)*sin(aa)*radius
  y=.012-(.087+dr)*sin(pp)*cos(aa)*radius
  z=1.414+(.074+dr)*cos(pp)+.004*sin(8*t+ph)
  pts.append((x,y,z))
 sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for j,co in enumerate(pts):sp.points[j].co=(*co,1);sp.points[j].radius=.85*(1-j/25)+.08
ob=bpy.data.objects.new('Swept wavy groom • 5200 strands',cu);coll.objects.link(ob);cu.materials.append(ma)
# ground framing, skin cohesion, realistic three-quarter inspection
for o in s.objects:
 if o.name.startswith('Studio floor'):o.location.z=.007
s.camera=next(o for o in s.objects if o.name.startswith('Camera • full character'))
s.camera.data.ortho_scale=1.61
s.render.resolution_x=1000;s.render.resolution_y=1250;s.render.resolution_percentage=100;s.cycles.samples=64
s.render.filepath='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh/enkidu-fresh-front.png'
bpy.ops.wm.save_as_mainfile(filepath='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh/Enkidu_fresh_v02.blend')
result={'file':bpy.data.filepath,'objects':len(s.objects),'scene':s.name}
