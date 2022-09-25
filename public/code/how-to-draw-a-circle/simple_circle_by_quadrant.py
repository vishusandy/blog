from PIL import Image
from math import pow, sqrt

# create a new 400x400 image with a white background
img = Image.new('RGB', (400, 400), (255, 255, 255))

color = (255, 0, 0)  # color to draw - red
c = (200, 200)  # center coordinates
r = 190  # radius

x = 0
y = r

# iterate over octant 7 and translate the coordinates for all 4 quadrants
while x < y:
    y = round(sqrt(pow(r, 2) - pow(x, 2)))

    # draw octant 7: (x, y)
    img.putpixel((x + c[0], y + c[1]), color)
    # draw octant 2: (x, -y)
    img.putpixel((x + c[0], -y + c[1]), color)
    # draw octant 3: (-x, -y)
    img.putpixel((-x + c[0], -y + c[1]), color)
    # draw octant 6: (-x, y)
    img.putpixel((-x + c[0], y + c[1]), color)

    x = x + 1

# iteratve over octant 8 and translate the coordinates for all 4 quadrants
while y != 0:
    x = round(sqrt(pow(r, 2) - pow(y, 2)))

    # draw octant 8: (x, y)
    img.putpixel((x + c[0], y + c[1]), color)
    # draw octant 1: (x, -y)
    img.putpixel((x + c[0], -y + c[1]), color)
    # draw octant 4: (-x, -y)
    img.putpixel((-x + c[0], -y + c[1]), color)
    # # draw octant 5: (-x, y)
    img.putpixel((-x + c[0], y + c[1]), color)

    y = y - 1
img.save("simple_circle_by_quadrant.png")
