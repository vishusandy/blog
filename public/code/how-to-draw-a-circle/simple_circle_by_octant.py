from PIL import Image
from math import pow, sqrt

# create a new 400x400 image with a white background
img = Image.new('RGB', (400, 400), (255, 255, 255))

color = (255, 0, 0)  # color to draw - red
c = (200, 200)  # center coordinates
r = 190  # radius

x = 0  # center of circle
y = r  # bottom of circle

# iterate over octant 7 and translate the coordinates for all 4 quadrants
while x < y:
    # draw octant 7: (x, y)
    img.putpixel((x + c[0], y + c[1]), color)
    # draw octant 2: (x, -y)
    img.putpixel((x + c[0], -y + c[1]), color)
    # draw octant 3: (-x, -y)
    img.putpixel((-x + c[0], -y + c[1]), color)
    # draw octant 6: (-x, y)
    img.putpixel((-x + c[0], y + c[1]), color)
    # draw octant 8: (y, x)
    img.putpixel((y + c[0], x + c[1]), color)
    # draw octant 1: (y, -x)
    img.putpixel((y + c[0], -x + c[1]), color)
    # # draw octant 4: (-y, -x)
    img.putpixel((-y + c[0], -x + c[1]), color)
    # # # draw octant 5: (-y, x)
    img.putpixel((-y + c[0], x + c[1]), color)

    x = x + 1
    y = round(sqrt(pow(r, 2) - pow(x, 2)))
img.save("simple_circle_by_octant.png")
