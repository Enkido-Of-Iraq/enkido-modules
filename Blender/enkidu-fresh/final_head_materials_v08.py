import bpy, math
s=bpy.context.scene
root='/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-fresh'
img=next(i for i in bpy.data.images if 'exec-400a2b28' in i.name)
# A reference-coloured iris is a normal texture on the modeled eye surface;
# geometry, lid depth and skin/head silhouette remain three dimensional.
m=bpy.data.materials.new('V08 • reference coloured eyes, moist surface');m.use_nodes=True
n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');t=n.new('ShaderNodeTexImage');t.image=img;t.extension='EXTEND';l.new(t.outputs['Color'],p.inputs['Base Color'])
p.inputs['Roughness'].default_value=.28;p.inputs['Specular IOR Level'].default_value=.22;p.inputs['Coat Weight'].default_value=.24;p.inputs['Coat Roughness'].default_value=.12
landmarks=[(1.257,440),(1.267,419),(1.296,343),(1.319,308),(1.344,270)]
def py(z):
 for (a,v0),(b,v1) in zip(landmarks,landmarks[1:]):
  if a<=z<=b:return v0+(v1-v0)*(z-a)/(b-a)
 return 343-(z-1.296)*2000
for o in s.objects:
 if o.type=='MESH' and (o.name.startswith('V07 • visible spherical sclera') or o.name.startswith('V05 • sculpted iris')):
  o.data.materials.clear();o.data.materials.append(m)
  uv=o.data.uv_layers.new(name='Eye pigment from original reference')
  for loop in o.data.loops:
   x,y,z=o.data.vertices[loop.vertex_index].co;uv.data[loop.index].uv=((1102+x*2150)/1536,1-py(z)/1024)
 if o.name.startswith('V05 • natural irregular eyebrow'):o.data.bevel_depth=.000082
 if o.name.startswith('V05 • upper eyelashes'):o.data.bevel_depth=.000065
 if o.name.startswith('V07 • nasal recess'):
  for v in o.data.vertices:v.co.y-=.0012
  p=o.data.materials[0].node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.045,.014,.006,1)
s.camera=bpy.data.objects['V05 • front comparison']
s.render.resolution_x=1100;s.render.resolution_y=1100;s.cycles.samples=96
s['Revision notes']+=' V08: original-reference eye pigment on modeled spherical eye/iris surfaces, denser brow fibres, corrected nasal interior shading. Front, profile and three-quarter review cameras retained.'
bpy.ops.wm.save_as_mainfile(filepath=root+'/Enkidu_sketch_head_v08.blend')
result={'file':bpy.data.filepath,'camera':s.camera.name,'eye_material':m.name}
