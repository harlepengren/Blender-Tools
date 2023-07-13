bl_info = {
    "name": "Render Settings Text",
    "author": "Harlepengren",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "3D View Sidebar",
    "description": "Creates renders with different settings to compare settings.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Scene",
}

#import the modules
import bpy
 
# Property Group for the settings
class RenderSettingsPropertyGroup(bpy.types.PropertyGroup):
    numRenders: bpy.props.IntProperty(name="numRenders",default=1)
    target: bpy.props.StringProperty(name="target", description="datapath of setting we want to change")
    start: bpy.props.FloatProperty(name="start", default=0.0, description="starting value")
    end: bpy.props.FloatProperty(name="end", default=1.0, description="ending value")
 
class RenderSettingsOperator(bpy.types.Operator):
    """Allows you to render multiple versions with different settings for comparison."""
    bl_idname = "scene.render_setting_operator"
    bl_label = "Render Instance Settings"


    def execute(self, context):
        print("Rendering the scene")

        renderSlots = bpy.data.images["Render Result"].render_slots
        
        startingValue = context.scene.render_settings_prop.start
        iterations = min(context.scene.render_settings_prop.numRenders,len(renderSlots))
        incrementalValue = (context.scene.render_settings_prop.end - startingValue)/iterations
        
        for index in range(0,iterations):
            renderSlots.active_index = index
            
            # Change the setting - using exec is not super safe
            exec(context.scene.render_settings_prop.target + "=" + str(startingValue + incrementalValue*index))
            
            bpy.ops.render.render()
        
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