# Copyright (c) 2023 Harlepengren
# http://harlepengren.com
#
# Licensed under Apache 2.0
# This software is provided AS IS WITH NO EXPRESS OR IMPLIED WARRANTY OF ANY KIND.

import bpy
import math
from mathutils import *
import random

class BouncePropertyGroup(bpy.types.PropertyGroup):
    radius: bpy.props.FloatProperty(name="radius", default=1)
    numBounces: bpy.props.IntProperty(name="bounces", default=5)
    

class BounceOperator(bpy.types.Operator):
    """Adds keyframes to bounce the object."""
    bl_idname = "object.bounce_operator"
    bl_label = "Bounce Operator"

    def execute(self, context):
        # The currently selected object - return failed if none
        currentObject = bpy.context.object
        if currentObject == None:
            print("No object selected")
            return {'CANCELLED'}
        
        origin = currentObject.location
        radius = currentObject.bounce_prop.radius
        numBounces = currentObject.bounce_prop.numBounces 
                
        # Get the start and end frames
        startFrame = bpy.data.scenes["Scene"].frame_start
        endFrame = bpy.data.scenes["Scene"].frame_end
        
        framesPerMove = math.floor((endFrame-startFrame)/numBounces)
        
        # Add keyframes
        for index in range(0,self.numBounces+1):
            # Add the keyframe
            currentObject.keyframe_insert(data_path='location',frame=(index*framesPerMove+1))
            
            # Move the object
            newX = (random.random()*2)-1
            newY = (random.random()*2)-1
            newZ = (random.random()*2)-1
            randomVector = Vector((newX,newY,newZ))*Vector((radius,radius,radius))
            moveVector = origin + randomVector
            
            currentObject.location = moveVector
        

        return {'FINISHED'}

class BouncePanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_bounce_panel'
    bl_label = 'Bounce Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        self.layout.label(text='Bounce')
        self.layout.prop(bpy.context.object.bounce_prop,"radius")
        self.layout.prop(bpy.context.object.bounce_prop,"numBounces")
        self.layout.operator(BounceOperator.bl_idname, text="Let's Bounce")

def menu_func(self, context):
    self.layout.operator(BounceOperator.bl_idname, text=BounceOperator.bl_label)


def register():
    bpy.utils.register_class(BouncePropertyGroup)
    bpy.utils.register_class(BounceOperator)
    bpy.utils.register_class(BouncePanel)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
    # Create pointer reference
    bpy.types.Object.bounce_prop = bpy.props.PointerProperty(type=BouncePropertyGroup)


def unregister():
    bpy.utils.unregister_class(BouncePropertyGroup)
    bpy.utils.unregister_class(BounceOperator)
    bpy.utils.unregister_class(BouncePanel)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
