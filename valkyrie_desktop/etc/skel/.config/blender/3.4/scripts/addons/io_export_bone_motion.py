bl_info = {
    "name": "Export Bone Motion (.csv)",
    "author": "dtk mnr",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Export Bone Motion",
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

armatures = []

bonenames = {}

bonenames["MOT00_Hips"] = (
    "MOT00_Hips",
    "MOT01_Head",
    "MOT02_Chest",
    "MOT_*Foot.1.L",
    "MOT_*ForeArm.1.L",
    "MOT_*Hand.1.L",
    "MOT_*UpLeg.1.L",
    "MOT_*Leg.1.L",
    "MOT_*Arm.1.L",
    "MOT_*Foot.1.R",
    "MOT_*ForeArm.1.R",
    "MOT_*Hand.1.R",
    "MOT_*UpLeg.1.R",
    "MOT_*Leg.1.R",
    "MOT_*Arm.1.R",
    "MOT15_Neck",
    "MOT16_Waist",
    "MOT_*Shoulder.1.L",
    "MOT_*Toe.1.L",
    "MOT_*Shoulder.1.R",
    "MOT_*Toe.1.R"
)

bonenames["OPT_Face_Root"] = (
    "OPT_Face_c_eyebrow",
    "OPT_Face_c_lip_lower",
    "OPT_Face_c_lip_upper",
    "OPT_Face_c_nose",
    "OPT_Face_c_tongue_a",
    "OPT_Face_c_tongue_b",
    "OPT_Face_jaw",
    "OPT_Face_*_cheek_a.0.l",
    "OPT_Face_*_cheek_b.0.l",
    "OPT_Face_*_cheek_c.0.l",
    "OPT_Face_*_eye.0.l",
    "OPT_Face_*_eye_lower_a.0.l",
    "OPT_Face_*_eye_lower_b.0.l",
    "OPT_Face_*_eyebrow_a.0.l",
    "OPT_Face_*_eyebrow_b.0.l",
    "OPT_Face_*_eyebrow_c.0.l",
    "OPT_Face_*_eyelid.0.l",
    "OPT_Face_*_forehead.0.l",
    "OPT_Face_*_lip_lower.0.l",
    "OPT_Face_*_lip_outside.0.l",
    "OPT_Face_*_lip_upper.0.l",
    "OPT_Face_*_nose_a.0.l",
    "OPT_Face_*_nose_b.0.l",
    "OPT_Face_*_nose_c.0.l",
    "OPT_Face_*_nose_d.0.l",
    "OPT_Face_*_cheek_a.0.r",
    "OPT_Face_*_cheek_b.0.r",
    "OPT_Face_*_cheek_c.0.r",
    "OPT_Face_*_eye.0.r",
    "OPT_Face_*_eye_lower_a.0.r",
    "OPT_Face_*_eye_lower_b.0.r",
    "OPT_Face_*_eyebrow_a.0.r",
    "OPT_Face_*_eyebrow_b.0.r",
    "OPT_Face_*_eyebrow_c.0.r",
    "OPT_Face_*_eyelid.0.r",
    "OPT_Face_*_forehead.0.r",
    "OPT_Face_*_lip_lower.0.r",
    "OPT_Face_*_lip_outside.0.r",
    "OPT_Face_*_lip_upper.0.r",
    "OPT_Face_*_nose_a.0.r",
    "OPT_Face_*_nose_b.0.r",
    "OPT_Face_*_nose_c.0.r",
    "OPT_Face_*_nose_d.0.r",
    "OPT_Face_Root"
)

bonenames["OPT_Hand_*_Root.1.L"] = (
    "OPT_Hand_*_Index1.1.L",
    "OPT_Hand_*_Index2.1.L",
    "OPT_Hand_*_Index3.1.L",
    "OPT_Hand_*_Metacarpal04.1.L",
    "OPT_Hand_*_Middle1.1.L",
    "OPT_Hand_*_Middle2.1.L",
    "OPT_Hand_*_Middle3.1.L",
    "OPT_Hand_*_Pinky1.1.L",
    "OPT_Hand_*_Pinky2.1.L",
    "OPT_Hand_*_Pinky3.1.L",
    "OPT_Hand_*_Ring1.1.L",
    "OPT_Hand_*_Ring2.1.L",
    "OPT_Hand_*_Ring3.1.L",
    "OPT_Hand_*_Root.1.L",
    "OPT_Hand_*_Thumb1.1.L",
    "OPT_Hand_*_Thumb2.1.L",
    "OPT_Hand_*_Thumb3.1.L"
)

bonenames["OPT_Hand_*_Root.1.R"] = (
    "OPT_Hand_*_Index1.1.R",
    "OPT_Hand_*_Index2.1.R",
    "OPT_Hand_*_Index3.1.R",
    "OPT_Hand_*_Metacarpal04.1.R",
    "OPT_Hand_*_Middle1.1.R",
    "OPT_Hand_*_Middle2.1.R",
    "OPT_Hand_*_Middle3.1.R",
    "OPT_Hand_*_Pinky1.1.R",
    "OPT_Hand_*_Pinky2.1.R",
    "OPT_Hand_*_Pinky3.1.R",
    "OPT_Hand_*_Ring1.1.R",
    "OPT_Hand_*_Ring2.1.R",
    "OPT_Hand_*_Ring3.1.R",
    "OPT_Hand_*_Root.1.R",
    "OPT_Hand_*_Thumb1.1.R",
    "OPT_Hand_*_Thumb2.1.R",
    "OPT_Hand_*_Thumb3.1.R"
)

bonenames["OPT_uchiwa_bone_Root"] = (
    "OPT_uchiwa_bone_01",
    "OPT_uchiwa_bone_02",
    "OPT_uchiwa_bone_03",
    "OPT_uchiwa_bone_04",
    "OPT_uchiwa_bone_05",
    "OPT_uchiwa_bone_06",
    "OPT_uchiwa_bone_07",
    "OPT_uchiwa_bone_08",
    "OPT_uchiwa_bone_Root"
)



def reset_bone_name(bone_name):

    mot_right = (("09","Foot"), ("10","ForeArm"), ("11","Hand"), ("12","UpLeg"), ("13","Leg"), ("14","Arm"), ("19","Shoulder"), ("20","Toe"))
    mot_left = (("03","Foot"), ("04","ForeArm"), ("05","Hand"), ("06","UpLeg"), ("07","Leg"), ("08","Arm"), ("17","Shoulder"), ("18","Toe"))

    s = bone_name
    if "*" in s:
        if s[:3] == "MOT" and ".1.R" in s:
            for i in range(len(mot_right)):
                if mot_right[i][1] in s:
                    s = s[:3] + mot_right[i][0] + s[3:]
                    break
        elif s[:3] == "MOT" and ".1.L" in s:
            for i in range(len(mot_left)):
                if mot_left[i][1] in s:
                    s = s[:3] + mot_left[i][0] + s[3:]
                    break
        if ".1.R" in s:
            pos = s.find(".")
            s = s[:pos].replace("*", "Right")
        elif ".1.L" in s:
            pos = s.find(".")
            s = s[:pos].replace("*", "Left")
        elif ".0.R" in s:
            pos = s.find(".")
            s = s[:pos].replace("*", "R")
        elif ".0.L" in s:
            pos = s.find(".")
            s = s[:pos].replace("*", "L")
        elif ".0.r" in s:
            pos = s.find(".")
            s = s[:pos].replace("*", "r")
        elif ".0.l" in s:
            pos = s.find(".")
            s = s[:pos].replace("*", "l")

    return s


def round_7(param):
    new_param = round(param,7)
    if (new_param == 0.0 or new_param == -0.0 or abs(new_param) < 0.00006):
        new_param = 0
    return new_param


def reset_bone_matrix(name, matrix):

    mat_rot_z180_nega = mathutils.Matrix.Rotation(math.radians(-180.0), 4, 'Z')
    mat_rot_z90_nega = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'Z')
    mat_rot_z270_nega = mathutils.Matrix.Rotation(math.radians(-270.0), 4, 'Z')
    mat_rot_x90_nega = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')

    if name == "MOT00_Hips" or name == "MOT16_Waist" or name == "MOT02_Chest" or "MOT15_Neck" in name or  "MOT01_Head" in name:
        return matrix
    elif "OPT_Face_" in name:
        return matrix @ mat_rot_x90_nega
    elif "Shoulder.1.L" in name or "Arm.1.L" in name or ("Hand" in name and ".1.L" in name):
        return matrix @ mat_rot_z270_nega
    elif "Shoulder.1.R" in name or "Arm.1.R" in name or ("Hand" in name and ".1.R" in name):
        return matrix @ mat_rot_z90_nega
    else:
        return matrix @ mat_rot_z180_nega


def get_motion_matrix(bone):

    bone_mat = reset_bone_matrix(bone.name, bone.matrix.copy())

    if bone.parent is None:
        return bone_mat
    else:
        parent_mat = reset_bone_matrix(bone.parent.name, bone.parent.matrix.copy())
        return parent_mat.inverted_safe() @ bone_mat


def build_csv_data(obj, type):
    global prop

    csv_data = []
    row_bone = []
    row_column = []
    bone_offset_matrices = {}

    row_bone.append("")
    row_column.append("Frame")

    for bone_name in bonenames[type]:
        row_bone.extend((reset_bone_name(bone_name), "", "", "", "", "", "", "", ""))
        row_column.extend(("PositionX", "PositionY", "PositionZ", "RotationX", "RotationY", "RotationZ", "ScaleX", "ScaleY", "ScaleZ"))

    csv_data.append(row_bone)
    csv_data.append(row_column)

    for i in range(3):
        bpy.context.scene.frame_set(prop["start_frame"])

    bpy.context.view_layer.objects.active = obj
    if obj.mode != 'POSE': bpy.ops.object.mode_set(mode='POSE')


    global_matrix = axis_conversion(to_forward='-Z', to_up='Y').to_4x4() @ obj.matrix_world

    for frame_index in range(prop["start_frame"], prop["end_frame"] - prop["start_frame"] + 1):
        row_data = []
        row_data.append(frame_index)
        bpy.context.scene.frame_set(frame_index)

        for bone_name in bonenames[type]:
            bone = obj.pose.bones[bone_name]

            mat = get_motion_matrix(bone)

            if bone.parent is None and prop["world_space"]:
                mat = global_matrix @ mat

            loc, rot_quaternion, sca = mat.decompose()

            loc_x, loc_y, loc_z = loc[0], loc[1], loc[2]

            row_data.extend((round_7(loc_x), round_7(loc_y), round_7(loc_z)))

            if "OPT_Face_" in bone.name:
                rot = rot_quaternion.to_euler('YXZ')
            else:
                rot = rot_quaternion.to_euler()

            rot_x, rot_y, rot_z = rot[0], rot[1], rot[2]

            row_data.extend((round_7(rot_x), round_7(rot_y), round_7(rot_z)))

            row_data.extend((1, 1, 1))

        csv_data.append(row_data)

    return csv_data



def collect_objects():
    global armatures

    armatures = []

    for obj in bpy.context.selectable_objects:
        if obj.type == 'ARMATURE':
            armatures.append(obj)


def get_frame_range(armature):

    start = 0
    end = 1

    if armature.animation_data is not None:
        if armature.animation_data.action is not None:
            start, end = armature.animation_data.action.frame_range
        elif armature.animation_data.use_nla:
            start_list = []
            end_list = []
            for track in armature.animation_data.nla_tracks:
                for strip in track.strips:
                    start_list.append(strip.frame_start)
                    end_list.append(strip.frame_end)
            if len(start_list) > 0 and len(end_list) > 0:
                return int(min(start_list)), int(max(end_list))

    if start == 0 and end == 1:
        start, end = bpy.context.scene.frame_start, bpy.context.scene.frame_end

    return int(start), int(end)


def get_armature_object_callback(self, context):
    global armatures
    items = []
    names = []
    for i, armature in enumerate(armatures):
        if armature.name[-4:] == "_Rig" and armature.name[:-4] in bpy.context.blend_data.objects:
            base_armature = bpy.context.blend_data.objects[armature.name[:-4]]
            armatures[i] = base_armature
            name = base_armature.name
        else:
            name = armature.name
        if name not in names:
            item = (str(i), name, "")
            names.append(name)
            items.append(item)
    return items


class Export_bone_motion(bpy.types.Operator, ImportHelper):
    """Export Bone Motion"""
    bl_idname = "export.bone_motion"
    bl_label = "Export Bone Motion"
    filename_ext = ".csv"

    filter_glob: StringProperty(
            default="*.csv",
            options={'HIDDEN'}
            )

    target_armature: EnumProperty(
            name="Armature",
            items=get_armature_object_callback,
            description="Target Armature Object",
            )

    export_body: BoolProperty(
            name="Export Body Motion",
            description="Export Body Motion",
            default=True,
            )

    export_face: BoolProperty(
            name="Export Face Motion",
            description="Export Face Motion",
            default=True,
            )

    export_lefthand: BoolProperty(
            name="Export Left Hand Motion",
            description="Export Left Hand Motion",
            default=True,
            )

    export_righthand: BoolProperty(
            name="Export Right Hand Motion",
            description="Export Right Hand Motion",
            default=True,
            )

    export_uchiwa: BoolProperty(
            name="Export Uchiwa Motion",
            description="Export Uchiwa Motion",
            default=True,
            )

    world_space: BoolProperty(
            name="World Space",
            description="World Space",
            default=True,
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
        layout.prop(self, "target_armature")

        col_body = layout.column()
        col_body.prop(self, "export_body")
        col_face = layout.column()
        col_face.prop(self, "export_face")
        col_lefthand = layout.column()
        col_lefthand.prop(self, "export_lefthand")
        col_righthand = layout.column()
        col_righthand.prop(self, "export_righthand")
        col_uchiwa = layout.column()
        col_uchiwa.prop(self, "export_uchiwa")

        obj = armatures[int(self.target_armature)]

        if "MOT00_Hips" in obj.data.bones:
            col_body.enabled = True
        else:
            col_body.enabled = False

        if "OPT_Face_Root" in obj.data.bones:
            col_face.enabled = True
        else:
            col_face.enabled = False

        if "OPT_Hand_*_Root.1.L" in obj.data.bones:
            col_lefthand.enabled = True
        else:
            col_lefthand.enabled = False

        if "OPT_Hand_*_Root.1.R" in obj.data.bones:
            col_righthand.enabled = True
        else:
            col_righthand.enabled = False

        if "OPT_uchiwa_bone_Root" in obj.data.bones:
            col_uchiwa.enabled = True
        else:
            col_uchiwa.enabled = False

        layout.separator()
        col_space = layout.column()
        col_space.prop(self, "world_space")

        if col_body.enabled and self.export_body:
            col_space.enabled = True
        else:
            col_space.enabled = False

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
        global armatures

        if set_default_target:
            collect_objects()
            set_default_target = False
            for i, armature in enumerate(armatures):
                if armature.select_get():
                    self.target_armature = str(i)
            self.start_frame, self.end_frame = get_frame_range(armatures[int(self.target_armature)])
        self.frame_count = self.end_frame - self.start_frame + 1
        return True

    def execute(self, context):
        global prop

        filename, ext = os.path.splitext(self.filepath)

        prop = {}

        obj = armatures[int(self.target_armature)]

        types = []

        if self.export_body and "MOT00_Hips" in obj.data.bones:
            types.append("MOT00_Hips")

        if self.export_face and "OPT_Face_Root" in obj.data.bones:
            types.append("OPT_Face_Root")

        if self.export_lefthand and "OPT_Hand_*_Root.1.L" in obj.data.bones:
            types.append("OPT_Hand_*_Root.1.L")

        if self.export_righthand and "OPT_Hand_*_Root.1.R" in obj.data.bones:
            types.append("OPT_Hand_*_Root.1.R")

        if self.export_uchiwa and "OPT_uchiwa_bone_Root" in obj.data.bones:
            types.append("OPT_uchiwa_bone_Root")

        prop["world_space"] = self.world_space

        hidden_obj = False
        if obj.hide_viewport:
            obj.hide_viewport = False
            name = obj.name + "_Rig"
            if name in bpy.context.blend_data.objects:
                rig_obj = bpy.context.blend_data.objects[obj.name + "_Rig"]
                hidden_obj = True

        if self.auto_set_frame_range:
            prop["start_frame"], prop["end_frame"] = get_frame_range(obj)
        else:
            prop["start_frame"] = self.start_frame
            prop["end_frame"] = self.end_frame

        for type in types:

            import time
            start = time.time()

            if type not in obj.data.bones:
                print("Nothing", type)
                continue

            csv_data = build_csv_data(obj, type)

            filename_type = ""
            if type == "MOT00_Hips":
                filename_type = "_BODY"
            elif type == "OPT_Face_Root":
                filename_type = "_FACE"
            elif type == "OPT_Hand_*_Root.1.L":
                filename_type = "_LEFTHAND"
            elif type == "OPT_Hand_*_Root.1.R":
                filename_type = "_RIGHTHAND"
            elif type == "OPT_uchiwa_bone_Root":
                filename_type = "_UCHIWA"
            csv_path = filename + filename_type + ".csv"
            count = 1
            while os.path.exists(csv_path):
                csv_path = filename + filename_type + " - " + str(count) + ".csv"
                count += 1

            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(csv_data)

            elapsed_time = time.time() - start
            print("{0} -> Elapsed Time : {1}".format(csv_path, elapsed_time))

        if hidden_obj:
            obj.hide_viewport = True
            bpy.context.view_layer.objects.active = rig_obj


        return {'FINISHED'}



classes = (
    Export_bone_motion,
)

def menu_func(self, context):
    global prop
    global set_default_target
    global armatures

    collect_objects()
    if len(armatures) == 0:
        return {'CANCELLED'}

    set_default_target = True

    default_path = bpy.path.display_name_from_filepath(bpy.context.blend_data.filepath) + ".csv"

    self.layout.operator(Export_bone_motion.bl_idname, text="Bone Motion (.csv)", icon='PLUGIN').filepath = default_path

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
