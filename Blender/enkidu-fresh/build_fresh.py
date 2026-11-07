import bpy, math, random
from mathutils import Vector
from math import sin, cos, pi, exp, sqrt
random.seed(91)
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
REF='/Users/abbasmamoori/.codex/generated_images/01a1b087-7f3d-7190-9b89-f900fbe62cff/exec-400a2b28-6e40-4b0b-98fc-ce9fdfb4f7ff.png'
scene=bpy.data.scenes.new('Enkidu • fresh character')
bpy.context.window.scene=scene
scene.unit_settings.system='METRIC'
scene.render.engine='CYCLES'; scene.cycles.samples=48
scene.cycles.use_denoising=True
scene.render.resolution_x=1000; scene.render.resolution_y=1250; scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Fresh studio environment'); scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.28,.32,.4,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.35
scene.view_settings.view_transform='AgX'
COL={}
for n in ['Anatomy','Eyes and lashes','Hair groom','Clothing','Backpack','Footwear','Studio','Reference']:
 c=bpy.data.collections.new(n);scene.collection.children.link(c);COL[n]=c

def link(o,coll):
 for c in list(o.users_collection):c.objects.unlink(o)
 COL[coll].objects.link(o)
 return o

def mesh(name,v,f,mat,coll='Clothing',sub=1):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);COL[coll].objects.link(o)
 if mat:o.data.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 if sub:
  m=o.modifiers.new('Surface refinement','SUBSURF');m.levels=sub;m.render_levels=sub
 return o

def mat(name,color,rough=.6,noise=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
 if noise:
  tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=noise;tex.inputs['Detail'].default_value=3
  ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.25;ramp.color_ramp.elements[1].position=.8
  ramp.color_ramp.elements[0].color=(*[v*.55 for v in color],1);ramp.color_ramp.elements[1].color=(*[min(v*1.4,1) for v in color],1)
  l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
 return m
skin=mat('Skin • warm olive, subsurface and pores',(.38,.21,.105),.48)
p=skin.node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.09;p.inputs['Subsurface Radius'].default_value=(1,.45,.2)
n=skin.node_tree.nodes;l=skin.node_tree.links
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=260;noise.inputs['Detail'].default_value=2
b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.15;b.inputs['Distance'].default_value=.00045;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
face=skin.copy();face.name='Face • reference colour projection with skin response'
img=bpy.data.images.load(REF,check_existing=True);img.pack()
n=face.node_tree.nodes;l=face.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexImage');tex.image=img;tex.extension='EXTEND'
attr=n.new('ShaderNodeAttribute');attr.attribute_name='FrontBlend'
mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.38,.21,.105,1);l.new(attr.outputs['Fac'],mix.inputs[0]);l.new(tex.outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
shirt=mat('Faded indigo cotton • dust and fibres',(.085,.12,.17),.88,7)
pants=mat('Worn brown twill • dust and fibres',(.12,.078,.043),.91,9)
canvas=mat('Backpack • aged ochre canvas',(.19,.12,.055),.87,12)
sole=mat('Dirty vulcanised rubber',(.24,.20,.14),.82,30)
shoe=mat('Dusty grey canvas',(.115,.12,.112),.85,14)
thread=mat('Faded stitching',(.35,.29,.19),.82)
hair=mat('Dark brown hair • strand highlights',(.018,.011,.007),.38)
# anisotropy uses Blender defaults
metal=mat('Tarnished brass buckles',(.23,.15,.065),.45);metal.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.75
white=mat('Warm eye sclera',(.68,.63,.49),.23)
iris=mat('Brown iris',(.09,.042,.012),.27,80)
pupil=mat('Pupil',(.002,.0015,.001),.12)
crease=mat('Skin crease',(.12,.055,.025),.65)
for m in [shirt,pants,canvas,shoe]:
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Sheen Weight'].default_value=.23
 t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=380;b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.22;b.inputs['Distance'].default_value=.0007;l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])

def uvball(name,loc,scale,ma,coll='Anatomy'):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(ma)
 for f in o.data.polygons:f.use_smooth=True
 return link(o,coll)

def curves(name,paths,radius,ma,coll):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=radius;cu.bevel_resolution=2
 for pts in paths:
  sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
  for i,co in enumerate(pts):
   sp.points[i].co=(*co,1);sp.points[i].radius=max(.15,1-i/max(len(pts)-1,1)*.75)
 o=bpy.data.objects.new(name,cu);COL[coll].objects.link(o);cu.materials.append(ma);return o

def loft(name,rings,ma,coll='Clothing',fold=0,N=64):
 # rings (x,y,z,width,depth), a garment surface with continuous folds
 v=[];f=[]
 for j,(x,y,z,w,d) in enumerate(rings):
  for i in range(N):
   a=2*pi*i/N
   q=1+fold*(.55*sin(a*9+j*.65)+.25*sin(a*17-j*.9)+.2*cos(a*5+j*1.2))
   v.append((x+w*sin(a)*q,y-d*cos(a)*q,z+fold*.007*sin(a*8+j)))
 for j in range(len(rings)-1):
  for i in range(N):
   a=j*N+i;b=j*N+(i+1)%N;f.append((a,b,b+N,a+N))
 f.append(tuple(reversed(range(N))));f.append(tuple((len(rings)-1)*N+i for i in range(N)))
 return mesh(name,v,f,ma,coll,2)

# Cranial / facial surface sculpted independently of earlier projects.
profiles=[(1.196,.018,.035),(1.207,.043,.045),(1.225,.063,.054),(1.25,.078,.061),(1.28,.086,.069),(1.31,.09,.074),(1.34,.087,.076),(1.37,.086,.077),(1.4,.083,.076),(1.43,.07,.065),(1.45,.048,.047),(1.46,.009,.014)]
def profile(z):
 for (z0,w0,d0),(z1,w1,d1) in zip(profiles,profiles[1:]):
  if z0<=z<=z1:
   t=(z-z0)/(z1-z0);return w0+(w1-w0)*t,d0+(d1-d0)*t
 return profiles[-1][1:]
def gauss(x,z,cx,cz,wx,wz):return exp(-((x-cx)/wx)**2-((z-cz)/wz)**2)
def surf(x,z,w,d,a):
 front=max(cos(a),0)**6
 bump=.023*gauss(x,z,0,1.302,.018,.019)+.013*gauss(x,z,0,1.33,.012,.042)
 bump+=.007*gauss(x,z,0,1.252,.036,.013)+.004*gauss(x,z,0,1.221,.035,.016)
 bump+=.006*(gauss(x,z,-.047,1.365,.03,.012)+gauss(x,z,.047,1.365,.03,.012))
 bump-=.008*(gauss(x,z,-.043,1.347,.025,.014)+gauss(x,z,.043,1.347,.025,.014))
 return -d*cos(a)-front*bump
N=160;R=150;v=[];f=[]
for j in range(R):
 z=1.196+(1.46-1.196)*j/(R-1);w,d=profile(z)
 for i in range(N):
  a=2*pi*i/N;x=w*sin(a);v.append((x,surf(x,z,w,d,a),z))
for j in range(R-1):
 for i in range(N):
  ids=(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i)
  x,y,z=Vector(sum((Vector(v[k]) for k in ids),Vector()))/4
  hole= any(((x-c)/.0205)**2+((z-1.347)/.0077)**2<1 for c in [-.043,.043]) and y<-.04
  if not hole:f.append(ids)
head=mesh('Enkidu • sculpted head with orbital openings',v,f,face,'Anatomy',1)
uv=head.data.uv_layers.new(name='Portrait frontal projection')
a=head.data.attributes.new('FrontBlend','FLOAT','POINT')
for k,(x,y,z) in enumerate(v):
 theta=2*pi*(k%N)/N
 a.data[k].value=max(cos(theta),0)**.6
for poly in head.data.polygons:
 for li in poly.loop_indices:
  x,y,z=v[head.data.loops[li].vertex_index]
  uv.data[li].uv=((1107+x*1600)/1536,1-(570-(z-1.2)*1538)/1024)
loft('Neck and clavicle',[(0,.006,1.115,.057,.047),(0,.006,1.15,.044,.038),(0,.008,1.205,.034,.034),(0,.012,1.23,.037,.037)],skin,'Anatomy',0)
for s in [-1,1]:
 uvball('Ear outer helix', (s*.089,.004,1.302),(.019,.015,.034),skin)
 uvball('Ear concha',(s*.096,-.009,1.303),(.009,.004,.021),crease)
 pts=[(s*(.094+.01*cos(t)),-.013,1.303+.027*sin(t)) for t in [2*pi*i/40 for i in range(41)]]
 curves('Ear helix contour',[pts],.0028,skin,'Anatomy')
 # Eyes, small irises and actual lashes
 uvball('Eyeball',(s*.043,-.059,1.347),(.020,.018,.017),white,'Eyes and lashes')
 uvball('Iris',(s*.043,-.0768,1.347),(.0077,.0013,.0077),iris,'Eyes and lashes')
 uvball('Pupil',(s*.043,-.0781,1.347),(.0033,.0005,.0033),pupil,'Eyes and lashes')
 for top in [True,False]:
  pts=[]
  for i in range(41):
   t=pi*i/40;x=s*.043+.021*cos(t);z=1.347+(1 if top else -1)*.008*sin(t);y=-.071-.006*sin(t)
   pts.append((x,y,z))
  curves('Upper eyelid' if top else 'Lower eyelid',[pts],.0017 if top else .0012,skin,'Eyes and lashes')
 paths=[]
 for i in range(35):
  t=.1+(pi-.2)*i/34;x=s*.043+.0205*cos(t);z=1.347+.008*sin(t)
  paths.append([(x,-.072-.006*sin(t),z),(x+.001*cos(t),-.080-.005*sin(t),z+.0025),(x+.002*cos(t),-.081,z+.004)])
 curves('Individual upper lashes',paths,.00019,hair,'Eyes and lashes')
 # sparse brow strands on the reference-matched brow ridge
 paths=[]
 for i in range(110):
  x=s*.043+random.uniform(-.025,.025);z=1.369+.004*(1-abs(x-s*.043)/.025)+random.uniform(-.002,.002)
  paths.append([(x,-.080,z),(x+s*.002,-.081,z+.003),(x+s*.003,-.08,z+.004)])
 curves('Eyebrow hairs',paths,.00016,hair,'Hair groom')

# Shirt panels and sewn sleeve tubes
loft('Oversized cotton T shirt',[(0,0,.744,.126,.071),(0,0,.752,.128,.071),(0,0,.79,.125,.07),(0,0,.87,.117,.068),(0,0,.95,.122,.07),(0,0,1.04,.135,.073),(0,0,1.11,.149,.066),(0,0,1.135,.143,.06),(0,0,1.155,.106,.05),(0,0,1.17,.053,.041)],shirt,fold=.055)
curves('Neck ribbing',[[(.053*sin(t),-.042*cos(t),1.171) for t in [2*pi*i/100 for i in range(101)]]],.004,shirt,'Clothing')
for s in [-1,1]:
 loft('Short sleeve',[(s*.124,0,1.115,.044,.061),(s*.145,0,1.102,.047,.063),(s*.172,0,1.05,.052,.062),(s*.19,0,.992,.052,.06),(s*.19,0,.986,.053,.06)],shirt,fold=.055)
 loft('Slim arm',[(s*.187,.004,1.02,.031,.032),(s*.199,.002,.96,.029,.029),(s*.205,-.002,.896,.025,.026),(s*.214,-.008,.867,.024,.025),(s*.22,-.012,.812,.022,.024),(s*.228,-.018,.735,.016,.019),(s*.23,-.02,.71,.016,.018)],skin,'Anatomy',.01,48)
 uvball('Palm',(s*.232,-.024,.688),(.021,.015,.038),skin)
 # fingers fall naturally with subtle knuckle variation
 for k in range(4):
  xx=s*(.217+k*.011);zz=.677+abs(k-1.3)*.003;le=[.041,.048,.046,.034][k]
  loft('Finger',[(xx,-.025,zz,.0055,.006),(xx+s*.001,-.029,zz-.017,.005,.0055),(xx+s*.002,-.035,zz-le,.004,.004),(xx+s*.002,-.034,zz-le-.003,.002,.002)],skin,'Anatomy',0,16)
 loft('Thumb',[(s*.215,-.03,.702,.008,.008),(s*.203,-.04,.684,.007,.007),(s*.204,-.046,.666,.005,.005)],skin,'Anatomy',0,20)
 # loose trouser legs with excess cloth folding at ankles
 loft('Trouser leg',[(s*.058,.007,.79,.063,.066),(s*.062,.007,.74,.066,.066),(s*.067,.007,.65,.062,.063),(s*.07,.006,.53,.057,.059),(s*.071,.008,.43,.051,.052),(s*.074,.008,.38,.055,.057),(s*.077,.005,.3,.05,.05),(s*.079,.001,.22,.045,.047),(s*.077,-.005,.18,.051,.05),(s*.078,-.008,.15,.04,.043),(s*.078,-.004,.135,.039,.042)],pants,fold=.095)
 # ankle hems
 curves('Trouser cuff seam',[[(s*.078+.041*sin(t),-.004-.043*cos(t),.146+.002*sin(t*8)) for t in [2*pi*i/64 for i in range(65)]]],.0009,thread,'Clothing')
 # sneakers distinct rubber outsole canvas upper toe cap lace system
 uvball('Sneaker sole',(s*.078,-.046,.033),(.045,.105,.025),sole,'Footwear')
 uvball('Canvas shoe upper',(s*.078,-.035,.068),(.041,.091,.044),shoe,'Footwear')
 uvball('Rubber toe cap',(s*.078,-.112,.054),(.042,.038,.024),sole,'Footwear')
 paths=[]
 for j in range(6):
  y=-.095+j*.017;z=.093+.013*sin(j/6*pi)
  paths.append([(s*.078-.025,y,z),(s*.078,y+.008,z+.003),(s*.078+.025,y+.014,z)])
  paths.append([(s*.078+.025,y,z),(s*.078,y+.008,z+.004),(s*.078-.025,y+.014,z)])
 curves('Crossed cotton shoelaces',paths,.0015,thread,'Footwear')

# Backpack sits behind torso, wide straps follow shoulders rather than floating.
uvball('Canvas backpack body',(0,.105,.987),(.111,.055,.161),canvas,'Backpack')
uvball('Backpack front pocket',(0,.154,.932),(.08,.025,.065),canvas,'Backpack')
uvball('Backpack flap',(0,.153,1.083),(.113,.021,.07),canvas,'Backpack')
for s in [-1,1]:
 pts=[(s*.083,.13,.96),(s*.102,.105,1.10),(s*.093,.04,1.16),(s*.086,-.02,1.162),(s*.087,-.077,1.115),(s*.083,-.08,1.02),(s*.08,-.077,.93),(s*.09,.04,.90)]
 # a true flat strap ribbon with solidified thickness
 vv=[]
 for x,y,z in pts:vv.extend([(x-.011,y,z),(x+.011,y,z)])
 ff=[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(pts)-1)]
 ob=mesh('Shoulder canvas strap',vv,ff,canvas,'Backpack',2);m=ob.modifiers.new('Woven strap thickness','SOLIDIFY');m.thickness=.003
 for z in [1.039]:
  paths=[]
  x=s*.083;y=-.084
  paths.append([(x-.013,y,z-.012),(x+.013,y,z-.012),(x+.013,y,z+.012),(x-.013,y,z+.012),(x-.013,y,z-.012)])
  curves('Brass strap adjuster',paths,.0018,metal,'Backpack')
 # shirt stitching near hem
 curves('T shirt hem topstitch',[[(.126*sin(t),-.072*cos(t),.755+.003*sin(t*7)) for t in [2*pi*i/128 for i in range(129)]]],.0006,thread,'Clothing')

# Groom made from thousands of individually tapered wavy strands.
# Scalp cap is inside groom; no clay clumps.
uvball('Hair underlayer',(0,.013,1.416),(.088,.083,.064),hair,'Hair groom')
paths=[]
for k in range(3800):
 a=random.uniform(-pi,pi);polar=random.uniform(.07,1.85)
 # roots upper scalp, wavy swept tips create irregular silhouette
 x=.087*sin(polar)*sin(a);y=.012-.079*sin(polar)*cos(a);z=1.412+.062*cos(polar)
 length=random.uniform(.04,.085);phase=random.uniform(0,2*pi);pts=[]
 for j in range(19):
  t=j/18
  xx=x+(.014*sin(phase+t*5)+.025*cos(a+.8))*sin(pi*t*.75)
  yy=y+(.015*sin(phase+t*6)+.025*sin(a))*sin(pi*t*.8)
  zz=z+length*sin(pi*t*.82)-.018*t
  pts.append((xx,yy,zz))
 paths.append(pts)
curves('Wavy groom • 3800 tapered strands',paths,.00033,hair,'Hair groom')

# Reference image lives in its own collection for modelling, never in render.
bpy.ops.object.empty_add(type='IMAGE',location=(.75,.14,.75));o=bpy.context.object;o.name='Provided concept • front and facial detail';o.data=img;o.empty_display_size=1.4;o.rotation_euler=(pi/2,0,0);o.hide_render=True;link(o,'Reference')
# studio
floor=mat('Neutral warm studio',(.19,.16,.125),.84)
bpy.ops.mesh.primitive_plane_add(size=200);o=bpy.context.object;o.name='Studio floor';o.data.materials.append(floor);link(o,'Studio')
def light(name,loc,power,size,color):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector((0,0,.95))-o.location).to_track_quat('-Z','Y').to_euler();link(o,'Studio')
light('Large soft key',(-2,-3,3.4),260,3,(1,.86,.70));light('Cool soft fill',(2,-1.2,2),100,2,(.72,.84,1));light('Hair rim',(0,1.5,2.7),200,1.8,(1,.83,.65))
def camera(name,loc,target,ortho):
 bpy.ops.object.camera_add(location=loc);o=bpy.context.object;o.name=name;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.type='ORTHO';o.data.ortho_scale=ortho;link(o,'Studio');return o
front=camera('Camera • full character',(0,-4,.81),(0,0,.77),1.68)
portrait=camera('Camera • face inspection',(.06,-3,1.36),(0,-.01,1.335),.43)
three=camera('Camera • three quarter',(.95,-3,.9),(0,0,.78),1.7)
scene.camera=front
# Save startup with real materials, not a solid clay override.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.shading.type='MATERIAL'
   area.spaces.active.overlay.show_overlays=False
   area.spaces.active.region_3d.view_perspective='CAMERA'
scene['Build notes']='New independent scene and geometry. Facial colour projected from supplied front concept; side/back anatomy inferred. Not rigged. Review front and three-quarter before animation topology.'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_fresh_v01.blend')
scene.render.filepath=ROOT+'/enkidu-fresh-front.png'
# Rendering is invoked separately so live bridge returns immediately.
result={'file':bpy.data.filepath,'scene':scene.name,'objects':len(scene.objects),'hair_strands':3800}
