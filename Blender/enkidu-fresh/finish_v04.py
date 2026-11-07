import bpy,bmesh,math,random
from math import sin,cos,pi,exp,sqrt,asin
from mathutils import Vector
random.seed(173)
s=bpy.context.scene
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
# recover the analytic surface functions without re-running construction
source=open(ROOT+'/enhance_v03.py').read()
start=source.index('profiles=');end=source.index('\ndef mesh(')
exec(source[start:end])
scale=.82
centerz=1.194+(1.347-1.194)*scale
head=next(o for o in s.objects if o.name.startswith('Enkidu • sculpted head'))
# Clean the orbital boundary to smooth ellipses rather than grid-cut jagged edges.
bm=bmesh.new();bm.from_mesh(head.data)
for v in bm.verts:
 if not v.is_boundary:continue
 for side in [-1,1]:
  cx=side*.043*scale;dx=v.co.x-cx;dz=v.co.z-centerz
  if abs(dx)<.028*scale and abs(dz)<.016*scale and v.co.y<-.03:
   r=sqrt((dx/(.0214*scale))**2+(dz/(.0076*scale))**2)
   if r>.05:
    v.co.x=cx+dx/r;v.co.z=centerz+dz/r*(.0095/.0076)
    z=1.194+(v.co.z-1.194)/scale;x=v.co.x/scale;v.co.y=front(x,z)*scale
bm.to_mesh(head.data);bm.free()
def uvface(me):
 uv=me.uv_layers.active
 for lo in me.loops:
  x,y,z=me.vertices[lo.vertex_index].co;x/=scale;z=1.194+(z-1.194)/scale
  uv.data[lo.index].uv=((1107+x*1600)/1536,1-(570-(z-1.2)*1538)/1024)
uvface(head.data)
for ob in s.objects:
 if ob.name.startswith('Inset almond eye'):
  for v in ob.data.vertices:
   v.co.z=centerz+(v.co.z-centerz)*1.24
   x=v.co.x/scale;z=1.194+(v.co.z-1.194)/scale
   side=1 if x>0 else -1;r=sqrt(((x-side*.043)/.0218)**2+((z-1.347)/.0098)**2)
   v.co.y=(front(x,z)+.0015-.0035*max(0,1-r*r))*scale
  uvface(ob.data)
  p=ob.data.materials[0].node_tree.nodes.get('Principled BSDF');p.inputs['Coat Weight'].default_value=.12;p.inputs['Coat Roughness'].default_value=.20;p.inputs['Roughness'].default_value=.42;p.inputs['Specular IOR Level'].default_value=.15
 if ob.type=='CURVE' and ob.name.startswith(('Upper lash line','Fine upper eyelashes')):
  for sp in ob.data.splines:
   for p in sp.points:
    p.co.z=centerz+(p.co.z-centerz)*1.2
    x=p.co.x/scale;z=1.194+(p.co.z-1.194)/scale;p.co.y=(front(x,z)-.0007)*scale
 if ob.name.startswith('Ear helix contour'):ob.data.bevel_depth*=.55
 if ob.name.startswith('Neck ribbing'):
  for sp in ob.data.splines:
   for p in sp.points:p.radius=1
# Dark scalp and fine under-groom remove the exposed skin gaps between long wave bundles.
coll=next(c for c in s.collection.children if c.name.startswith('Hair groom'))
ma=next(o for o in coll.objects if o.name.startswith('Tousled wavy locks 0')).data.materials[0]
N=160;R=56;v=[];f=[]
for j in range(R):
 for i in range(N):
  a=2*pi*i/N;end=1.72+.14*sin(5*a)+.06*cos(9*a)
  if cos(a)<0:end=2.3+.08*sin(a*7)
  p=.005+(end-.005)*j/(R-1)
  x=.087*sin(p)*sin(a);y=.01-.079*sin(p)*cos(a);z=1.411+.064*cos(p)
  v.append((x*scale,y*scale,1.194+(z-1.194)*scale))
for j in range(R-1):
 for i in range(N):a=j*N+i;b=j*N+(i+1)%N;f.append((a,a+N,b+N,b))
me=bpy.data.meshes.new('Scalp hairline mesh');me.from_pydata(v,[],f);me.update();me.materials.append(ma)
ob=bpy.data.objects.new('Dark root underlayer with irregular hairline',me);coll.objects.link(ob)
for p in me.polygons:p.use_smooth=True
cu=bpy.data.curves.new('Fine root filler hairs','CURVE');cu.dimensions='3D';cu.bevel_depth=.00010;cu.bevel_resolution=1
for k in range(16000):
 a=random.uniform(-pi,pi);end=1.7 if cos(a)>.1 else 2.3;p=random.uniform(.02,end);phase=random.uniform(-pi,pi);pts=[]
 for j in range(12):
  t=j/11;aa=a+.18*t;pp=p+.16*t;rr=.002*sin(pi*t)+.0007*sin(7*t+phase)
  x=(.09+rr)*sin(pp)*sin(aa);y=.01-(.082+rr)*sin(pp)*cos(aa);z=1.411+(.068+rr)*cos(pp)
  pts.append((x*scale,y*scale,1.194+(z-1.194)*scale))
 sp=cu.splines.new('POLY');sp.points.add(11)
 for j,co in enumerate(pts):sp.points[j].co=(*co,1);sp.points[j].radius=1-j/12
ob=bpy.data.objects.new('Fine root and short hair detail',cu);coll.objects.link(ob);cu.materials.append(ma)
# subtle cartilage folds and tragus integrate with the existing outer ear.
skin=next(o for o in s.objects if o.name.startswith('Slim arm')).data.materials[0]
colla=next(c for c in s.collection.children if c.name.startswith('Anatomy'))
for side in [-1,1]:
 cu=bpy.data.curves.new('Ear inner cartilage','CURVE');cu.dimensions='3D';cu.bevel_depth=.00085;cu.bevel_resolution=3
 sp=cu.splines.new('NURBS');sp.points.add(17);sp.order_u=3;sp.use_endpoint_u=True
 for j in range(18):
  t=j/17;a=-pi*.45+pi*1.35*t;x=side*(.094+.005*cos(a));y=-.013-.002*sin(pi*t);z=1.303+.019*sin(a)
  sp.points[j].co=(x*scale,y*scale,1.194+(z-1.194)*scale,1);sp.points[j].radius=.6+.3*sin(pi*t)
 ob=bpy.data.objects.new('Inner ear antihelix '+str(side),cu);colla.objects.link(ob);cu.materials.append(skin)
# front studio softened to avoid a strip reflection across the eyes
for o in s.objects:
 if o.type=='LIGHT' and 'key' in o.name:o.location.x=-2.7;o.data.energy=175
s.render.resolution_x=1100;s.render.resolution_y=1100;s.cycles.samples=128
s.render.filepath=ROOT+'/enkidu-face-v04.png'
s['Revision notes']+=' V04: smoothed orbital boundaries, larger natural eye openings, subdued corneal reflection, filled hair roots, inner ear cartilage, continuous collar seam.'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_enhanced_v04.blend')
result={'file':bpy.data.filepath,'objects':len(s.objects),'root_hairs':16000}
