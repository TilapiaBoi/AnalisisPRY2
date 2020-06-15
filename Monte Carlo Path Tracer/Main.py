import sys
import threading
import random
import math
from PIL import Image
from Line import *
from Light import *
from Ray import *

def renderLight():
    while True:

        # loop through all the pixels
        for x in range (500):
            for y in range (500):

                # pixel color black
                color = 0

                # calculate direct lighting
                for source in lightSources:

                    # if the pixel is a light source skip
                    if x == source.pos[0] and y == source.pos[1]:
                        continue

                    # create a ray from pixel to light source
                    ray = Ray(x, y, 0)
                    ray.setDir(source.pos[0], source.pos[1])

                    # calculate distance from pixel to light source
                    sourceDist = math.sqrt(((x-source.pos[0])**2)+((y-source.pos[1])**2))

                    # check if ray collisions
                    noCollision = True
                    for boundary in boundaries:

                        # obtain an array [collisionX, collisionY, distance] if collision
                        pointWithDist = ray.cast(boundary)

                        # if collision is before reaching the source keep pixel black
                        if pointWithDist is not None and pointWithDist[2] < sourceDist:
                            noCollision = False
                            break

                    if noCollision:

                        # calculate light intensity
                        intensity = (1-(sourceDist/500))**2

                        # obtain reference pixel value
                        refValue = (referencePixels[y][x])[:3]

                        # combine color, light source and light color
                        refValue = refValue * intensity * light

                        # add all light sources
                        color += refValue

                # calculate indirect lighting with monte carlo
                for i in range (NUM_SAMPLES):

                    # get random direction
                    angle = random.uniform(0, 360)

                    # create ray from pixel to random direction
                    ray = Ray(x, y, angle)

                    # calculate pixel color by tracing ray path recursively
                    color += tracePath(ray, 0)

                # average pixel value and assign
                drawingPixels[x][y] = color // len(lightSources) + NUM_SAMPLES

def tracePath(ray, depth):
    if depth >= MAX_DEPTH:
        return 0
    # CHECK IF DIR HITS A LIGHT SOURCE
    lightSource = random.randint(0,1)
    if lightSource:
        if depth == 0:
            return 0
        #ADD DISTANCE TO LIGHT SOURCE TO DISTANCE
        intensity = (1 - (distance / 500)) ** 2
        return values * intensity * light
    #CHECK IF DIR HITS A SEGMENT
    hitSegment = random.randint(0, 1)
    if hitSegment:
        #IF IT DOES, CREATE A NEW DIRECTION AND MODIFY VALUES AND DISTANCE
        return tracePath (depth+1, point, dir, values, distance)
    return 0

# globals
WIDTH = 500
HEIGHT = 500
RUNNING = True
NUM_SAMPLES = 0
MAX_DEPTH = 0

# pygame setup
py.init()
WINDOW = py.display.set_mode([WIDTH, HEIGHT])
py.display.set_caption("2D Path Tracer")
clock = py.time.Clock()

# random setup
random.seed()

# black image setup
blankImg = Image.new("RGB", (500, 500), (0, 0, 0))
drawingPixels = np.array(blankImg)

# reference image setup
refImage = Image.open("room.png")
referencePixels = np.array(refImage)

# light positions
lightSources = [LightSource(195, 200, "color"), LightSource(294, 200, "color")]

# light color
light = np.array([1, 1, 0.75])

# boundary positions
boundaries = [
            Line(0, 0, WIDTH, 0, False),
            Line(0, 0, 0, HEIGHT, False),
            Line(0, HEIGHT, WIDTH, HEIGHT, False),
            Line(WIDTH, 0, WIDTH, HEIGHT, False),
            Line(180, 135, 215, 135, False),
            Line(285, 135, 320, 135, False),
            Line(320, 135, 320, 280, False),
            Line(320, 320, 320, 355, False),
            Line(320, 355, 215, 355, False),
            Line(180, 390, 180, 286, False),
            Line(180, 286, 140, 286, False),
            Line(320, 320, 360, 320, False),
            Line(180, 250, 180, 135, False),
            ]

# temporary utility functions
def drawBoundaries():
    for line in boundaries:
        line.draw(WINDOW)

# thread setup
tracerThread = threading.Thread(target = renderLight, daemon = True)
tracerThread.start()

# main loop
while RUNNING:

    for event in py.event.get():

        if event.type == py.QUIT:
            sys.exit()

    # set screen to white
    WINDOW.fill((255, 255, 255))

    # convert drawing image to surface and set to screen
    surface = py.surfarray.make_surface(drawingPixels)
    WINDOW.blit(surface, (0, 0))

    drawBoundaries()

    # update pygame
    py.display.flip()
    clock.tick(60)



