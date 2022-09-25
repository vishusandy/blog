from PIL import Image
from math import pow, sqrt, modf, floor, ceil

# create a new 400x400 image with a white background
img = Image.new('RGBA', (400, 400), (255, 255, 255, 255))

color = (255, 0, 0, 255)  # color to draw - red
c = (200, 200)  # center coordinates
r = 190  # radius

# forty-five degree point where octants change
ffd = round(r / sqrt(2))

x = 0
y = r

# iterate over octant 7
for x in range(ffd):
    # create a new image to blend img with
    img2 = Image.new('RGBA', (400, 400), (255, 255, 255, 0))

    # get the exact value of y
    y = sqrt(pow(r, 2) - pow(x, 2))
    # get the fractional portion of y
    (fract, _) = modf(sqrt(pow(r, 2) - pow(x, 2)))

    # get the two closest pixel coordinates for y
    y1 = ceil(y)
    y2 = floor(y)

    # split the full opacity (255) between the two pixels
    o1 = round(255 * fract)
    o2 = 255 - o1

    # draw both pixels in octant 7
    img2.putpixel((x + c[0], y1 + c[1]), (color[0], color[1], color[2], o1))
    img2.putpixel((x + c[0], y2 + c[1]), (color[0], color[1], color[2], o2))

    # blend into existing image
    img.alpha_composite(img2)

    x = x + 1
img.save("simple_antialiased_octant.png")
