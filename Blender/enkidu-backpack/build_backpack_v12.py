import bpy, math, random, bmesh
from math import sin, cos, pi, exp, sqrt
from mathutils import Vector
random.seed(71)
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-backpack'
REF='/Users/abbasmamoori/.codex/generated_images/01a1b087-7f3d-7190-9b89-f900fbe62cff/exec-a2165755-2984-43f5-bf48-4672c7e39661.png'
s=bpy.context.scene
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
old=bpy.data.collections.get('V09 • backpack')
if old:old.hide_render=True;old.hide_viewport=True;old.name='Backpack v11 • preserved'
C=bpy.data.collections.new('V12 • Enkidu reference backpack');s.collection.children.link(C)

def mat(name,col,rough=.8,metal=0):
 m=bpy.data.materials.new('V12 • '+name);m.use_nodes=True;m.diffuse_color=(*col,1)
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 return m

def fabric(name,col):
 m=mat(name,col);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Sheen Weight'].default_value=.23;p.inputs['Sheen Roughness'].default_value=.8
 uv=n.new('ShaderNodeTexCoord');geom=n.new('ShaderNodeNewGeometry')
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=42;noise.inputs['Detail'].default_value=5;noise.inputs['Roughness'].default_value=.74;l.new(geom.outputs['Position'],noise.inputs[0])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.23;ramp.color_ramp.elements[0].color=(*[v*.38 for v in col],1);ramp.color_ramp.elements[1].position=.78;ramp.color_ramp.elements[1].color=(*[v*1.6 for v in col],1);l.new(noise.outputs['Fac'],ramp.inputs[0])
 attr=n.new('ShaderNodeAttribute');attr.attribute_name='edge_wear'
 mix=n.new('ShaderNodeMixRGB');l.new(attr.outputs['Fac'],mix.inputs[0]);l.new(ramp.outputs[0],mix.inputs[1]);mix.inputs[2].default_value=(.28,.219,.146,1);l.new(mix.outputs[0],p.inputs['Base Color'])
 waves=[]
 for axis in ['X','Y']:
  w=n.new('ShaderNodeTexWave');w.wave_type='BANDS';w.bands_direction=axis;w.inputs['Scale'].default_value=570;w.inputs['Distortion'].default_value=.4;w.inputs['Detail Scale'].default_value=2;l.new(uv.outputs['UV'],w.inputs['Vector']);waves.append(w)
 mult=n.new('ShaderNodeMath');mult.operation='MULTIPLY';l.new(waves[0].outputs['Color'],mult.inputs[0]);l.new(waves[1].outputs['Color'],mult.inputs[1])
 b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.42;b.inputs['Distance'].default_value=.00024;l.new(mult.outputs[0],b.inputs['Height'])
 fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=1900;fine.inputs['Detail'].default_value=2;l.new(geom.outputs['Position'],fine.inputs[0]);b2=n.new('ShaderNodeBump');b2.inputs['Strength'].default_value=.22;b2.inputs['Distance'].default_value=.00013;l.new(fine.outputs['Fac'],b2.inputs['Height']);l.new(b.outputs[0],b2.inputs['Normal']);l.new(b2.outputs[0],p.inputs['Normal'])
 return m
canvas=fabric('sun faded brown canvas',(.155,.111,.066))
web=fabric('dense flat cotton webbing',(.184,.136,.080))
lining=fabric('dark cotton inner lining',(.074,.053,.031))
thread=mat('muted flax seam thread',(.32,.255,.171),.9)
fray=mat('exposed worn cotton fibres',(.28,.226,.155),.94)
metal=mat('worn brass buttons and adjusters',(.30,.201,.086),.43,.82)
n=metal.node_tree.nodes;l=metal.node_tree.links;p=n.get('Principled BSDF');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=130;noise.inputs['Detail'].default_value=3;r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.07,.044,.015,1);r.color_ramp.elements[1].color=(.43,.29,.12,1);l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])

def mesh(name,v,f,ma,uvs=None,wear=None,sub=1,thick=0):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('V12 • '+name,me);C.objects.link(o);me.materials.append(ma)
 for poly in me.polygons:poly.use_smooth=True
 layer=me.uv_layers.new(name='Fabric UV')
 for poly in me.polygons:
  for li in poly.loop_indices:
   idx=me.loops[li].vertex_index;co=v[idx];layer.data[li].uv=uvs[idx] if uvs else (co[0],co[2])
 if wear:
  a=me.attributes.new('edge_wear','FLOAT','POINT')
  for i,x in enumerate(wear):a.data[i].value=x
 if sub:
  mod=o.modifiers.new('Smooth tailored surface','SUBSURF');mod.levels=sub;mod.render_levels=sub
 if thick:
  me.materials.append(lining);mod=o.modifiers.new('Actual fabric and lining thickness','SOLIDIFY');mod.thickness=thick;mod.offset=-1;mod.material_offset=1;mod.material_offset_rim=1
 return o

def curves(name,paths,radius,ma):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=radius;cu.bevel_resolution=2
 for pts in paths:
  if len(pts)<2:continue
  sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
  for p,co in zip(sp.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new('V12 • '+name,cu);C.objects.link(o);cu.materials.append(ma);return o

def stitches(name,paths,ma=thread,spacing=.003,length=.0018,radius=.00023):
 dashes=[]
 for pts in paths:
  pts=[Vector(p) for p in pts];remaining=0
  for a,b in zip(pts[:-1],pts[1:]):
   delta=b-a;d=delta.length
   if not d:continue
   while remaining<d:
    start=a+delta*(remaining/d);end=a+delta*(min(d,remaining+length)/d);mid=(start+end)/2
    dashes.append([start,mid,end]);remaining+=spacing
   remaining-=d
 return curves(name,dashes,radius,ma)

def attach(o,parent):
 o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted();return o

def catmull(points,n=120):
 P=[Vector(x) for x in points];out=[]
 for k in range(n):
  t=k/(n-1)*(len(P)-1);i=min(len(P)-2,int(t));u=t-i
  p0=P[max(0,i-1)];p1=P[i];p2=P[i+1];p3=P[min(len(P)-1,i+2)]
  out.append(.5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u))
 return out

# Organic hollow shell: wider belly, gathered top, rounded compressed base.
def shell(t,a,off=0):
 z=.832+.306*t
 w=.111*(.91+.09*sin(pi*t))*(.70+.30*min(1,t/.085)**.45)*(1-.105*t**6)
 d=.062*(.78+.22*sin(pi*t)**.6)*(.65+.35*min(1,t/.08)**.5)
 xx=math.copysign(abs(sin(a))**.52,sin(a));yy=math.copysign(abs(cos(a))**.52,cos(a))
 # low amplitude broken gravity creases, strongest near the sides and base
 amp=(.0013+.0020*abs(sin(a))**6)*sin(pi*t)**.55
 fold=amp*(sin(11*a+4*sin(t*5))+.36*sin(23*a-8*t))
 fold+=.0016*sin(53*t+2*sin(a*3))*exp(-((t-.11)/.12)**2)
 fold-=.0035*exp(-((t-.48-.12*sin(2*a))/.10)**2)*abs(sin(a))**10
 x=(w+fold+off)*xx
 y=.131+(d+fold*.6+off)*yy
 # flatten body side for a comfortable contact panel
 if yy<0:y=.073+(y-.073)*.42
 zz=z+.0015*sin(9*a+.4)*t**8+.001*sin(6*a)*sin(pi*t)
 return (x,y,zz)
N=160;R=111;vv=[];ff=[];uv=[];wear=[]
for j in range(R):
 t=j/(R-1)
 for i in range(N+1):
  a=2*pi*i/N;vv.append(shell(t,a));uv.append((i/N*.60,t*.306));wear.append(.24*exp(-((t-.06)/.045)**2)+.13*abs(sin(a))**20+.1*t**12)
for j in range(R-1):
 for i in range(N):
  k=j*(N+1)+i;ff.append((k,k+1,k+N+2,k+N+1))
ff.append(tuple(reversed(range(N))))
body=mesh('01 hollow tapered canvas shell',vv,ff,canvas,uv,wear,1,.0022)
# Recalculate outward normals.
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
body['construction']='Hollow main compartment with actual lining thickness and bound mouth; no external front pocket.'
# Rim and seams follow the actual surface.
rim=[shell(1,2*pi*i/240,.0008) for i in range(241)]
curves('09 bound main opening',[rim],.0020,web)
stitches('09 rim stitching',[[shell(.982,2*pi*i/250,.0016) for i in range(251)]])
seams=[]
for a in [pi*.31,pi*.69,pi*1.31,pi*1.69]:seams.append([shell(.035+.965*j/140,a,.0010) for j in range(141)])
curves('07 subtle gusset folded seam',seams,.00085,canvas)
stitches('07 gusset seam stitches',seams)
for t in [.058,.075]:stitches('08 base seam topstitch',[[shell(t,2*pi*i/340,.0012) for i in range(341)]])
# Reinforced base band stays part of the soft silhouette.
vv=[];ff=[];uv=[]
for j in range(7):
 t=.012+.051*j/6
 for i in range(161):vv.append(shell(t,2*pi*i/160,.0006));uv.append((i/160*.6,t*.306))
for j in range(6):
 for i in range(160):k=j*161+i;ff.append((k,k+1,k+162,k+161))
mesh('08 rubbed reinforced base strip',vv,ff,web,uv,[.28]*len(vv),1,.0008)
# Fold-over lid is a single separate fabric piece sewn to rear edge.
hinge=bpy.data.objects.new('V12 • FLAP CONTROL — rotate local X to open',None);C.objects.link(hinge);hinge.location=(0,.078,1.139);hinge.empty_display_size=.018;bpy.context.view_layer.update()
center=catmull([(0,.078,1.139),(0,.101,1.150),(0,.153,1.151),(0,.189,1.139),(0,.202,1.113),(0,.207,1.069),(0,.205,1.028)],85)
def flap(u,v):
 k=min(len(center)-1,round(v*(len(center)-1)));c=center[k];w=.103*(1-.045*v)
 x=u*w;z=c.z+.021*abs(u)**8*v**5+.0011*sin(u*11+v*6)*sin(pi*v)
 y=c.y-.009*abs(u)**4+.0013*sin(u*13+v*4)*sin(pi*v)
 return (x,y,z)
vv=[];ff=[];uv=[];wear=[];NX=65;NY=85
for j in range(NY):
 v=j/(NY-1)
 for i in range(NX):
  u=-1+2*i/(NX-1);vv.append(flap(u,v));uv.append((u*.103,v*.25));wear.append(.25*abs(u)**24+.28*v**30)
for j in range(NY-1):
 for i in range(NX-1):k=j*NX+i;ff.append((k,k+1,k+NX+1,k+NX))
lid=attach(mesh('02 rounded fold-over flap',vv,ff,canvas,uv,wear,1,.0024),hinge)
edge=[flap(-1,j/100) for j in range(101)]+[flap(-1+2*i/100,1) for i in range(1,101)]+[flap(1,1-j/100) for j in range(1,101)]
attach(curves('02 rolled flap binding',[edge],.0011,web),hinge)
edge2=[flap(-.967,j/100*.987) for j in range(101)]+[flap(-.967+1.934*i/100,.987) for i in range(1,101)]+[flap(.967,.987*(1-j/100)) for j in range(1,101)]
edge2=[(x,y+.0016,z+.0006) for x,y,z in edge2]
attach(stitches('02 individual flap edge stitches',[edge2]),hinge)
# Rounded canvas tab, button and reinforcing stitches.
def tab(u,t):
 w=.0135*(1-.20*max(0,(t-.75)/.25));return (u*w,.208-.006*t+.0005*sin(pi*t),1.038-.060*t+.003*abs(u)**6*t**6)
vv=[];uv=[];ff=[]
for j in range(33):
 for i in range(17):u=-1+2*i/16;t=j/32;vv.append(tab(u,t));uv.append((u*.014,t*.06))
for j in range(32):
 for i in range(16):k=j*17+i;ff.append((k,k+1,k+18,k+17))
attach(mesh('03 rounded closure tab',vv,ff,web,uv,[.15]*len(vv),1,.002),hinge)
tabedge=[tab(-.8,t/80) for t in range(81)]+[tab(-.8+1.6*i/40,.96) for i in range(1,41)]+[tab(.8,.96*(1-j/80)) for j in range(1,81)]
attach(stitches('03 closure tab stitches',[[(x,y+.0014,z) for x,y,z in tabedge]],spacing=.0025,length=.0015),hinge)
def button(name,loc,r=.007):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=20,location=loc);o=bpy.context.object;o.name='V12 • '+name;o.scale=(r,.0025,r)
 for col in list(o.users_collection):col.objects.unlink(o)
 C.objects.link(o);o.data.materials.append(metal)
 for p in o.data.polygons:p.use_smooth=True
 return o
button('03 domed aged brass fastener',(0,.207,.993))
curves('03 engraved button rim',[[(.0061*sin(a),.2091,.993+.0061*cos(a)) for a in [2*pi*i/72 for i in range(73)]]],.00028,metal)
# Top carry loop: flat rectangular webbing, not a round rope.
def ribbon(name,points,width,ma=web):
 v=[];f=[];uv=[];dist=0
 for i,c in enumerate(points):
  if i:dist+=(Vector(c)-Vector(points[i-1])).length
  for j in range(5):
   q=-.5+j/4;v.append((c[0]+width*q,c[1],c[2]));uv.append((q*width,dist))
 for i in range(len(points)-1):
  for j in range(4):k=i*5+j;f.append((k,k+1,k+6,k+5))
 return mesh(name,v,f,ma,uv,[.10]*len(v),1,.0022)
# carry loop travels in X/Z plane, transverse strip direction follows Y.
pts=catmull([(-.020,.083,1.132),(-.019,.081,1.169),(0,.080,1.183),(.019,.081,1.169),(.020,.083,1.132)],65)
vv=[];uv=[];ff=[]
for i,p in enumerate(pts):
 for q in [-.5,0,.5]:vv.append((p.x,p.y+.012*q,p.z));uv.append((q*.012,i/64*.105))
for i in range(64):
 for j in range(2):k=i*3+j;ff.append((k,k+1,k+4,k+3))
mesh('10 folded webbing carry loop',vv,ff,web,uv,[.12]*len(vv),1,.002)
stitches('10 carry loop edge stitching',[[(p.x,p.y+dy,p.z+.001) for p in pts] for dy in [-.004,.004]])
# Shoulder straps: fitted to existing character with relaxed display shape keys.
strap_objects=[]
for side in [-1,1]:
 points=catmull([(side*.065,.074,1.12),(side*.081,.064,1.15),(side*.089,.025,1.175),(side*.082,-.035,1.153),(side*.080,-.079,1.098),(side*.079,-.080,1.025),(side*.086,-.066,.963),(side*.105,.006,.918),(side*.089,.072,.866)],151)
 rest=catmull([(side*.065,.074,1.12),(side*.070,.034,1.18),(side*.075,-.012,1.19),(side*.080,-.042,1.146),(side*.081,-.057,1.08),(side*.082,-.053,1.018),(side*.086,-.033,.953),(side*.096,.006,.902),(side*.089,.072,.866)],151)
 ob=ribbon('04 woven shoulder strap '+str(side),points,.024);ob.shape_key_add(name='Worn on Enkidu');key=ob.shape_key_add(name='Relaxed display')
 for i,p in enumerate(rest):
  for j in range(5):key.data[i*5+j].co=(p.x+.024*(-.5+j/4),p.y,p.z)
 strap_objects.append(ob)
 # Parallel dotted seams have matching shape keys via mesh tubes created as curves converted later if needed; leave fitted version on character.
 paths=[]
 for dx in [-.0095,.0095]:paths.append([(p.x+dx,p.y-.0013,p.z) for p in points])
 st=stitches('04 strap edge stitches '+str(side),paths,spacing=.0031,length=.0017,radius=.00019)
 st['display_note']='Fitted to worn position.'
 # Rectangular brass adjuster with rounded corners and center bar.
 x=side*.080;y=-.083;z=1.042
 frame=[]
 for i in range(97):
  a=2*pi*i/96;frame.append((x+.015*math.copysign(abs(sin(a))**.35,sin(a)),y,z+.012*math.copysign(abs(cos(a))**.35,cos(a))))
 curves('05 rounded brass slider '+str(side),[frame,[(x-.014,y-.001,z),(x+.014,y-.001,z)]],.00165,metal)
 # Small webbing return visibly crosses center bar.
 ribbon('05 threaded strap return '+str(side),catmull([(x,y+.002,z+.018),(x,y-.003,z+.005),(x,y-.003,z-.006),(x,y+.002,z-.031)],35),.022)
 # Flat anchor tabs with box-and-cross stitches on body side.
 cx=side*.087;cy=.070;cz=.879
 vv=[(cx+x,cy,cz+z) for x,z in [(-.016,-.019),(.016,-.019),(.016,.019),(-.016,.019)]]
 mesh('06 reinforced lower anchor '+str(side),vv,[(0,1,2,3)],web,sub=0,thick=.002)
 paths=[[(cx-.012,cy-.0018,cz-.015),(cx+.012,cy-.0018,cz-.015),(cx+.012,cy-.0018,cz+.015),(cx-.012,cy-.0018,cz+.015),(cx-.012,cy-.0018,cz-.015)],[(cx-.012,cy-.002,cz-.015),(cx+.012,cy-.002,cz+.015)],[(cx+.012,cy-.002,cz-.015),(cx-.012,cy-.002,cz+.015)]]
 stitches('06 box X reinforcement '+str(side),paths,spacing=.0023,length=.0014)
# Sparse loose fibres mainly around base and flap; restrained rather than shredded.
paths=[]
for i in range(180):
 a=random.uniform(0,2*pi);t=random.choice([.025,.065,.078])+random.uniform(-.01,.01);p=Vector(shell(t,a,.0013));d=Vector((random.uniform(-.002,.002),random.uniform(-.002,.002),random.uniform(-.003,.001)))
 paths.append([p,p+d*.5+Vector((0,.0005,0)),p+d])
curves('08 lightly frayed base fibres',paths,.000065,fray)
paths=[]
for i in range(105):
 u=random.uniform(-1,1);p=Vector(flap(u,1));d=Vector((random.uniform(-.002,.002),random.uniform(0,.001),random.uniform(-.0025,.0005)));paths.append([p,p+d*.6,p+d])
attach(curves('02 short flap edge fraying',paths,.000060,fray),hinge)
# Pack the exact user reference.
ref=bpy.data.images.load(REF,check_existing=True);ref.pack()
o=bpy.data.objects.new('V12 • exact backpack reference',None);s.collection.objects.link(o);o.empty_display_type='IMAGE';o.data=ref;o.empty_display_size=.65;o.location=(.7,.10,1.04);o.rotation_euler=(pi/2,0,0);o.hide_render=True
# Independent study scene shares backpack mesh and materials, with no character occlusion.
study=bpy.data.scenes.new('BACKPACK • isolated construction review');study.collection.children.link(C);study.render.engine='CYCLES';study.cycles.samples=48;study.cycles.use_denoising=True
world=bpy.data.worlds.new('Backpack neutral studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.22,.22,1);world.node_tree.nodes['Background'].inputs[1].default_value=.4;study.world=world
study.view_settings.view_transform='AgX'
def camera(scene,name,loc,target,scale):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=scale;return o
for name,loc,target,scale in [('outer',(0,1.3,1.08),(0,.11,1.005),.43),('body',(0,-1.3,1.06),(0,.04,1.01),.44),('side',(1.4,.12,1.06),(0,.075,1.015),.43),('open',(.48,.85,1.63),(0,.12,1.04),.49),('hero',(.42,.85,1.27),(0,.1,1.01),.46)]:camera(study,'V12 • bag '+name,loc,target,scale)
for name,loc,power,size in [('key',(-.45,.6,1.8),32,.65),('fill',(.5,.4,1.45),16,.5),('rim',(.0,-.55,1.5),25,.5)]:
 d=bpy.data.lights.new('V12 • '+name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(d.name,d);study.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,.12,1))-o.location).to_track_quat('-Z','Y').to_euler()
floor=mat('neutral warm backdrop',(.16,.145,.12),.9)
me=bpy.data.meshes.new('Bag studio floor');me.from_pydata([(-200,-200,.829),(200,-200,.829),(200,200,.829),(-200,200,.829)],[],[(0,1,2,3)]);o=bpy.data.objects.new('V12 • isolated studio floor',me);study.collection.objects.link(o);me.materials.append(floor)
study.camera=bpy.data.objects['V12 • bag hero'];study.render.resolution_x=1100;study.render.resolution_y=1200;study.render.resolution_percentage=100
camera(s,'V12 • worn backpack review',(.95,1.6,1.5),(0,.08,1.05),.8)
s['Backpack revision']='V12: sketch-matched soft hollow canvas shell, single rounded fold-over flap, one button tab, bound mouth, sewn gussets, reinforced base, woven straps, rectangular brass sliders, carry loop, box-X anchors and edge fraying. Existing head and body retained.'
s.camera=bpy.data.objects['V12 • worn backpack review'];s.render.resolution_x=1000;s.render.resolution_y=1100
# Show material appearance in solid viewport as well as rendered view.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.shading.color_type='MATERIAL';area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_backpack_sketch_v12.blend')
result={'file':bpy.data.filepath,'backpack_objects':len(C.objects),'vertices':sum(len(o.data.vertices) for o in C.objects if o.type=='MESH'),'scenes':[x.name for x in bpy.data.scenes]}
