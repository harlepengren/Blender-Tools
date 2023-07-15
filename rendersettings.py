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
    targetName: bpy.props.StringProperty(name="targetName",description="Name of the setting that will change.")
    target: bpy.props.StringProperty(name="target", description="datapath of setting we want to change")
    start: bpy.props.FloatProperty(name="start", default=0.0, description="starting value")
    end: bpy.props.FloatProperty(name="end", default=1.0, description="ending value")
 
class RenderSettingsOperator(bpy.types.Operator):
    """Allows you to render multiple versions with different settings for comparison."""
    bl_idname = "scene.render_setting_operator"
    bl_label = "Render Instance Settings"

    def CreateMaterial(self,text_object):
        mat = bpy.data.materials.get("TextMaterial")
        if mat is None:
            mat = bpy.data.materials.new(name="TextMaterial")
        
        if not mat.use_nodes:
            mat.use_nodes = True
            nodes = mat.node_tree.nodes

        # Add emission
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Emission'].default_value = (1.0,1.0,1.0,1.0)
        bsdf.inputs['Emission Strength'].default_value = 0.3
        
        
        
        if text_object.data.materials:
            text_object.materials[0] = mat
        else:
            text_object.data.materials.append(mat)
        

    def execute(self, context):
        print("Rendering the scene")

        renderSlots = bpy.data.images["Render Result"].render_slots
        
        # Set the render seetings
        startingValue = context.scene.render_settings_prop.start
        iterations = min(context.scene.render_settings_prop.numRenders,len(renderSlots))
        incrementalValue = (context.scene.render_settings_prop.end - startingValue)/iterations
        
        # Create the text
        bpy.ops.object.add(type="FONT")
        currText = bpy.context.object
        currText.parent = bpy.data.objects["Camera"]
        currText.location = (-1.4,-0.696,-4.0)
        currText.scale = (0.5,0.5,0.5)
        self.CreateMaterial(currText)
        
        wm = bpy.context.window_manager
        totalProgress = iterations
        wm.progress_begin(0,totalProgress)
        for index in range(0,iterations):
            renderSlots.active_index = index
            
            # Change the setting - using exec is not super safe
            currentValue = startingValue + incrementalValue*index
            exec(context.scene.render_settings_prop.target + "=" + str(currentValue))
            currText.data.body = bpy.context.scene.render_settings_prop.targetName + ": " + str(currentValue)
            bpy.ops.render.render()
            wm.progress_update(index)
            
        # Delete the text
        bpy.ops.object.select_all(action="DESELECT")
        currText.select_set(True)
        bpy.context.view_layer.objects.active = currText
        bpy.ops.object.delete()
        wm.progress_end()
        
        return {'FINISHED'}
     
class RenderSettingsPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_ender_settings_panel'
    bl_label = 'Render Settings'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        self.layout.prop(bpy.context.scene.render_settings_prop,"numRenders")
        self.layout.prop(bpy.context.scene.render_settings_prop,"targetName")
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