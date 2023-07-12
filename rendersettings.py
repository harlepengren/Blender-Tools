bl_info = {
    "name": "Camera Rotation",
    "author": "Harlepengren",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "3D View Sidebar",
    "description": "Rotates camera around a target object over a given number of frames.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object",
}

#import the modules
import bpy
 
# Property Group for the settings
class RenderSettingsPropertyGroup(bpy.types.PropertyGroup):
    numRenders: bpy.props.IntProperty(name="numRenders",default=30)
    target: bpy.props.StringProperty(name="target", description="datapath of setting we want to change")
    start: bpy.props.FloatProperty(name="start", default=0.0, description="starting value")
    end: bpy.props.FloatProperty(name="end", default=1.0, description="ending value")
 
class RenderSettingOperator(bpy.types.Operator):
    """Allows you to render multiple versions with different settings for comparison."""
    bl_idname = "scene.render_setting_operator"
    bl_label = "Render Instance Settings"


    def execute(self, context):            
        return {'FINISHED'}
     
class RenderSettingsPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_ender_settings_panel'
    bl_label = 'Render Settings'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        self.layout.prop(bpy.context.scene.render_settings_prop,"numRenders")
        self.layout.prop(bpy.context.scene.render_settings_prop,"target")
        self.layout.prop(bpy.context.scene.render_settings_prop,"start")
        self.layout.prop(bpy.context.scene.render_settings_prop,"end")        
        self.layout.separator()
        self.layout.operator(RenderSettingsOperator.bl_idname, text=RenderSettingsOperator.bl_label)
        
def register():
    bpy.utils.register_class(RenderSettingsPropertyGroup)
    bpy.utils.register_class(RenderSettingsOperator)
    bpy.utils.register_class(RenderSettingsPanel)
    
    # Create pointer reference for the property group
    bpy.types.Scene.render_settings_prop = bpy.props.PointerProperty(type=RenderSettingsPropertyGroup)
    
def unregister():
    bpy.utils.unregister_class(RenderSettingsPropertyGroup)
    bpy.utils.unregister_class(RenderSettingsOperator)
    bpy.utils.unregister_class(RenderSettingsPanel)
    
if __name__ == "__main__":
    register()