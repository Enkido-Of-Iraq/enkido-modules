import bpy, math, random
from math import sin,cos,pi,exp,sqrt,asin
from mathutils import Vector
random.seed(240)
s=bpy.context.scene
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
COL={k:next(c for c in s.collection.children if c.name.startswith(k)) for k in ['Anatomy','Eyes and lashes','Hair groom','Clothing','Studio']}
head=next(o for o in s.objects if o.name.startswith('Enkidu • sculpted head'))
face=head.data.materials[0];skin=next(o for o in s.objects if o.name.startswith('Slim arm')).data.materials[0]
ref=next(n.image for n in face.node_tree.nodes if n.type=='TEX_IMAGE')
# Smooth anatomical profiles using cubic Hermite interpolation rather than linear rings.
profiles=[(1.194,.012,.032),(1.205,.034,.043),(1.225,.055,.053),(1.25,.073,.062),(1.28,.085,.071),(1.31,.088,.075),(1.34,.086,.077),(1.37,.084,.079),(1.40,.082,.078),(1.43,.069,.067),(1.45,.047,.047),(1.461,.006,.012)]
def prof(z):
 z=max(profiles[0][0],min(profiles[-1][0],z))
 for i in range(len(profiles)-1):
  a,b=profiles[i],profiles[i+1]
  if a[0]<=z<=b[0]:
   t=(z-a[0])/(b[0]-a[0]);prev=profiles[max(0,i-1)];nex=profiles[min(len(profiles)-1,i+2)]
   vals=[]
   for k in [1,2]:
    m0=(b[k]-prev[k])/(b[0]-prev[0])*(b[0]-a[0]);m1=(nex[k]-a[k])/(nex[0]-a[0])*(b[0]-a[0])
    vals.append((2*t**3-3*t*t+1)*a[k]+(t**3-2*t*t+t)*m0+(-2*t**3+3*t*t)*b[k]+(t**3-t*t)*m1)
   return vals
 return profiles[-1][1:]
def G(x,z,cx,cz,wx,wz):return exp(-((x-cx)/wx)**2-((z-cz)/wz)**2)
def front(x,z):
 w,d=prof(z);a=asin(max(-.9999,min(.9999,x/w)));c=max(cos(a),0)
 y=-d*c**.62
 # nasal bridge, tip, alar wings, philtrum, lip rolls, chin and malar eminences
 dlt=.024*G(x,z,0,1.302,.015,.015)+.014*G(x,z,0,1.331,.011,.036)
 dlt+=.008*(G(x,z,-.014,1.298,.009,.009)+G(x,z,.014,1.298,.009,.009))
 dlt+=.006*G(x,z,0,1.255,.032,.009)+.0045*G(x,z,0,1.246,.028,.006)
 dlt-=.0018*G(x,z,0,1.251,.033,.0018)
 dlt+=.004*G(x,z,0,1.218,.026,.018)
 dlt+=.005*(G(x,z,-.052,1.314,.027,.022)+G(x,z,.052,1.314,.027,.022))
 dlt+=.004*(G(x,z,-.046,1.37,.031,.011)+G(x,z,.046,1.37,.031,.011))
 dlt-=.003*(G(x,z,-.043,1.347,.025,.013)+G(x,z,.043,1.347,.025,.013))
 return y-c**5*dlt

def mesh(name,v,f,ma,coll,sub=1):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);COL[coll].objects.link(o)
 me.materials.append(ma)
 for p in me.polygons:p.use_smooth=True
 if sub:m=o.modifiers.new('Smooth surface subdivision','SUBSURF');m.levels=sub;m.render_levels=sub
 return o

def projection(me,weight=True):
 uv=me.uv_layers.new(name='Reference face colour')
 if weight:at=me.attributes.new('FrontBlend','FLOAT','POINT')
 for i,v in enumerate(me.vertices):
  x,y,z=v.co
  if weight:at.data[i].value=max(0,min(1,-y/.035))
 for lo in me.loops:
  x,y,z=me.vertices[lo.vertex_index].co
  uv.data[lo.index].uv=((1107+x*1600)/1536,1-(570-(z-1.2)*1538)/1024)

N=192;R=210;v=[];f=[]
for j in range(R):
 z=1.194+.267*j/(R-1);w,d=prof(z)
 for i in range(N):
  a=2*pi*i/N;x=w*sin(a);y=front(x,z) if cos(a)>=0 else -d*cos(a)
  # subtle natural facial asymmetry
  if cos(a)>0:y-=.0006*sin(x*43)*G(x,z,0,1.29,.1,.12)
  v.append((x,y,z))
for j in range(R-1):
 for i in range(N):
  ids=(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i)
  x,y,z=sum((Vector(v[k]) for k in ids),Vector())/4
  hole=y<-.035 and any(((x-c)/.0214)**2+((z-1.347)/.0076)**2<1 for c in [-.043,.043])
  if not hole:f.append(ids)
me=bpy.data.meshes.new('Cubic facial contour with modeled nose lips and cheeks');me.from_pydata(v,[],f);me.update();me.materials.append(face);projection(me)
head.data=me
for p in me.polygons:p.use_smooth=True
for mod in head.modifiers:mod.levels=2;mod.render_levels=2
# Subtle pores, lower waxiness, skin colour matched to the reference.
for ma in [skin,face]:
 n=ma.node_tree.nodes;l=ma.node_tree.links;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.53;p.inputs['Specular IOR Level'].default_value=.26
 p.inputs['Subsurface Weight'].default_value=.055;p.inputs['Subsurface Scale'].default_value=.006
 for b in n:
  if b.type=='BUMP':b.inputs['Strength'].default_value=.16;b.inputs['Distance'].default_value=.00014
 if ma==skin:p.inputs['Base Color'].default_value=(.25,.125,.054,1)
 else:
  for m in n:
   if m.type=='MIX_RGB':m.inputs[1].default_value=(.25,.125,.054,1)
# Hide the previous eye assemblies and brow groom, replace with inset corneal surfaces.
for coll in ['Eyes and lashes','Hair groom']:
 for o in list(COL[coll].objects):
  if coll=='Eyes and lashes' or o.name.startswith(('Eyebrow','Swept wavy','Hair underlayer')):
   bpy.data.objects.remove(o,do_unlink=True)

def curves(name,paths,radius,ma,coll,tip=.05):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=2;cu.resolution_u=2
 for pts in paths:
  sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
  for i,p in enumerate(pts):sp.points[i].co=(*p,1);sp.points[i].radius=1-(1-tip)*(i/(len(pts)-1))**2
 ob=bpy.data.objects.new(name,cu);COL[coll].objects.link(ob);cu.materials.append(ma);return ob

def simple(name,col,rough):
 ma=bpy.data.materials.new(name);ma.use_nodes=True;p=ma.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;return ma
strandmats=[simple('Hair • deep brown strand '+str(i),c,.38) for i,c in enumerate([(.012,.006,.003),(.022,.011,.005),(.035,.018,.008),(.055,.029,.014)])]
for ma in strandmats:ma.node_tree.nodes.get('Principled BSDF').inputs['Anisotropic'].default_value=.55
# Actual curved eye surfaces use the photographed iris / sclera colours to preserve identity.
eye=face.copy();eye.name='Eyes • reference iris, moist corneal coat'
n=eye.node_tree.nodes;l=eye.node_tree.links;p=n.get('Principled BSDF');t=next(n for n in n if n.type=='TEX_IMAGE');l.new(t.outputs['Color'],p.inputs['Base Color']);p.inputs['Subsurface Weight'].default_value=0;p.inputs['Roughness'].default_value=.24;p.inputs['Coat Weight'].default_value=.5;p.inputs['Coat Roughness'].default_value=.08
for li in list(p.inputs['Normal'].links):l.remove(li)
for side in [-1,1]:
 cx=side*.043
 # centre-to-rim radial topology; the visible almond masks all excess sclera.
 vv=[(cx,front(cx,1.347)-.002,1.347)];ff=[];A=96;B=16
 for j in range(1,B+1):
  r=j/B
  for i in range(A):
   a=2*pi*i/A;x=cx+.0218*r*cos(a);z=1.347+.0079*r*sin(a)
   y=front(x,z)+.0015-.0035*(1-r*r)
   vv.append((x,y,z))
 for i in range(A):ff.append((0,1+i,1+(i+1)%A))
 for j in range(B-1):
  for i in range(A):
   a=1+j*A+i;b=1+j*A+(i+1)%A;ff.append((a,a+A,b+A,b))
 ob=mesh('Inset almond eye '+str(side),vv,ff,eye,'Eyes and lashes',1);projection(ob.data)
 # a very thin upper waterline and natural tapering lashes
 paths=[]
 for i in range(50):
  a=.08+(pi-.16)*i/49;x=cx+.021*cos(a);z=1.347+.0078*sin(a);y=front(x,z)-.0003
  length=.0025+.0018*sin(a)
  paths.append([(x,y,z),(x+.0005*cos(a),y-.0018,z+length*.5),(x+.001*cos(a),y-.0025,z+length)])
 curves('Fine upper eyelashes '+str(side),paths,.00012,strandmats[0],'Eyes and lashes')
 water=[(cx+.021*cos(a),front(cx+.021*cos(a),1.347+.0077*sin(a))-.0002,1.347+.0077*sin(a)) for a in [pi*i/80 for i in range(81)]]
 curves('Upper lash line '+str(side),[water],.00035,strandmats[0],'Eyes and lashes',.5)
 # brow hair grows directly from brow surface; shape follows the photographic outline
 paths=[]
 for i in range(330):
  x=cx+random.uniform(-.025,.025);z=1.370+.004*(1-abs(x-cx)/.025)+random.uniform(-.0024,.0024);y=front(x,z)-.0004
  paths.append([(x,y,z),(x+side*.001,y-.0005,z+.0017),(x+side*.002,y,z+.0025)])
 curves('Individual tapered eyebrow hairs '+str(side),paths,.0001,strandmats[0],'Hair groom')
# Add nostril inset and alar creases rather than painted black spheres.
nostril=simple('Nostril warm occlusion',(.025,.009,.004),.85)
for side in [-1,1]:
 pts=[]
 for i in range(25):
  a=pi*.12+pi*.82*i/24;x=side*.011+.005*cos(a);z=1.294-.0015*sin(a);pts.append((x,front(x,z)-.0004,z))
 curves('Nostril rim '+str(side),[pts],.00065,nostril,'Anatomy',.3)

# A new tousled groom: wavy bundles, longer falling fringe, loose wisps.
# Bundles vary in length, direction and lift instead of following one spherical shell.
def hairpoint(a,p,r=1):
 return Vector((.09*sin(p)*sin(a)*r,.01-.081*sin(p)*cos(a)*r,1.411+.067*cos(p)*r))
paths=[[],[],[],[]]
for bundle in range(200):
 a=random.uniform(-pi,pi);p=random.uniform(.12,1.9)
 if cos(a)>.4:p=min(p,1.5)
 root=hairpoint(a,p,.97)
 length=random.uniform(.34,.8);sweep=random.uniform(-.6,.6)
 if cos(a)>.4:sweep-=.2
 phase=random.uniform(-pi,pi);lift=random.uniform(.008,.029);wave=random.uniform(.006,.013)
 # make 45 related strands form one visible S shaped wavy lock
 for strand in range(45):
  offa=random.gauss(0,.028);offp=random.gauss(0,.025);offr=random.uniform(-.002,.002);pts=[]
  for j in range(32):
   t=j/31;aa=a+offa+sweep*t+.09*sin(t*5.5+phase)*sin(pi*t)
   pp=p+offp+length*t
   q=hairpoint(aa,pp,1.03)
   outward=Vector((sin(pp)*sin(aa),-sin(pp)*cos(aa),cos(pp)))
   q+=outward*(lift*sin(pi*t)+wave*sin(2*pi*t+phase)*sin(pi*t)+offr)
   # raise crown waves, drop forehead fringe and sideburns naturally
   if cos(a)>.3:q.z-=.013*t*t
   pts.append(tuple(q))
  paths[random.choices(range(4),[.45,.35,.17,.03])[0]].append(pts)
for i,p in enumerate(paths):curves('Tousled wavy locks '+str(i),p,.00020 if i<3 else .00015,strandmats[i],'Hair groom',.035)
# Fine broken flyaways on the outer silhouette.
fly=[]
for k in range(220):
 a=random.uniform(-pi,pi);p=random.uniform(.1,1.9);pts=[]
 for j in range(24):
  t=j/23;q=hairpoint(a+.5*t,p+.45*t,1.07);q+=Vector((.006*sin(6*t+k),-.006*sin(4*t+k),.015*sin(pi*t)));pts.append(tuple(q))
 fly.append(pts)
curves('Loose hair flyaways',fly,.00010,strandmats[1],'Hair groom')
# Resize entire head assembly to the child's reference proportions while retaining geometry detail.
headobjects=[head]+[o for o in COL['Anatomy'].objects if o.name.startswith(('Ear','Nostril'))]+list(COL['Eyes and lashes'].objects)+list(COL['Hair groom'].objects)
scale=.82
for ob in headobjects:
 if ob.type=='MESH':
  for ve in ob.data.vertices:
   co=ob.matrix_world@ve.co;co.x*=scale;co.y*=scale;co.z=1.194+(co.z-1.194)*scale;ve.co=ob.matrix_world.inverted()@co
 elif ob.type=='CURVE':
  for sp in ob.data.splines:
   for pt in sp.points:
    co=ob.matrix_world@Vector(pt.co[:3]);co.x*=scale;co.y*=scale;co.z=1.194+(co.z-1.194)*scale;pt.co=(*tuple(ob.matrix_world.inverted()@co),1)
  ob.data.bevel_depth*=scale
# Refine ear occlusion: previous dark circles too graphic.
for o in s.objects:
 if o.name.startswith('Ear concha'):
  o.data.materials[0]=skin
  o.scale.y*=.6
# Improve clothed silhouette with many rings and low-amplitude fabric folds.
for o in list(s.objects):
 if o.type!='MESH' or not o.name.startswith(('Oversized cotton','Short sleeve','Trouser leg')):continue
 # apply subdivision for more points so secondary folds can follow cloth tension
 bpy.context.view_layer.objects.active=o;o.select_set(True)
 for mod in list(o.modifiers):
  if mod.type=='SUBSURF':bpy.ops.object.modifier_apply(modifier=mod.name)
 o.select_set(False)
 for ve in o.data.vertices:
  x,y,z=ve.co
  if o.name.startswith('Trouser'):
   center=.073*(1 if x>0 else -1);angle=math.atan2(x-center,-y+.005)
   # loose knee folds and stacking above the shoes
   d=.0023*exp(-((z-.42)/.065)**2)*sin(z*100+angle*2)+.003*exp(-((z-.16)/.055)**2)*sin(z*160+angle*2.2)
   ve.co.x+=d*sin(angle);ve.co.y-=d*cos(angle)
  else:
   angle=math.atan2(x,-y)
   d=.0015*sin(z*55+x*35)*exp(-((z-.87)/.17)**2)
   ve.co.y+=d*cos(angle)
 ma=o.data.materials[0];n=ma.node_tree.nodes;l=ma.node_tree.links;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.88;p.inputs['Sheen Weight'].default_value=.16
 # Update reference sampling to avoid background and straps baked over the modeled straps.
 uv=o.data.uv_layers.active
 if uv:
  for lo in o.data.loops:
   x,y,z=o.data.vertices[lo.vertex_index].co
   if o.name.startswith('Trouser'):
    cx=.073*(1 if x>0 else -1);px=(334 if x<0 else 423)+(x-cx)*500;py=925-(z-.10)*630
    px=max(296,min(457,px));py=max(525,min(925,py))
   elif o.name.startswith('Short sleeve'):
    px=370+(x% .05-.025)*600;py=260+(1.13-z)*720
   else:
    px=382+x*540;py=510-(z-.744)*710
    if z>1.0 and abs(x)>.045:px=382+(x% .035-.0175)*600
    px=max(299,min(458,px));py=max(220,min(505,py))
   uv.data[lo.index].uv=(px/1536,1-py/1024)
 for bump in n:
  if bump.type=='BUMP':bump.inputs['Distance'].default_value=.00025;bump.inputs['Strength'].default_value=.22
 mod=o.modifiers.new('Final fabric smoothing','SUBSURF');mod.levels=1;mod.render_levels=1
# Seamless curved studio backdrop eliminates the harsh horizon line.
floor=next(o for o in s.objects if o.name.startswith('Studio floor'));floor.hide_render=True;floor.hide_set(True)
bg=simple('Warm neutral seamless backdrop',(.23,.19,.145),.9)
verts=[];faces=[]
profile=[(-5,.006),(.7,.006)]+[(.7+.8*sin(pi*.5*i/32),.806-.8*cos(pi*.5*i/32)) for i in range(1,33)]+[(1.5,5)]
for y,z in profile:verts.extend([(-8,y,z),(8,y,z)])
for j in range(len(profile)-1):faces.append((j*2,j*2+1,j*2+3,j*2+2))
mesh('Seamless studio sweep',verts,faces,bg,'Studio',2)
# softer neutral lighting supports pores without hard plastic highlights
for o in s.objects:
 if o.type=='LIGHT':
  if 'key' in o.name:o.data.energy=190;o.data.size=3.0;o.data.color=(1,.89,.77)
  if 'fill' in o.name:o.data.energy=70
  if 'rim' in o.name:o.data.energy=85
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.36,.31,.25,1)
s.world.node_tree.nodes['Background'].inputs[1].default_value=.25
cam=next(o for o in s.objects if o.name.startswith('Camera • face inspection'))
cam.location=(.018,-3,1.326);cam.rotation_euler=(Vector((0,-.01,1.326))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.35
s.camera=cam;s.render.resolution_x=1100;s.render.resolution_y=1100;s.cycles.samples=96
s['Revision notes']='V03: cubic facial contours, inset photographic iris surfaces with moist corneal shading, 9,000 tapered wavy hairs grouped in 200 irregular locks plus flyaways, resized head, smoothed fabric, cleaned clothing sampling. Still an unrigged likeness study with inferred side/back anatomy.'
s.render.filepath=ROOT+'/enkidu-face-v03.png'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_enhanced_v03.blend')
result={'file':bpy.data.filepath,'scene':s.name,'head_vertices':len(head.data.vertices),'objects':len(s.objects)}
