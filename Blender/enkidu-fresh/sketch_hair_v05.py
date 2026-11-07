"""Compact Enkidu sketch groom, revision 3.

Call build_sketch_hair(scene, collection). Only creates its own objects;
never executes on import, clears other objects, renders, or saves files.
All main locks stay against a dense hair envelope. There are no long arching
crown-to-temple guides or large empty side loops.
"""
import math
import random
import bpy
from mathutils import Vector


def build_sketch_hair(scene, collection):
    rng = random.Random(505303)
    created = []
    cy, cz = -0.012, 1.342

    def material(name, colour, roughness=.53):
        ma = bpy.data.materials.new(name)
        ma.use_nodes = True
        ma.diffuse_color = (*colour, 1)
        bs = ma.node_tree.nodes.get('Principled BSDF')
        bs.inputs['Base Color'].default_value = (*colour, 1)
        bs.inputs['Roughness'].default_value = roughness
        bs.inputs['Specular IOR Level'].default_value = .23
        if 'Anisotropic' in bs.inputs:
            bs.inputs['Anisotropic'].default_value = .29
        return ma

    mats = [
        material('V05r3 hair | soft espresso fibre', (.012, .0065, .0031)),
        material('V05r3 hair | natural dark brown fibre', (.017, .0093, .0043)),
        material('V05r3 hair | subtle brown fibre', (.026, .0140, .0062)),
        material('V05r3 hair | sparse warm fibre', (.036, .0195, .0083), .56),
    ]
    rootma = material('V05r3 hair | dense matte inner coverage', (.008, .0041, .0021), .80)

    def end_p(a):
        # Fringe above brows; softly longer side hair; rear nape at ~1.275.
        return (2.05 - .34 * max(math.cos(a), 0) +
                .40 * max(-math.cos(a), 0) + .045 * math.sin(5*a))

    def envelope(a, p, inset=0):
        # Low-frequency irregularity gives natural small masses, not a smooth
        # spherical cap. Base surface is recessed under lifted open main locks.
        irregular = .0021*math.sin(4*a+2.5*p) + .0012*math.cos(7*a-4*p)
        rx, ry, rz = .087-inset, .098-inset, .082-inset
        x = (rx + irregular)*math.sin(p)*math.sin(a)
        y = cy - (ry + irregular)*math.sin(p)*math.cos(a)
        z = cz + (rz + irregular)*math.cos(p)
        return Vector((x, y, z))

    def bound(q):
        # Smooth safety envelope, never a hard flat cap or shaved side.
        # Ordinary guide points remain unaffected; only rare outward wisps
        # approach the soft limits of x=.105 and crown z=1.445.
        if abs(q.x) > .100:
            q.x = math.copysign(.100+.005*math.tanh((abs(q.x)-.100)/.005),q.x)
        if q.z > 1.437:
            q.z = 1.437+.008*math.tanh((q.z-1.437)/.008)
        return q

    # Dense continuous inner coverage is slightly under the fibres. This fills
    # the previous bald gaps and the empty spaces inside the side arches.
    ns, nr = 160, 48
    vv, ff = [], []
    for j in range(nr):
        for i in range(ns):
            a = math.tau*i/ns
            # Hidden root edge is higher and irregular at the forehead.
            # The visible fringe comes from the long main S-wave locks below.
            ep = end_p(a)-.080-.200*max(math.cos(a),0)
            ep += .055*math.sin(a*7+.7)
            p = .004 + (ep-.004)*j/(nr-1)
            vv.append(tuple(envelope(a, p, .010)))
    for j in range(nr-1):
        for i in range(ns):
            a, b = j*ns+i, j*ns+(i+1)%ns
            ff.append((a, a+ns, b+ns, b))
    me = bpy.data.meshes.new('V05r3 compact dense root volume')
    me.from_pydata(vv, [], ff)
    me.update()
    me.materials.append(rootma)
    ob = bpy.data.objects.new('V05r3 hair | filled compact root mass', me)
    collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    created.append(ob)

    # Main locks are 4-7cm open S waves over a recessed substrate. Their
    # changing lift creates readable small clumps and a broken silhouette.
    guide_data = []
    for i in range(300):
        a = rng.uniform(-.95,.95) if i<80 else rng.uniform(-math.pi,math.pi)
        ep = end_p(a) + rng.uniform(-.10, .13)
        length = rng.uniform(.50, .85)
        if i<80:
            # Individually broken forehead tips: never one cut fringe band.
            p1=rng.uniform(1.63,1.86)
            p0=max(.05,p1-length)
        else:
            p0 = rng.uniform(.025, ep-.35)
            p1 = min(ep, p0+length)
        drift = rng.uniform(-.15, .15)
        phase = rng.uniform(-math.pi, math.pi)
        width = rng.uniform(.0022, .0044)
        amp = rng.uniform(.0040, .0070)
        guide = []
        for j in range(28):
            t = j/27
            pp = p0+(p1-p0)*t
            aa = a+drift*t+.13*math.sin(math.tau*t+phase)*math.sin(math.pi*t)
            q = envelope(aa, pp, .003)
            normal = Vector((math.sin(pp)*math.sin(aa),
                             -math.sin(pp)*math.cos(aa), math.cos(pp))).normalized()
            # A little outward lift, never a large arch over empty space.
            q += normal*((.003+amp*math.sin(math.tau*t+phase))*math.sin(math.pi*t))
            guide.append(bound(q))
        guide_data.append((guide, width))

    groups = [[], [], [], []]
    def matidx():
        return rng.choices((0,1,2,3), (.41,.41,.16,.02))[0]

    # 14,400 main fibres in 300 irregular locks; moderate clump widths and
    # independently ending fibres avoid both broad ribbons and a cut bowl edge.
    for guide, width in guide_data:
        tangents, lateral, normal = [], [], []
        for j, q in enumerate(guide):
            tangent = guide[min(j+1,27)]-guide[max(j-1,0)]
            if tangent.length < 1e-7:
                tangent = Vector((0,0,-1))
            tangent.normalize()
            n = q-Vector((0,cy,cz))
            n.normalize()
            lat = tangent.cross(n)
            if lat.length < .01:
                lat = tangent.cross(Vector((0,1,0)))
            lat.normalize()
            if lateral and lat.dot(lateral[-1])<0:
                lat.negate()
            no = tangent.cross(lat).normalized()
            tangents.append(tangent)
            lateral.append(lat)
            normal.append(no)
        for k in range(48):
            off = rng.uniform(-width,width)
            deep = rng.uniform(-.00065,.00065)
            phase = rng.uniform(0, math.tau)
            endfrac = rng.uniform(.86,1)
            pts=[]
            for j in range(28):
                t=j/27
                u=t*endfrac*27
                lo=min(int(u),26)
                f=u-lo
                q=guide[lo].lerp(guide[lo+1],f)
                lat=lateral[lo].lerp(lateral[lo+1],f).normalized()
                no=normal[lo].lerp(normal[lo+1],f).normalized()
                q+=lat*(off*(.83+.12*math.cos(math.pi*t))+.00035*math.sin(5*t+phase)*t)
                q+=no*(deep+.00025*math.sin(7*t+phase)*math.sin(math.pi*t))
                pts.append(tuple(bound(q)))
            groups[matidx()].append(pts)

    # 7,500 dense short fibres cover the recessed substrate, not the silhouette.
    # They are .00007m in radius as requested, and particularly dense at the
    # forehead / temples so the front root volume does not look bald.
    filler=[[],[],[],[]]
    for i in range(7500):
        a=rng.uniform(-math.pi,math.pi)
        ep=end_p(a)-.07-.18*max(math.cos(a),0)+rng.uniform(-.035,.025)
        p0=rng.uniform(.02,ep-.03)
        le=rng.uniform(.11,.29)
        p1=min(ep+.025,p0+le)
        drift=rng.uniform(-.07,.07)
        phase=rng.uniform(0,math.tau)
        pts=[]
        for j in range(20):
            t=j/19
            p=p0+(p1-p0)*t
            aa=a+drift*t+.018*math.sin(5*t+phase)*math.sin(math.pi*t)
            q=envelope(aa,p,.009)
            n=Vector((math.sin(p)*math.sin(aa),-math.sin(p)*math.cos(aa),math.cos(p))).normalized()
            q+=n*(.0007*math.sin(math.pi*t))
            pts.append(tuple(bound(q)))
        filler[matidx()].append(pts)

    def add_curves(name, paths, ma, radius):
        cu=bpy.data.curves.new(name,'CURVE')
        cu.dimensions='3D'
        cu.bevel_depth=radius
        cu.bevel_resolution=1
        cu.resolution_u=2
        for pts in paths:
            sp=cu.splines.new('POLY')
            sp.points.add(len(pts)-1)
            for j,co in enumerate(pts):
                t=j/(len(pts)-1)
                sp.points[j].co=(*co,1)
                sp.points[j].radius=max(.025,1-t**2)
        ob=bpy.data.objects.new(name,cu)
        collection.objects.link(ob)
        cu.materials.append(ma)
        ob['strand_count']=len(paths)
        ob['guide_style']='Medium-length irregular open S-wave locks over recessed dense substrate; no large side arches'
        created.append(ob)
        return ob

    for i in range(4):
        add_curves('V05r3 hair | small irregular S-wave fibres %02d'%i,groups[i],mats[i],.000055)
        add_curves('V05r3 hair | dense soft filler fibres %02d'%i,filler[i],mats[i],.000070)

    # A restrained broken contour, rather than conspicuous giant loop flyaways.
    wisps=[]
    for i in range(180):
        guide,width=rng.choice(guide_data)
        lift=rng.uniform(.001,.0035)
        pts=[]
        for j,q0 in enumerate(guide):
            t=j/27
            q=q0.copy()
            no=q-Vector((0,cy,cz))
            no.normalize()
            q+=no*(lift*math.sin(math.pi*t))
            pts.append(tuple(bound(q)))
        wisps.append(pts)
    add_curves('V05r3 hair | subtle isolated wisps',wisps,mats[1],.000035)

    for ob in created:
        ob['design_reference']='Enkidu front and profile head sketch'
        ob['revision']='r3: irregular raised rootline, recessed substrate, longer readable open S-wave clumps and varied fringe tips'
    return created
