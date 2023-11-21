import bpy
import time

bpy.types.Scene.render_time = bpy.props.FloatProperty(name="Render Time Property")
bpy.types.Scene.frame_time = bpy.props.FloatProperty(name="Render Frame Time")
bpy.types.Scene.num_frames = bpy.props.IntProperty(name="Render Frames")

def render_start(scene):
    bpy.data.scenes[0].render_time = time.time()
    bpy.context.scene.num_frames = 0
    print("Render Started")
    

def render_end(scene):
    end_time = time.time() - bpy.data.scenes[0].render_time
    print("Render Finished: " + str(bpy.context.scene.num_frames) + " frames in " + str(end_time) + " seconds")
    
    if bpy.context.scene.num_frames > 0:
        print("Average: ", str(end_time / bpy.context.scene.num_frames) + " seconds/frame")
    

def frame_start(scene):
    bpy.context.scene.frame_time = time.perf_counter()
    print("Frame Started")
    

def frame_end(scene):
    bpy.context.scene.num_frames += 1
    frame_end_time = time.perf_counter() - bpy.context.scene.frame_time
    print("Frame Finished: ", str(frame_end_time) + " seconds")

bpy.app.handlers.render_init.append(render_start)
bpy.app.handlers.render_complete.append(render_end)
bpy.app.handlers.render_pre.append(frame_start)
bpy.app.handlers.render_write.append(frame_end)
bpy.app.handlers.render_cancel.append(render_end)
