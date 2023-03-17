# Copyright (c) 2023 Harlepengren
# http://harlepengren.com
#
# Licensed under Apache 2.0
# This software is provided AS IS WITH NO EXPRESS OR IMPLIED WARRANTY OF ANY KIND.

import bpy

bl_info = {
    "name": "World Nodes",
    "author": "Harlepengren",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "3D View Sidebar",
    "description": "Adds world node setup.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Material",
}

def CreateWorldNodes():
    world = bpy.data.worlds['World']

    if not world.use_nodes:
        world.use_nodes = True

    nodes = world.node_tree.nodes

    # Clear Existing nodes
    for current_node in nodes:
        world.node_tree.nodes.remove(current_node)

    # Add output node
    world_output = nodes.new('ShaderNodeOutputWorld')
    world_output.location = (217,27)

    current_background = nodes.new('ShaderNodeBackground')
    current_background.location = (-234,-5)

    # Add mix shader and connect to output
    mix_node = nodes.new('ShaderNodeMixShader')
    mix_node.location = (16,27)
    world.node_tree.links.new(world_output.inputs[0],mix_node.outputs[0])
    world.node_tree.links.new(mix_node.inputs[1],current_background.outputs[0])

    # Add background node
    background_node = nodes.new('ShaderNodeBackground')
    background_node.inputs['Color'].default_value = (0,0,0,1)
    background_node.location = (-231,-132)
    world.node_tree.links.new(mix_node.inputs[2],background_node.outputs[0])

    # Add environment texture
    env_node = nodes.new('ShaderNodeTexEnvironment')
    env_node.location = (-548, -100)
    world.node_tree.links.new(current_background.inputs[0],env_node.outputs[0])


    # Add light path
    light_path = nodes.new('ShaderNodeLightPath')
    light_path.location = (-424,268)
    world.node_tree.links.new(mix_node.inputs[0],light_path.outputs[0])

class WORLDNODE_OT(bpy.types.Operator):
    '''Add world nodes.'''
    bl_idname = 'scene.world_node_operator'
    bl_label = 'Add HDRI world node setup.'
    
    def execute(self, context):
        CreateWorldNodes()
        return {'FINISHED'}
        
class WORLDNODE_PT(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_WORLDNODE'
    bl_label = 'World Nodes'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw (self, context):
        self.layout.operator(WORLDNODE_OT.bl_idname, text=WORLDNODE_OT.bl_label)
        
def register():
    bpy.utils.register_class(WORLDNODE_OT)
    bpy.utils.register_class(WORLDNODE_PT)
    
def unregister():
    bpy.utils.unregister_class(WORLDNODE_PT)
    bpy.utils.unregister_class(WORLDNODE_OT)
    
if __name__ == "__main__":
    register()
