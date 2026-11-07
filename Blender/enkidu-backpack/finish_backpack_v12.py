import bpy,ast,math,bmesh
from math import sin,cos,pi,exp
from mathutils import Vector
from mathutils.bvhtree import BVHTree
C=bpy.data.collections['V12 • Enkidu reference backpack'];thread=bpy.data.materials['V12 • muted flax seam thread']
source=ast.parse(open('/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-backpack/build_backpack_v12.py').read())
for node in source.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['curves','stitches','catmull']:exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
for side in [-1,1]:
 ob=bpy.data.objects['V12 • 04 woven shoulder strap '+str(side)]
 pts=catmull([(side*.065,.074,1.12),(side*.081,.064,1.15),(side*.089,.025,1.175),(side*.082,-.035,1.153),(side*.080,-.079,1.098),(side*.079,-.080,1.025),(side*.086,-.066,.963),(side*.105,.022,.926),(side*.089,.071,.897),(side*.089,.071,.866)],151)
 # Remove unused alternate shape that did not include stitch/hardware deformation.
 ob.shape_key_clear()
 for i,p in enumerate(pts):
  for j in range(5):ob.data.vertices[i*5+j].co=(p.x+.024*(-.5+j/4),p.y,p.z)
 bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();tree=BVHTree.FromObject(ob,deps)
 paths=[]
 for dx in [-.0095,.0095]:
  path=[]
  for p in pts:
   query=Vector((p.x+dx,p.y-.005,p.z));hit,n,idx,d=tree.find_nearest(query)
   path.append(hit+n*.00025 if hit else query)
  paths.append(path)
 old=bpy.data.objects['V12 • 04 strap edge stitches '+str(side)]
 new=stitches('04 continuous fitted webbing stitches '+str(side),paths,spacing=.0027,length=.00165,radius=.00023)
 old.hide_render=True;old.hide_viewport=True
 # Anchor patch sits above the flat lower strap so the box/X is actually visible.
 ob=bpy.data.objects['V12 • 06 reinforced lower anchor '+str(side)]
 for v in ob.data.vertices:v.co.y=.0677
 st=bpy.data.objects['V12 • 06 box X reinforcement '+str(side)]
 for sp in st.data.splines:
  for p in sp.points:p.co.y=.065
# Plain canvas weave: alternating warp/weft relief plus subtle yarn color.
for ma in [bpy.data.materials['V12 • sun faded brown canvas'],bpy.data.materials['V12 • dense flat cotton webbing'],bpy.data.materials['V12 • dark cotton inner lining']]:
 n=ma.node_tree.nodes;l=ma.node_tree.links;p=n.get('Principled BSDF')
 for w in [x for x in n if x.type=='TEX_WAVE']:w.inputs['Scale'].default_value=390;w.inputs['Distortion'].default_value=.03
 weave=next(x for x in n if x.type=='MATH')
 color=n.new('ShaderNodeValToRGB');color.name='Individual warp and weft yarn tone';color.color_ramp.elements[0].color=(.58,.54,.48,1);color.color_ramp.elements[1].color=(1,1,1,1);l.new(weave.outputs[0],color.inputs[0])
 old=p.inputs['Base Color'].links[0].from_socket
 mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.48;l.new(old,mix.inputs[1]);l.new(color.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
 bumps=[x for x in n if x.type=='BUMP'];bumps[0].inputs['Strength'].default_value=.55;bumps[0].inputs['Distance'].default_value=.00038
 # Keep the dirt mottled but reduce the suede-like broad contrast.
 ramp=next(x for x in n if x.type=='VALTORGB');c0=Vector(ramp.color_ramp.elements[0].color[:3]);c1=Vector(ramp.color_ramp.elements[1].color[:3]);mid=(c0+c1)/2
 ramp.color_ramp.elements[0].color=(*(mid*.76),1);ramp.color_ramp.elements[1].color=(*(mid*1.24),1)
sc=bpy.data.scenes['BACKPACK • isolated construction review'];cam=bpy.data.objects['V12 • bag open'];cam.data.ortho_scale=.59;target=Vector((0,.12,1.105));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
# Extra material / hardware close-up for visual inspection.
d=bpy.data.cameras.new('V12 • bag detail');o=bpy.data.objects.new(d.name,d);sc.collection.objects.link(o);o.location=(.25,.80,1.12);o.rotation_euler=(Vector((.015,.19,1.025))-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=.16
bpy.ops.wm.save_as_mainfile(filepath='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-backpack/Enkidu_backpack_sketch_v12.blend')
result={'saved':True,'weave':'warp/weft relief and yarn color','straps':'stitched on evaluated outer fabric surface'}
