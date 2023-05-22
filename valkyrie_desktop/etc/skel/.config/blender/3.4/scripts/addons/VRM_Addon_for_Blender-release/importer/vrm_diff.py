from typing import Dict, List, Tuple

from ..common import deep, gltf
from ..common.deep import Json, make_json
from .vrm_parser import decode_bin


def human_bone_sort_key(human_bone_dict: Json) -> int:
    if not isinstance(human_bone_dict, dict):
        return -1
    node = human_bone_dict.get("node")
    if not isinstance(node, int):
        return -1
    return node


def create_vrm_json_dict(data: bytes) -> Dict[str, Json]:
    vrm_json, binary_chunk = gltf.parse_glb(data)

    vrm_json["~accessors_decoded"] = make_json(decode_bin(vrm_json, binary_chunk))

    extensions_dict = vrm_json.get("extensions")
    if not isinstance(extensions_dict, dict):
        return vrm_json

    vrm0_extension = extensions_dict.get("VRM")
    if not isinstance(vrm0_extension, dict):
        return vrm_json

    vrm0_first_person_dict = vrm0_extension.get("firstPerson")
    if not isinstance(vrm0_first_person_dict, dict):
        vrm0_first_person_dict = {}
        vrm0_extension["firstPerson"] = vrm0_first_person_dict

    vrm0_humanoid_dict = vrm0_extension.get("humanoid")
    if isinstance(vrm0_humanoid_dict, dict):
        vrm0_human_bone_dicts = vrm0_humanoid_dict.get("humanBones")
        if isinstance(vrm0_human_bone_dicts, list):
            vrm0_humanoid_dict["humanBones"] = sorted(
                vrm0_human_bone_dicts, key=human_bone_sort_key
            )

            vrm0_first_person_bone = vrm0_first_person_dict.get("firstPersonBone")
            if vrm0_first_person_bone in [None, -1]:
                for vrm0_human_bone_dict in vrm0_human_bone_dicts:
                    if not isinstance(vrm0_human_bone_dict, dict):
                        continue
                    node = vrm0_human_bone_dict.get("node")
                    if not isinstance(node, int) or node < 0:
                        continue
                    if vrm0_human_bone_dict.get("bone") == "head":
                        vrm0_first_person_dict["firstPersonBone"] = node
                        break

    for look_at_key in [
        "lookAtHorizontalInner",
        "lookAtHorizontalOuter",
        "lookAtVerticalDown",
        "lookAtVerticalUp",
    ]:
        if look_at_key not in vrm0_first_person_dict:
            vrm0_first_person_dict[look_at_key] = {}
        look_at_dict = vrm0_first_person_dict[look_at_key]
        if not isinstance(look_at_dict, dict):
            continue
        if "curve" not in look_at_dict:
            look_at_dict["curve"] = [0, 0, 0, 1, 1, 1, 1, 0]

    vrm0_blend_shape_master_dict = vrm0_extension.get("blendShapeMaster")
    if isinstance(vrm0_blend_shape_master_dict, dict):
        vrm0_blend_shape_group_dicts = vrm0_blend_shape_master_dict.get(
            "blendShapeGroups"
        )
        if isinstance(vrm0_blend_shape_group_dicts, list):
            for vrm0_blend_shape_group_dict in vrm0_blend_shape_group_dicts:
                if not isinstance(vrm0_blend_shape_group_dict, dict):
                    continue
                if "isBinary" not in vrm0_blend_shape_group_dict:
                    vrm0_blend_shape_group_dict["isBinary"] = False
                if "binds" not in vrm0_blend_shape_group_dict:
                    vrm0_blend_shape_group_dict["binds"] = []
                if "materialValues" not in vrm0_blend_shape_group_dict:
                    vrm0_blend_shape_group_dict["materialValues"] = []

    vrm0_secondary_animation = vrm0_extension.get("secondaryAnimation")
    if isinstance(vrm0_secondary_animation, dict):
        vrm0_collider_group_dicts = vrm0_secondary_animation.get("colliderGroups")
        if isinstance(vrm0_collider_group_dicts, list):

            def sort_collider_groups_with_index_key(
                collider_group_with_index: Tuple[int, Json]
            ) -> int:
                (_, collider_group) = collider_group_with_index
                if not isinstance(collider_group, dict):
                    return -999
                node = collider_group.get("node")
                if not isinstance(node, int):
                    return -999
                return node

            sorted_collider_groups_with_original_index = sorted(
                enumerate(vrm0_collider_group_dicts),
                key=sort_collider_groups_with_index_key,
            )
            vrm0_collider_group_dicts = [
                collider_group
                for _, collider_group in sorted_collider_groups_with_original_index
            ]
            original_index_to_sorted_index = {
                original_index: sorted_index
                for (sorted_index, (original_index, _)) in enumerate(
                    sorted_collider_groups_with_original_index
                )
            }

            vrm0_bone_groups = vrm0_secondary_animation.get("boneGroups")
            if isinstance(vrm0_bone_groups, list):
                for vrm0_bone_group in vrm0_bone_groups:
                    if not isinstance(vrm0_bone_group, dict):
                        continue
                    if "comment" not in vrm0_bone_group:
                        vrm0_bone_group["comment"] = ""
                    collider_groups = vrm0_bone_group.get("colliderGroups")
                    if not isinstance(collider_groups, list):
                        continue
                    for i, collider_group in enumerate(list(collider_groups)):
                        if not isinstance(collider_group, int):
                            continue
                        if collider_group not in original_index_to_sorted_index:
                            collider_groups[i] = -999
                            continue
                        collider_groups[i] = original_index_to_sorted_index[
                            collider_group
                        ]

    return vrm_json


def vrm_diff(before: bytes, after: bytes, float_tolerance: float) -> List[str]:
    return deep.diff(
        create_vrm_json_dict(before), create_vrm_json_dict(after), float_tolerance
    )
