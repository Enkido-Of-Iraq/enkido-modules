"""Rebuild from preserved V04 using V05 construction plus reviewed corrections."""
from pathlib import Path
ROOT='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
code=Path(ROOT+'/rebuild_sketch_head_v05.py').read_text()
code=code.replace('(1.194,.019,','(1.194,.042,').replace('(1.205,.036,','(1.205,.047,').replace('(1.221,.052,','(1.221,.056,')
code=code.replace('val=.027*G(x,z,0,1.267,.0115,.0115)','val=.020*G(x,z,0,1.267,.0125,.014)')
code=code.replace('val+=.014*G(x,z,0,1.237,.027,.0045)+.012*G(x,z,0,1.230,.026,.005)','val+=.010*G(x,z,0,1.237,.027,.0055)+.0085*G(x,z,0,1.230,.026,.0055)\n val+=.010*G(x,z,0,1.248,.018,.013)')
code=code.replace("c=cos(a);return 1.194+.034*(1-max(c,0))**.72+.020*max(-c,0)","c=cos(a);t=(1-c)/2;return 1.194+.054*(3*t*t-2*t*t*t)+.007*sin(pi*t)**2")
code=code.replace("c**.62-face_depth", "c**.90-face_depth")
# Do not execute the save portion until all reconstruction fixes are applied.
code=code[:code.index("bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_sketch_head_v05.blend')")]
code=code.replace('topz=1.186+.05*(1-c)/2','topz=1.212+.028*(1-c)/2')
code=code.replace('co.z-=.003*sin(pi*t)','co.z-=.0015*sin(pi*t)')
code=code.replace('.010,1.257,.0038,.0025','.010,1.2625,.0038,.0025')
exec(compile(code,'rebuild_sketch_head_v07_core','exec'))
# Maintain natural procedural skin pigmentation around the photo-derived centre.
n=face.node_tree.nodes;l=face.node_tree.links
ramp=next(no for no in n if no.type=='VALTORGB')
mix=next(no for no in n if no.type=='MIX_RGB')
l.new(ramp.outputs['Color'],mix.inputs[1])
face.node_tree.nodes.get('Principled BSDF').inputs['Diffuse Roughness'].default_value=.12
# Keep full eyeball geometry hidden for editing; render the spherical anterior patch
# only inside the lid aperture. This prevents sclera protruding through the skin.
for side in [-1,1]:
 ball=next(o for o in EC.objects if o.name=='V05 • inset eyeball '+str(side));ball.hide_render=True;ball.hide_set(True)
 cx,cy,cz=ball.location;A=112;B=20;vv=[(cx,cy-EYER,cz)];ff=[]
 for j in range(1,B+1):
  r=j/B
  for i in range(A):
   a=2*pi*i/A;dx=.0152*r*cos(a);dz=(.0059 if sin(a)>0 else .0048)*r*sin(a)
   y=cy-sqrt(max(.000001,EYER*EYER-dx*dx-dz*dz));vv.append((cx+dx,y,cz+dz))
 for i in range(A):ff.append((0,i+1,(i+1)%A+1))
 for j in range(B-1):
  for i in range(A):a=1+j*A+i;b=1+j*A+(i+1)%A;ff.append((a,a+A,b+A,b))
 make_mesh('V07 • visible spherical sclera '+str(side),vv,ff,sclera,EC,1)
# Join the head and its lid tissue so shared edges subdivide as one surface.
bpy.ops.object.select_all(action='DESELECT')
head.select_set(True)
for ob in list(EC.objects):
 if ob.name.startswith('V05 • continuous upper and lower eyelids'):ob.select_set(True)
bpy.context.view_layer.objects.active=head
bpy.ops.object.join()
bm=bmesh.new();bm.from_mesh(head.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000015)
loose=[v for v in bm.verts if not v.link_edges]
if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
bm.normal_update();bm.to_mesh(head.data);bm.free();head.data.update()
# Restrict frontal photographic pigment to camera-facing facial skin.
# Ear, temple, side of jaw and nape use the actual skin shader without front smears.
at=head.data.attributes.get('PortraitWeight')
for i,ve in enumerate(head.data.vertices):
 x,y,z=ve.co;w=spline(PRO,z,1) if z>=1.194 else .05
 c=sqrt(max(0,1-(x/max(.001,w))**2))
 weight=c**5 * max(0,-ve.normal.y)**.6 if y<-.025 else 0
 if z<1.205:weight*=max(0,min(1,(z-1.18)/.025))
 at.data[i].value=weight
# Recessed nasal shading follows the actual nostril dimple as a small continuous fan.
for ob in list(HC.objects):
 if ob.name.startswith('V05 • nostril opening'):bpy.data.objects.remove(ob,do_unlink=True)
for side in [-1,1]:
 cx=side*.010;cz=1.2625;A=64;B=10;vv=[(cx,surface(cx,cz)-.0002,cz)];ff=[]
 for j in range(1,B+1):
  r=j/B
  for i in range(A):
   a=2*pi*i/A;x=cx+.0032*r*cos(a);z=cz+.0013*r*sin(a);vv.append((x,surface(x,z)-.0002,z))
 for i in range(A):ff.append((0,(i+1)%A+1,i+1))
 for j in range(B-1):
  for i in range(A):a=1+j*A+i;b=1+j*A+(i+1)%A;ff.append((a,b,b+A,a+A))
 make_mesh('V07 • nasal recess '+str(side),vv,ff,nasal,HC,1)
head.name='V07 • sketch fitted face skull neck and welded lids'
s['Revision notes']+=' V07 review: rounder chin, smooth philtrum, welded lids, no excess sclera, temple colour projection restricted, compact dense open wave groom, attached soft ear lobules.'
s.camera=front;s.render.resolution_x=1000;s.render.resolution_y=1000;s.cycles.samples=64
s.render.filepath=ROOT+'/enkidu-sketch-head-front-v07.png'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/Enkidu_sketch_head_v07.blend')
print('V07 reconstruction saved',len(head.data.vertices),'head vertices')
