+++
title = "3d Mobius Strip"
date = 2022-12-13
description = "How to create a 3d mobius strip using Blender and Python."
+++

<figure>
    <a href="../assets/mobius_strip/verts_rendered.png">
        <img title="3d mobius strip" src="../assets/mobius_strip/verts_rendered.png" alt="3d mobius strip in Blender" class="img-center">
    </a>
    <figcaption>The final product</figcaption>
</figure>


## Getting started

The purpose of this article to clearly explain how to create a Mobius Strip in Blender using Python.  Technically it's a Mobius Ring since it is a 3d object, but I'll refer to it as a Mobius Strip since that will be a more familiar term for most people.  The goal here is not to be as accurate as possible, but be as clear as possible with easy to understand steps and code.

First I'll describe the steps needed to make a 3d mobius strip then we'll implement those steps in Python code.

> If you aren't familiar with using Python in Blender I'd recommend reading my article on [Setting up Blender](@/blender_python_setup.md).  It is written for Linux, but the section [Importing local Python files](@/blender_python_setup.md#importing-local-python-files) applies to all operating systems and will help make it easier to run Python code.


## General Overview

We will loop over a specified `resolution`, creating 4 vertices at each iteration, and then apply some transformations to move and rotate them into the correct positions.  This will create all of the vertices needed for the mesh.

1. Create 4 vertices.  The width between the vertices is the `thickness` (distance between front and back sides) and the height is the `minor_radius` (how tall it should be).
    
    <figure>
    <figcaption class="title"><h5>Front view</h5></figcaption>
    <a href="../assets/mobius_strip/front_verts.png">
        <img title="4 vertices" src="../assets/mobius_strip/front_verts.png" alt="4 vertices that form a rectangle" class="img-center">
    </a>
    <figcaption>The vertices form a rectangle</figcaption>
    </figure>
    

2. Rotate those vertices around the minor axis and move the vertices `major_radius` away from the center.  Here we are using y as the minor axis and z as the major axis.

    <figure>
    <figcaption class="title"><h5>Front view</h5></figcaption>
    <video loop="true" autoplay="true" class="full">
    <source src="../assets/mobius_strip/vert_placement_front.webm">
    </video>
    <figcaption>Rotate around minor axis and move vertices</figcaption>
    </figure>

3. Rotate the vertices around the major axis

    <figure>
    <figcaption class="title"><h5>Top view</h5></figcaption>
    <video loop="true" autoplay="true" class="full">
    <source src="../assets/mobius_strip/vert_placement_top.webm">
    </video>
    <figcaption>Rotate around major axis</figcaption>
    </figure>

Here is the final placement of vertices after each loop iteration:

<figure>
<figcaption class="title"><h5>Top view</h5></figcaption>
<video loop="true" autoplay="true" class="full">
<source src="../assets/mobius_strip/verts_animation.webm">
</video>
<figcaption>First few steps of the loop</figcaption>
</figure>

Then we just repeat this for the rest of the loop and we will have placed all of our vertices.

<figure>
<figcaption class="title"><h5>Top view</h5></figcaption>
<a href="../assets/mobius_strip/verts_all.png">
    <img title="Final placement of vertices" src="../assets/mobius_strip/verts_all.png" alt="Final placement of all vertices in a mobius strip" class="img-center">
</a>
<figcaption>All of the vertices after completing the loop</figcaption>
</figure>



## Python Code


We will be using Blender's [Mathutils](https://docs.blender.org/api/current/mathutils.html) module - specifically the [Vector](https://docs.blender.org/api/current/mathutils.html#mathutils.Vector) and [Matrix](https://docs.blender.org/api/current/mathutils.html#mathutils.Matrix) types.  Vector will be used to store 3d coordinates and Matrix will be used to rotate the coordinates.

Note: just like above we will be using the y axis as our minor axis, and z as our major axis.

### Imports

Let's import some math libraries and Blender's Python utilities:

```python
import bpy
from math import *
from mathutils import Vector, Matrix
```

### Helpers

Let's define an `apply` function to multiply a 3d coordinate (vector) with a matrix in order to rotate it:

```python
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
```

We'll talk more about matrices later.

### Variables

We'll create a function with some user-defined variables:

```python
def mobius(major_radius: float = 1, minor_radius: float = 0.15, thick: float = 0.1, resolution: int = 108):
    '''
    major_radius - how large the strip will be
    minor_radius - defines how tall the strip will be (surface width)
    thick        - distance between front and back sides
    resolution   - number of loop iterations to perform
    '''
```

Initalize an empty list to hold our vertices and eventually faces:

```python
verts = []
faces = []
```

And finally create a variable to later be used to move the vertices away from the center (step 2 from earlier):

```python
dx = Vector([major_radius, 0, 0])
```

When added to another vector this will move the vertices `major_radius` units away from the center, which will be applied before rotating around the major axis.  We store the distance in the x coordinate to move vertices horizontally before rotating around the z axis.



### Adding vertices

Let's define our main loop:

```python
for i in range(resolution):
    # the angle to rotate around the minor axis (covers a 180° rotation)
    phi = pi * i / resolution
    
    # the angle to rotate around the major axis (covers a 360° rotation)
    theta = phi * 2
    
    # how many vertices do we have in our list
    idx = len(verts)
```

In the loop body we define two angles, represented in [Radians](https://en.wikipedia.org/wiki/Radian).  The angles will be gradually increased as `i` is incremented.

`phi` represents the angle to rotate around the minor axis (step 2 from earlier).  It will end up covering a 180&deg; rotation, which means it will only be rotated half way.  This is how we rotate the surface of the mobius strip.  The vertices of the last loop iteration will rotated 180&deg; so the top of those vertices will connect to the bottom of the vertices from the first loop iteration and vice versa.

`theta` represents the angle to rotate around the major axis (step 3 from earlier).  It will end up covering a 360&deg; rotation, which means it will be rotated all the way around.  This is how we get an overall circular shape.

`idx` is our current position in the list of vertices.  We will use this later to create faces between the vertices.

#### Initial vertices

In the body of the loop we'll create our initial points:

```python
p0 = Vector(( -thick/2, 0,  minor_radius ))
p1 = Vector((  thick/2, 0,  minor_radius ))
p2 = Vector((  thick/2, 0, -minor_radius ))
p3 = Vector(( -thick/2, 0, -minor_radius ))
```

Since the four vertices will initially be a rectangle be centered around `(0, 0)`, we can just specify the coordinates we want.  The thickness is divided by 2 because `thick` defines the total thickness, not the distance from the center (although that detail is less important since we could have just defined `thick = 0.05` instead of using `0.1`).

#### Defining Rotation Matrices

In order to create the mesh we'll need to use a little math.  If you're not familiar with rotation matrices that's *ok*, the most important thing to know is that we can multiply a vector (which stores the `(x,y,z` coordinates) by a matrix in order to rotate the coordinates.  For more detailed information on how this works see [Wikipedia - Rotation matrix](https://en.wikipedia.org/wiki/Rotation_matrix) or [Stack Exchange - Understanding rotation matrices](https://math.stackexchange.com/questions/363652/understanding-rotation-matrices).

Here we create a couple rotation matrices to rotate our vertices around the major and minor axes:

```python
# Rotates along major radius
# angle=theta, size=3, axis=[0, 0, 1]
rot_theta = Matrix.Rotation(theta, 3, [0, 0, 1])

# Rotates along minor radius
# angle=phi, size=3, axis=[0, 1, 0]
rot_phi = Matrix.Rotation(phi, 3, [0, 1, 0])
```

`rot_theta` uses `[0, 0, 1]` to specify a rotation around the z axis while `rot_phi` uses `[0, 1, 0]` to specify a rotation around the y axis.  The size is set to 3 because we want a 3-dimensional matrix.

#### Transforms

We will need to perform three operations on the vertices:

1. Rotate around the minor axis

    ```python
    p0_rotated = apply(rot_phi, p0)
    p1_rotated = apply(rot_phi, p1)
    p2_rotated = apply(rot_phi, p2)
    p3_rotated = apply(rot_phi, p3)
    ```
    
    We are using the `apply()` function from earlier to multiply each row of the rotation matrix by the 3d coordinates in the vector:

2. Move the vertices away from the center (horizontally)

    ```python
    p0_moved = p0_rotated + dx
    p1_moved = p1_rotated + dx
    p2_moved = p2_rotated + dx
    p3_moved = p3_rotated + dx
    ```
    
3. Rotate around the major axis to get our final vertices

    ```python
    v0 =  apply(rot_theta, p0_moved)
    v1 =  apply(rot_theta, p1_moved)
    v2 =  apply(rot_theta, p2_moved)
    v3 =  apply(rot_theta, p3_moved)
    ```

Then we will add those vertices to our collection with:

```python
verts.extend([v0, v1, v2, v3])
```

### Faces

Faces are added by connecting multiple vertices.  The vertices are referenced by their position in the `verts` list.

Here we find which vertices to connect to the vertices that we just added to our list:

```python
# define the index of where the next vertices will begin
next_verts = idx + 4

# Check if we are not at the last loop iteration
if i+1 < resolution:
    # Find positions of vertices that will be added in the next loop iteration
    n0 = next_verts + 0
    n1 = next_verts + 1
    n2 = next_verts + 2
    n3 = next_verts + 3
else:
    # Since we are at the last loop iteration, find positions of the
    # vertices from the very first loop iteration.
    #
    # Remember the top and bottoms get switched at the end because 
    # it will be rotated by 180°, so the ordering will look weird
    #
    n0 =  2
    n1 =  3
    n2 =  0
    n3 =  1
```

And finally let's create those faces in our list:

```python
faces.append([idx+0, idx+1, n1, n0])  # top face
faces.append([idx+1, idx+2, n2, n1])  # front side face
faces.append([idx+2, idx+3, n3, n2])  # bottom face
faces.append([idx+3, idx+0, n0, n3])  # back side face
```

### Creating the mesh

Once the loop is finished we can use the `verts` list to create our mesh.

```python
# Create a blank mesh
mesh = bpy.data.meshes.new("mobius_strip")

# Add the vertices to the mesh
mesh.from_pydata(verts, [], faces)

# Ensure the mesh is valid
if mesh.validate():
    print('Invalid mesh')
    return
    
# Create a new object
ob = bpy.data.objects.new("Mobius Strip Mesh", mesh)

# Add our object to the current collection
bpy.context.collection.objects.link(ob)
```

<figure>
    <figcaption class="title">Final mesh</figcaption>
    <a href="../assets/mobius_strip/verts_rendered.png">
        <img title="3d mobius strip" src="../assets/mobius_strip/verts_rendered.png" alt="3d mobius strip in Blender" class="img-center">
    </a>
    <figcaption>Final mesh</figcaption>
</figure>

## Final code

You can just paste the into new a Blender text document and press the Run icon (the triangle).  Very simple.

You can find the final code here:
[mobius_strip.py](../assets/mobius_strip/mobius_strip.py)


## Credits

This article is basically a much more verbose explanation and reimplementation of the code from [this Stack Exchange post](https://blender.stackexchange.com/questions/82480/how-to-make-a-mobius-strip/168967#168967)
