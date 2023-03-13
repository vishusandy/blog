from PIL import Image, ImageColor
from math import sqrt

# create a new 400x400 image with a white background
img = Image.new('RGBA', (400, 400), (255, 255, 255, 255))

color = (255, 0, 0, 255)  # color to draw - red
c = (200, 200)  # center coordinates
r = 190  # radius

x = 0
y = r
d = 3 - 2 * r  # radius error
ffd = round(r / sqrt(2))  # forty-five degree point where octants change

# iterate over octant 7
for x in range(ffd):
    img.putpixel((x + c[0], y + c[1]), color)
    x = x + 1
    if d <= 0:
        d += 4 * x + 6
    else:
        y = y - 1
        d += 4 * (x - y) + 10
img.save("bresenham_octant.png")
