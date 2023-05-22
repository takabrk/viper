import bpy

from .property_group import Vrm1HumanBonesPropertyGroup, Vrm1PropertyGroup


def migrate(vrm1: Vrm1PropertyGroup, armature: bpy.types.Object) -> None:
    human_bones = vrm1.humanoid.human_bones
    human_bones.last_bone_names.clear()
    Vrm1HumanBonesPropertyGroup.fixup_human_bones(armature)
    Vrm1HumanBonesPropertyGroup.check_last_bone_names_and_update(
        armature.data.name,
        defer=False,
    )

    if human_bones.initial_automatic_bone_assignment:
        human_bones.initial_automatic_bone_assignment = False
        human_bone_name_to_human_bone = human_bones.human_bone_name_to_human_bone()
        if all(not b.node.value for b in human_bone_name_to_human_bone.values()):
            bpy.ops.vrm.assign_vrm1_humanoid_human_bones_automatically(
                armature_name=armature.name
            )
