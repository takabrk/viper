bl_info = {
    "name": "Export Camera Motion (.csv)",
    "author": "dtk mnr",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Export Camera Motion",
    "warning": "",
    "category": "Import-Export",
}

import bpy
import struct, os, io, array, csv
import math
import mathutils
from mathutils import Vector, Matrix
from bpy.props import *
from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        orientation_helper,
        path_reference_mode,
        axis_conversion,
        )



prop = {}

set_default_target = True

emptys = []
cameras = []



def build_csv_data():
    global prop

    csv_data = []
    csv_data.append(("Frame", "PositionX", "PositionY", "PositionZ", "PorX", "PorY", "PorZ", "Tilt", "Angle"))

    for i in range(3):
        bpy.context.scene.frame_set(prop["start_frame"])

    # Check Old Type
    old_type = False
    for constraint in bpy.context.active_object.constraints:
        if constraint.type == 'TRACK_TO' and not constraint.mute:
            old_type = True
            break

    for frame_index in range(prop["start_frame"], prop["end_frame"] - prop["start_frame"] + 1):
        row_data = []
        row_data.append(frame_index)
        bpy.context.scene.frame_set(frame_index)

        # Camera Position
        loc, rot, sca = prop["target_camera"].matrix_world.decompose()
        cam_x, cam_y, cam_z = loc

        if cam_y != 0:
            cam_y = -cam_y
        row_data.extend((cam_x, cam_z, cam_y))

        # POR Position
        loc, rot, sca = prop["target_por"].matrix_world.decompose()
        por_x, por_y, por_z = loc

        if por_y != 0:
            por_y = -por_y
        row_data.extend((por_x, por_z, por_y))

        # Tilt
        if old_type:
            #row_data.append(0)
            rot_x, rot_y, rot_z = prop["target_por"].matrix_world.to_euler('XYZ')
            row_data.append(math.degrees(rot_y))

        else:
            rot_x, rot_y, rot_z = prop["target_camera"].matrix_local.to_euler('XYZ')
            deg_z = round(math.degrees(-rot_z), 4)
            if deg_z == round(deg_z):
                deg_z = round(deg_z)
            row_data.append(deg_z)

        # Angle Y
        row_data.append(math.degrees(prop["target_camera"].data.angle_y))

        csv_data.append(row_data)

    return csv_data



def collect_objects():
    global emptys
    global cameras

    emptys = []
    cameras = []

    for obj in bpy.context.selectable_objects:
        if obj.type == 'EMPTY':
            emptys.append(obj)
        elif obj.type == 'CAMERA':
            cameras.append(obj)


def get_frame_range(cam, por):

    cam_start = angle_start = por_start = 0
    cam_end = angle_end = por_end = 1

    cam_start, cam_end = get_obj_frame_range(cam)
    angle_start, angle_end = get_obj_frame_range(cam.data)
    por_start, por_end = get_obj_frame_range(por)

    start = min(cam_start, angle_start, por_start)
    end = max(cam_end , angle_end, por_end)

    return int(start), int(end)


def get_obj_frame_range(obj):
    if obj.animation_data is not None:
        if obj.animation_data.action is not None:
            return obj.animation_data.action.frame_range
        elif obj.animation_data.use_nla:
            start_list = []
            end_list = []
            for track in obj.animation_data.nla_tracks:
                for strip in track.strips:
                    start_list.append(strip.frame_start)
                    end_list.append(strip.frame_end)
            if len(start_list) > 0 and len(end_list) > 0:
                return min(start_list), max(end_list)
    return bpy.context.scene.frame_start, bpy.context.scene.frame_end


def get_camera_object_callback(self, context):
    global cameras
    items = []
    for i, camera in enumerate(cameras):
        item = (str(i), camera.name, "")
        items.append(item)
    return items


def get_empty_object_callback(self, context):
    global emptys
    items = []
    for i, empty in enumerate(emptys):
        item = (str(i), empty.name, "")
        items.append(item)
    return items


class Export_camera_motion(bpy.types.Operator, ImportHelper):
    """Export Camera Motion"""
    bl_idname = "export.camera_motion"
    bl_label = "Export Camera Motion"
    filename_ext = ".csv"

    filter_glob: StringProperty(
            default="*.csv",
            options={'HIDDEN'}
            )

    target_camera: EnumProperty(
            name="Camera",
            items=get_camera_object_callback,
            description="Target Camera Object",
            )

    target_por: EnumProperty(
            name="POR",
            items=get_empty_object_callback,
            description="Target POR Object",
            )

    auto_set_frame_range: BoolProperty(
            name="Auto Set Frame Range",
            description="Auto Set Frame Range",
            default=True,
            )

    start_frame: IntProperty(
            name="Start Frame",
            description="Start Frame",
            default=0,
            )

    end_frame: IntProperty(
            name="End Frame",
            description="End Frame",
            default=1,
            )

    frame_count: IntProperty(
            name="Frame Count",
            description="Frame Count",
            default=1,
            )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "target_camera")
        layout.prop(self, "target_por")
        layout.separator()
        layout.prop(self, "auto_set_frame_range")
        row = layout.row(align=True)
        row.prop(self, "start_frame", text = "Start")
        row.prop(self, "end_frame", text = "End")
        if self.auto_set_frame_range:
            row.enabled = False
        layout.label(text="Frame Count : " + str(self.frame_count))

    def check(self, context):
        global set_default_target
        global cameras
        global emptys

        if set_default_target:
            collect_objects()
            set_default_target = False
            for i, empty in enumerate(emptys):
                if empty.select_get():
                    self.target_por = str(i)
            for i, camera in enumerate(cameras):
                if camera.select_get():
                    self.target_camera = str(i)
            self.start_frame, self.end_frame = get_frame_range(cameras[int(self.target_camera)], emptys[int(self.target_por)])
        self.frame_count = self.end_frame - self.start_frame + 1
        return True

    def execute(self, context):
        global prop

        prop = {}
        prop["target_camera"] = cameras[int(self.target_camera)]
        prop["target_por"] = emptys[int(self.target_por)]

        if self.auto_set_frame_range:
            prop["start_frame"], prop["end_frame"] = get_frame_range(prop["target_camera"], prop["target_por"])
        else:
            prop["start_frame"] = self.start_frame
            prop["end_frame"] = self.end_frame

        csv_data = build_csv_data()

        with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        return {"FINISHED"}



classes = (
    Export_camera_motion,
)

def menu_func(self, context):
    global prop
    global set_default_target
    global cameras
    global emptys

    collect_objects()
    if len(cameras) == 0 or len(emptys) == 0:
        return {'CANCELLED'}

    set_default_target = True

    default_path = bpy.path.display_name_from_filepath(bpy.context.blend_data.filepath) + "_CAMERA.csv"

    self.layout.operator(Export_camera_motion.bl_idname, text="Camera Motion (.csv)", icon='PLUGIN').filepath = default_path

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
