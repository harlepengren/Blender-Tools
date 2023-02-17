#import the modules
import bpy
import numpy as np
import math
from mathutils import *
 
# Property Group for the settings
class RotationPropertyGroup(bpy.types.PropertyGroup):
    radius: bpy.props.FloatProperty(name="radius", default=7)
    speed: bpy.props.FloatProperty(name="speed",default=1, description="number of rotations in timeframe")
    numKeyframes: bpy.props.IntProperty(name="keyframes",default=30)
    target: bpy.props.StringProperty(name="target")
 
class RotationOperator(bpy.types.Operator):
    """Adds keyframes to an object to rotate around another object."""
    bl_idname = "object.rotation_operator"
    bl_label = "Camera Rotation"

    def rotateCamera(self,frameNumber):
        """Rotate the camera around an object."""
        
        newTheta = self.theta*frameNumber
        rotationMatrix = np.array([[math.cos(newTheta),-math.sin(newTheta),0],
                                [math.sin(newTheta), math.cos(newTheta),0],
                                [0,0,1]])
        return np.dot(self.cameraOrigin,rotationMatrix) + self.focusObject.location    

    def execute(self, context):
        # Create a variable to hold the currently selected object
        camera = bpy.context.object
        self.cameraOrigin = Vector(camera.location)

        # Create a variable to hold the focus object
        self.focusObject = bpy.data.objects[bpy.context.object.rotation_prop.target]
        
        keyframes = bpy.context.object.rotation_prop.numKeyframes
        radius = bpy.context.object.rotation_prop.radius
        speed = bpy.context.object.rotation_prop.speed

        # Angle (in radians) that the camera will rotate each frame
        self.theta = 2*math.pi*speed/(bpy.context.scene.frame_end - bpy.context.scene.frame_start)
        framesPerKey = (bpy.context.scene.frame_end - bpy.context.scene.frame_start)/keyframes
        
        for currentKeyframe in range(0,keyframes):
            currentFrame = currentKeyframe*framesPerKey + 1
            newPos = self.rotateCamera(currentFrame)
            camera.location = newPos
            camera.keyframe_insert(data_path='location',frame=currentFrame)
            
        # Reset to the first frame
        bpy.context.scene.frame_current = bpy.context.scene.frame_start
            
        return {'FINISHED'}

class RotationClearOperator(bpy.types.Operator):
    """Clear keyframes."""
    bl_idname = "object.rotation_clear_operator"
    bl_label = "Clear object rotation keyframes"
    
    def execute(self, context):
        return bpy.ops.anim.keyframe_clear_v3d()
     
class RotationPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_rotation_panel'
    bl_label = 'Camera Rotation'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        # Radius is currently not used - the rotation is based on the starting location of the object
        #self.layout.prop(bpy.context.object.rotation_prop,"radius")
        
        self.layout.prop(bpy.context.object.rotation_prop,"speed")
        self.layout.prop(bpy.context.object.rotation_prop,"numKeyframes")
        self.layout.prop_search(bpy.context.object.rotation_prop, "target", bpy.context.scene, "objects")
        self.layout.separator()
        self.layout.operator(RotationOperator.bl_idname, text=RotationOperator.bl_label)
        self.layout.operator(RotationClearOperator.bl_idname,text="Clear keyframes")
        
def register():
    bpy.utils.register_class(RotationPropertyGroup)
    bpy.utils.register_class(RotationOperator)
    bpy.utils.register_class(RotationClearOperator)
    bpy.utils.register_class(RotationPanel)
    
    # Create pointer reference for the property group
    bpy.types.Object.rotation_prop = bpy.props.PointerProperty(type=RotationPropertyGroup)
    
if __name__ == "__main__":
    register()