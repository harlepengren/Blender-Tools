import bpy

def my_handler(scene):
    print("milestone1")
    
bpy.app.handlers.render_stats.append(my_handler)

text = bpy.data.curves['Text']
text.body = "Changed"
