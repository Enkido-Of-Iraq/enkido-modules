"""Continuous auricle meshes for the Enkidu head sketch revision.

The pinna is a closed double-sided surface. Cartilage ridges, recesses and
lobule are part of the front mesh, not torus primitives or black disks.
Coordinates are metres; Z is up and -Y is the character's forward direction.
No scene changes occur until build_sketch_ears is called by the integrator.
"""
import math
import bpy


def _gaussian(u, v, cu, cv, ru, rv):
    return math.exp(-((u-cu)/ru)**2 - ((v-cv)/rv)**2)


def _catmull(points, count=90):
    """A smooth sampled 2D cartilage guide with clamped end tangents."""
    out = []
    segments = len(points)-1
    for j in range(count):
        q = (segments * j) / (count-1)
        i = min(int(q), segments-1)
        t = q-i
        p0 = points[max(0, i-1)]
        p1 = points[i]
        p2 = points[i+1]
        p3 = points[min(segments, i+2)]
        out.append(tuple(.5*((2*p1[k]) + (-p0[k]+p2[k])*t +
                       (2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t +
                       (-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t)
                         for k in range(2)))
    return out


def _distance_to_path(u, v, points):
    # The densely sampled guides are short, and nearest-point distance gives
    # one smooth ridge without flat curve tubes protruding from the skin.
    return min((u-p[0])**2 + (v-p[1])**2 for p in points)**.5


_ANTIHELIX = _catmull([(-.003, -.015), (.002, -.010), (.0058, -.002),
                       (.0058, .007), (.003, .015)], 100)
_SUPERIOR_CRUS = _catmull([(.0055, .005), (.002, .011), (-.0025, .016)], 60)
_INFERIOR_CRUS = _catmull([(.0050, .003), (.000, .0058), (-.0045, .0078)], 60)


def _outline(angle):
    """Non-elliptical outline: broad upper bowl and soft anterior lobule."""
    sa, ca = math.sin(angle), math.cos(angle)
    u = .0147*ca*(1 + .075*sa + .035*math.cos(2*angle))
    u -= .0014*(1-sa)*.5
    v = .0260*sa
    # The lobule is rounder and slightly narrower than the cartilage above.
    u *= 1 - .10*max(0, -sa)**3
    return u, v


def _front_height(u, v, radius, angle):
    # Base surface is lifted from the side of the skull. Its anterior edge
    # can sink into the head so the ear attachment is visually continuous.
    height = .0025 + .0045*max(0.0, 1-radius*radius)**.6
    angle_from_anterior = math.atan2(math.sin(angle-math.pi),
                                    math.cos(angle-math.pi))
    # Rolled helix follows an open organic arc, interrupted at the tragus.
    opening = 1 - .85*math.exp(-(angle_from_anterior/.42)**2)
    helix = .0038*math.exp(-((radius-.855)/.088)**2)*opening
    helix *= .87 + .13*math.sin(angle+.45)
    height += helix
    # Scapha separates helix from the branching antihelix.
    height -= .0009*math.exp(-((radius-.66)/.10)**2) * max(0, math.cos(angle))
    stem_dist = _distance_to_path(u, v, _ANTIHELIX)
    sup_dist = _distance_to_path(u, v, _SUPERIOR_CRUS)
    inf_dist = _distance_to_path(u, v, _INFERIOR_CRUS)
    height += .0022*math.exp(-(stem_dist/.00175)**2)
    height += .0014*math.exp(-(sup_dist/.00145)**2)
    height += .0015*math.exp(-(inf_dist/.0015)**2)
    # Concha and triangular fossa are depressions rather than dark inserts.
    height -= .0022*_gaussian(u, v, -.0042, -.002, .0063, .0088)
    height -= .0010*_gaussian(u, v, -.0005, .0111, .0034, .0030)
    # Tragus / antitragus and the small intertragic notch.
    height += .0026*_gaussian(u, v, -.0115, -.0005, .0027, .0045)
    height += .0018*_gaussian(u, v, -.0030, -.0134, .0035, .0027)
    height -= .0009*_gaussian(u, v, -.0072, -.0095, .0020, .0023)
    # Supple unpierced lobule, round and free of the helix ridge.
    height += .0016*_gaussian(u, v, -.0032, -.0210, .0060, .0055)
    return height


def build_sketch_ears(scene, collection, skin_material):
    """Return the two new ear objects without altering any existing objects.

    scene is accepted for a consistent builder interface. collection must be
    linked to that scene by the caller. skin_material should be the existing
    real skin shader, not the photographic face-projection material.
    """
    created = []
    segments = 112
    rings = 34
    center_y = -.002
    center_z = 1.272
    root_x = .070

    def attachment_x(local_v):
        # Follow the actual V05 cheek / jaw taper. A constant X attachment
        # left the lower lobule floating outside the narrowing cheek, which
        # read as a square skin flap in the front render.
        z = center_z + local_v
        table = [(1.240, .0600), (1.250, .0635), (1.260, .0670),
                 (1.280, .0705), (1.300, .0685), (1.310, .0680)]
        if z <= table[0][0]:
            return table[0][1]
        if z >= table[-1][0]:
            return table[-1][1]
        for a, b in zip(table, table[1:]):
            if a[0] <= z <= b[0]:
                t = (z-a[0])/(b[0]-a[0])
                # Smoothstep softens the transition at section boundaries.
                t = t*t*(3-2*t)
                return a[1] + (b[1]-a[1])*t
        return root_x

    for side in (-1, 1):
        vertices = []
        faces = []
        # A little natural asymmetry without changing landmark alignment.
        size_u = 1.0 if side < 0 else .975
        size_v = 1.0 if side < 0 else .988
        dz = 0.00015 if side > 0 else 0.0

        def append_surface(back=False):
            offset = len(vertices)
            h = .0022 if back else _front_height(0, 0, 0, 0)
            vertices.append((side*(attachment_x(0)+h), center_y-.10*h, center_z+dz))
            for j in range(1, rings+1):
                r = j/rings
                for i in range(segments):
                    angle = 2*math.pi*i/segments
                    edge_u, edge_v = _outline(angle)
                    u, v = r*edge_u, r*edge_v
                    if back:
                        # Convex rear cartilage under the lobe, almost flat
                        # at the attachment. Gives a physically closed rim.
                        h = .0007 + .0020*(1-r*r)
                    else:
                        h = _front_height(u, v, r, angle)
                    # The plane turns subtly forward, not a flat side disk.
                    # A modest forward tilt exposes a little concha in
                    # front view and places the tragus closer to the cheek.
                    # Edge heights are gentle enough not to form spikes.
                    xx = attachment_x(v*size_v)+h + .24*u
                    yy = center_y + u*size_u - .10*h
                    zz = center_z + v*size_v + dz
                    vertices.append((side*xx, yy, zz))
            local_faces = []
            for i in range(segments):
                local_faces.append((offset, offset+1+i,
                                    offset+1+(i+1)%segments))
            for j in range(rings-1):
                for i in range(segments):
                    a = offset+1+j*segments+i
                    b = offset+1+j*segments+(i+1)%segments
                    local_faces.append((a, a+segments, b+segments, b))
            # Radial triangles and quads both point outwards along +X.
            for face in local_faces:
                if back:
                    face = tuple(reversed(face))
                if side < 0:
                    face = tuple(reversed(face))
                faces.append(face)
            return offset

        front = append_surface(False)
        back = append_surface(True)
        # The outer edge joins front and back with a thin cartilage thickness.
        front_ring = front+1+(rings-1)*segments
        back_ring = back+1+(rings-1)*segments
        for i in range(segments):
            j = (i+1)%segments
            face = (front_ring+i, back_ring+i, back_ring+j, front_ring+j)
            if side < 0:
                face = tuple(reversed(face))
            faces.append(face)

        mesh = bpy.data.meshes.new('Enkidu auricle cartilage surface ' + str(side))
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        mesh.materials.append(skin_material)
        for polygon in mesh.polygons:
            polygon.use_smooth = True
        obj = bpy.data.objects.new('Enkidu sculpted ear ' + ('R' if side < 0 else 'L'), mesh)
        collection.objects.link(obj)
        obj['anatomy'] = ('Continuous helix, branching antihelix, concha, tragus, '
                          'antitragus, intertragic notch and lobule. '
                          'Profile inferred from the user-selected sketch.')
        modifier = obj.modifiers.new('Cartilage surface smoothing', 'SUBSURF')
        modifier.levels = 1
        modifier.render_levels = 1
        created.append(obj)
    return created
