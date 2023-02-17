# (c) 2020 Harlepengren
# http://harlepengren.com
#
# Licensed under Apache 2.0
# This software is provided AS IS WITH NO EXPRESS OR IMPLIED WARRANTY OF ANY KIND.

#import the modules
import bpy
import numpy as np
import math
import mathutils
 
# Create a variable to hold the camera object and the origin of the camera
camera = bpy.data.objects['Camera']
cameraOrigin = np.array(camera.location)

# Create a variable to hold the focus object
focusObject = bpy.data.objects['Cube']

# Angle (in radians) that the camera will rotate each frame
theta = 2*math.pi/250
 
def rotateCamera(scene):
    """Rotate the camera around an object. Takes the scene as parameter from handler."""


    newTheta = theta*scene.frame_current
    rotationMatrix = np.array([[math.cos(newTheta),-math.sin(newTheta),0],
                                [math.sin(newTheta), math.cos(newTheta),0],
                                [0,0,1]])
    camera.location = np.dot(cameraOrigin,rotationMatrix) + focusObject.location
     
def setRotation():
    """ Set handlers to call the rotateCamera function."""
    # clear old handlers
    bpy.app.handlers.frame_change_pre.clear()
    #register a new handler
    bpy.app.handlers.frame_change_pre.append(rotateCamera)
     
setRotation()
