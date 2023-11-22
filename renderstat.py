import bpy
import time


def render_start(scene):
    global start_time 
    global num_frames
    start_time = time.time()
    num_frames = 0
    print("++++++++++++++++++++++++++++++")
    print("Render Started")
    

def render_end(scene):
    end_time = time.time() - start_time
    print("Render Finished: " + str(num_frames) + " frames in " + str(end_time) + " seconds")
    
    if num_frames > 0:
        print("Average: ", str(end_time / num_frames) + " seconds/frame")
    print("++++++++++++++++++++++++++++++")
    

def frame_start(scene):
    global frame_time
    frame_time = time.time()
    print("Frame Started")
    

def frame_end(scene):
    global num_frames
    num_frames += 1
    frame_end_time = time.time() - frame_time
    print("Frame Finished: ", str(frame_end_time) + " seconds")

bpy.app.handlers.render_init.append(render_start)
bpy.app.handlers.render_complete.append(render_end)
bpy.app.handlers.render_pre.append(frame_start)
bpy.app.handlers.render_write.append(frame_end)
bpy.app.handlers.render_cancel.append(render_end)
