bl_info = {
    "name": "Export Camera Animation",
    "author": "Dmitry Romashin",
    "version": (1, 0, 0),
    "blender": (4, 4, 0),
    "location": "File > Export > Camera Animation (.json)",
    "description": "Export active camera animation (location, rotation, FOV) to JSON",
    "category": "Import-Export",
}

import bpy
import json
import os
import math

class EXPORT_OT_camera_animation(bpy.types.Operator):
    bl_idname = "export.camera_animation"
    bl_label = "Export Camera Animation to JSON"
    bl_description = "Export camera location, rotation, and FOV per frame to a JSON file"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath for exporting the JSON file",
        default="",
        subtype='FILE_PATH'
    )

    def execute(self, context):
        scene = context.scene
        camera = scene.camera
        if not camera:
            self.report({'ERROR'}, "No active camera in the scene.")
            return {'CANCELLED'}

        start_frame = scene.frame_start
        end_frame = scene.frame_end
        camera_data = []

        for frame in range(start_frame, end_frame + 1):
            scene.frame_set(frame)
            bpy.context.view_layer.update()

            loc = camera.location
            rot = camera.rotation_euler
            fov_deg = math.degrees(camera.data.angle)

            camera_data.append({
                'frame': frame,
                'location': [loc.x, loc.y, loc.z],
                'rotation_euler': [rot.x, rot.y, rot.z],
                'fov_degrees': fov_deg
            })

        out_path = bpy.path.abspath(self.filepath)
        out_dir = os.path.dirname(out_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)

        with open(out_path, 'w') as f:
            json.dump({
                'start_frame': start_frame,
                'end_frame': end_frame,
                'camera_animation': camera_data
            }, f, indent=4)

        self.report({'INFO'}, f"Camera animation exported to: {out_path}")
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.filepath:
            self.filepath = bpy.path.abspath('//camera_animation.json')
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_func_export(self, context):
    self.layout.operator(EXPORT_OT_camera_animation.bl_idname, text="Camera Animation (.json)")


def register():
    bpy.utils.register_class(EXPORT_OT_camera_animation)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(EXPORT_OT_camera_animation)


if __name__ == "__main__":
    register()
