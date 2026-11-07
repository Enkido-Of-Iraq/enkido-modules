import bpy,math
from math import sin,cos,pi
s=bpy.context.scene
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
for o in s.objects:
 if o.name.startswith('V09 • gravity folded trouser'):
  for v in o.data.vertices:
   if v.co.z>.65:v.co.z-=.027*min(1,(v.co.z-.65)/.07)
 if o.name.startswith('V09 • continuous shirt'):
  for v in o.data.vertices:
   k=1+.14*max(0,min(1,(.85-v.co.z)/.17));v.co.x*=k;v.co.y*=k
 if o.type=='CURVE' and o.name.startswith(('V09 • double shirt hem','V09 • uneven hand sewn','V09 • frayed shirt')):
  for sp in o.data.splines:
   for p in sp.points:
    k=1+.14*max(0,min(1,(.85-p.co.z)/.17));p.co.x*=k;p.co.y*=k
# Fine irregular dirt/fading on cotton and rubber, separate from modeled tears.
for ma in bpy.data.materials:
 if not ma.name.startswith('V09') or not any(k in ma.name for k in ['cotton','twill','canvas','rubber foxing']):continue
 n=ma.node_tree.nodes;l=ma.node_tree.links;p=n.get('Principled BSDF')
 old=p.inputs['Base Color'].links[0].from_socket if p.inputs['Base Color'].is_linked else None
 geo=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=380;noise.inputs['Detail'].default_value=4;l.new(geo.outputs['Position'],noise.inputs[0])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.48;ramp.color_ramp.elements[0].color=(0,0,0,1);ramp.color_ramp.elements[1].position=.73;ramp.color_ramp.elements[1].color=(.6,.6,.6,1);l.new(noise.outputs['Fac'],ramp.inputs[0])
 mix=n.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.215,.154,.086,1);l.new(ramp.outputs['Color'],mix.inputs[0])
 if old:l.new(old,mix.inputs[1])
 else:mix.inputs[1].default_value=ma.diffuse_color
 l.new(mix.outputs[0],p.inputs['Base Color'])
B=next(c for c in s.collection.children if c.name.startswith('V09 • backpack'))
bagmat=next(m for m in bpy.data.materials if m.name.startswith('V09 • worn brown backpack'))
thread=next(m for m in bpy.data.materials if m.name.startswith('V09 • aged cream'))
for o in list(B.objects):
 if any(k in o.name for k in ['Canvas backpack','Backpack front','Backpack flap','panel piping']):bpy.data.objects.remove(o,do_unlink=True)
def box(name,loc,dim,bevel):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for c in list(o.users_collection):c.objects.unlink(o)
 B.objects.link(o);o.data.materials.append(bagmat);m=o.modifiers.new('Soft rounded canvas corners','BEVEL');m.width=bevel;m.segments=5
 for p in o.data.polygons:p.use_smooth=True
 m=o.modifiers.new('Weighted panel normals','WEIGHTED_NORMAL');m.keep_sharp=True
 return o
box('V11 • fitted soft canvas backpack',(0,.121,.992),(.205,.102,.292),.024)
box('V11 • attached flap',(0,.174,1.086),(.204,.008,.094),.018)
box('V11 • attached lower canvas pocket',(0,.181,.94),(.139,.027,.101),.014)
# Rounded rectangular seams sit on the back panels.
cu=bpy.data.curves.new('Backpack panel topstitches','CURVE');cu.dimensions='3D';cu.bevel_depth=.0005;cu.bevel_resolution=2
for w,h,y,z in [(.095,.136,.173,.992),(.061,.042,.196,.94),(.093,.037,.179,1.086)]:
 pts=[]
 for i in range(161):
  a=2*pi*i/160;pts.append((w*math.copysign(abs(sin(a))**.35,sin(a)),y,z+h*math.copysign(abs(cos(a))**.35,cos(a))))
 sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for i,p in enumerate(pts):sp.points[i].co=(*p,1)
o=bpy.data.objects.new('V11 • backpack panel seams',cu);B.objects.link(o);cu.materials.append(thread)
s['Body revision']+=' V11: flared shirt hem, waist clearance, fine dirt speckling, fitted backpack body flap and pocket seams.'
s.camera=bpy.data.objects['V09 • full body']
bpy.ops.wm.save_as_mainfile(filepath=root+'/Enkidu_body_sketch_v11.blend')
result={'file':bpy.data.filepath,'saved':True}
