from PIL import Image
import bpy

# Image Settings
height = 2048
width = 2048
extent = (-2,-2,2,2)
quality = 512

# color of the image
color = 0xffffff
invert = False

# function to convert mandelbrot to a color
def getColor(input, channel):
    if channel == 'R':
        bitshift = 16
    elif channel == 'B':
        bitshift = 8
    elif channel == 'G':
        bitshift = 0
    
    if invert:
        return (((color >> bitshift) & 0xff) & input)/0xff
        
    return 1 - (((color >> bitshift) & 0xff) & input)/0xff

# create a new image
mandelbrot_image = bpy.data.images.new("Mandelbrot", width=width, height=height)

# Generate the mandelbrot
mandelbrot = Image.effect_mandelbrot((width,height),extent,quality)

# Create empty list of pixels
pixelData = [None]*height*width

# Loop through the data
for y in range(height):
    for x in range(width):
        currentPixel = mandelbrot.getpixel((x,y))
        pixelData[(y*width)+x] = [getColor(currentPixel,'R'), 
            getColor(currentPixel,'G'), 
            getColor(currentPixel,'B'), 1.0]

# Unpack the data into a single list - this is not Pythonic
# for pixel in pixelData:
#     for channel in pixel:
pixelData = [channel for pixel in pixelData for channel in pixel]

mandelbrot_image.pixels = pixelData

        