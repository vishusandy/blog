from PIL import Image
from math import pow, sqrt

# create a new 400x400 image with a white background
img = Image.new('RGB', (400, 400), (255, 255, 255))

color = (255, 0, 0)  # color to draw - red
c = (200, 200)  # center coordinates
r = 190  # radius

x = -r  # initial x value (center of circle
# remember the circle is centered at (0,0)

while x < r:
    # calculate y for the current x value
    y = round(sqrt(pow(r, 2) - pow(x, 2)))

    # draw a pixel at the (x, y) coordinates
    #   remember to add center since the circle is centered at (0,0)
    img.putpixel((x + c[0], y + c[1]), color)

    # increment x
    x = x + 1
img.save("naive_circle_attempt.png")
