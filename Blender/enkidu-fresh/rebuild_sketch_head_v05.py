"""Enkidu head reconstruction from the front + profile sketch, v05.
Actual shaped volumes, inset eyeballs, continuous lids, cartilage and open hair guides.
Body and wardrobe stay in their existing collections; previous head is retained hidden.
"""
import bpy, bmesh, math, random
from math import sin,cos,pi,exp,sqrt,asin
from mathutils import Vector
random.seed(5801)
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
SKETCH='/Users/abbasmamoori/Documents/ChatGPT/New project/concept-art/turnarounds/enkidu-head-turnaround-v1.png'
s=bpy.context.scene
s.name='Enkidu • sketch-fitted head'
# Save and preserve the earlier head; never repurpose it as reference geometry.
backup=bpy.data.collections.new('Head v04 • preserved');s.collection.children.link(backup)
oldhead=next(o for o in s.objects if o.name.startswith('Enkidu • sculpted head'))
source_image=next(n.image for n in oldhead.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE')
oldneck=next(o for o in s.objects if o.name=='Neck and clavicle')
heads=[oldhead,oldneck]
for col in s.collection.children:
 if col.name.startswith(('Eyes and lashes','Hair groom')):heads+=list(col.all_objects)
for ob in list(s.objects):
 if ob.name.startswith(('Ear','Inner ear','Nostril')):heads.append(ob)
for ob in set(heads):
 for c in list(ob.users_collection):c.objects.unlink(ob)
 backup.objects.link(ob)
backup.hide_render=True;backup.hide_viewport=True
colls={}
for name in ['V05 • head and neck','V05 • eyes lids and brows','V05 • cartilage','V05 • groom','V05 • sketch reference']:
 c=bpy.data.collections.new(name);s.collection.children.link(c);colls[name]=c
HC=colls['V05 • head and neck'];EC=colls['V05 • eyes lids and brows'];AC=colls['V05 • cartilage'];GC=colls['V05 • groom'];RC=colls['V05 • sketch reference']

def material(name,col,rough):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*col,1)
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough
 return m
skin=material('V05 • olive skin, pores and subsurface',(.245,.125,.059),.51)
n=skin.node_tree.nodes;l=skin.node_tree.links;p=n.get('Principled BSDF')
p.inputs['Specular IOR Level'].default_value=.27;p.inputs['Subsurface Weight'].default_value=.07;p.inputs['Subsurface Scale'].default_value=.005;p.inputs['Subsurface Radius'].default_value=(1,.43,.22)
geo=n.new('ShaderNodeNewGeometry')
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2200;noise.inputs['Detail'].default_value=2;l.new(geo.outputs['Position'],noise.inputs['Vector'])
b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.12;b.inputs['Distance'].default_value=.00009;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
macro=n.new('ShaderNodeTexNoise');macro.inputs['Scale'].default_value=42;macro.inputs['Detail'].default_value=3;l.new(geo.outputs['Position'],macro.inputs[0])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.210,.101,.047,1);ramp.color_ramp.elements[1].color=(.272,.145,.070,1)
l.new(macro.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
face=skin.copy();face.name='V05 • coloured face, geometry follows sketch'
n=face.node_tree.nodes;l=face.node_tree.links;p=n.get('Principled BSDF')
tex=n.new('ShaderNodeTexImage');tex.image=source_image;tex.extension='EXTEND'
attr=n.new('ShaderNodeAttribute');attr.attribute_name='PortraitWeight'
mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.245,.125,.059,1);l.new(attr.outputs['Fac'],mix.inputs[0]);l.new(tex.outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
# Cross-sectional skull / cheek / jaw volume. Z is fitted to the sketch's feature spacing.
PRO=[(1.194,.019,-.100,-.030),(1.205,.036,-.100,.004),(1.221,.052,-.101,.026),(1.240,.062,-.101,.045),(1.260,.069,-.102,.060),(1.280,.073,-.102,.069),(1.300,.071,-.103,.074),(1.320,.070,-.105,.075),(1.340,.071,-.103,.071),(1.360,.069,-.094,.064),(1.380,.057,-.069,.047),(1.392,.035,-.041,.021),(1.399,.001,-.009,-.007)]
def spline(table,z,k):
 z=max(table[0][0],min(table[-1][0],z))
 for i in range(len(table)-1):
  a,b=table[i],table[i+1]
  if a[0]<=z<=b[0]:
   t=(z-a[0])/(b[0]-a[0]);pr=table[max(0,i-1)];ne=table[min(len(table)-1,i+2)]
   m0=(b[k]-pr[k])/(b[0]-pr[0])*(b[0]-a[0]);m1=(ne[k]-a[k])/(ne[0]-a[0])*(b[0]-a[0])
   return (2*t**3-3*t*t+1)*a[k]+(t**3-2*t*t+t)*m0+(-2*t**3+3*t*t)*b[k]+(t**3-t*t)*m1
 return table[-1][k]
def G(x,z,cx,cz,wx,wz):return exp(-((x-cx)/wx)**2-((z-cz)/wz)**2)
def face_depth(x,z):
 # Features are sculpted as blended volume, not attached spheres.
 val=.027*G(x,z,0,1.267,.0115,.0115)+.014*G(x,z,0,1.287,.010,.027)
 val+=.007*(G(x,z,-.011,1.260,.007,.007)+G(x,z,.011,1.260,.007,.007))
 val-=.004*(G(x,z,-.010,1.257,.0038,.0025)+G(x,z,.010,1.257,.0038,.0025))
 val+=.014*G(x,z,0,1.237,.027,.0045)+.012*G(x,z,0,1.230,.026,.005)
 val-=.003*G(x,z,0,1.234,.029,.0014)
 val+=.004*G(x,z,0,1.209,.026,.013)
 val+=.004*(G(x,z,-.035,1.319,.025,.009)+G(x,z,.035,1.319,.025,.009))
 val-=.002*(G(x,z,-.032,1.296,.023,.012)+G(x,z,.032,1.296,.023,.012))
 val+=.003*(G(x,z,-.044,1.275,.025,.02)+G(x,z,.044,1.275,.025,.02))
 return val

def surface(x,z):
 w=spline(PRO,z,1);a=asin(max(-.999999,min(.999999,x/max(w,.001))));c=cos(a)
 yf=spline(PRO,z,2);yc=-.008
 return yc-(yc-yf)*c**.62-face_depth(x,z)*c**3

def jawmin(a):
 c=cos(a);return 1.194+.034*(1-max(c,0))**.72+.020*max(-c,0)
def skull(a,z):
 w=spline(PRO,z,1);x=w*sin(a);c=cos(a)
 y=surface(x,z) if c>=0 else -.008+(spline(PRO,z,3)+.008)*(-c)**.9
 return Vector((x,y,z))

def make_mesh(name,v,f,ma,coll,sub=1):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new(name,me);coll.objects.link(ob)
 me.materials.append(ma)
 for p in me.polygons:p.use_smooth=True
 if sub:
  m=ob.modifiers.new('Surface subdivision','SUBSURF');m.levels=sub;m.render_levels=sub
 return ob

def curves(name,paths,radius,ma,coll,tip=.04):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=2
 for pts in paths:
  sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
  for i,p in enumerate(pts):sp.points[i].co=(*p,1);sp.points[i].radius=1-(1-tip)*(i/max(1,len(pts)-1))**2
 ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(ma);return ob
# Photo pigment is mapped to the new feature locations; the sketch is never painted onto skin.
ZUV=[(1.13,720),(1.16,665),(1.194,570),(1.209,542),(1.230,495),(1.237,478),(1.257,440),(1.267,419),(1.296,343),(1.319,308),(1.344,270),(1.399,150)]
def face_uv(me):
 uv=me.uv_layers.new(name='Colour reference aligned to new landmarks')
 at=me.attributes.new('PortraitWeight','FLOAT','POINT')
 for i,ve in enumerate(me.vertices):
  x,y,z=ve.co;w=spline(PRO,z,1) if z>=1.194 else .05
  c=sqrt(max(0,1-(x/max(.001,w))**2))
  weight=c**.5 if y<-.02 else 0
  # Keep printed clothing in the portrait out of the neck material.
  if z<1.17:weight*=max(0,(z-1.135)/.035)
  at.data[i].value=weight
 for lo in me.loops:
  x,y,z=me.vertices[lo.vertex_index].co
  py=spline(ZUV,z,1)
  uv.data[lo.index].uv=((1102+x*2150)/1536,1-py/1024)
N=224;v=[];f=[];rings=[]
# Neck flows to the underside of the jaw, rather than a detached capped cylinder.
for j in range(13):
 t=j/12;ring=[]
 for i in range(N):
  a=2*pi*i/N;c=cos(a);topz=1.186+.05*(1-c)/2
  z=1.125+(topz-1.125)*t;w=.054*(1-t)+.030*t;d=.043*(1-t)+.031*t;cy=.006*(1-t)-.009*t
  x=w*sin(a);y=cy-d*cos(a)
  # restrained sternocleidomastoid neck form
  y-=.0012*sin(pi*t)**2*exp(-((abs(sin(a))-.65)/.20)**2)*max(c,0)
  ring.append((x,y,z))
 rings.append(ring)
necktop=rings[-1]
for j in range(1,7):
 t=j/6;ring=[]
 for i in range(N):
  a=2*pi*i/N;outer=skull(a,jawmin(a));co=Vector(necktop[i]).lerp(outer,t)
  co.z-=.003*sin(pi*t)*max(cos(a),0)
  ring.append(tuple(co))
 rings.append(ring)
R=220
for j in range(1,R+1):
 t=j/R;ring=[]
 for i in range(N):
  a=2*pi*i/N;z=jawmin(a)+(1.399-jawmin(a))*t;ring.append(tuple(skull(a,z)))
 rings.append(ring)
for ring in rings:v.extend(ring)
for j in range(len(rings)-1):
 for i in range(N):
  ids=(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i)
  x,y,z=sum((Vector(v[k]) for k in ids),Vector())/4
  hole=y<-.04 and any(((x-cx)/.0183)**2+((z-1.296)/.0077)**2<1 for cx in [-.032,.032])
  if not hole:f.append(ids)
f.append(tuple(reversed(range(N))));f.append(tuple((len(rings)-1)*N+i for i in range(N)))
head=make_mesh('V05 • sketch-fitted continuous face skull and neck',v,f,face,HC,2)
# Turn grid boundaries into smooth almond orbital loops, then construct real lid tissue.
bm=bmesh.new();bm.from_mesh(head.data);bm.verts.ensure_lookup_table()
boundary={side:[] for side in [-1,1]}
for ve in bm.verts:
 if not ve.is_boundary:continue
 for side in [-1,1]:
  cx=side*.032;dx=ve.co.x-cx;dz=ve.co.z-1.296
  if abs(dx)<.026 and abs(dz)<.015 and ve.co.y<-.035:
   a=math.atan2(dz/.0077,dx/.0183);x=cx+.0195*cos(a);z=1.296+(.0085 if sin(a)>0 else .0073)*sin(a)
   ve.co=Vector((x,surface(x,z),z));boundary[side].append((a,ve.index))
bm.to_mesh(head.data);bm.free()
face_uv(head.data)
# Eye radii and lid edge depths use the same sphere, eliminating floating circular whites.
EYER=.0168;ECZ=1.296
sclera=material('V05 • naturally warm sclera',(.50,.47,.40),.25);sclera.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.25
iris_mat=material('V05 • brown iris radial fibres',(.08,.035,.011),.34)
n=iris_mat.node_tree.nodes;l=iris_mat.node_tree.links;p=n.get('Principled BSDF');at=n.new('ShaderNodeAttribute');at.attribute_name='IrisColour';l.new(at.outputs['Color'],p.inputs['Base Color']);p.inputs['Coat Weight'].default_value=.22;p.inputs['Coat Roughness'].default_value=.13
pupilmat=material('V05 • pupil',(.0015,.001,.0007),.22)
lashmat=material('V05 • dark brows and fine eyelashes',(.011,.006,.003),.55)
watermat=material('V05 • subtle lid waterline',(.22,.092,.045),.35)
for side in [-1,1]:
 cx=side*.032;cy=surface(cx,ECZ)+.0141
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=40,location=(cx,cy,ECZ))
 ball=bpy.context.object;ball.name='V05 • inset eyeball '+str(side);ball.scale=(EYER,EYER,EYER);ball.data.materials.append(sclera)
 for c in list(ball.users_collection):c.objects.unlink(ball)
 EC.objects.link(ball)
 for p in ball.data.polygons:p.use_smooth=True
 # Brown iris annulus conforms to the eyeball's front, with fine radial pigmentation.
 vv=[];ff=[];colors=[];A=160;B=22;inner=.00235;outer=.0064
 for j in range(B+1):
  r=inner+(outer-inner)*j/B
  for i in range(A):
   a=2*pi*i/A;xx=r*cos(a);zz=r*sin(a);yy=cy-sqrt(max(.000001,EYER*EYER-r*r))-.00008
   vv.append((cx+xx,yy,ECZ+zz))
   ray=.5+.22*sin(79*a+.8*sin(r*1900))+.14*sin(137*a+1.3)+.1*sin(243*a+r*2400)
   limbal=1-.64*exp(-((r/outer-.98)/.07)**2);col=(.055+.052*ray,.022+.030*ray,.006+.012*ray)
   colors.append((*[k*limbal for k in col],1))
 for j in range(B):
  for i in range(A):a=j*A+i;b=j*A+(i+1)%A;ff.append((a,a+A,b+A,b))
 ob=make_mesh('V05 • sculpted iris '+str(side),vv,ff,iris_mat,EC,1)
 at=ob.data.color_attributes.new(name='IrisColour',type='FLOAT_COLOR',domain='POINT')
 for i,co in enumerate(colors):at.data[i].color=co
 # Pupil is recessed just beneath iris plane, not a painted dot.
 vv=[(cx,cy-EYER-.00007,ECZ)]+[(cx+inner*cos(2*pi*i/A),cy-sqrt(EYER*EYER-inner*inner)-.00008,ECZ+inner*sin(2*pi*i/A)) for i in range(A)]
 ff=[(0,i+1,(i+1)%A+1) for i in range(A)]
 make_mesh('V05 • pupil recess '+str(side),vv,ff,pupilmat,EC,0)
 loop=sorted(boundary[side]);vv=[];ff=[];L=len(loop)
 for j in range(7):
  t=j/6
  for a,ind in loop:
   outer=Vector(head.data.vertices[ind].co)
   dx=.0149*cos(a);dz=(.0057 if sin(a)>0 else .0046)*sin(a)
   innerco=Vector((cx+dx,cy-sqrt(max(.000001,EYER*EYER-dx*dx-dz*dz))-.00035,ECZ+dz))
   co=outer.lerp(innerco,t);co.y-=.00045*sin(pi*t)
   vv.append(tuple(co))
 for j in range(6):
  for i in range(L):a=j*L+i;b=j*L+(i+1)%L;ff.append((a,b,b+L,a+L))
 lid=make_mesh('V05 • continuous upper and lower eyelids '+str(side),vv,ff,face,EC,2);face_uv(lid.data)
 # Waterline and tapered lashes follow the actual aperture, not a detached ring.
 for upper in [True,False]:
  pts=[];lashes=[]
  for k in range(81):
   a=(0 if upper else pi)+pi*k/80;dx=.0149*cos(a);dz=(.0057 if upper else .0046)*sin(a)
   yy=cy-sqrt(max(.000001,EYER*EYER-dx*dx-dz*dz))-.00045;pts.append((cx+dx,yy,ECZ+dz))
  curves('V05 • '+('upper' if upper else 'lower')+' waterline '+str(side),[pts],.00018,watermat,EC,.7)
  for k in range(66 if upper else 35):
   a=(.12 if upper else pi+.15)+(pi-.3)*k/(65 if upper else 34);dx=.0149*cos(a);dz=(.0057 if upper else .0046)*sin(a)
   yy=cy-sqrt(max(.000001,EYER*EYER-dx*dx-dz*dz))-.0006;le=(.0028 if upper else .0015)*(.5+.5*abs(sin(a)))
   lashes.append([(cx+dx,yy,ECZ+dz),(cx+dx+.0005*cos(a),yy-.0012,ECZ+dz+(le*.5 if upper else -le*.5)),(cx+dx+.001*cos(a),yy-.0017,ECZ+dz+(le if upper else -le))])
  curves('V05 • '+('upper' if upper else 'lower')+' eyelashes '+str(side),lashes,.00005 if upper else .000035,lashmat,EC)
 # brows taper at either end, varying grain and length
 paths=[]
 for k in range(520):
  t=random.uniform(-1,1);x=cx+.023*t
  z=1.316+.004*(1-t*t)+random.uniform(-.002,.002)*(1-.6*abs(t))
  y=surface(x,z)-.00035;le=random.uniform(.0018,.0035)*(1-.5*abs(t));dx=side*.0016
  paths.append([(x,y,z),(x+dx*.5,y-.00035,z+le*.7),(x+dx,y,z+le)])
 curves('V05 • natural irregular eyebrow '+str(side),paths,.000055,lashmat,EC)
# Small nostril interiors are inside the geometry's nasal dimples.
nasal=material('V05 • nasal interior',(.035,.010,.004),.7)
for side in [-1,1]:
 cx=side*.010;cz=1.2575;vv=[];ff=[];A=48;B=8
 for j in range(B+1):
  r=j/B
  for i in range(A):
   a=2*pi*i/A;x=cx+.0036*r*cos(a);z=cz+.0015*r*sin(a);y=surface(x,z)-.00018+.0007*(1-r*r);vv.append((x,y,z))
 for j in range(B):
  for i in range(A):a=j*A+i;b=j*A+(i+1)%A;ff.append((a,b,b+A,a+A))
 make_mesh('V05 • nostril opening '+str(side),vv,ff,nasal,HC,1)
# Add the supplied sketch as a packed, non-rendering viewport reference.
image=bpy.data.images.load(SKETCH,check_existing=True);image.pack()
bpy.ops.object.empty_add(type='IMAGE',location=(.32,.03,1.315));ob=bpy.context.object;ob.name='V05 • supplied three-view head sketch';ob.data=image;ob.empty_display_size=.42;ob.rotation_euler=(pi/2,0,0);ob.hide_render=True
for c in list(ob.users_collection):c.objects.unlink(ob)
RC.objects.link(ob)
# Separate independent modules provide ears and hair in the agreed world coordinates.
exec(compile(open(ROOT+'/sketch_ears_v05.py').read(),'sketch_ears_v05.py','exec'))
ears=build_sketch_ears(s,AC,skin)
exec(compile(open(ROOT+'/sketch_hair_v05.py').read(),'sketch_hair_v05.py','exec'))
hairs=build_sketch_hair(s,GC)
# Keep lights soft and neutral for shape comparison, while retaining real skin and hair.
for o in s.objects:
 if o.type=='LIGHT':
  if 'key' in o.name:o.location=(-2.3,-2.8,3);o.data.energy=180;o.data.size=3;o.data.color=(1,.9,.79)
  if 'fill' in o.name:o.data.energy=85;o.data.size=2.6
  if 'rim' in o.name:o.data.energy=100;o.data.size=2.4
s.world.node_tree.nodes['Background'].inputs[1].default_value=.30
# Orthographic review cameras: labels describe nose direction on the page.
def camera(name,loc,target,scale):
 data=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=scale;return ob
front=camera('V05 • front comparison',(0,-3,1.315),(0,-.02,1.315),.34)
left=camera('V05 • left-facing profile',(3,-.015,1.315),(0,-.015,1.315),.34)
right=camera('V05 • right-facing profile',(-3,-.015,1.315),(0,-.015,1.315),.34)
three=camera('V05 • three-quarter review',(2,-3,1.315),(0,-.02,1.315),.34)
s.camera=front;s.render.engine='CYCLES';s.cycles.samples=96;s.cycles.use_denoising=True;s.render.resolution_x=1100;s.render.resolution_y=1100;s.render.resolution_percentage=100
s.render.filepath=ROOT+'/enkidu-sketch-head-front-v05.png'
s['Head reference']='concept-art/turnarounds/enkidu-head-turnaround-v1.png; front and profile contours interpreted, original front portrait retained only for colour.'
s['Revision notes']='V05 reconstructs head geometry from three-view sketch; continuous neck/jaw transition, real eyeballs and radial irises with anatomical eyelid tissue, new continuous cartilage ears, open S-wave fine strand groom. Original body preserved. V04 head retained hidden in separate collection. Not rigged or animation-retopologized.'
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.shading.type='MATERIAL';area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_sketch_head_v05.blend')
result={'file':bpy.data.filepath,'head_vertices':len(head.data.vertices),'eyelid_rings':7,'ear_objects':len(ears),'groom_objects':len(hairs),'head_collection':HC.name}
