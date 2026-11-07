import bpy,math,bmesh
from math import sin,cos,pi,exp
from mathutils import Vector
C=bpy.data.collections['V12 • Enkidu reference backpack']
for o in C.objects:
 if o.type=='MESH' and o.data.shape_keys:
  for k in o.data.shape_keys.key_blocks:k.value=0
# Keep the visibly brown canvas under soft studio lights; preserve distinct woven grain.
for ma in [bpy.data.materials['V12 • sun faded brown canvas'],bpy.data.materials['V12 • dense flat cotton webbing'],bpy.data.materials['V12 • dark cotton inner lining']]:
 n=ma.node_tree.nodes;l=ma.node_tree.links;p=n.get('Principled BSDF');p.inputs['Sheen Weight'].default_value=.055;p.inputs['Specular IOR Level'].default_value=.25
 r=next(x for x in n if x.type=='VALTORGB')
 for e in r.color_ramp.elements:
  c=e.color;e.color=(c[0]*.68,c[1]*.60,c[2]*.48,1)
 mix=next(x for x in n if x.type=='MIX_RGB');mix.inputs[2].default_value=(.17,.115,.065,1)
 for w in [x for x in n if x.type=='TEX_WAVE']:w.inputs['Scale'].default_value=1250;w.inputs['Distortion'].default_value=.15
 for b in [x for x in n if x.type=='BUMP']:b.inputs['Strength'].default_value=.27;b.inputs['Distance'].default_value=.00012
# Welding the original wrapped shell seam prevents the central shading stripe.
body=bpy.data.objects['V12 • 01 hollow tapered canvas shell'];bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
# Localized compression creases on the lower face and soft side panels.
def deform(co):
 x,y,z=co;front=max(0,min(1,(y-.155)/.035));side=min(1,(abs(x)/.10)**6)
 amount=(.0032*exp(-((z-(.874+.22*x))/.006)**2)-.0016*exp(-((z-(.886+.22*x))/.008)**2))
 amount+=.0022*exp(-((z-(.909-.32*x))/.011)**2)*exp(-((x+.045)/.08)**2)
 y+=front*amount
 x+=math.copysign(.0018*sin((z-.84)*70+4*y)*side*exp(-((z-.91)/.11)**2),x)
 return Vector((x,y,z))
for o in C.objects:
 if o.name.startswith(('V12 • 01 ','V12 • 07 ','V12 • 08 ')):
  if o.type=='MESH':
   for v in o.data.vertices:v.co=deform(v.co)
  if o.type=='CURVE':
   for sp in o.data.splines:
    for p in sp.points:p.co=(*deform(p.co[:3]),1)
# Flap corner fit: taper the sewn rear edge to the body, increase lower corner rounding.
for o in C.objects:
 if o.name.startswith('V12 • 02 '):
  def fix(co):
   x,y,z=co
   rear=max(0,min(1,(.115-y)/.04));x*=1-.14*rear
   z+=.010*(abs(x)/.103)**8*max(0,min(1,(1.09-z)/.06))
   return (x,y,z)
  if o.type=='MESH':
   for v in o.data.vertices:v.co=fix(v.co)
  elif o.type=='CURVE':
   for sp in o.data.splines:
    for p in sp.points:p.co=(*fix(p.co[:3]),1)
for o in bpy.data.scenes['BACKPACK • isolated construction review'].objects:
 if o.type=='LIGHT':o.data.energy*=.60
bpy.ops.wm.save_as_mainfile(filepath='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-backpack/Enkidu_backpack_sketch_v12.blend')
result={'saved':True}
