import bpy
from math import *
from mathutils import Vector, Matrix


def apply(matrix, vector):
    '''
    apply(matrix, vector) -> vector

    this function receives a matrix and a vector and returns
    the vector obtained by multipling each row of the matrix
    with the vector
    '''
    V_0 = vector @ matrix[0]
    V_1 = vector @ matrix[1]
    V_2 = vector @ matrix[2]
    return Vector((V_0, V_1, V_2))


def mobius(major_radius: float = 1, minor_radius: float = 0.15, thick: float = 0.1, resolution: int = 108):
    '''
    major_radius - how large the strip will be
    minor_radius - defines how tall the strip will be (surface width)
    thick        - distance between front and back sides
    resolution   - number of loop iterations to perform
    '''

    verts = []
    faces = []
    dx = Vector([major_radius, 0, 0])

    for i in range(resolution):
        # the angle to rotate around the minor axis (covers a 180° rotation)
        phi = pi * i / resolution

        # the angle to rotate around the major axis (covers a 360° rotation)
        theta = phi * 2

        # how many vertices do we have in our list
        idx = len(verts)

        p0 = Vector((-thick/2, 0,  minor_radius))
        p1 = Vector((thick/2, 0,  minor_radius))
        p2 = Vector((thick/2, 0, -minor_radius))
        p3 = Vector((-thick/2, 0, -minor_radius))

        # Rotates along major radius
        # angle=theta, size=3, axis=[0, 0, 1]
        rot_theta = Matrix.Rotation(theta, 3, [0, 0, 1])

        # Rotates along minor radius
        # angle=phi, size=3, axis=[0, 1, 0]
        rot_phi = Matrix.Rotation(phi, 3, [0, 1, 0])

        p0_rotated = apply(rot_phi, p0)
        p1_rotated = apply(rot_phi, p1)
        p2_rotated = apply(rot_phi, p2)
        p3_rotated = apply(rot_phi, p3)

        p0_moved = p0_rotated + dx
        p1_moved = p1_rotated + dx
        p2_moved = p2_rotated + dx
        p3_moved = p3_rotated + dx

        v0 = apply(rot_theta, p0_moved)
        v1 = apply(rot_theta, p1_moved)
        v2 = apply(rot_theta, p2_moved)
        v3 = apply(rot_theta, p3_moved)

        verts.extend([v0, v1, v2, v3])

        # `idx` represents the position of the first newly added vertice
        # so since we want the position of the next vertices we add 4 to that
        next_verts = idx + 4

        # If we are not at the end of the loop we find the index positions
        # of the next vertices in the `verts` list
        if i+1 < resolution:
            n0 = next_verts + 0
            n1 = next_verts + 1
            n2 = next_verts + 2
            n3 = next_verts + 3
        # Otherwise reference the vertices created the very first loop iteration
        else:
            n0 = 2
            n1 = 3
            n2 = 0
            n3 = 1
        faces.append([idx+0, idx+1, n1, n0])  # top face
        faces.append([idx+1, idx+2, n2, n1])  # front side face
        faces.append([idx+2, idx+3, n3, n2])  # bottom face
        faces.append([idx+3, idx+0, n0, n3])  # back side face

    # Create a blank mesh
    mesh = bpy.data.meshes.new("mobius_strip")

    # Create a mesh from the given vertices and faces
    mesh.from_pydata(verts, [], faces)

    # Ensure the mesh is valid
    if mesh.validate():
        print('Invalid mesh')
        return

    # Create a new object
    ob = bpy.data.objects.new("Mobius Strip Mesh", mesh)

    # Add our object to the current collection
    bpy.context.collection.objects.link(ob)


mobius()
