import functools
import math
from typing import Optional

import bpy
from mathutils import Matrix, Quaternion

from ..common.logging import get_logger
from .mtoon1.property_group import Mtoon1MaterialPropertyGroup
from .node_constraint1.property_group import NodeConstraint1NodeConstraintPropertyGroup
from .property_group import StringPropertyGroup
from .spring_bone1.property_group import SpringBone1SpringBonePropertyGroup
from .vrm0.property_group import Vrm0HumanoidPropertyGroup, Vrm0PropertyGroup
from .vrm1.property_group import Vrm1HumanBonesPropertyGroup, Vrm1PropertyGroup

logger = get_logger(__name__)


class VrmAddonSceneExtensionPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    mesh_object_names: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=StringPropertyGroup
    )

    @staticmethod
    def check_mesh_object_names_and_update(
        scene_name: str,
        defer: bool = True,
    ) -> None:
        scene = bpy.data.scenes.get(scene_name)
        if not scene:
            logger.error(f'No scene "{scene_name}"')
            return
        ext = scene.vrm_addon_extension

        mesh_object_names = [obj.name for obj in bpy.data.objects if obj.type == "MESH"]
        up_to_date = mesh_object_names == ext.mesh_object_names[:]

        if up_to_date:
            return

        if defer:
            bpy.app.timers.register(
                functools.partial(
                    VrmAddonSceneExtensionPropertyGroup.check_mesh_object_names_and_update,
                    scene_name,
                    False,
                )
            )
            return

        ext.mesh_object_names.clear()
        for mesh_object_name in mesh_object_names:
            n = ext.mesh_object_names.add()
            n.value = mesh_object_name
            n.name = mesh_object_name  # for UI


class VrmAddonBoneExtensionPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    uuid: bpy.props.StringProperty()  # type: ignore[valid-type]

    AXIS_TRANSLATION_AUTO_ID = "AUTO"
    AXIS_TRANSLATION_NONE_ID = "NONE"
    AXIS_TRANSLATION_X_TO_Y_ID = "X_TO_Y"
    AXIS_TRANSLATION_MINUS_X_TO_Y_ID = "MINUS_X_TO_Y"
    AXIS_TRANSLATION_Z_TO_Y_ID = "Z_TO_Y"
    AXIS_TRANSLATION_MINUS_Z_TO_Y_ID = "MINUS_Z_TO_Y"
    AXIS_TRANSLATION_MINUS_Y_TO_Y_AROUND_Z_ID = "MINUS_Y_TO_Y_AROUND_Z"

    @classmethod
    def reverse_axis_translation(cls, axis_translation: str) -> str:
        return {
            cls.AXIS_TRANSLATION_AUTO_ID: cls.AXIS_TRANSLATION_AUTO_ID,
            cls.AXIS_TRANSLATION_NONE_ID: cls.AXIS_TRANSLATION_NONE_ID,
            cls.AXIS_TRANSLATION_X_TO_Y_ID: cls.AXIS_TRANSLATION_MINUS_X_TO_Y_ID,
            cls.AXIS_TRANSLATION_MINUS_X_TO_Y_ID: cls.AXIS_TRANSLATION_X_TO_Y_ID,
            cls.AXIS_TRANSLATION_Z_TO_Y_ID: cls.AXIS_TRANSLATION_MINUS_Z_TO_Y_ID,
            cls.AXIS_TRANSLATION_MINUS_Z_TO_Y_ID: cls.AXIS_TRANSLATION_Z_TO_Y_ID,
            cls.AXIS_TRANSLATION_MINUS_Y_TO_Y_AROUND_Z_ID: cls.AXIS_TRANSLATION_MINUS_Y_TO_Y_AROUND_Z_ID,
        }[axis_translation]

    @classmethod
    def node_constraint_roll_axis_translation(
        cls, axis_translation: str, roll_axis: Optional[str]
    ) -> Optional[str]:
        if roll_axis is None:
            return None
        return {
            cls.AXIS_TRANSLATION_AUTO_ID: {"X": "X", "Y": "Y", "Z": "Z"},
            cls.AXIS_TRANSLATION_NONE_ID: {"X": "X", "Y": "Y", "Z": "Z"},
            cls.AXIS_TRANSLATION_X_TO_Y_ID: {"X": "Y", "Y": "X", "Z": "Z"},
            cls.AXIS_TRANSLATION_MINUS_X_TO_Y_ID: {"X": "Y", "Y": "X", "Z": "Z"},
            cls.AXIS_TRANSLATION_Z_TO_Y_ID: {"X": "X", "Y": "Z", "Z": "Y"},
            cls.AXIS_TRANSLATION_MINUS_Z_TO_Y_ID: {"X": "X", "Y": "Z", "Z": "Y"},
            cls.AXIS_TRANSLATION_MINUS_Y_TO_Y_AROUND_Z_ID: {
                "X": "X",
                "Y": "Y",
                "Z": "Z",
            },
        }[axis_translation][roll_axis]

    @classmethod
    def node_constraint_aim_axis_translation(
        cls, axis_translation: str, aim_axis: Optional[str]
    ) -> Optional[str]:
        if aim_axis is None:
            return None
        return {
            cls.AXIS_TRANSLATION_AUTO_ID: {
                "PositiveX": "PositiveX",
                "PositiveY": "PositiveY",
                "PositiveZ": "PositiveZ",
                "NegativeX": "NegativeX",
                "NegativeY": "NegativeY",
                "NegativeZ": "NegativeZ",
            },
            cls.AXIS_TRANSLATION_NONE_ID: {
                "PositiveX": "PositiveX",
                "PositiveY": "PositiveY",
                "PositiveZ": "PositiveZ",
                "NegativeX": "NegativeX",
                "NegativeY": "NegativeY",
                "NegativeZ": "NegativeZ",
            },
            cls.AXIS_TRANSLATION_X_TO_Y_ID: {
                "PositiveX": "PositiveY",
                "PositiveY": "NegativeX",
                "PositiveZ": "PositiveZ",
                "NegativeX": "NegativeY",
                "NegativeY": "PositiveX",
                "NegativeZ": "NegativeZ",
            },
            cls.AXIS_TRANSLATION_MINUS_X_TO_Y_ID: {
                "PositiveY": "PositiveX",
                "NegativeX": "PositiveY",
                "PositiveZ": "PositiveZ",
                "NegativeY": "NegativeX",
                "PositiveX": "NegativeY",
                "NegativeZ": "NegativeZ",
            },
            cls.AXIS_TRANSLATION_Z_TO_Y_ID: {
                "PositiveX": "PositiveX",
                "PositiveY": "NegativeZ",
                "PositiveZ": "PositiveY",
                "NegativeX": "NegativeX",
                "NegativeY": "PositiveZ",
                "NegativeZ": "NegativeY",
            },
            cls.AXIS_TRANSLATION_MINUS_Z_TO_Y_ID: {
                "PositiveX": "PositiveX",
                "NegativeZ": "PositiveY",
                "PositiveY": "PositiveZ",
                "NegativeX": "NegativeX",
                "PositiveZ": "NegativeY",
                "NegativeY": "NegativeZ",
            },
            cls.AXIS_TRANSLATION_MINUS_Y_TO_Y_AROUND_Z_ID: {
                "PositiveX": "NegativeX",
                "PositiveY": "NegativeY",
                "PositiveZ": "PositiveZ",
                "NegativeX": "PositiveX",
                "NegativeY": "PositiveY",
                "NegativeZ": "NegativeZ",
            },
        }[axis_translation][aim_axis]

    @classmethod
    def translate_axis(cls, matrix: Matrix, axis_translation: str) -> Matrix:
        location, rotation, scale = matrix.decompose()

        if axis_translation == cls.AXIS_TRANSLATION_X_TO_Y_ID:
            rotation @= Quaternion((0, 0, 1), -math.pi / 2)
        elif axis_translation == cls.AXIS_TRANSLATION_MINUS_X_TO_Y_ID:
            rotation @= Quaternion((0, 0, 1), math.pi / 2)
        elif axis_translation == cls.AXIS_TRANSLATION_MINUS_Y_TO_Y_AROUND_Z_ID:
            rotation @= Quaternion((0, 0, 1), math.pi)
        elif axis_translation == cls.AXIS_TRANSLATION_Z_TO_Y_ID:
            rotation @= Quaternion((1, 0, 0), math.pi / 2)
        elif axis_translation == cls.AXIS_TRANSLATION_MINUS_Z_TO_Y_ID:
            rotation @= Quaternion((1, 0, 0), -math.pi / 2)

        # return Matrix.LocRotScale(location, rotation, scale)
        return (
            Matrix.Translation(location)
            @ rotation.to_matrix().to_4x4()
            @ Matrix.Scale(scale[0], 4, (1, 0, 0))
            @ Matrix.Scale(scale[1], 4, (0, 1, 0))
            @ Matrix.Scale(scale[2], 4, (0, 0, 1))
        )

    axis_translation_items = [
        (AXIS_TRANSLATION_AUTO_ID, "Auto", "", "NONE", 0),
        (AXIS_TRANSLATION_NONE_ID, "None", "", "NONE", 1),
        (AXIS_TRANSLATION_X_TO_Y_ID, "X,Y to Y,-X", "", "NONE", 2),
        (AXIS_TRANSLATION_MINUS_X_TO_Y_ID, "X,Y to -Y,X", "", "NONE", 3),
        (AXIS_TRANSLATION_MINUS_Y_TO_Y_AROUND_Z_ID, "X,Y to -X,-Y", "", "NONE", 4),
        (AXIS_TRANSLATION_Z_TO_Y_ID, "Y,Z to -Z,Y", "", "NONE", 5),
        (AXIS_TRANSLATION_MINUS_Z_TO_Y_ID, "Y,Z to Z,-Y", "", "NONE", 6),
    ]

    axis_translation: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=axis_translation_items,
        name="Axis Translation on Export",  # noqa: F722
    )


class VrmAddonObjectExtensionPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    axis_translation: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=VrmAddonBoneExtensionPropertyGroup.axis_translation_items,
        name="Axis Translation on Export",  # noqa: F722
    )


class VrmAddonArmatureExtensionPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    INITIAL_ADDON_VERSION = (0, 0, 0)

    addon_version: bpy.props.IntVectorProperty(  # type: ignore[valid-type]
        size=3,  # noqa: F722
        default=INITIAL_ADDON_VERSION,
    )

    vrm0: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm0PropertyGroup  # noqa: F722
    )

    vrm1: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1PropertyGroup  # noqa: F722
    )

    spring_bone1: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=SpringBone1SpringBonePropertyGroup  # noqa: F722
    )

    node_constraint1: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=NodeConstraint1NodeConstraintPropertyGroup  # noqa: F722
    )

    armature_data_name: bpy.props.StringProperty()  # type: ignore[valid-type]

    SPEC_VERSION_VRM0 = "0.0"
    SPEC_VERSION_VRM1 = "1.0"
    spec_version_items = [
        (SPEC_VERSION_VRM0, "VRM 0.0", "", "NONE", 0),
        (SPEC_VERSION_VRM1, "VRM 1.0 (EXPERIMENTAL)", "", "EXPERIMENTAL", 1),
    ]

    def __update_spec_version(self, _context: bpy.types.Context) -> None:
        if self.spec_version == self.SPEC_VERSION_VRM0:
            vrm0_hidden = False
            vrm1_hidden = True
        elif self.spec_version == self.SPEC_VERSION_VRM1:
            vrm0_hidden = True
            vrm1_hidden = False
        else:
            return

        for vrm0_collider in [
            collider.bpy_object
            for collider_group in self.vrm0.secondary_animation.collider_groups
            for collider in collider_group.colliders
            if collider.bpy_object
        ]:
            vrm0_collider.hide_set(vrm0_hidden)

        for vrm1_collider in [
            collider.bpy_object
            for collider in self.spring_bone1.colliders
            if collider.bpy_object
        ]:
            vrm1_collider.hide_set(vrm1_hidden)
            for child in vrm1_collider.children:
                child.hide_set(vrm1_hidden)

    spec_version: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=spec_version_items,
        name="Spec Version",  # noqa: F722
        update=__update_spec_version,
    )

    def is_vrm0(self) -> bool:
        return str(self.spec_version) == self.SPEC_VERSION_VRM0

    def is_vrm1(self) -> bool:
        return str(self.spec_version) == self.SPEC_VERSION_VRM1


def update_internal_cache(context: bpy.types.Context) -> None:
    VrmAddonSceneExtensionPropertyGroup.check_mesh_object_names_and_update(
        context.scene.name,
        defer=False,
    )
    for armature in bpy.data.armatures:
        Vrm0HumanoidPropertyGroup.check_last_bone_names_and_update(
            armature.name, defer=False
        )
        Vrm1HumanBonesPropertyGroup.check_last_bone_names_and_update(
            armature.name, defer=False
        )


class VrmAddonMaterialExtensionPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    mtoon1: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1MaterialPropertyGroup  # noqa: F722
    )
