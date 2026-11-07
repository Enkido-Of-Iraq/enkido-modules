import bpy,bmesh,math,random
from math import sin,cos,pi,exp,sqrt
from mathutils import Vector
random.seed(909)
s=bpy.context.scene
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
old=bpy.data.collections.new('Body v08 • preserved');s.collection.children.link(old)
for c in list(s.collection.children):
 if c.name.startswith(('Clothing','Footwear','Backpack')):
  for o in list(c.objects):
   c.objects.unlink(o);old.objects.link(o)
old.hide_render=True;old.hide_viewport=True
COL={}
for n in ['V09 • clothing','V09 • repairs and stitching','V09 • sneakers','V09 • backpack','V09 • reference']:
 c=bpy.data.collections.new(n);s.collection.children.link(c);COL[n]=c
C=COL['V09 • clothing'];D=COL['V09 • repairs and stitching'];F=COL['V09 • sneakers'];B=COL['V09 • backpack']
def mesh(name,v,f,m,c,sub=1):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);c.objects.link(o);me.materials.append(m)
 for p in me.polygons:p.use_smooth=True
 if sub:mod=o.modifiers.new('Smooth cloth surface','SUBSURF');mod.levels=sub;mod.render_levels=sub
 return o
def curves(name,paths,radius,ma,c,closed=False):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=2
 for pts in paths:
  sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
  for i,co in enumerate(pts):sp.points[i].co=(*co,1);sp.points[i].radius=1 if closed else .8+.2*sin(pi*i/max(1,len(pts)-1))
 o=bpy.data.objects.new(name,cu);c.objects.link(o);cu.materials.append(ma);return o
def material(name,color,rough=.8,fabric=False):
 ma=bpy.data.materials.new(name);ma.use_nodes=True;ma.diffuse_color=(*color,1);n=ma.node_tree.nodes;l=ma.node_tree.links;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
 if fabric:
  p.inputs['Sheen Weight'].default_value=.18
  geo=n.new('ShaderNodeNewGeometry');t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=28;t.inputs['Detail'].default_value=5;l.new(geo.outputs['Position'],t.inputs[0])
  r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.23;r.color_ramp.elements[0].color=(*[v*.55 for v in color],1);r.color_ramp.elements[1].position=.78;r.color_ramp.elements[1].color=(*[min(1,v*1.5+.025) for v in color],1);l.new(t.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
  t2=n.new('ShaderNodeTexNoise');t2.inputs['Scale'].default_value=2400;t2.inputs['Detail'].default_value=2;l.new(geo.outputs['Position'],t2.inputs[0]);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.23;b.inputs['Distance'].default_value=.00016;l.new(t2.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
 return ma
shirt=material('V09 • faded dusty blue cotton',(.095,.125,.166),.88,True)
pants=material('V09 • worn brown twill',(.13,.082,.046),.9,True)
patchmat=material('V09 • faded knee patch twill',(.16,.106,.064),.92,True)
canvas=material('V09 • dusty grey canvas sneaker',(.11,.12,.113),.87,True)
bagmat=material('V09 • worn brown backpack canvas',(.18,.116,.056),.89,True)
thread=material('V09 • aged cream cotton stitching',(.33,.265,.17),.86,True)
fray=material('V09 • exposed faded cotton fibres',(.22,.23,.22),.92)
rubber=material('V09 • dirt stained rubber foxing',(.28,.235,.173),.84,True)
tread=material('V09 • dark worn outsole',(.09,.075,.052),.89)
metal=material('V09 • tarnished brass',(.22,.145,.07),.44);metal.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.78
hole=material('V09 • dark eyelet interiors',(.025,.018,.012),.85)
# Torso and sleeve geometry share armhole boundary vertices.
N=144;R=100;v=[];f=[]
def torso(z,a):
 t=(z-.745)/.425
 w=.124+.013*exp(-((z-1.085)/.08)**2)-.007*exp(-((z-.88)/.08)**2)
 if z>1.135:w=.14-(z-1.135)/.04*.087
 d=.065+.004*sin(pi*t)
 fold=.0025*sin(9*a+z*27)+.0013*sin(17*a-z*40)
 x=(w+fold)*sin(a);y=-(d+fold*.6)*cos(a)
 zz=z+.002*sin(a*7)*exp(-((z-.745)/.03)**2)
 return (x,y,zz)
for j in range(R):
 z=.745+.43*j/(R-1)
 for i in range(N):v.append(torso(z,2*pi*i/N))
for j in range(R-1):
 for i in range(N):
  ids=(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i)
  x,y,z=sum((Vector(v[k]) for k in ids),Vector())/4
  armhole=abs(x)>.112 and (y/.055)**2+((z-1.100)/.054)**2<1
  tear=y<-.04 and ((((x+.049)/.0038)**2+((z-1.087)/.005)**2<1) or (((x+.058)/.004)**2+((z-.89)/.005)**2<1) or (((x-.073)/.009)**2+((z-.816)/.015)**2<1))
  if not armhole and not tear:f.append(ids)
body=mesh('V09 • continuous shirt panels with real tears',v,f,shirt,C,1)
bm=bmesh.new();bm.from_mesh(body.data);bm.verts.ensure_lookup_table()
# Extend sleeves from the two existing armhole loops, keeping welded shoulders.
for side in [-1,1]:
 loop=[]
 for ve in bm.verts:
  x,y,z=ve.co
  if ve.is_boundary and x*side>.105 and 1.035<z<1.16:
   a=math.atan2((z-1.1)/.054,y/.055);loop.append((a,ve))
 loop.sort(key=lambda q:q[0]);L=len(loop)
 if L<10:continue
 prev=[q[1] for q in loop];start=[q[1].co.copy() for q in loop]
 for j in range(1,13):
  t=j/12;ring=[]
  for k,(a,ve) in enumerate(loop):
   end=Vector((side*(.189+.040*.88*sin(a)),.055*cos(a),1.004+.04*.47*sin(a)))
   co=start[k].lerp(end,t);co.y+=.0017*sin(a*7+t*4)*sin(pi*t)
   ring.append(bm.verts.new(co))
  for k in range(L):
   try:bm.faces.new((prev[k],prev[(k+1)%L],ring[(k+1)%L],ring[k]))
   except ValueError:pass
  prev=ring
bm.normal_update();bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
mod=body.modifiers.new('Actual cotton thickness','SOLIDIFY');mod.thickness=.0013
# Collar ribbing has an actual elliptical section and fine rib lines.
pts=[(.052*sin(a),-.042*cos(a),1.175+.001*cos(3*a)) for a in [2*pi*i/160 for i in range(161)]]
curves('V09 • round ribbed collar',[pts],.004,shirt,D,True)
ribs=[]
for i in range(160):
 a=2*pi*i/160;ribs.append([(.049*sin(a),-.039*cos(a),1.177),(.052*sin(a),-.042*cos(a),1.179),(.055*sin(a),-.045*cos(a),1.174)])
curves('V09 • individual collar ribs',ribs,.00020,thread,D)
# Shirt hems, arm cuff stitches and several tiny frayed fibres near tears.
curves('V09 • double shirt hem',[[(torso(z,2*pi*i/180)[0],torso(z,2*pi*i/180)[1]*1.015,torso(z,2*pi*i/180)[2]) for i in range(181)] for z in [.749,.754]],.00045,thread,D,True)
frays=[]
for cx,cz,rx,rz in [(-.049,1.087,.0038,.005),(-.058,.89,.004,.005),(.073,.816,.009,.015)]:
 for i in range(44):
  a=2*pi*i/44;x=cx+rx*cos(a);z=cz+rz*sin(a);frays.append([(x,-.069,z),(x+random.uniform(-.0015,.0015),-.070,z+random.uniform(-.002,.002))])
curves('V09 • frayed shirt tear edges',frays,.00013,fray,D)
# Hand repaired shirt tear: cross stitches on the subject's left, viewer-right.
st=[]
for i in range(10):
 z=.800+i*.0034;x=.073+.002*sin(i*.8)
 st.append([(x-.011,-.071,z-.001),(x,-.073,z+.001),(x+.011,-.071,z+.003)])
for i in range(5):
 x=.064+i*.004;st.append([(x,-.071,.796),(x+.003,-.073,.814),(x+.006,-.071,.835)])
curves('V09 • uneven hand sewn shirt repair',st,.00040,thread,D)
# Lower torso inside clothes gives real depth to tears without a floating dark sticker.
skin=next(o.data.materials[0] for o in s.objects if o.name.startswith('Slim arm'))
bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=32,location=(0,.004,.97));o=bpy.context.object;o.name='V09 • underlying clothed torso';o.scale=(.109,.058,.199);o.data.materials.append(skin)
for c in list(o.users_collection):c.objects.unlink(o)
C.objects.link(o)
for p in o.data.polygons:p.use_smooth=True
# Trousers: many quad rings for gravity folds and compressed ankle cloth.
def legpt(side,z,a):
 t=(z-.096)/.675;cx=side*(.078-.018*t)
 w=.039+.024*t;d=.041+.022*t
 folds=.0042*exp(-((z-.165)/.06)**2)*sin(z*165+2*a)+.0028*exp(-((z-.40)/.06)**2)*sin(z*100+3*a)+.0016*sin(a*9+z*30)
 return (cx+(w+folds)*sin(a),.007-(d+folds)*cos(a),z+.001*sin(a*7))
for side in [-1,1]:
 vv=[];ff=[];NN=96;RR=90
 for j in range(RR):
  z=.096+.675*j/(RR-1)
  for i in range(NN):vv.append(legpt(side,z,2*pi*i/NN))
 for j in range(RR-1):
  for i in range(NN):a=j*NN+i;b=j*NN+(i+1)%NN;ff.append((a,b,b+NN,a+NN))
 ob=mesh('V09 • gravity folded trouser leg '+str(side),vv,ff,pants,C,1);mod=ob.modifiers.new('Twill thickness','SOLIDIFY');mod.thickness=.0016
 curves('V09 • trouser side seam '+str(side),[[legpt(side,.101+.656*j/120,side*pi/2) for j in range(121)]],.00048,thread,D)
 curves('V09 • ankle cuff '+str(side),[[legpt(side,.103,2*pi*i/120) for i in range(121)]],.0007,pants,D,True)
# Raised repaired panel follows the front of the RIGHT knee (viewer-left).
vv=[];ff=[];nx=20;nz=26
for j in range(nz):
 z=.365+.074*j/(nz-1)
 for i in range(nx):
  x=-.071+(i/(nx-1)-.5)*.052;y=-.054-.002*sin(z*80+x*50);vv.append((x,y,z))
for j in range(nz-1):
 for i in range(nx-1):a=j*nx+i;ff.append((a,a+1,a+1+nx,a+nx))
ob=mesh('V09 • right knee repaired twill panel',vv,ff,patchmat,D,1);mod=ob.modifiers.new('Patch fabric thickness','SOLIDIFY');mod.thickness=.001
st=[]
for i in range(13):
 x=-.097+.052*i/12
 for z in [.365,.439]:st.append([(x-.001,-.056,z-.003),(x+.001,-.058,z),(x+.002,-.056,z+.003)])
for j in range(15):
 z=.365+.074*j/14
 for x in [-.097,-.045]:st.append([(x-.003,-.056,z-.001),(x,-.058,z+.001),(x+.003,-.056,z+.002)])
curves('V09 • visible uneven knee patch stitches',st,.00050,thread,D)
# Sneakers: footprint, layered sidewall and closed canvas last, not ellipsoids.
def outline(a):
 # shoe points toward -Y; toe broad, heel narrower
 y=-.037-.104*cos(a);w=.033+.011*(.5+.5*cos(a));x=w*sin(a)
 return x,y
for side in [-1,1]:
 cx=side*.078;NN=128
 # Layered rubber sole volume with broad flat sole and round upper edge.
 vv=[];ff=[];levels=[(.012,.93),(.015,1),(.032,1),(.039,.985),(.042,.94)]
 for z,sc in levels:
  for i in range(NN):
   x,y=outline(2*pi*i/NN);vv.append((cx+x*sc,-.037+(y+.037)*sc,z))
 for j in range(len(levels)-1):
  for i in range(NN):a=j*NN+i;b=j*NN+(i+1)%NN;ff.append((a,b,b+NN,a+NN))
 ff.append(tuple(reversed(range(NN))));ff.append(tuple((len(levels)-1)*NN+i for i in range(NN)))
 mesh('V09 • layered sneaker rubber sole '+str(side),vv,ff,rubber,F,1)
 # Canvas upper: rings contract toward ankle, toe remains broad and low.
 vv=[];ff=[];RR=24
 for j in range(RR):
  t=j/(RR-1)
  for i in range(NN):
   a=2*pi*i/NN;x,y=outline(a)
   # transition from footprint to tilted ankle opening at rear
   xx=(1-t)*x+t*.027*sin(a);yy=(1-t)*y+t*(.004-.033*cos(a));zz=.040+t*(.066-.012*cos(a))+.003*sin(pi*t)*sin(6*a)
   vv.append((cx+xx,yy,zz))
 for j in range(RR-1):
  for i in range(NN):a=j*NN+i;b=j*NN+(i+1)%NN;ff.append((a,b,b+NN,a+NN))
 ob=mesh('V09 • stitched canvas sneaker upper '+str(side),vv,ff,canvas,F,1);mod=ob.modifiers.new('Canvas thickness','SOLIDIFY');mod.thickness=.0016
 # Rounded rubber toe guard on front quarter of the actual last.
 vv=[];ff=[];A=70;R=13
 for j in range(R):
  t=j/(R-1)*.28
  for i in range(A):
   a=-pi*.48+pi*.96*i/(A-1);x,y=outline(a)
   vv.append((cx+(1-t)*x+t*.027*sin(a), (1-t)*y+t*(.004-.033*cos(a))-.0007,.041+t*(.066-.012*cos(a))+.001))
 for j in range(R-1):
  for i in range(A-1):a=j*A+i;ff.append((a,a+1,a+1+A,a+A))
 mesh('V09 • curved rubber toe cap '+str(side),vv,ff,rubber,F,1)
 # Foxing stripe, fine rubber edge and canvas stitching.
 for zz,rad in [(.023,.0007),(.034,.0005),(.041,.00045)]:
  curves('V09 • rubber foxing edge '+str(side),[[(cx+outline(2*pi*i/NN)[0]*1.003,outline(2*pi*i/NN)[1],zz) for i in range(NN+1)]],rad,tread if zz==.023 else thread,F,True)
 # Tongue follows instep behind laces.
 vv=[];ff=[]
 for j in range(16):
  t=j/15;y=-.099+.112*t;z=.060+.051*t
  for i in range(9):
   x=-.019+.038*i/8;vv.append((cx+x,y,z+.003*(1-(x/.02)**2)))
 for j in range(15):
  for i in range(8):a=j*9+i;ff.append((a,a+1,a+10,a+9))
 mesh('V09 • soft canvas tongue '+str(side),vv,ff,canvas,F,1)
 lacepaths=[]
 for j in range(7):
  t=j/6;y=-.099+.1*t;z=.066+.045*t
  for sign in [-1,1]:
   x=cx+sign*.022
   ring=[(x+.0023*cos(a),y+.0023*sin(a),z+.001) for a in [2*pi*i/28 for i in range(29)]]
   curves('V09 • metal lace eyelet '+str(side),[ring],.00065,metal,F,True)
  if j<6:
   for sign in [-1,1]:lacepaths.append([(cx+sign*.022,y,z+.002),(cx,y+.008,z+.006),(cx-sign*.022,y+.0167,z+.0095)])
 curves('V09 • crossed round cotton laces '+str(side),lacepaths,.0010,thread,F)
 # Bow loops and dangling irregular lace ends.
 loops=[]
 for sign in [-1,1]:loops.append([(cx+sign*.022*sin(pi*i/35),.004+.012*sin(2*pi*i/35),.118+.003*sin(pi*i/35)) for i in range(36)])
 loops.extend([[(cx,.005,.117),(cx-.012,-.015,.108),(cx-.015,-.04,.086)],[(cx,.005,.117),(cx+.014,-.008,.107),(cx+.022,-.028,.091)]])
 curves('V09 • tied lace bow and ends '+str(side),loops,.0009,thread,F)
 # Local scuff scratches and dirt chips near the toe/sole, irregular not patterned.
 scuffs=[]
 for k in range(75):
  a=random.uniform(-1.3,1.3);x,y=outline(a);z=random.uniform(.018,.047)
  scuffs.append([(cx+x,y-.001,z),(cx+x+random.uniform(-.003,.003),y-.0015,z+random.uniform(.001,.004))])
 curves('V09 • rubber scuffs '+str(side),scuffs,.00018,tread,F)
# Backpack: retain existing soft body shapes, replace straps and add panel seams.
for ob in list(old.objects):
 if ob.name.startswith(('Canvas backpack','Backpack front','Backpack flap')):
  new=ob.copy();new.data=ob.data.copy();B.objects.link(new);new.hide_render=False;new.hide_viewport=False;new.name='V09 • '+ob.name;new.data.materials.clear();new.data.materials.append(bagmat)
for side in [-1,1]:
 pts=[(side*.083,.13,.96),(side*.101,.10,1.10),(side*.09,.04,1.164),(side*.082,-.02,1.167),(side*.083,-.070,1.12),(side*.08,-.074,1.04),(side*.079,-.074,.947),(side*.099,.02,.92)]
 vv=[];ff=[]
 for x,y,z in pts:vv.extend([(x-.010,y,z),(x+.010,y,z)])
 for i in range(len(pts)-1):ff.append((i*2,i*2+1,i*2+3,i*2+2))
 ob=mesh('V09 • canvas shoulder strap '+str(side),vv,ff,bagmat,B,2);mod=ob.modifiers.new('Strap thickness','SOLIDIFY');mod.thickness=.0025
 for dx in [-.008,.008]:curves('V09 • strap topstitch '+str(side),[[(x+dx,y-.001,z) for x,y,z in pts]],.0004,thread,B)
 x=side*.08;y=-.080;z=1.04
 curves('V09 • brass strap adjuster '+str(side),[[(x-.012,y,z-.012),(x+.012,y,z-.012),(x+.012,y,z+.012),(x-.012,y,z+.012),(x-.012,y,z-.012)],[(x-.012,y-.0005,z),(x+.012,y-.0005,z)]],.0015,metal,B,True)
curves('V09 • backpack panel piping',[[(.104*sin(a),.105+.052*cos(a),.988+.14*cos(2*a)) for a in [2*pi*i/160 for i in range(161)]]],.001,thread,B,True)
# Reference kept packed and separate from modeled surfaces.
ref=bpy.data.images.load('/Users/abbasmamoori/Documents/ChatGPT/New project/concept-art/turnarounds/enkidu-body-turnaround-v1.png',check_existing=True);ref.pack()
bpy.ops.object.empty_add(type='IMAGE',location=(.8,.10,.74));o=bpy.context.object;o.name='V09 • body sketch reference';o.data=ref;o.empty_display_size=1.5;o.rotation_euler=(pi/2,0,0);o.hide_render=True
for c in list(o.users_collection):c.objects.unlink(o)
COL['V09 • reference'].objects.link(o)
def camera(name,loc,target,scale):
 data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=scale;return o
s.camera=camera('V09 • full body',(0,-3,.76),(0,0,.73),1.54)
camera('V09 • shoe detail',(.33,-.55,.26),(0,-.04,.075),.43)
camera('V09 • clothing repair detail',(.18,-2,.75),(0,-.02,.74),.89)
camera('V09 • full profile',(3,-.02,.76),(0,-.02,.73),1.54)
s.render.resolution_x=1000;s.render.resolution_y=1300;s.cycles.samples=64;s.render.filepath=ROOT+'/enkidu-body-v09.png'
s['Body revision']='V09: welded sleeve joins, thick cotton collar, garment tears and fraying, sewn left shirt repair and right knee patch, gravity trouser folds, constructed canvas shoes with layered soles toe guards metal eyelets laces and scuffs, detailed straps. Existing V08 head retained; previous garments preserved hidden.'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_body_sketch_v09.blend')
result={'file':bpy.data.filepath,'new_objects':sum(len(c.objects) for c in COL.values()),'camera':s.camera.name}
