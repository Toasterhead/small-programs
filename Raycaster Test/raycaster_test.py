import pygame, sys, math
from pygame.locals import *

print("A simple psuedo-3D rendering engine. Press TAB to toggle between first-person and top-down view.\n")

RESOLUTION      = (256, 240)
DIMENSIONS_MAP  = (12, 12)
DIMENSIONS_TILE = (100, 100)

COLOR_BLACK     = (0,       0,      0)
COLOR_WHITE     = (255,     255,    255)
COLOR_RED       = (255,     0,      0)
COLOR_GREEN     = (0,       255,    0)
COLOR_BLUE      = (0,       0,      255)
COLOR_YELLOW    = (255,     255,    0)

QI      = 0
QII     = 1
QIII    = 2
QIV     = 3

X       = 0
Y       = 1
THETA   = 2

MAZE = (
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1),
    (1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))

IMAGE_WALL_RED      = pygame.Surface((1, RESOLUTION[Y]))
IMAGE_WALL_GREEN    = pygame.Surface((1, RESOLUTION[Y]))
IMAGE_WALL_BLUE     = pygame.Surface((1, RESOLUTION[Y]))
IMAGE_WALL_YELLOW   = pygame.Surface((1, RESOLUTION[Y]))
IMAGE_WALL_RED.fill(    COLOR_RED)
IMAGE_WALL_GREEN.fill(  COLOR_GREEN)
IMAGE_WALL_BLUE.fill(   COLOR_BLUE)
IMAGE_WALL_YELLOW.fill( COLOR_YELLOW)

IMAGE_CLEAR = pygame.Surface((1, RESOLUTION[Y]))
IMAGE_CLEAR.set_alpha(0)

pygame.init()
pygame.display.init()
pygame.display.set_caption('3D Maze')
pygame.display.set_mode((RESOLUTION[X], RESOLUTION[Y]), pygame.SCALED)

def draw_screen(screen, background, wallStrips, sprites, camera, maze):

    halfScreenVertical = RESOLUTION[Y] / 2

    for i in range(RESOLUTION[X]):
        
        wallScale, wallColor = cast_ray(i, camera, maze)
        scaledImage = pygame.transform.scale(get_color_image(wallColor), (1, int(wallScale * RESOLUTION[Y])))
        if wallColor: scaledImage.fill(brightness_adjusted_color(wallScale, wallColor))
        wallStrips[i].image = scaledImage
        wallStrips[i].rect.y = halfScreenVertical - (scaledImage.get_height() / 2)

    pygame.display.update(sprites.draw(screen, background))

def draw_overhead_map(screen, camera, mazeGrid):

    tileSize = (RESOLUTION[X] / DIMENSIONS_MAP[X], RESOLUTION[Y] / DIMENSIONS_MAP[Y])
    tile = pygame.Surface((tileSize[X], tileSize[Y]))
    tile.fill(COLOR_BLUE)
    
    background = pygame.Surface(RESOLUTION)
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    position = (
        (camera[X] / float(DIMENSIONS_MAP[X] * DIMENSIONS_TILE[Y])) * RESOLUTION[X],
        (camera[Y] / float(DIMENSIONS_MAP[Y] * DIMENSIONS_TILE[Y])) * RESOLUTION[Y])
    arrow = pygame.Surface((20, 20))
    pygame.draw.polygon(
        arrow,
        COLOR_YELLOW,
        [((arrow.get_width() / 2) + 5, (arrow.get_height() / 2)),
         ((arrow.get_width() / 2) - 5, (arrow.get_height() / 2) + 5),
         ((arrow.get_width() / 2) - 5, (arrow.get_height() / 2) - 5)])
    
    for i in range(len(mazeGrid)):
        for j in range(len(mazeGrid[i])):
            if mazeGrid[i][j] == 1:
                screen.blit(tile, (i * tileSize[X], j * tileSize[Y]))

    screen.blit(
        pygame.transform.rotate(arrow, -(camera[THETA] * (180.0 / math.pi))),
        (position[X] - (arrow.get_width()   / 2),
         position[Y] - (arrow.get_height()  / 2)))

    pygame.display.update()

def get_color_image(wallColor):

    if not wallColor: return IMAGE_CLEAR

    if      wallColor == COLOR_RED:     return IMAGE_WALL_RED
    elif    wallColor == COLOR_GREEN:   return IMAGE_WALL_GREEN
    elif    wallColor == COLOR_BLUE:    return IMAGE_WALL_BLUE
    elif    wallColor == COLOR_YELLOW:  return IMAGE_WALL_YELLOW
    else:                               return IMAGE_CLEAR

def brightness_adjusted_color(wallScale, wallColor):

    MULTIPLIER      = 3
    MAX_BRIGHTNESS  = 255

    red     = wallScale * wallColor[0] * MULTIPLIER
    green   = wallScale * wallColor[1] * MULTIPLIER
    blue    = wallScale * wallColor[2] * MULTIPLIER

    if red      > MAX_BRIGHTNESS: red   = MAX_BRIGHTNESS
    if blue     > MAX_BRIGHTNESS: blue  = MAX_BRIGHTNESS
    if green    > MAX_BRIGHTNESS: green = MAX_BRIGHTNESS

    return (red, green, blue)

def determine_quadrant(theta):

    theta = reduce_angle(theta)

    if      theta >= 0.0            and theta < math.pi * 0.5:   return QI
    elif    theta >= math.pi * 0.5  and theta < math.pi:         return QII
    elif    theta >= math.pi        and theta < math.pi * 1.5:  return QIII

    return QIV

def reduce_angle(theta):

    MULTIPLIER = 10000
    ROTATION = (2 * math.pi)

    return (int(theta * MULTIPLIER) % int(ROTATION * MULTIPLIER)) / float(MULTIPLIER)

def forward_vector(theta):

    MAGNITUDE = 5

    return (math.cos(theta) * MAGNITUDE, math.sin(theta) * MAGNITUDE)

def backward_vector(theta):

    forwardVector = forward_vector(theta)
    
    return (-forwardVector[X], -forwardVector[Y])

def rotate_clockwise(camera): camera[THETA] += 0.025

def rotate_counter_clockwise(camera): camera[THETA] -= 0.025

def move_forward(camera):
    
    forward = forward_vector(camera[THETA])
    camera[X] += forward[X]
    camera[Y] += forward[Y]

def move_backward(camera):

    backward = backward_vector(camera[THETA])
    camera[X] += backward[X]
    camera[Y] += backward[Y]

def collides_with_rect(point, rect):

    return \
           point[X] >= rect.left    and point[X] < rect.right and \
           point[Y] >= rect.top     and point[Y] < rect.bottom

def cast_ray(rayIndex, camera, maze):

    VIEW_SPAN = 0.1667 * (2 * math.pi)

    cameraPosition = (camera[X], camera[Y])
    rayPosition = [camera[X], camera[Y]]
    rayAngle = camera[THETA] - (0.5 * VIEW_SPAN) + (rayIndex * (VIEW_SPAN / RESOLUTION[X]))
    rayVector = (math.cos(rayAngle), math.sin(rayAngle))
    quadrant = determine_quadrant(rayAngle)

    rayPosition = [rayPosition[X] + rayVector[X], rayPosition[Y] + rayVector[Y]]
    
    largestScale = 0.0
    wallColor = None

    if quadrant == QI:

        for rect in maze:
            
            if rect.right >= cameraPosition[X] and rect.bottom >= cameraPosition[Y]:
                
                xIntercept, yIntercept, slope = linear_values(rayPosition, cameraPosition, rect.topleft)

                if not slope: return 0.0, None      #For detecting vertical rays. Implement later.
                if not xIntercept: return 0.0, None #For detecting horizontal rays. Implement later.

                if yIntercept >= 0 and yIntercept < rect.height:
                    
                    scale = wall_scale(camera, rayVector, rayAngle, (rect.left, rect.top + yIntercept))
                    if scale > largestScale:
                        largestScale = scale
                        wallColor = COLOR_RED
                        
                elif xIntercept >= 0 and xIntercept < rect.width:
                    
                    scale = wall_scale(camera, rayVector, rayAngle, (rect.left + xIntercept, rect.top))
                    if scale > largestScale:
                        largestScale = scale
                        wallColor = COLOR_YELLOW

    elif quadrant == QII:

        for rect in maze:

            if rect.left < cameraPosition[X] and rect.bottom >= cameraPosition[Y]:

                xIntercept, yIntercept, slope = linear_values(rayPosition, cameraPosition, rect.topright)

                if not slope: return 0.0, None      #For detecting vertical rays. Implement later.
                if not xIntercept: return 0.0, None #For detecting horizontal rays. Implement later.

                if yIntercept >= 0 and yIntercept < rect.height:
                   
                    scale = wall_scale(camera, rayVector, rayAngle, (rect.right, rect.top + yIntercept))
                    if scale > largestScale:
                        largestScale = scale
                        wallColor = COLOR_BLUE
                        
                elif xIntercept < 0 and xIntercept >= -rect.width:
                    
                    scale = wall_scale(camera, rayVector, rayAngle, (rect.right + xIntercept, rect.top))
                    if scale > largestScale:
                        largestScale = scale
                        wallColor = COLOR_YELLOW

    elif quadrant == QIII:

        for rect in maze:

            if rect.left < cameraPosition[X] and rect.top < cameraPosition[Y]:

                xIntercept, yIntercept, slope = linear_values(rayPosition, cameraPosition, rect.bottomright)

                if not slope: return 0.0, None      #For detecting vertical rays. Implement later.
                if not xIntercept: return 0.0, None #For detecting horizontal rays. Implement later.

                if yIntercept < 0 and yIntercept >= -rect.height:
                   
                    scale = wall_scale(camera, rayVector, rayAngle, (rect.right, rect.bottom + yIntercept))
                    if scale > largestScale:
                        largestScale = scale
                        wallColor = COLOR_BLUE
                        
                elif xIntercept < 0 and xIntercept >= -rect.width:
                    
                    scale = wall_scale(camera, rayVector, rayAngle, (rect.right + xIntercept, rect.bottom))
                    if scale > largestScale:
                        largestScale = scale
                        wallColor = COLOR_GREEN

    elif quadrant == QIV:

        for rect in maze:

            if rect.right >= cameraPosition[X] and rect.top < cameraPosition[Y]:

                xIntercept, yIntercept, slope = linear_values(rayPosition, cameraPosition, rect.bottomleft)

                if not slope: return 0.0, None      #For detecting vertical rays. Implement later.
                if not xIntercept: return 0.0, None #For detecting horizontal rays. Implement later.

                if yIntercept < 0 and yIntercept >= -rect.height:
                   
                    scale = wall_scale(camera, rayVector, rayAngle, (rect.left, rect.bottom + yIntercept))
                    if scale > largestScale:
                        largestScale = scale
                        wallColor = COLOR_RED
                        
                elif xIntercept >= 0 and xIntercept <= rect.width:
                    
                    scale = wall_scale(camera, rayVector, rayAngle, (rect.left + xIntercept, rect.bottom))
                    if scale > largestScale:
                        largestScale = scale
                        wallColor = COLOR_GREEN

    return largestScale, wallColor

def f(x, m, b): return (m * x) + b

def f_inv(y, m, b): return (y - b) / m

def linear_values(pointOne, pointTwo, tileOrigin):

    #Conditional for vertical lines.
    if pointTwo[X] - pointOne[X] == 0: return 0, None, None

    relativeX = pointOne[X] - tileOrigin[X]
    relativeY = pointOne[Y] - tileOrigin[Y]
    
    m = (pointTwo[Y] - pointOne[Y]) / (pointTwo[X] - pointOne[X])
    b = relativeY - (m * relativeX)

    if m == 0: return m, 0, None

    slope       =   m
    yIntercept  =   b
    xIntercept  = -(b / m)

    return xIntercept, yIntercept, m

def dot_product_2d(vectorLeft, vectorRight):

    return (vectorLeft[X] * vectorRight[X]) + (vectorLeft[Y] * vectorRight[Y])

def wall_scale(camera, rayVector, rayAngle, intersection): #Delete unnecessary parameters after "fish-eye" problem is fixed.

    SCALE_RATE = 0.996

    distance = get_distance((camera[X], camera[Y]), intersection)

    #Solution 1: use dot-product projection.
    cameraVector = (math.cos(camera[THETA]), math.sin(camera[THETA]))
    rayVectorScaled = (rayVector[X] * distance, rayVector[Y] * distance)
    projectionLength = dot_product_2d(cameraVector, rayVectorScaled)

    #Solution 2: multiply distance by cosine of angle to camera?
    adjustedDistance = distance * math.cos(rayAngle - camera[THETA])

    #return pow(SCALE_RATE, projectedLength)
    
    return RESOLUTION[Y] / (3 * projectionLength) #Linear scaling appears more natural.
    
def get_distance(positionOne, positionTwo):

    a = positionTwo[X] - positionOne[X]
    b = positionTwo[Y] - positionOne[Y]

    return math.sqrt((a * a) + (b * b))

screen = pygame.display.get_surface()
camera = [
    DIMENSIONS_MAP[X] * DIMENSIONS_TILE[X] * 0.5,
    DIMENSIONS_MAP[Y] * DIMENSIONS_TILE[Y] * 0.5,
    math.pi * 0.5]
wallStrips = []
sprites = pygame.sprite.LayeredDirty()
maze = []
clock = pygame.time.Clock()
background = pygame.Surface(RESOLUTION)

ceilingAndFloor = pygame.Surface((RESOLUTION[X], RESOLUTION[Y] / 2))
ceilingAndFloor.fill(COLOR_BLACK)
background.blit(ceilingAndFloor, (0, 0))
ceilingAndFloor.fill((127, 127, 127))
background.blit(ceilingAndFloor, (0, RESOLUTION[Y] / 2))

for i in range(RESOLUTION[X]):
    wallStrips.append(pygame.sprite.DirtySprite(sprites))
    wallStrips[i].dirty = 2
    wallStrips[i].rect = pygame.Rect((i, 0), (1, 100))
    wallStrips[i].image = IMAGE_WALL_RED

for i in range(len(MAZE[X])):
    for j in range(len(MAZE[Y])):
        if MAZE[i][j] == 1:
            maze.append(pygame.Rect(
                (i * DIMENSIONS_TILE[X],
                 j * DIMENSIONS_TILE[Y]),
                (DIMENSIONS_TILE[X],
                 DIMENSIONS_TILE[Y])))

terminate = False
viewMap = True

while not terminate:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                screen.blit(background, (0, 0))
                viewMap = not viewMap
            if event.key == pygame.K_ESCAPE:
                terminate = True
                break

    if      pygame.key.get_pressed()[pygame.K_LEFT]:    rotate_counter_clockwise(camera)
    elif    pygame.key.get_pressed()[pygame.K_RIGHT]:   rotate_clockwise(camera)

    if      pygame.key.get_pressed()[pygame.K_UP]:      move_forward(camera)
    elif    pygame.key.get_pressed()[pygame.K_DOWN]:    move_backward(camera)
       
    if  viewMap:    draw_overhead_map(screen, camera, MAZE)
    else:           draw_screen(screen, background, wallStrips, sprites, camera, maze)

    clock.tick(60)

input("Program closed. Press any key to continue...")
