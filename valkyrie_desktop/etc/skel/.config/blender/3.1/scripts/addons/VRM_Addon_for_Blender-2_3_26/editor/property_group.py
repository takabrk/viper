import uuid
from typing import Any, Dict, Iterator, Set, Union

import bpy

from ..common.char import INTERNAL_NAME_PREFIX
from ..common.human_bone import (
    HumanBoneName,
    HumanBoneSpecification,
    HumanBoneSpecifications,
)


class StringPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    value: bpy.props.StringProperty(  # type: ignore[valid-type]
        name="String Value"  # noqa: F722
    )


class FloatPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    value: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Float Value"  # noqa: F722
    )


class MeshObjectPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    def __get_value(self) -> str:
        if (
            not self.bpy_object
            or not self.bpy_object.name
            or self.bpy_object.type != "MESH"
        ):
            return ""
        return str(self.bpy_object.name)

    def __set_value(self, value: Any) -> None:
        if (
            not isinstance(value, str)
            or value not in bpy.data.objects
            or bpy.data.objects[value].type != "MESH"
        ):
            self.bpy_object = None
            return
        self.bpy_object = bpy.data.objects[value]

    value: bpy.props.StringProperty(  # type: ignore[valid-type]
        get=__get_value, set=__set_value
    )

    bpy_object: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Object  # noqa: F722
    )


class BonePropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    @staticmethod
    def get_all_bone_property_groups(
        armature: bpy.types.Object,
    ) -> Iterator[bpy.types.PropertyGroup]:
        ext = armature.data.vrm_addon_extension
        yield ext.vrm0.first_person.first_person_bone
        for human_bone in ext.vrm0.humanoid.human_bones:
            yield human_bone.node
        for collider_group in ext.vrm0.secondary_animation.collider_groups:
            yield collider_group.node
        for bone_group in ext.vrm0.secondary_animation.bone_groups:
            yield bone_group.center
            yield from bone_group.bones
        for (
            human_bone
        ) in ext.vrm1.humanoid.human_bones.human_bone_name_to_human_bone().values():
            yield human_bone.node
        for collider in ext.spring_bone1.colliders:
            yield collider.node
        for spring in ext.spring_bone1.springs:
            for joint in spring.joints:
                yield joint.node

    @staticmethod
    def find_bone_candidates(
        armature_data: bpy.types.Armature,
        target: HumanBoneSpecification,
        bpy_bone_name_to_human_bone_specification: Dict[str, HumanBoneSpecification],
    ) -> Set[str]:
        bones: Union[Dict[str, bpy.types.Bone], Dict[str, bpy.types.EditBone]] = {}
        if armature_data.is_editmode:
            bones = armature_data.edit_bones
        else:
            bones = armature_data.bones
        result: Set[str] = set(bones.keys())
        remove_bones_tree: Union[Set[bpy.types.Bone], Set[bpy.types.EditBone]] = set()

        for (
            bpy_bone_name,
            human_bone_specification,
        ) in bpy_bone_name_to_human_bone_specification.items():
            if human_bone_specification == target:
                continue

            if human_bone_specification.is_ancestor_of(target):
                remove_ancestors = True
                remove_ancestor_branches = True
            elif target.is_ancestor_of(human_bone_specification):
                remove_bones_tree.add(bones[bpy_bone_name])
                remove_ancestors = False
                remove_ancestor_branches = True
            else:
                remove_bones_tree.add(bones[bpy_bone_name])
                remove_ancestors = True
                remove_ancestor_branches = False

            parent = bones[bpy_bone_name]
            while True:
                if remove_ancestors and parent.name in result:
                    result.remove(parent.name)
                grand_parent = parent.parent
                if not grand_parent:
                    if remove_ancestor_branches:
                        remove_bones_tree.update(
                            bone
                            for bone in bones.values()
                            if not bone.parent and bone != parent
                        )
                    break

                if remove_ancestor_branches:
                    for grand_parent_child in grand_parent.children:
                        if grand_parent_child != parent:
                            remove_bones_tree.add(grand_parent_child)

                parent = grand_parent

        while remove_bones_tree:
            child = remove_bones_tree.pop()
            if child.name in result:
                result.remove(child.name)
            remove_bones_tree.update(child.children)

        return result

    def refresh(self, armature: bpy.types.Object) -> None:
        if (
            self.link_to_bone
            and self.link_to_bone.parent
            and self.link_to_bone.parent == armature
        ):
            return

        value = self.value
        uuid_str = uuid.uuid4().hex
        self.link_to_bone = bpy.data.objects.new(
            name=INTERNAL_NAME_PREFIX + "VrmAddonLinkToBone" + uuid_str,
            object_data=None,
        )
        self.link_to_bone.hide_render = True
        self.link_to_bone.hide_select = True
        self.link_to_bone.hide_viewport = True
        self.link_to_bone.parent = armature
        self.value = value

    def __get_value(self) -> str:
        if (
            self.link_to_bone
            and self.link_to_bone.parent_bone
            and self.link_to_bone.parent
            and self.link_to_bone.parent.name
            and self.link_to_bone.parent.type == "ARMATURE"
            and self.link_to_bone.parent_bone in self.link_to_bone.parent.data.bones
        ):
            return str(self.link_to_bone.parent_bone)
        return ""

    def __set_value(self, value: Any) -> None:
        if not self.link_to_bone or not self.link_to_bone.parent:
            # Armatureごとコピーされた場合UUIDもコピーされるため毎回生成しなおす必要がある
            self.search_one_time_uuid = uuid.uuid4().hex
            for armature in bpy.data.objects:
                if armature.type != "ARMATURE":
                    continue
                if all(
                    bone_property_group.search_one_time_uuid
                    != self.search_one_time_uuid
                    for bone_property_group in BonePropertyGroup.get_all_bone_property_groups(
                        armature
                    )
                ):
                    continue
                self.refresh(armature)
                break
        if not self.link_to_bone or not self.link_to_bone.parent:
            print("WARNING: No armature found")
            return

        value_str = str(value)
        if not value_str or value_str not in self.link_to_bone.parent.data.bones:
            if self.link_to_bone.parent_type != "OBJECT":
                self.link_to_bone.parent_type = "OBJECT"
            if not self.link_to_bone.parent_bone:
                return
            self.link_to_bone.parent_bone = ""
        elif self.link_to_bone.parent_bone == value_str:
            return
        else:
            if self.link_to_bone.parent_type != "BONE":
                self.link_to_bone.parent_type = "BONE"
            self.link_to_bone.parent_bone = value_str

        armature_data = self.link_to_bone.parent.data
        ext = armature_data.vrm_addon_extension
        for collider_group in ext.vrm0.secondary_animation.collider_groups:
            collider_group.refresh(self.link_to_bone.parent)

        vrm0_bpy_bone_name_to_human_bone_specification: Dict[
            str, HumanBoneSpecification
        ] = {
            human_bone.node.value: HumanBoneSpecifications.get(
                HumanBoneName(human_bone.bone)
            )
            for human_bone in ext.vrm0.humanoid.human_bones
            if human_bone.node.value
            and HumanBoneName.from_str(human_bone.bone) is not None
        }

        for human_bone in ext.vrm0.humanoid.human_bones:
            human_bone.update_node_candidates(
                armature_data,
                vrm0_bpy_bone_name_to_human_bone_specification,
            )

        human_bone_name_to_human_bone = (
            ext.vrm1.humanoid.human_bones.human_bone_name_to_human_bone()
        )
        vrm1_bpy_bone_name_to_human_bone_specification: Dict[
            str, HumanBoneSpecification
        ] = {
            human_bone.node.value: HumanBoneSpecifications.get(human_bone_name)
            for human_bone_name, human_bone in human_bone_name_to_human_bone.items()
            if human_bone.node.value
        }

        for (
            human_bone_name,
            human_bone,
        ) in human_bone_name_to_human_bone.items():
            human_bone.update_node_candidates(
                armature_data,
                HumanBoneSpecifications.get(human_bone_name),
                vrm1_bpy_bone_name_to_human_bone_specification,
            )

    value: bpy.props.StringProperty(  # type: ignore[valid-type]
        name="Bone",  # noqa: F821
        get=__get_value,
        set=__set_value,
    )
    link_to_bone: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Object  # noqa: F722
    )
    search_one_time_uuid: bpy.props.StringProperty()  # type: ignore[valid-type]
