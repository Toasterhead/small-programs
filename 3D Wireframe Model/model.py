import pygame, sys, types, math, point, vector, matrix, conversion, transformation, graph
from pygame.locals  import *

print("Testing 3D model...")

RESOLUTION  = (640, 480)
WHITE       = (255, 255, 255)
GREY        = (50, 50, 50)
BLACK       = (0, 0, 0) 
THICKNESS   = 5
GRID_SIZE   = 10
VANISH_RATE = 0.999
X = 0
Y = 1
Z = 2

pygame.init()
pygame.display.init()
pygame.display.set_mode(RESOLUTION)

screen  = pygame.display.get_surface()
model   = graph.Graph()
perspectiveOn = False

grid = pygame.Surface(RESOLUTION)
GRID_LINES_X = int(RESOLUTION[X] / GRID_SIZE)
GRID_LINES_Y = int(RESOLUTION[Y] / GRID_SIZE)
for i in range(GRID_LINES_X):
    color = GREY
    if i == GRID_LINES_X / 2:   color = (GREY[0] + 50, GREY[1] + 50, GREY[2] + 50)
    elif i % 4 == 0:            color = (GREY[0] + 25, GREY[1] + 25, GREY[2] + 25)
    pygame.draw.line(grid, color, (i * GRID_SIZE, 0), (i * GRID_SIZE, RESOLUTION[Y]))
for i in range(GRID_LINES_Y):
    color = GREY
    if i == GRID_LINES_Y / 2:   color = (GREY[0] + 50, GREY[1] + 50, GREY[2] + 50)
    elif i % 4 == 0:            color = (GREY[0] + 25, GREY[1] + 25, GREY[2] + 25)
    pygame.draw.line(grid, color, (0, i * GRID_SIZE), (RESOLUTION[X], i * GRID_SIZE))

def rotate(theta, handler):

    assert type(theta)      is float
    assert type(handler)    is types.FunctionType
    
    global model
    
    for i in range(model.Size):
        thePoint    = model.get_vertex(i).get_data()
        position    = transformation.position_matrix(
            thePoint.X,
            thePoint.Y,
            thePoint.Z)
        rotation    = handler(theta)
        delta       = rotation.multiply(position)
        deltaData   = delta.get_data()
        model.get_vertex(i).Data = point.Point3D(
            deltaData[X][0],
            deltaData[Y][0],
            deltaData[Z][0])

def add_rectangle(left, top, right, bottom, z):

    model.add_vertex(graph.Vertex(point.Point3D(left,   top,    z)))
    model.add_vertex(graph.Vertex(point.Point3D(right,  top,    z)))
    model.add_vertex(graph.Vertex(point.Point3D(right,  bottom, z)))
    model.add_vertex(graph.Vertex(point.Point3D(left,   bottom, z)))
    model.add_edge(model.Size - 4, model.Size - 3)
    model.add_edge(model.Size - 3, model.Size - 2)
    model.add_edge(model.Size - 2, model.Size - 1)
    model.add_edge(model.Size - 1, model.Size - 4)

def add_disc(centerX, centerY, centerZ, thePitch, theYaw, theRoll, radius, resolution):

    assert type(centerX)    is float
    assert type(centerY)    is float
    assert type(centerZ)    is float
    assert type(thePitch)   is float
    assert type(theYaw)     is float
    assert type(theRoll)    is float
    assert type(radius)     is float
    assert type(resolution) is int

    segment             = (2.0 * math.pi) / resolution
    initialModelSize    = model.Size
            
    for i in range(resolution):
                
        x = radius * math.cos(i * segment) + centerX
        y = radius * math.sin(i * segment) + centerY
        z = centerZ
                
        position    = transformation.position_matrix(x, y, z)
        transPitch  = transformation.pitch(thePitch)
        transYaw    = transformation.yaw(theYaw)
        transRoll   = transformation.roll(theRoll)
        delta       = transPitch.multiply(transYaw).multiply(transRoll).multiply(position)
        deltaData   = delta.get_data()
        deltaPoint  = point.Point3D(deltaData[X][0], deltaData[Y][0], deltaData[Z][0])

        model.add_vertex(graph.Vertex(deltaPoint))
        if i > 0:
            model.add_edge(initialModelSize + i, initialModelSize + (i - 1))
        if i == resolution - 1:
            model.add_edge(initialModelSize, initialModelSize + (resolution - 1))

def render_model():

    screen.blit(grid, (0, 0))

    matrix = model.AdjacencyMatrix

    for i in range(model.Size):        
        for j in range(i, model.Size):        
            if matrix[i][j] == True:
                
                start   = model.get_vertex(i).get_data()
                end     = model.get_vertex(j).get_data()

                if perspectiveOn:
                    
                    perspectiveStart    = (start.X  * pow(VANISH_RATE, -start.Z),   start.Y * pow(VANISH_RATE, -start.Z))
                    perspectiveEnd      = (end.X    * pow(VANISH_RATE, -end.Z),     end.Y   * pow(VANISH_RATE, -end.Z))

                    axisStart   = ((RESOLUTION[X] / 2) + perspectiveStart[X],   (RESOLUTION[Y] / 2) - perspectiveStart[Y])
                    axisEnd     = ((RESOLUTION[X] / 2) + perspectiveEnd[X],     (RESOLUTION[Y] / 2) - perspectiveEnd[Y])

                else :

                    axisStart   = ((RESOLUTION[X] / 2) + start.X,   (RESOLUTION[Y] / 2) - start.Y)
                    axisEnd     = ((RESOLUTION[X] / 2) + end.X,     (RESOLUTION[Y] / 2) - end.Y)

                pygame.draw.line(
                    screen,
                    WHITE,
                    axisStart,
                    axisEnd,
                    THICKNESS)

    for event in pygame.event.get(): pass

    pygame.display.update()

render_model()

while True:
    
    selection = input("\n"                                  +
                      "1) Add vertex.\n"                    +
                      "2) Delete vertex.\n"                 +
                      "3) View all vertices.\n"             +
                      "4) Connect two vertices.\n"          +
                      "5) Translate model.\n"               +
                      "6) Rotate about X-axis. (Pitch)\n"   +
                      "7) Rotate about Y-axis. (Yaw)\n"     +
                      "8) Rotate about Z-axis. (Roll)\n"    +
                      "9) [N/A]\n\n"                        +
                      "0) More options.\n\n"                +
                      "Make a selection: ")

    if selection == '1':
        
        print("Enter vertex coordinates...")
        try:
            x = float(input("x: "))
            y = float(input("y: "))
            z = float(input("z: "))
            model.add_vertex(graph.Vertex(point.Point3D(x, y, z)))
        except ValueError: print("Error - Number expected in input field.")
        
    elif selection == '2':

        try: model.delete_vertex(int(input("Enter vertex ID: ")))
        except AssertionError: print("Error - Invalid input.")
        render_model()
        
    elif selection == '3':
        
        for i in range(model.Size):
            print(str(i) + ": " + str(model.get_vertex(i).get_data().get_data()))
            
    elif selection == '4':

        try: 
            first   = int(input("Enter the ID for the first vertex: "))
            second  = int(input("Enter the ID for the second: "))
            model.add_edge(first, second)
        except AssertionError:  print("Error - At least one of the ID's entered is invalid.")
        except ValueError:      print("Error - Number expected in input field.")
        render_model()
        
    elif selection == '5':

        print("Enter shift values...")
        try:
            
            dx = int(input("dx: "))
            dy = int(input("dy: "))
            dz = int(input("dz: "))

            for i in range(model.Size):
                thePoint    = model.get_vertex(i).get_data()
                position    = transformation.position_matrix(
                    thePoint.X,
                    thePoint.Y,
                    thePoint.Z)
                translation = transformation.translate(dx, dy, dz)
                delta       = translation.multiply(position)
                deltaData   = delta.get_data()
                model.get_vertex(i).Data = point.Point3D(
                    deltaData[X][0],
                    deltaData[Y][0],
                    deltaData[Z][0])
                        
            render_model()
            
        except ValueError: print("Error - Number expected in input field.")
        
    elif selection == '6':

        try:
            theta = float(input("Enter rotation in degrees: "))
            rotate(theta, transformation.pitch)
            render_model()
        except ValueError: print("Error - Number expected in input field.")
        
    elif selection == '7':

        try:
            theta = float(input("Enter rotation in degrees: "))
            rotate(theta, transformation.yaw)
            render_model()
        except ValueError: print("Error - Number expected in input field.")
        
    elif selection == '8':

        try:
            theta = float(input("Enter rotation in degrees: "))
            rotate(theta, transformation.roll)
            render_model()
        except ValueError: print("Error - Number expected in input field.")
        
    elif selection == '9':
        pass
    elif selection == '0':
        
        print("\n"                                                          +
            "Type 'disc', 'cylinder', 'sphere', 'rectangle', or 'box' to "  +
            "quickly build a shape. Here are a few other commands...\n\n"   +
            "perspective: toggle perspective on and off.\n"                 +
            "clear:       delete all vertices.\n"                           +
            "quit:        exit the program.")
        
    elif selection == 'disc':

        try:            
            centerX     = float(input("Enter the center X-value: "))
            centerY     = float(input("Enter the center Y-value: "))
            centerZ     = float(input("Enter the center Z-value: "))
            thePitch    = float(input("Enter the rotation about the X-axis: "))
            theYaw      = float(input("Enter the rotation about the Y-axis: "))
            theRoll     = float(input("Enter the rotation about the Z-axis: "))
            radius      = float(input("Enter the radius: "))
            resolution  = int(  input("Enter the curve resolution: "))
            add_disc(centerX, centerY, centerZ, thePitch, theYaw, theRoll, radius, resolution)
            render_model()
        except ValueError: print("Error - Number expected in input field.")

    elif selection == 'cylinder':

        try:            
            centerX     = float(input("Enter the center X-value: "))
            centerY     = float(input("Enter the center Y-value: "))
            centerZ     = float(input("Enter the center Z-value: "))
            thePitch    = float(input("Enter the rotation about the X-axis: "))
            theYaw      = float(input("Enter the rotation about the Y-axis: "))
            theRoll     = float(input("Enter the rotation about the Z-axis: "))
            radius      = float(input("Enter the radius: "))
            depth       = float(input("Enter the depth: "))
            resolution  = int(  input("Enter the curve resolution: "))
            add_disc(centerX, centerY, centerZ,         thePitch, theYaw, theRoll, radius, resolution)
            add_disc(centerX, centerY, centerZ - depth, thePitch, theYaw, theRoll, radius, resolution)
            for i in range(resolution):
                model.add_edge(model.Size - i - 1, model.Size - resolution - i - 1)
            render_model()
        except ValueError: print("Error - Number expected in input field.")

    elif selection == 'sphere':

        try:            
            centerX     = float(input("Enter the center X-value: "))
            centerY     = float(input("Enter the center Y-value: "))
            centerZ     = float(input("Enter the center Z-value: "))
            radius      = float(input("Enter the radius: "))
            resolution  = int(  input("Enter the curve resolution: "))
            for i in range(resolution):
                add_disc(
                    centerX,
                    centerY,
                    centerZ,
                    0.0,
                    i * (360.0 / resolution),
                    0.0,
                    radius,
                    resolution)
            render_model()
        except ValueError: print("Error - Number expected in input field.")

    elif selection == 'rectangle':

        try:           
            left    = float(input("Enter left value: "))
            top     = float(input("Enter top value: "))
            right   = float(input("Enter right value: "))
            bottom  = float(input("Enter bottom value: "))
            z       = float(input("Enter Z-value: "))
            add_rectangle(left, top, right, bottom, z)
        except ValueError: print("Error - Number expected in input field.")

        render_model()

    elif selection == 'box':

        try:           
            left    = float(input("Enter left value: "))
            top     = float(input("Enter top value: "))
            right   = float(input("Enter right value: "))
            bottom  = float(input("Enter bottom value: "))
            depth   = float(input("Enter the depth: "))
            z       = float(input("Enter Z-value: "))
            add_rectangle(left, top, right, bottom, z)
            add_rectangle(left, top, right, bottom, z - depth)
            model.add_edge(model.Size - 8, model.Size - 4)
            model.add_edge(model.Size - 7, model.Size - 3)
            model.add_edge(model.Size - 6, model.Size - 2)
            model.add_edge(model.Size - 5, model.Size - 1)
        except ValueError: print("Error - Number expected in input field.")

        render_model()

    elif selection == 'perspective':

        if perspectiveOn == True:   perspectiveOn = False
        else:                       perspectiveOn = True
        print("Perspective on? " + str(perspectiveOn))
        render_model()

    elif selection == 'clear':
        
        while model.Size > 0: model.delete_vertex(0)
        render_model()
            
    elif selection in ('exit', 'quit', 'q'): break
    
    else: print("Unable to recognize command.")
