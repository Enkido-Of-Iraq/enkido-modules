import bpy,math
from math import sin,cos,pi,sqrt,exp
s=bpy.context.scene
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
def shirt_y(x,z):
 a=math.asin(max(-.99,min(.99,x/.124)))
 def pt(a):
  w=.124+.013*exp(-((z-1.085)/.08)**2)-.007*exp(-((z-.88)/.08)**2)
  d=.065+.004*sin(pi*(z-.745)/.425);f=.0025*sin(9*a+z*27)+.0013*sin(17*a-z*40)
  return (w+f)*sin(a),-(d+f*.6)*cos(a)
 for _ in range(6):
  xx,yy=pt(a);der=(pt(a+.0001)[0]-xx)/.0001
  if abs(der)>.001:a-=(xx-x)/der
 return pt(a)[1]
def lower(z):return z-.065*max(0,min(1,(1.05-z)/.305))
for o in s.objects:
 if o.name.startswith('V09 • continuous shirt'):
  for v in o.data.vertices:
   if v.co.z>1.135:
    t=(v.co.z-1.135)/.04;v.co.y*=1-.35*t
   v.co.z=lower(v.co.z)
 if o.name.startswith('V09 • gravity folded trouser'):
  side=1 if sum(v.co.x for v in o.data.vertices)>0 else -1
  for v in o.data.vertices:
   if v.co.z>.69:
    t=min(1,(v.co.z-.69)/.081);v.co.y*=1-.26*t;cx=side*.06;v.co.x=cx+(v.co.x-cx)*(1-.23*t);v.co.z-=.025*t
 if o.name.startswith('V09 • right knee repaired'):
  for v in o.data.vertices:
   dx=v.co.x+.071;v.co.y=.007-.056*sqrt(max(.1,1-(dx/.054)**2))-.002
 if o.type=='CURVE' and o.name.startswith(('V09 • uneven hand sewn','V09 • frayed shirt','V09 • double shirt hem')):
  for sp in o.data.splines:
   for p in sp.points:
    x,y,z=p.co[:3]
    if 'hem' not in o.name:p.co.y=shirt_y(x,z)-.0012
    p.co.z=lower(z)
 if o.type=='CURVE' and o.name.startswith('V09 • visible uneven knee'):
  for sp in o.data.splines:
   for p in sp.points:
    dx=p.co.x+.071;p.co.y=.007-.056*sqrt(max(.1,1-(dx/.054)**2))-.003
# Slim arm proportions follow the long relaxed forearm in the new body sketch.
for o in s.objects:
 if o.name.startswith('Slim arm'):
  for v in o.data.vertices:v.co.z-=.045*max(0,min(1,(.95-v.co.z)/.24))
 elif o.name.startswith(('Palm','Finger','Thumb')):o.location.z-=.045
# Tone down the broad noisy colour variation; preserve fine weave and rubbed fading.
for m in bpy.data.materials:
 if not m.name.startswith('V09'):continue
 if m.use_nodes:
  for n in m.node_tree.nodes:
   if n.type=='VALTORGB':
    for e in n.color_ramp.elements:
     base=m.diffuse_color;fac=.85 if e.position<.5 else 1.13
     e.color=(*[min(1,v*fac) for v in base[:3]],1)
  if 'rubber foxing' in m.name or 'rubber' in m.name:
   p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Sheen Weight'].default_value=0;p.inputs['Roughness'].default_value=.77
# Solve height of the actual canvas last at each eyelet / lace location.
def shoez(x,y):
 t=.5;a=math.asin(max(-.9,min(.9,x/.04)))
 def pt(t,a):
  w=.033+.011*(.5+.5*cos(a));xx=((1-t)*w+t*.027)*sin(a)
  yy=-.037+.041*t-(.104-.071*t)*cos(a)
  zz=.040+t*(.066-.012*cos(a))+.003*sin(pi*t)*sin(6*a)
  return xx,yy,zz
 for _ in range(12):
  xx,yy,zz=pt(t,a);ex=xx-x;ey=yy-y;dt=.0001;da=.0001
  q=pt(t+dt,a);r=pt(t,a+da);A=(q[0]-xx)/dt;B=(r[0]-xx)/da;C=(q[1]-yy)/dt;D=(r[1]-yy)/da;det=A*D-B*C
  if abs(det)<1e-8:break
  t-=max(-.15,min(.15,(ex*D-ey*B)/det));a-=max(-.3,min(.3,(A*ey-C*ex)/det));t=max(0,min(1,t))
 return pt(t,a)[2]
foot=next(c for c in s.collection.children if c.name.startswith('V09 • sneakers'))
for o in foot.objects:
 side=1 if o.name.endswith('1') and not o.name.endswith('-1') else -1;cx=side*.078
 if 'tongue' in o.name:
  for v in o.data.vertices:v.co.z=shoez(v.co.x-cx,v.co.y)+.0015
 if o.type=='CURVE' and ('eyelet' in o.name or 'crossed round' in o.name):
  for sp in o.data.splines:
   for i,p in enumerate(sp.points):p.co.z=shoez(p.co.x-cx,p.co.y)+(.0025 if 'crossed' in o.name else .0014)
 if o.type=='CURVE' and 'scuffs' in o.name:
  o.data.bevel_depth=.00010
  for sp in o.data.splines:
   co=sp.points[0].co.copy()
   for p in sp.points:p.co=co+(p.co-co)*.3
 if o.type=='MESH':
  for v in o.data.vertices:v.co.z-=.006
 elif o.type=='CURVE':
  for sp in o.data.splines:
   for p in sp.points:p.co.z-=.006
# More restrained, faded seams and visible wear, retaining every modeled repair.
s.camera=bpy.data.objects['V09 • full body'];s['Body revision']+=' V10: longer shirt, relaxed longer forearms, hidden waist overlap, surface fitted repairs and laces, grounded soles, restrained fabric colour.'
bpy.ops.wm.save_as_mainfile(filepath=root+'/Enkidu_body_sketch_v10.blend')
result={'file':bpy.data.filepath,'camera':s.camera.name}
