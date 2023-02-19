import pygame, sys
from pygame.locals import *

print("Quick Auto-translucency Tool by Leonard Young\n")

pygame.init()
pygame.display.init()
pygame.display.set_caption('Quick Translucancy Tool')
pygame.display.set_mode((640, 480))

def load_image(directory):
    """Loads an image from the given directory."""

    try:
        img = pygame.image.load('input/' + directory).convert_alpha()
    except:
        print("Error - Unable to load the specified image. Exiting program...")
        sys.exit()

    return img

def display_image(img):
    """Displays an image after resizing the program window."""

    pygame.display.set_mode(img.get_size())
    screen.blit(img, (0, 0))
    pygame.display.flip()

screen = pygame.display.get_surface()

sourceImage = load_image(input("Enter the source image file name: "))
display_image(sourceImage)

finalImage = input("Enter a name for the output image (without extension): ")

print("Enter red/green/blue values to target...\n")
targetRed   = int(input("R: "))
targetGreen = int(input("G: "))
targetBlue  = int(input("B: "))
translucency = float(input("Translucency (0.0 >= x >= 1.0): "))

SHADE_RANGE = 256

RED     = 0
GREEN   = 1
BLUE    = 2

assert targetRed   >= 0 and targetRed      < SHADE_RANGE, "Error - R-value is out of range."
assert targetGreen >= 0 and targetGreen    < SHADE_RANGE, "Error - G-value is out of range."
assert targetBlue  >= 0 and targetBlue     < SHADE_RANGE, "Error - B-value is out or range."

pixels = pygame.PixelArray(sourceImage)

for i in range(sourceImage.get_width()):

    for j in range(sourceImage.get_height()):

        color = sourceImage.unmap_rgb(pixels[i, j])

        if (color[RED] == targetRed and color[GREEN] == targetGreen and color[BLUE] == targetBlue):
            pixels[i, j] = (color[RED], color[GREEN], color[BLUE], translucency * SHADE_RANGE)

del pixels
pygame.image.save(sourceImage, 'output/' + finalImage + '.png')

print("Done. Saved to output folder.")
