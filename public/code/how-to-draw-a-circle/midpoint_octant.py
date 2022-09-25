from PIL import Image
from math import pow

# create a new 400x400 image with a white background
img = Image.new('RGB', (400, 400), (255, 255, 255))

color = (255, 0, 0)  # color to draw - red
c = (200, 200)  # center coordinates
r = 150  # radius

x = 0
y = r
while x < y:
    img.putpixel((x + c[0], y + c[1]), color)

    # test whether fast+1 and slow-0.5 is inside or outside the circle
    p = pow(x + 1.0, 2) + pow(y - 0.5, 2) - pow(r, 2)
    if p <= 0:
        x = x+1  # inside the circle - only move in the fast direction
    else:
        # outside circle - move in both directions
        x = x+1
        y = y-1
img.save("midpoint_octant.png")
