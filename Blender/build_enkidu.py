import bpy, math, random, os
from mathutils import Vector, Quaternion
from math import sin,cos,pi
random.seed(17)
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d'
REF='/Users/abbasmamoori/.codex/generated_images/01a1b087-7f3d-7190-9b89-f900fbe62cff/exec-400a2b28-6e40-4b0b-98fc-ce9fdfb4f7ff.png'
# New dedicated file; original interactive scene remains untouched.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene;sc.name='Enkidu | Character development 01'
sc.unit_settings.system='METRIC'
cols={}
for n in ['01 Anatomy','02 Face','03 Hair','04 Clothing','05 Backpack','06 References','07 Studio']:
 c=bpy.data.collections.new(n);sc.collection.children.link(c);cols[n]=c

def move(o,c):
 for old in list(o.users_collection):old.objects.unlink(o)
 cols[c].objects.link(o)
 return o

def mat(n,color,rough=.7,noise=False):
 m=bpy.data.materials.new(n);m.diffuse_color=(*color,1);m.use_nodes=True
 ns=m.node_tree.nodes;bs=ns.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough
 if noise:
  tex=ns.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=90;tex.inputs['Detail'].default_value=3
  ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.18;ramp.color_ramp.elements[0].color=(*[a*.7 for a in color],1);ramp.color_ramp.elements[1].position=.82;ramp.color_ramp.elements[1].color=(*[min(a*1.25,1) for a in color],1)
  m.node_tree.links.new(tex.outputs['Fac'],ramp.inputs[0]);m.node_tree.links.new(ramp.outputs[0],bs.inputs['Base Color'])
  bump=ns.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.14;bump.inputs['Distance'].default_value=.0012;m.node_tree.links.new(tex.outputs['Fac'],bump.inputs['Height']);m.node_tree.links.new(bump.outputs[0],bs.inputs['Normal'])
 return m
skin=mat('Skin | warm olive brown',(.36,.205,.112),.65,True)
blue=mat('Shirt | faded indigo cotton',(.105,.16,.205),.9,True)
brown=mat('Trousers | worn earth cotton',(.19,.115,.066),.95,True)
canvas=mat('Bag | dusty ochre canvas',(.235,.155,.083),.9,True)
shoe=mat('Shoes | worn grey canvas',(.255,.24,.195),.92,True)
sole=mat('Soles | old cream rubber',(.38,.33,.247),.87,True)
hair=mat('Hair | black brown',(.018,.011,.007),.8)
hair2=mat('Hair | warm ridge highlights',(.032,.020,.012),.82)
white=mat('Eye | warm ivory',(.62,.59,.48),.25)
iris=mat('Iris | dark umber',(.069,.031,.012),.28)
black=mat('Pupil and lash',(.008,.005,.003),.34)
lip=mat('Lips | muted natural brown',(.30,.125,.075),.65)
shadow=mat('Mouth crease',(.085,.035,.018),.8)
thread=mat('Thread | faded flax',(.37,.29,.19),.9)
metal=mat('Buckles | aged brass',(.24,.17,.075),.45)

def mesh(n,verts,faces,ma,c,sub=1):
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);cols[c].objects.link(o)
 if ma:o.data.materials.append(ma)
 for p in me.polygons:p.use_smooth=True
 if sub:
  md=o.modifiers.new('Editable surface smoothing','SUBSURF');md.levels=sub;md.render_levels=sub
 return o

def uv(n,loc,scale,ma,c='01 Anatomy',seg=32,rings=20):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc);o=bpy.context.object;o.name=n;move(o,c)
 for v in o.data.vertices:v.co.x*=scale[0];v.co.y*=scale[1];v.co.z*=scale[2]
 o.data.materials.append(ma)
 for p in o.data.polygons:p.use_smooth=True
 return o

def curve(n,pts,r,ma,c='04 Clothing',radii=None):
 cu=bpy.data.curves.new(n,'CURVE');cu.dimensions='3D';cu.resolution_u=10;cu.bevel_depth=r;cu.bevel_resolution=3
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for i,(p,co) in enumerate(zip(sp.bezier_points,pts)):
  p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
  if radii:p.radius=radii[i]
 o=bpy.data.objects.new(n,cu);cols[c].objects.link(o);o.data.materials.append(ma);return o

def tube(n,rings,ma,c='04 Clothing',segments=32,sub=2,wrinkle=0):
 # rings: center x,y,z and horizontal and depth radii
 vs=[];fs=[]
 for j,(x,y,z,rx,ry) in enumerate(rings):
  for k in range(segments):
   a=2*pi*k/segments;w=1+wrinkle*(sin(7*a+j*.9)+.4*sin(13*a-j))
   vs.append((x+rx*cos(a)*w,y+ry*sin(a)*w,z+.002*wrinkle*sin(a*5+j)))
 for j in range(len(rings)-1):
  for k in range(segments):a=j*segments+k;b=j*segments+(k+1)%segments;fs.append((a,b,b+segments,a+segments))
 fs.append(tuple(reversed(range(segments))));fs.append(tuple((len(rings)-1)*segments+k for k in range(segments)))
 return mesh(n,vs,fs,ma,c,sub)

def rounded(n,loc,dim,ma,c='05 Backpack',bevel=.015):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;move(o,c)
 for v in o.data.vertices:v.co.x*=dim[0];v.co.y*=dim[1];v.co.z*=dim[2]
 o.data.materials.append(ma);m=o.modifiers.new('Soft sewn corners','BEVEL');m.width=bevel;m.segments=4
 m=o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL')
 return o
# Slender torso and neck, with an oversized shirt silhouette.
tube('Neck',[(0,0,1.16,.035,.033),(0,0,1.205,.031,.032),(0,0,1.255,.036,.036)],skin,'01 Anatomy',sub=2)
shirt=tube('Shirt | main cloth shell',[(0,0,.705,.147,.079),(0,0,.72,.148,.080),(0,0,.80,.135,.075),(0,0,.91,.112,.065),(0,0,1.035,.119,.063),(0,0,1.13,.136,.057),(0,0,1.177,.137,.050),(0,0,1.205,.052,.039),(0,0,1.208,.038,.034)],blue,wrinkle=.045)
# Collar and bottom hem piping.
curve('Collar stitched ring',[(.039*cos(a),-.002+.035*sin(a),1.205-.009*max(0,-sin(a))) for a in [2*pi*k/16 for k in range(17)]],.004,blue)
curve('Shirt bottom hem',[(.147*cos(a),.079*sin(a),.718+.003*sin(3*a)) for a in [2*pi*k/32 for k in range(33)]],.002,blue)
for s,side in [(-1,'L'),(1,'R')]:
 tube('Sleeve.'+side,[(s*.12,0,1.174,.043,.052),(s*.16,0,1.139,.047,.056),(s*.181,-.001,1.062,.051,.055),(s*.184,-.002,1.048,.051,.056)],blue,wrinkle=.014)
 tube('Arm.'+side,[(s*.183,0,1.075,.027,.030),(s*.189,-.002,1.012,.024,.026),(s*.204,-.005,.941,.022,.023),(s*.207,-.014,.916,.024,.022),(s*.217,-.023,.855,.019,.021),(s*.224,-.032,.770,.016,.018)],skin,'01 Anatomy',sub=2)
 # Palm and separate finger forms for later retopology.
 palm=uv('Palm.'+side,(s*.226,-.031,.753),(.022,.015,.038),skin)
 for j in range(4):
  x=s*(.210+j*.011);end=.696+abs(j-1.4)*.006
  curve('Finger_%d.%s'%(j+1,side),[(x,-.033,.746),(x+s*.002,-.040,.719),(x+s*.004,-.035,end)],.0052,skin,'01 Anatomy',radii=[1,.9,.65])
 curve('Thumb.'+side,[(s*.208,-.034,.767),(s*.196,-.050,.746),(s*.200,-.056,.727)],.0075,skin,'01 Anatomy',radii=[1,.85,.65])
 # Trousers broad at thigh, loose at knee, bunched at ankles.
 tube('Trouser leg.'+side,[(s*.064,.004,.795,.050,.048),(s*.068,.005,.752,.055,.052),(s*.072,.004,.670,.063,.068),(s*.078,.002,.565,.057,.060),(s*.082,-.008,.455,.049,.054),(s*.081,.006,.405,.054,.058),(s*.084,.006,.350,.049,.050),(s*.084,.009,.250,.041,.048),(s*.086,-.001,.173,.050,.047),(s*.085,.002,.142,.039,.043),(s*.085,0,.126,.042,.044)],brown,wrinkle=.10)
 uv('Shoe ankle.'+side,(s*.085,.008,.113),(.030,.036,.045),shoe,'04 Clothing')
 # Shoes with layered sole, upper, toe, tongue and laces.
 rounded('Sole.'+side,(s*.085,-.027,.038),(.095,.188,.042),sole,'04 Clothing',.018)
 uv('Canvas shoe upper.'+side,(s*.085,-.021,.072),(.045,.088,.043),shoe,'04 Clothing')
 uv('Rubber toe cap.'+side,(s*.085,-.089,.063),(.044,.035,.026),sole,'04 Clothing')
 rounded('Shoe tongue.'+side,(s*.085,-.018,.104),(.045,.068,.009),shoe,'04 Clothing',.009)
 for j in range(5):
  y=-.054+j*.014
  curve('Lace.%s.%02d'%(side,j),[(s*.085-.021,y,.103),(s*.085,y+.006,.112),(s*.085+.021,y,.103)],.0015,thread)
 # side seam is subtle, follows the silhouette
 curve('Trouser outer seam.'+side,[(s*.13,0,.73),(s*.132,0,.57),(s*.13,0,.42),(s*.125,0,.23),(s*.122,0,.15)],.0012,brown)
# Join only the newly built clothing shells to soften sleeve/body joins.
parts=[o for o in cols['04 Clothing'].objects if o.name.startswith('Sleeve.') or o.name.startswith('Shirt | main')]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=shirt
bpy.ops.object.convert(target='MESH');bpy.ops.object.join()
shirt=bpy.context.object
md=shirt.modifiers.new('Cloth shell union','REMESH');md.mode='VOXEL';md.voxel_size=.003;md.use_smooth_shade=True
md=shirt.modifiers.new('Relax sleeve joins','SMOOTH');md.factor=.65;md.iterations=3
for s,side in [(-1,'L'),(1,'R')]:
 for j in range(4):
  z=.18+j*.021
  curve('Ankle fabric fold.%s.%d'%(side,j),[(s*.085-.033,-.034,z),(s*.085,-.049,z+.009),(s*.085+.033,-.034,z-.002)],.0027,brown)
# Small flat repair on left trouser knee.
patch=rounded('Knee repair patch',(-.081,-.054,.444),(.041,.006,.067),brown,'04 Clothing',.005)
for i in range(5):
 z=.419+i*.012;curve('Knee hand stitch %d'%i,[(-.107,-.060,z),(-.096,-.061,z+.004)],.00085,thread)
# Head as a continuous editable quad surface with shaped forehead, cheek and chin profiles.
profiles=[(1.235,.025,.036),(1.244,.048,.045),(1.262,.065,.054),(1.285,.077,.062),(1.312,.090,.067),(1.336,.096,.071),(1.361,.093,.073),(1.385,.092,.075),(1.411,.090,.075),(1.435,.080,.068),(1.453,.060,.054),(1.465,.028,.027)]
vs=[];fs=[];N=64
for j,(z,rx,ry) in enumerate(profiles):
 for k in range(N):
  a=2*pi*k/N;x=rx*cos(a);y=ry*sin(a)
  # Face features are formed on the front, not the back of the skull.
  fw=max(0,-sin(a))**6
  nose=.012*math.exp(-(x/.022)**2-((z-1.322)/.045)**2)
  muzzle=.004*math.exp(-(x/.045)**2-((z-1.284)/.023)**2)
  sockets=.006*(math.exp(-((x-.040)/.026)**2-((z-1.36)/.014)**2)+math.exp(-((x+.040)/.026)**2-((z-1.36)/.014)**2))
  y+=fw*(-nose-muzzle+sockets)
  vs.append((x,y,z))
for j in range(len(profiles)-1):
 for k in range(N):a=j*N+k;b=j*N+(k+1)%N;fs.append((a,b,b+N,a+N))
fs.append(tuple(reversed(range(N))));fs.append(tuple((len(profiles)-1)*N+k for k in range(N)))
head=mesh('Head | primary facial form',vs,fs,skin,'01 Anatomy',2)
# Nose integrated detail forms.
uv('Nose bridge',(0,-.074,1.331),(.014,.013,.030),skin,'02 Face')
uv('Nose tip',(0,-.087,1.313),(.018,.017,.012),skin,'02 Face')
for s,side in [(-1,'L'),(1,'R')]:
 uv('Nose wing.'+side,(s*.014,-.078,1.309),(.010,.012,.009),skin,'02 Face')
 uv('Nostril.'+side,(s*.011,-.088,1.304),(.004,.002,.0025),shadow,'02 Face')
 # Ears with inset concha and outer helix.
 uv('Ear.'+side,(s*.095,.001,1.333),(.020,.014,.032),skin,'01 Anatomy')
 uv('Ear concha.'+side,(s*.103,-.010,1.334),(.009,.004,.018),lip,'02 Face')
 curve('Ear helix.'+side,[(s*.099,-.013,1.307),(s*.111,-.012,1.321),(s*.112,-.010,1.350),(s*.103,-.008,1.36),(s*.092,-.010,1.346)],.0035,skin,'02 Face')
 # Modest almond eye apertures with eyelids; eyeball mostly buried in skull.
 x=s*.040
 uv('Eye globe.'+side,(x,-.059,1.359),(.023,.016,.0125),white,'02 Face')
 uv('Iris.'+side,(x,-.076,1.359),(.0105,.0018,.0105),iris,'02 Face')
 uv('Pupil.'+side,(x,-.0778,1.359),(.0049,.001,.0052),black,'02 Face')
 uv('Eye glint.'+side,(x-.0025,-.079,1.362),(.0016,.0007,.0017),white,'02 Face',16,12)
 upper=[(x-.026,-.066,1.358),(x-.014,-.074,1.371),(x+.004,-.076,1.374),(x+.022,-.068,1.365),(x+.027,-.063,1.359)]
 lower=[(x-.026,-.066,1.358),(x-.013,-.074,1.349),(x+.008,-.075,1.348),(x+.027,-.063,1.359)]
 curve('Upper lid.'+side,upper,.004,skin,'02 Face',radii=[.6,1,1,.8,.4]);curve('Lower lid.'+side,lower,.0032,skin,'02 Face',radii=[.5,1,1,.5])
 curve('Upper lash line.'+side,[(a,b-.0018,c-.001) for a,b,c in upper],.0012,black,'02 Face',radii=[.3,.7,1,.7,.2])
 brow=[(x-.025,-.069,1.389),(x-.013,-.076,1.395),(x+.005,-.076,1.396),(x+.024,-.068,1.390)]
 curve('Thick eyebrow.'+side,brow,.0044,hair,'02 Face',radii=[.3,1.1,1,.2])
 for j in range(11):
  xx=x-.020+j*.004
  zz=1.393+.003*sin(j*pi/10)
  curve('Brow strand.%s.%02d'%(side,j),[(xx,-.076,zz-.002),(xx+s*.002,-.077,zz+.003)],.00055,hair2,'02 Face')
# Closed relaxed smile, cupid bow and subtle lower lip.
curve('Upper lip',[(-.027,-.064,1.284),(-.013,-.076,1.287),(0,-.079,1.285),(.012,-.075,1.287),(.027,-.064,1.284)],.0033,lip,'02 Face',radii=[.15,.9,.8,.9,.15])
curve('Lower lip',[(-.026,-.065,1.283),(0,-.079,1.279),(.026,-.065,1.283)],.0036,lip,'02 Face',radii=[.15,1,.15])
curve('Mouth expression crease',[(-.027,-.067,1.284),(-.012,-.078,1.283),(0,-.080,1.2825),(.013,-.078,1.283),(.027,-.067,1.284)],.00095,shadow,'02 Face')
# Fitted scalp shell with irregular hairline plus individually editable tapered curls.
vs=[];fs=[];NN=48;RR=12
for j in range(RR):
 t=j/(RR-1)
 for k in range(NN):
  a=2*pi*k/NN;end=1.8+.33*sin(a) # front hairline higher than back
  theta=.06+t*end
  vs.append((.103*sin(theta)*cos(a),.004+.085*sin(theta)*sin(a),1.405+.087*cos(theta)))
for j in range(RR-1):
 for k in range(NN):a=j*NN+k;b=j*NN+(k+1)%NN;fs.append((a,b,b+NN,a+NN))
mesh('Hair | scalp foundation',vs,fs,hair,'03 Hair',1)
for i in range(42):
 a=random.uniform(0,2*pi);theta=random.uniform(.12,1.62)
 x=.100*sin(theta)*cos(a);y=.004+.083*sin(theta)*sin(a);z=1.405+.092*cos(theta)
 o=uv('Hair sculpted mass %02d'%i,(x,y,z),(.020+random.random()*.009,.019,.024+random.random()*.014),hair,'03 Hair',24,16)
 o.rotation_euler=(random.uniform(-.6,.6),random.uniform(-.6,.6),random.uniform(-pi,pi))
for i in range(70):
 a=random.uniform(0,2*pi);t=random.uniform(.15,1.65);phase=random.uniform(0,2*pi)
 pts=[]
 for j in range(7):
  u=j/6;ang=a+.48*u;theta=t-.35*u
  lift=.009+.018*sin(pi*u)
  x=(.103+lift)*sin(theta)*cos(ang)+.007*sin(u*2*pi+phase)
  y=.004+(.086+lift)*sin(theta)*sin(ang)+.006*cos(u*2*pi+phase)
  z=1.405+(.092+lift)*cos(theta)+.006*sin(u*3*pi+phase)
  pts.append((x,y,z))
 curve('Tousled hair lock %03d'%i,pts,random.uniform(.0014,.0025),hair2 if i%4==0 else hair,'03 Hair',radii=[.6,1,1,.9,.7,.4,.05])
# Fringe falls across forehead in curved, tapered locks.
for i in range(11):
 x=-.083+i*.0165;z=1.422+random.uniform(-.008,.012)
 curve('Front fringe %02d'%i,[(x,.001,1.479),(x-.01,-.052,1.462),(x+.01,-.080,z+.009),(x+.004,-.082,z-.023)],.006,hair,'03 Hair',radii=[1.2,1.3,.9,.04])
# Backpack body and usable pockets, seam piping, shoulder straps and buckles.
rounded('Backpack main body',(0,.090,1.009),(.185,.103,.238),canvas,bevel=.026)
rounded('Backpack front pocket',(0,.151,.975),(.143,.027,.099),canvas,bevel=.014)
rounded('Backpack lid flap',(0,.151,1.102),(.177,.019,.076),canvas,bevel=.018)
curve('Carry handle',[(-.03,.1,1.13),(-.025,.105,1.17),(.025,.105,1.17),(.03,.1,1.13)],.007,canvas,'05 Backpack')
for s,side in [(-1,'L'),(1,'R')]:
 pts=[(s*.067,.126,1.10),(s*.088,.048,1.196),(s*.092,-.048,1.173),(s*.088,-.077,1.07),(s*.078,-.079,.96),(s*.073,.045,.90)]
 # flat ribbon shoulder strap
 vs=[];fs=[]
 for x,y,z in pts:vs.extend([(x-.009,y,z),(x+.009,y,z)])
 for j in range(len(pts)-1):fs.append((2*j,2*j+1,2*j+3,2*j+2))
 o=mesh('Shoulder strap.'+side,vs,fs,canvas,'05 Backpack',2);md=o.modifiers.new('Canvas strap thickness','SOLIDIFY');md.thickness=.003
 for dx in [-.007,.007]:curve('Strap edge stitching.'+side+str(dx),[(x+dx,y-.001,z) for x,y,z in pts],.0006,thread,'05 Backpack')
 curve('Brass strap buckle.'+side,[(s*.088-.010,-.083,1.07),(s*.088+.010,-.083,1.07),(s*.088+.010,-.083,1.048),(s*.088-.010,-.083,1.048),(s*.088-.010,-.083,1.07)],.002,metal,'05 Backpack')
# Packed original concept image, displayed as a reference card beside the model in viewport.
im=bpy.data.images.load(REF,check_existing=True);im.name='Enkidu | original full concept and portrait';im.pack()
ref=bpy.data.objects.new('REFERENCE | full concept (packed)',None);cols['06 References'].objects.link(ref);ref.empty_display_type='IMAGE';ref.data=im;ref.empty_display_size=1.6;ref.location=(1.35,.20,.76);ref.rotation_euler=(pi/2,0,0);ref.color[3]=1;ref.hide_render=True
ref['role']='Original concept art. Front body and portrait are different scales; compare proportion and identity separately.'
# Anatomical proportional guide, hidden from render, optional aligned tracing reference.
trace=bpy.data.objects.new('REFERENCE | aligned body tracing (toggle visibility)',None);cols['06 References'].objects.link(trace);trace.empty_display_type='IMAGE';trace.data=im;trace.empty_display_size=2.30;trace.empty_image_offset=(-.247,-.035);trace.location=(0,.13,0);trace.rotation_euler=(pi/2,0,0);trace.color[3]=.30;trace.hide_render=True;trace.hide_set(True)
# Studio setup.
floor=mat('Studio | warm limestone',(.20,.19,.16),.9)
rounded('Ground',(0,0,-.018),(200,200,.02),floor,'07 Studio',.002)
world=bpy.data.worlds.new('Warm neutral studio');sc.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.23,.25,.29,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35

def light(n,loc,energy,size,color):
 d=bpy.data.lights.new(n,'AREA');d.energy=energy;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(n,d);cols['07 Studio'].objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.85))-o.location).to_track_quat('-Z','Y').to_euler()
light('Key softbox',(-2,-3,4),180,3,(1,.83,.65));light('Fill softbox',(2,-1,2),110,2,(.7,.82,1));light('Hair rim',(0,2,3),230,2,(1,.79,.53))
camd=bpy.data.cameras.new('Character portrait lens');cam=bpy.data.objects.new('Camera | full body',camd);cols['07 Studio'].objects.link(cam);cam.location=(1.35,-4,1.72);target=Vector((0,0,.78));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camd.type='ORTHO';camd.ortho_scale=1.78;sc.camera=cam
sc.render.engine='CYCLES';sc.cycles.samples=32;sc.cycles.use_denoising=True
sc.render.resolution_x=900;sc.render.resolution_y=1100;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG';sc.render.filepath=ROOT+'/enkidu-starter-preview-v03.png'
sc.view_settings.view_transform='AgX'
# Honest development note saved inside file.
t=bpy.data.texts.new('START HERE | Enkidu development notes');t.write('Enkidu — initial editable character study\n\nOriginal full concept and portrait are packed into the file and available in References.\nApproximate height 1.5 m is a modeling assumption, not established canon.\nSeparate editable anatomy, face, hair locks, clothes, backpack, and studio collections.\nThis is an initial modeled study, not a finished likeness or production-ready character.\nNext: sculpt likeness against portrait; integrate nose/eyelids/ears; refine hands, cloth folds and hair masses; retopology, UVs, painted textures and rig.\nBack/side proportions are inferred because only front reference is supplied.\n')
# Frame front view and show materials on reopening.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   sp=area.spaces.active;sp.shading.type='MATERIAL';sp.region_3d.view_rotation=Quaternion((1,0,0),pi/2);sp.region_3d.view_distance=2.8;sp.region_3d.view_location=(.48,0,.77);sp.region_3d.view_perspective='ORTHO';sp.clip_end=500
bpy.ops.object.select_all(action='DESELECT');head.select_set(True);bpy.context.view_layer.objects.active=head
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_character_starter_v03.blend')
bpy.ops.render.render(write_still=True)
print('ENKIDU_SAVED',len(sc.objects),ROOT)
