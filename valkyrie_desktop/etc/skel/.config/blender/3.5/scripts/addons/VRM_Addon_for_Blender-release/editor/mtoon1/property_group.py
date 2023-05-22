import functools
import re
from collections import abc
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import bpy
import mathutils

from ...common import shader
from ...common.logging import get_logger

logger = get_logger(__name__)


class MaterialTraceablePropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    def find_material(self) -> bpy.types.Material:
        if self.id_data.is_evaluated:
            logger.error(f"{self} is evaluated. May cause a problem.")

        chain = self.get_material_property_chain()
        for material in bpy.data.materials:
            if not material:
                continue
            ext = material.vrm_addon_extension.mtoon1
            if functools.reduce(getattr, chain, ext) == self:
                return material

        raise AssertionError(f"No matching material: {type(self)} {chain}")

    @classmethod
    def get_material_property_chain(cls) -> List[str]:
        chain = getattr(cls, "material_property_chain", None)
        if not isinstance(chain, list):
            raise NotImplementedError(
                f"No material property chain: {cls}.{type(chain)} => {chain}",
            )
        result: List[str] = []
        for property_name in list(chain):
            if isinstance(property_name, str):
                result.append(property_name)
                continue
            raise AssertionError(
                f"Invalid material property chain: {cls}.{type(chain)} => {chain}",
            )
        return result

    @classmethod
    def find_outline_property_group(
        cls, material: bpy.types.Material
    ) -> Optional[bpy.types.PropertyGroup]:
        mtoon1 = material.vrm_addon_extension.mtoon1
        if mtoon1.is_outline_material:
            return None
        outline_material = mtoon1.outline_material
        if not outline_material:
            return None
        if material.name == outline_material.name:
            logger.error(
                "Base material and outline material are same. name={material.name}"
            )
            return None
        chain = cls.get_material_property_chain()
        property_group = functools.reduce(
            getattr, chain, outline_material.vrm_addon_extension.mtoon1
        )
        if isinstance(property_group, bpy.types.PropertyGroup):
            return property_group
        raise AssertionError(f"No matching property group: {cls} {chain}")

    def set_value(
        self,
        name: str,
        value: object,
    ) -> None:
        if not isinstance(value, (int, float)):
            return
        node_name = self.get_node_name(name)
        material = self.find_material()
        node_tree = material.node_tree
        if not node_tree:
            return
        node = node_tree.nodes.get(node_name)
        if not isinstance(node, bpy.types.ShaderNodeValue):
            logger.warning(f'No shader node value "{node_name}" for "{material.name}"')
            return
        node.outputs[0].default_value = value

        outline = self.find_outline_property_group(material)
        if outline:
            outline.set_value(name, value)

    def set_bool(
        self,
        name: str,
        value: object,
    ) -> None:
        self.set_value(name, 1 if value else 0)

    def set_int(
        self,
        name: str,
        value: object,
    ) -> None:
        self.set_value(name, value)

    def set_rgba(
        self,
        name: str,
        value: object,
        default_value: Optional[Tuple[float, float, float, float]] = None,
    ) -> None:
        if not default_value:
            default_value = (0.0, 0.0, 0.0, 0.0)
        node_name = self.get_node_name(name)
        material = self.find_material()
        node = material.node_tree.nodes.get(node_name)
        if not isinstance(node, bpy.types.ShaderNodeRGB):
            logger.warning(f'No shader node rgb "{node_name}"')
            return
        if not isinstance(value, abc.Iterable):
            node.outputs[0].default_value = default_value
            return
        list_value = list(value)
        if len(list_value) < 4:
            node.outputs[0].default_value = default_value
            return
        list_value = list_value[0:4]
        node.outputs[0].default_value = list_value

        outline = self.find_outline_property_group(material)
        if outline:
            outline.set_rgba(name, value, default_value)

    def set_rgb(
        self,
        name: str,
        value: object,
        default_value: Optional[Tuple[float, float, float]] = None,
    ) -> None:
        if not default_value:
            default_value = (0.0, 0.0, 0.0)
        node_name = self.get_node_name(name)
        material = self.find_material()
        node = material.node_tree.nodes.get(node_name)
        if not isinstance(node, bpy.types.ShaderNodeRGB):
            logger.warning(f'No shader node rgb "{node_name}"')
            return
        if isinstance(value, mathutils.Color):
            value = [value.r, value.g, value.b]
        elif not isinstance(value, abc.Iterable):
            node.outputs[0].default_value = default_value + (1.0,)
            return
        list_value = list(value)
        if len(list_value) < 3:
            node.outputs[0].default_value = default_value + (1.0,)
            return
        list_value = list_value[0:3]
        list_value.append(1.0)
        node.outputs[0].default_value = list_value

        outline = self.find_outline_property_group(material)
        if outline:
            outline.set_rgb(name, value, default_value)

    def get_node_name(self, extra: Optional[str] = None) -> str:
        base = re.sub("PropertyGroup$", "", type(self).__name__)
        if extra is not None:
            return base + "." + extra
        return base

    def link_reroutes(self, base_node_name: str, connect: bool) -> None:
        material = self.find_material()
        node_tree = material.node_tree
        in_node_name = base_node_name + "In"
        in_node = node_tree.nodes.get(in_node_name)
        out_node_name = base_node_name + "Out"
        out_node = node_tree.nodes.get(out_node_name)
        if not isinstance(in_node, bpy.types.NodeReroute):
            # logger.warning(f'No node reroute "{in_node_name}"')
            return
        if not isinstance(out_node, bpy.types.NodeReroute):
            logger.warning(f'No node reroute "{out_node_name}"')
            return

        if connect:
            if not any(
                1
                for link in node_tree.links
                if link.to_socket == in_node.inputs[0]
                and link.from_socket == out_node.outputs[0]
            ):
                node_tree.links.new(in_node.inputs[0], out_node.outputs[0])
            return

        while True:
            disconnecting_link = {
                0: link
                for link in node_tree.links
                if link.to_socket == in_node.inputs[0]
                and link.from_socket == out_node.outputs[0]
            }.get(0)
            if not disconnecting_link:
                break
            node_tree.links.remove(disconnecting_link)

        outline = self.find_outline_property_group(material)
        if outline:
            outline.link_reroutes(base_node_name, connect)

    def switch_link_reroutes(self, base_node_name: str, up: bool) -> None:
        material = self.find_material()
        node_tree = material.node_tree
        in_node_name = base_node_name + "SwitchIn"
        in_node = node_tree.nodes.get(in_node_name)
        down_node_name = base_node_name + "SwitchDown"
        down_node = node_tree.nodes.get(down_node_name)
        up_node_name = base_node_name + "SwitchUp"
        up_node = node_tree.nodes.get(up_node_name)

        if not isinstance(in_node, bpy.types.NodeReroute):
            logger.warning(f'No node reroute "{in_node_name}"')
            return
        if not isinstance(down_node, bpy.types.NodeReroute):
            logger.warning(f'No node reroute "{down_node_name}"')
            return
        if not isinstance(up_node, bpy.types.NodeReroute):
            logger.warning(f'No node reroute "{up_node_name}"')
            return

        while True:
            disconnecting_socket = down_node.outputs[0] if up else up_node.outputs[0]
            disconnecting_link = {
                0: link
                for link in node_tree.links
                if link.to_socket == in_node.inputs[0]
                and link.from_socket == disconnecting_socket
            }.get(0)
            if not disconnecting_link:
                break
            node_tree.links.remove(disconnecting_link)

        connecting_socket = up_node.outputs[0] if up else down_node.outputs[0]
        if not any(
            1
            for link in node_tree.links
            if link.to_socket == in_node.inputs[0]
            and link.from_socket == connecting_socket
        ):
            node_tree.links.new(in_node.inputs[0], connecting_socket)

        outline = self.find_outline_property_group(material)
        if outline:
            outline.switch_link_reroutes(base_node_name, up)


class TextureTraceablePropertyGroup(MaterialTraceablePropertyGroup):
    def get_texture_info_property_group(self) -> "Mtoon1TextureInfoPropertyGroup":
        chain = self.get_material_property_chain()
        if chain[-1:] == ["sampler"]:
            chain = chain[:-1]
        if chain[-1:] == ["index"]:
            chain = chain[:-1]
        if chain[-1:] == ["khr_texture_transform"]:
            chain = chain[:-1]
        if chain[-1:] == ["extensions"]:
            chain = chain[:-1]
        material = self.find_material()
        ext = material.vrm_addon_extension.mtoon1
        property_group = functools.reduce(getattr, chain, ext)
        if not isinstance(property_group, Mtoon1TextureInfoPropertyGroup):
            raise ValueError(
                f"{property_group} is not a Mtoon1TextureInfoPropertyGroup"
            )
        return property_group

    def get_texture_node_name(self, extra: str) -> str:
        texture_info = self.get_texture_info_property_group()
        name = type(texture_info.index).__name__
        return re.sub("PropertyGroup$", "", name) + "." + extra

    def update_image(self, image: Optional[bpy.types.Image]) -> None:
        node_name = self.get_texture_node_name("Image")
        material = self.find_material()
        node_tree = material.node_tree
        node = node_tree.nodes.get(node_name)
        if not isinstance(node, bpy.types.ShaderNodeTexImage):
            logger.warning(f'No shader node tex image "{node_name}"')
            return
        node.image = image

        self.set_texture_uv("Image Width", max(image.size[0], 1) if image else 1)
        self.set_texture_uv("Image Height", max(image.size[1], 1) if image else 1)

        self.link_reroutes(self.get_texture_node_name("Color"), bool(node.image))
        self.link_reroutes(self.get_texture_node_name("Alpha"), bool(node.image))

        outline = self.find_outline_property_group(material)
        if outline:
            outline.update_image(image)

    def set_texture_uv(self, name: str, value: object) -> None:
        node_name = self.get_texture_node_name("Uv")
        material = self.find_material()
        node_tree = material.node_tree
        node = node_tree.nodes.get(node_name)
        if not isinstance(node, bpy.types.ShaderNodeGroup):
            logger.warning(f'No shader node group "{node_name}"')
            return
        socket = node.inputs.get(name)
        if not socket:
            logger.warning(f'No "{name}" in shader node group "{node_name}"')
            return

        socket.default_value = value

        outline = self.find_outline_property_group(material)
        if outline:
            outline.set_texture_uv(name, value)


class Mtoon1KhrTextureTransformPropertyGroup(TextureTraceablePropertyGroup):
    def update_texture_offset(self, _context: bpy.types.Context) -> None:
        self.set_texture_uv("UV Offset X", self.offset[0])
        self.set_texture_uv("UV Offset Y", self.offset[1])

        node_name = self.get_texture_node_name("Image")
        material = self.find_material()
        node = material.node_tree.nodes.get(node_name)
        if not isinstance(node, bpy.types.ShaderNodeTexImage):
            logger.warning(f'No shader node tex image "{node_name}"')
            return
        node.texture_mapping.translation = (0, 0, 0)

        outline = self.find_outline_property_group(material)
        if outline:
            outline.update_texture_offset(_context)

    def update_texture_scale(self, _context: bpy.types.Context) -> None:
        self.set_texture_uv("UV Scale X", self.scale[0])
        self.set_texture_uv("UV Scale Y", self.scale[1])

        node_name = self.get_texture_node_name("Image")
        material = self.find_material()
        node = material.node_tree.nodes.get(node_name)
        if not isinstance(node, bpy.types.ShaderNodeTexImage):
            logger.warning(f'No shader node tex image "{node_name}"')
            return
        node.texture_mapping.scale = (1, 1, 1)

        outline = self.find_outline_property_group(material)
        if outline:
            outline.update_texture_scale(_context)


class Mtoon1BaseColorKhrTextureTransformPropertyGroup(
    Mtoon1KhrTextureTransformPropertyGroup
):
    material_property_chain = [
        "pbr_metallic_roughness",
        "base_color_texture",
        "extensions",
        "khr_texture_transform",
    ]

    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset",  # noqa: F821
        size=2,
        default=(0, 0),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_offset,
    )

    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        size=2,
        default=(1, 1),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_scale,
    )


class Mtoon1ShadeMultiplyKhrTextureTransformPropertyGroup(
    Mtoon1KhrTextureTransformPropertyGroup
):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "shade_multiply_texture",
        "extensions",
        "khr_texture_transform",
    ]

    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset",  # noqa: F821
        size=2,
        default=(0, 0),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_offset,
    )

    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        size=2,
        default=(1, 1),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_scale,
    )


class Mtoon1NormalKhrTextureTransformPropertyGroup(
    Mtoon1KhrTextureTransformPropertyGroup
):
    material_property_chain = [
        "normal_texture",
        "extensions",
        "khr_texture_transform",
    ]

    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset",  # noqa: F821
        size=2,
        default=(0, 0),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_offset,
    )

    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        size=2,
        default=(1, 1),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_scale,
    )


class Mtoon1ShadingShiftKhrTextureTransformPropertyGroup(
    Mtoon1KhrTextureTransformPropertyGroup
):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "shading_shift_texture",
        "extensions",
        "khr_texture_transform",
    ]

    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset",  # noqa: F821
        size=2,
        default=(0, 0),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_offset,
    )

    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        size=2,
        default=(1, 1),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_scale,
    )


class Mtoon1EmissiveKhrTextureTransformPropertyGroup(
    Mtoon1KhrTextureTransformPropertyGroup
):
    material_property_chain = [
        "emissive_texture",
        "extensions",
        "khr_texture_transform",
    ]

    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset",  # noqa: F821
        size=2,
        default=(0, 0),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_offset,
    )

    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        size=2,
        default=(1, 1),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_scale,
    )


class Mtoon1RimMultiplyKhrTextureTransformPropertyGroup(
    Mtoon1KhrTextureTransformPropertyGroup
):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "rim_multiply_texture",
        "extensions",
        "khr_texture_transform",
    ]

    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset",  # noqa: F821
        size=2,
        default=(0, 0),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_offset,
    )

    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        size=2,
        default=(1, 1),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_scale,
    )


class Mtoon1MatcapKhrTextureTransformPropertyGroup(
    Mtoon1KhrTextureTransformPropertyGroup
):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "matcap_texture",
        "extensions",
        "khr_texture_transform",
    ]

    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset",  # noqa: F821
        size=2,
        default=(0, 0),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_offset,
    )

    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        size=2,
        default=(1, 1),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_scale,
    )


class Mtoon1OutlineWidthMultiplyKhrTextureTransformPropertyGroup(
    Mtoon1KhrTextureTransformPropertyGroup
):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "outline_width_multiply_texture",
        "extensions",
        "khr_texture_transform",
    ]

    def update_texture_offset_and_outline(self, context: bpy.types.Context) -> None:
        material = self.find_material()
        if material.vrm_addon_extension.mtoon1.is_outline_material:
            return
        self.update_texture_offset(context)
        bpy.ops.vrm.refresh_mtoon1_outline(material_name=material.name)

    def update_texture_scale_and_outline(self, context: bpy.types.Context) -> None:
        material = self.find_material()
        if material.vrm_addon_extension.mtoon1.is_outline_material:
            return
        self.update_texture_scale(context)
        bpy.ops.vrm.refresh_mtoon1_outline(material_name=material.name)

    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset",  # noqa: F821
        size=2,
        default=(0, 0),
        update=update_texture_offset_and_outline,
    )

    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        size=2,
        default=(1, 1),
        update=update_texture_scale_and_outline,
    )


class Mtoon1UvAnimationMaskKhrTextureTransformPropertyGroup(
    Mtoon1KhrTextureTransformPropertyGroup
):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "uv_animation_mask_texture",
        "extensions",
        "khr_texture_transform",
    ]

    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset",  # noqa: F821
        size=2,
        default=(0, 0),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_offset,
    )

    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        size=2,
        default=(1, 1),
        update=Mtoon1KhrTextureTransformPropertyGroup.update_texture_scale,
    )


class Mtoon1BaseColorTextureInfoExtensionsPropertyGroup(
    bpy.types.PropertyGroup  # type: ignore[misc]
):
    khr_texture_transform: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1BaseColorKhrTextureTransformPropertyGroup  # noqa: F722
    )


class Mtoon1ShadeMultiplyTextureInfoExtensionsPropertyGroup(
    bpy.types.PropertyGroup  # type: ignore[misc]
):
    khr_texture_transform: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadeMultiplyKhrTextureTransformPropertyGroup  # noqa: F722
    )


class Mtoon1NormalTextureInfoExtensionsPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    khr_texture_transform: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1NormalKhrTextureTransformPropertyGroup  # noqa: F722
    )


class Mtoon1ShadingShiftTextureInfoExtensionsPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    khr_texture_transform: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadingShiftKhrTextureTransformPropertyGroup  # noqa: F722
    )


class Mtoon1EmissiveTextureInfoExtensionsPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    khr_texture_transform: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1EmissiveKhrTextureTransformPropertyGroup  # noqa: F722
    )


class Mtoon1RimMultiplyTextureInfoExtensionsPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    khr_texture_transform: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1RimMultiplyKhrTextureTransformPropertyGroup  # noqa: F722
    )


class Mtoon1MatcapTextureInfoExtensionsPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    khr_texture_transform: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1MatcapKhrTextureTransformPropertyGroup  # noqa: F722
    )


class Mtoon1OutlineWidthMultiplyTextureInfoExtensionsPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    khr_texture_transform: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1OutlineWidthMultiplyKhrTextureTransformPropertyGroup  # noqa: F722
    )


class Mtoon1UvAnimationMaskTextureInfoExtensionsPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    khr_texture_transform: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1UvAnimationMaskKhrTextureTransformPropertyGroup  # noqa: F722
    )


class Mtoon1SamplerPropertyGroup(TextureTraceablePropertyGroup):
    mag_filter_items = [
        ("NEAREST", "Nearest", "", 9728),
        ("LINEAR", "Linear", "", 9729),
    ]
    MAG_FILTER_NUMBER_TO_ID: Dict[int, str] = {
        filter[-1]: filter[0] for filter in mag_filter_items
    }
    MAG_FILTER_ID_TO_NUMBER: Dict[str, int] = {
        filter[0]: filter[-1] for filter in mag_filter_items
    }

    def get_mag_filter(self) -> int:
        value = self.get("mag_filter")
        if value in self.MAG_FILTER_NUMBER_TO_ID:
            return int(value)
        return list(self.MAG_FILTER_NUMBER_TO_ID.keys())[0]

    def set_mag_filter(self, value: int) -> None:
        if value not in self.MAG_FILTER_NUMBER_TO_ID:
            return
        self["mag_filter"] = value

    min_filter_items = [
        ("NEAREST", "Nearest", "", 9728),
        ("LINEAR", "Linear", "", 9729),
        (
            "NEAREST_MIPMAP_NEAREST",
            "Nearest Mipmap Nearest",
            "",
            9984,
        ),
        (
            "LINEAR_MIPMAP_NEAREST",
            "Linear Mipmap Nearest",
            "",
            9985,
        ),
        (
            "NEAREST_MIPMAP_LINEAR",
            "Nearest Mipmap Linear",
            "",
            9986,
        ),
        (
            "LINEAR_MIPMAP_LINEAR",
            "Linear Mipmap Linear",
            "",
            9987,
        ),
    ]
    MIN_FILTER_NUMBER_TO_ID: Dict[int, str] = {
        filter[-1]: filter[0] for filter in min_filter_items
    }
    MIN_FILTER_ID_TO_NUMBER: Dict[str, int] = {
        filter[0]: filter[-1] for filter in min_filter_items
    }

    # https://github.com/KhronosGroup/glTF/blob/2a9996a2ea66ab712590eaf62f39f1115996f5a3/specification/2.0/schema/sampler.schema.json#L67-L117
    WRAP_DEFAULT_NUMBER = 10497
    WRAP_DEFAULT_ID = "REPEAT"

    wrap_items = [
        ("CLAMP_TO_EDGE", "Clamp to Edge", "", 33071),
        ("MIRRORED_REPEAT", "Mirrored Repeat", "", 33648),
        (WRAP_DEFAULT_ID, "Repeat", "", WRAP_DEFAULT_NUMBER),
    ]
    WRAP_NUMBER_TO_ID: Dict[int, str] = {wrap[-1]: wrap[0] for wrap in wrap_items}
    WRAP_ID_TO_NUMBER: Dict[str, int] = {wrap[0]: wrap[-1] for wrap in wrap_items}

    def update_wrap_s(self, _context: bpy.types.Context) -> None:
        wrap_s = self.WRAP_ID_TO_NUMBER.get(self.wrap_s, self.WRAP_DEFAULT_NUMBER)
        self.set_texture_uv("Wrap S", wrap_s)

    def update_wrap_t(self, _context: bpy.types.Context) -> None:
        wrap_t = self.WRAP_ID_TO_NUMBER.get(self.wrap_t, self.WRAP_DEFAULT_NUMBER)
        self.set_texture_uv("Wrap T", wrap_t)


class Mtoon1BaseColorSamplerPropertyGroup(Mtoon1SamplerPropertyGroup):
    material_property_chain = [
        "pbr_metallic_roughness",
        "base_color_texture",
        "index",
        "sampler",
    ]

    mag_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.mag_filter_items,
        name="Mag Filter",  # noqa: F722
    )

    min_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.min_filter_items,
        name="Min Filter",  # noqa: F722
    )

    wrap_s: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap S",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_s,
    )

    wrap_t: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap T",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_t,
    )


class Mtoon1ShadeMultiplySamplerPropertyGroup(Mtoon1SamplerPropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "shade_multiply_texture",
        "index",
        "sampler",
    ]

    mag_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.mag_filter_items,
        name="Mag Filter",  # noqa: F722
    )

    min_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.min_filter_items,
        name="Min Filter",  # noqa: F722
    )

    wrap_s: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap S",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_s,
    )

    wrap_t: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap T",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_t,
    )


class Mtoon1NormalSamplerPropertyGroup(Mtoon1SamplerPropertyGroup):
    material_property_chain = [
        "normal_texture",
        "index",
        "sampler",
    ]

    mag_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.mag_filter_items,
        name="Mag Filter",  # noqa: F722
    )

    min_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.min_filter_items,
        name="Min Filter",  # noqa: F722
    )

    wrap_s: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap S",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_s,
    )

    wrap_t: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap T",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_t,
    )


class Mtoon1ShadingShiftSamplerPropertyGroup(Mtoon1SamplerPropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "shading_shift_texture",
        "index",
        "sampler",
    ]

    mag_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.mag_filter_items,
        name="Mag Filter",  # noqa: F722
    )

    min_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.min_filter_items,
        name="Min Filter",  # noqa: F722
    )

    wrap_s: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap S",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_s,
    )

    wrap_t: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap T",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_t,
    )


class Mtoon1EmissiveSamplerPropertyGroup(Mtoon1SamplerPropertyGroup):
    material_property_chain = [
        "emissive_texture",
        "index",
        "sampler",
    ]

    mag_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.mag_filter_items,
        name="Mag Filter",  # noqa: F722
    )

    min_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.min_filter_items,
        name="Min Filter",  # noqa: F722
    )

    wrap_s: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap S",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_s,
    )

    wrap_t: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap T",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_t,
    )


class Mtoon1RimMultiplySamplerPropertyGroup(Mtoon1SamplerPropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "rim_multiply_texture",
        "index",
        "sampler",
    ]

    mag_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.mag_filter_items,
        name="Mag Filter",  # noqa: F722
    )

    min_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.min_filter_items,
        name="Min Filter",  # noqa: F722
    )

    wrap_s: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap S",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_s,
    )

    wrap_t: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap T",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_t,
    )


class Mtoon1MatcapSamplerPropertyGroup(Mtoon1SamplerPropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "matcap_texture",
        "index",
        "sampler",
    ]

    mag_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.mag_filter_items,
        name="Mag Filter",  # noqa: F722
    )

    min_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.min_filter_items,
        name="Min Filter",  # noqa: F722
    )

    wrap_s: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap S",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_s,
    )

    wrap_t: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap T",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_t,
    )


class Mtoon1OutlineWidthMultiplySamplerPropertyGroup(Mtoon1SamplerPropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "outline_width_multiply_texture",
        "index",
        "sampler",
    ]

    mag_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.mag_filter_items,
        name="Mag Filter",  # noqa: F722
    )

    min_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.min_filter_items,
        name="Min Filter",  # noqa: F722
    )

    wrap_s: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap S",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_s,
    )

    wrap_t: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap T",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_t,
    )


class Mtoon1UvAnimationMaskSamplerPropertyGroup(Mtoon1SamplerPropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "uv_animation_mask_texture",
        "index",
        "sampler",
    ]

    mag_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.mag_filter_items,
        name="Mag Filter",  # noqa: F722
    )

    min_filter: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.min_filter_items,
        name="Min Filter",  # noqa: F722
    )

    wrap_s: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap S",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_s,
    )

    wrap_t: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=Mtoon1SamplerPropertyGroup.wrap_items,
        name="Wrap T",  # noqa: F722
        default=Mtoon1SamplerPropertyGroup.WRAP_DEFAULT_ID,
        update=Mtoon1SamplerPropertyGroup.update_wrap_t,
    )


class Mtoon1TexturePropertyGroup(TextureTraceablePropertyGroup):
    def update_source(self, _context: bpy.types.Context) -> None:
        self.update_image(self.source)


class Mtoon1BaseColorTexturePropertyGroup(Mtoon1TexturePropertyGroup):
    material_property_chain = [
        "pbr_metallic_roughness",
        "base_color_texture",
        "index",
    ]

    source: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Image,  # noqa: F722
        update=Mtoon1TexturePropertyGroup.update_source,
    )

    sampler: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1BaseColorSamplerPropertyGroup  # noqa: F722
    )


class Mtoon1ShadeMultiplyTexturePropertyGroup(Mtoon1TexturePropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "shade_multiply_texture",
        "index",
    ]

    source: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Image,  # noqa: F722
        update=Mtoon1TexturePropertyGroup.update_source,
    )

    sampler: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadeMultiplySamplerPropertyGroup  # noqa: F722
    )


class Mtoon1NormalTexturePropertyGroup(Mtoon1TexturePropertyGroup):
    material_property_chain = [
        "normal_texture",
        "index",
    ]

    def update_source(self, _context: bpy.types.Context) -> None:
        self.switch_link_reroutes(self.get_node_name("Normal"), up=bool(self.source))
        self.update_image(self.source)

    source: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Image,  # noqa: F722
        update=update_source,
    )

    sampler: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1NormalSamplerPropertyGroup  # noqa: F722
    )


class Mtoon1ShadingShiftTexturePropertyGroup(Mtoon1TexturePropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "shading_shift_texture",
        "index",
    ]

    source: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Image,  # noqa: F722
        update=Mtoon1TexturePropertyGroup.update_source,
    )

    sampler: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadingShiftSamplerPropertyGroup  # noqa: F722
    )


class Mtoon1EmissiveTexturePropertyGroup(Mtoon1TexturePropertyGroup):
    material_property_chain = [
        "emissive_texture",
        "index",
    ]

    source: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Image,  # noqa: F722
        update=Mtoon1TexturePropertyGroup.update_source,
    )

    sampler: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1EmissiveSamplerPropertyGroup  # noqa: F722
    )


class Mtoon1RimMultiplyTexturePropertyGroup(Mtoon1TexturePropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "rim_multiply_texture",
        "index",
    ]

    source: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Image,  # noqa: F722
        update=Mtoon1TexturePropertyGroup.update_source,
    )

    sampler: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1RimMultiplySamplerPropertyGroup  # noqa: F722
    )


class Mtoon1MatcapTexturePropertyGroup(Mtoon1TexturePropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "matcap_texture",
        "index",
    ]

    source: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Image,  # noqa: F722
        update=Mtoon1TexturePropertyGroup.update_source,
    )

    sampler: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1MatcapSamplerPropertyGroup  # noqa: F722
    )


class Mtoon1OutlineWidthMultiplyTexturePropertyGroup(Mtoon1TexturePropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "outline_width_multiply_texture",
        "index",
    ]

    def update_outline_width_multiply_texture_source(
        self, context: bpy.types.Context
    ) -> None:
        mtoon = (
            self.find_material().vrm_addon_extension.mtoon1.extensions.vrmc_materials_mtoon
        )
        mtoon.update_outline_geometry(context)
        self.update_source(context)

    source: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Image,  # noqa: F722
        update=update_outline_width_multiply_texture_source,
    )

    sampler: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1OutlineWidthMultiplySamplerPropertyGroup  # noqa: F722
    )


class Mtoon1UvAnimationMaskTexturePropertyGroup(Mtoon1TexturePropertyGroup):
    material_property_chain = [
        "extensions",
        "vrmc_materials_mtoon",
        "uv_animation_mask_texture",
        "index",
    ]

    source: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Image,  # noqa: F722
        update=Mtoon1TexturePropertyGroup.update_source,
    )

    sampler: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1UvAnimationMaskSamplerPropertyGroup  # noqa: F722
    )


class Mtoon1TextureInfoPropertyGroup(MaterialTraceablePropertyGroup):
    @dataclass(frozen=True)
    class TextureInfoBackup:
        source: bpy.types.Image
        mag_filter: str
        min_filter: str
        wrap_s: str
        wrap_t: str
        offset: Tuple[float, float]
        scale: Tuple[float, float]

    def backup(self) -> TextureInfoBackup:
        return Mtoon1TextureInfoPropertyGroup.TextureInfoBackup(
            source=self.index.source,
            mag_filter=self.index.sampler.mag_filter,
            min_filter=self.index.sampler.min_filter,
            wrap_s=self.index.sampler.wrap_s,
            wrap_t=self.index.sampler.wrap_t,
            offset=(
                self.extensions.khr_texture_transform.offset[0],
                self.extensions.khr_texture_transform.offset[1],
            ),
            scale=(
                self.extensions.khr_texture_transform.scale[0],
                self.extensions.khr_texture_transform.scale[1],
            ),
        )

    def restore(self, backup: TextureInfoBackup) -> None:
        # pylint: disable=attribute-defined-outside-init
        self.index.source = backup.source
        self.index.sampler.mag_filter = backup.mag_filter
        self.index.sampler.min_filter = backup.min_filter
        self.index.sampler.wrap_s = backup.wrap_s
        self.index.sampler.wrap_t = backup.wrap_t
        self.extensions.khr_texture_transform.offset = backup.offset
        self.extensions.khr_texture_transform.scale = backup.scale
        # pylint: enable=attribute-defined-outside-init


# https://github.com/KhronosGroup/glTF/blob/1ab49ec412e638f2e5af0289e9fbb60c7271e457/specification/2.0/schema/textureInfo.schema.json
class Mtoon1BaseColorTextureInfoPropertyGroup(Mtoon1TextureInfoPropertyGroup):
    label = "Lit Color, Alpha"
    panel_label = label
    colorspace = "sRGB"

    index: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1BaseColorTexturePropertyGroup  # noqa: F722
    )
    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1BaseColorTextureInfoExtensionsPropertyGroup  # noqa: F722
    )
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]


class Mtoon1ShadeMultiplyTextureInfoPropertyGroup(Mtoon1TextureInfoPropertyGroup):
    label = "Shade Color"
    panel_label = label
    colorspace = "sRGB"

    index: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadeMultiplyTexturePropertyGroup  # noqa: F722
    )
    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadeMultiplyTextureInfoExtensionsPropertyGroup  # noqa: F722
    )
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]


# https://github.com/KhronosGroup/glTF/blob/1ab49ec412e638f2e5af0289e9fbb60c7271e457/specification/2.0/schema/material.normalTextureInfo.schema.json
class Mtoon1NormalTextureInfoPropertyGroup(Mtoon1TextureInfoPropertyGroup):
    material_property_chain: List[str] = ["normal_texture"]
    label = "Normal Map"
    panel_label = label
    colorspace = "Non-Color"

    index: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1NormalTexturePropertyGroup  # noqa: F722
    )
    scale: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        default=1.0,
        update=lambda self, _context: self.set_value("Scale", self.scale),
    )
    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1NormalTextureInfoExtensionsPropertyGroup  # noqa: F722
    )
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]


# https://github.com/vrm-c/vrm-specification/blob/c5d1afdc4d59c292cb4fd6d54cad1dc0c4d19c60/specification/VRMC_materials_mtoon-1.0/schema/mtoon.shadingShiftTexture.schema.json
class Mtoon1ShadingShiftTextureInfoPropertyGroup(Mtoon1TextureInfoPropertyGroup):
    material_property_chain: List[str] = [
        "extensions",
        "vrmc_materials_mtoon",
        "shading_shift_texture",
    ]
    label = "Additive Shading Shift"
    panel_label = label
    colorspace = "Non-Color"

    index: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadingShiftTexturePropertyGroup  # noqa: F722
    )
    scale: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Scale",  # noqa: F821
        default=1.0,
        update=lambda self, _context: self.set_value("Scale", self.scale),
    )
    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadingShiftTextureInfoExtensionsPropertyGroup  # noqa: F722
    )
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]


# https://github.com/KhronosGroup/glTF/blob/1ab49ec412e638f2e5af0289e9fbb60c7271e457/specification/2.0/schema/textureInfo.schema.json
class Mtoon1EmissiveTextureInfoPropertyGroup(Mtoon1TextureInfoPropertyGroup):
    label = "Emission"
    panel_label = label
    colorspace = "sRGB"

    index: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1EmissiveTexturePropertyGroup  # noqa: F722
    )
    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1EmissiveTextureInfoExtensionsPropertyGroup  # noqa: F722
    )
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]


class Mtoon1RimMultiplyTextureInfoPropertyGroup(Mtoon1TextureInfoPropertyGroup):
    label = "Rim Color"
    panel_label = label
    colorspace = "sRGB"

    index: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1RimMultiplyTexturePropertyGroup  # noqa: F722
    )
    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1RimMultiplyTextureInfoExtensionsPropertyGroup  # noqa: F722
    )
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]


class Mtoon1MatcapTextureInfoPropertyGroup(Mtoon1TextureInfoPropertyGroup):
    label = "Matcap Rim"
    panel_label = label
    colorspace = "sRGB"

    index: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1MatcapTexturePropertyGroup  # noqa: F722
    )
    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1MatcapTextureInfoExtensionsPropertyGroup  # noqa: F722
    )
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]


class Mtoon1OutlineWidthMultiplyTextureInfoPropertyGroup(
    Mtoon1TextureInfoPropertyGroup
):
    label = "Outline Width"
    panel_label = label
    colorspace = "Non-Color"

    index: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1OutlineWidthMultiplyTexturePropertyGroup  # noqa: F722
    )
    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1OutlineWidthMultiplyTextureInfoExtensionsPropertyGroup  # noqa: F722
    )
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]


class Mtoon1UvAnimationMaskTextureInfoPropertyGroup(Mtoon1TextureInfoPropertyGroup):
    label = "UV Animation Mask"
    panel_label = "Mask"
    colorspace = "Non-Color"

    index: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1UvAnimationMaskTexturePropertyGroup  # noqa: F722
    )
    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1UvAnimationMaskTextureInfoExtensionsPropertyGroup  # noqa: F722
    )
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]


# https://github.com/KhronosGroup/glTF/blob/1ab49ec412e638f2e5af0289e9fbb60c7271e457/specification/2.0/schema/material.pbrMetallicRoughness.schema.json#L9-L26
class Mtoon1PbrMetallicRoughnessPropertyGroup(MaterialTraceablePropertyGroup):
    material_property_chain = ["pbr_metallic_roughness"]

    def __update_base_color_factor(self, _context: bpy.types.Context) -> None:
        self.set_rgba("BaseColorFactor", self.base_color_factor)
        self.set_value("BaseColorFactorAlpha", self.base_color_factor[3])

    base_color_factor: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        size=4,
        subtype="COLOR",  # noqa: F821
        default=(1, 1, 1, 1),
        min=0,
        max=1,
        update=__update_base_color_factor,
    )

    base_color_texture: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1BaseColorTextureInfoPropertyGroup  # noqa: F722
    )


class Mtoon1VrmcMaterialsMtoonPropertyGroup(MaterialTraceablePropertyGroup):
    material_property_chain: List[str] = ["extensions", "vrmc_materials_mtoon"]

    transparent_with_z_write: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Transparent With ZWrite Mode",  # noqa: F722
        update=lambda self, _context: self.set_bool(
            "TransparentWithZWrite", self.transparent_with_z_write
        ),
    )

    render_queue_offset_number: bpy.props.IntProperty(  # type: ignore[valid-type]
        name="RenderQueue Offset",  # noqa: F722
        min=-9,
        default=0,
        max=9,
        update=lambda self, _context: self.set_int(
            "RenderQueueOffsetNumber", self.render_queue_offset_number
        ),
    )

    shade_multiply_texture: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadeMultiplyTextureInfoPropertyGroup  # noqa: F722
    )

    shade_color_factor: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        size=3,
        subtype="COLOR",  # noqa: F821
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        update=lambda self, _context: self.set_rgb(
            "ShadeColorFactor", self.shade_color_factor
        ),
    )

    shading_shift_texture: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1ShadingShiftTextureInfoPropertyGroup  # noqa: F722
    )

    shading_shift_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Shading Shift",  # noqa: F722
        soft_min=-1.0,
        default=-0.2,
        soft_max=1.0,
        update=lambda self, _context: self.set_value(
            "ShadingShiftFactor", self.shading_shift_factor
        ),
    )

    shading_toony_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Shading Toony",  # noqa: F722
        min=0.0,
        default=0.9,
        max=1.0,
        update=lambda self, _context: self.set_value(
            "ShadingToonyFactor", self.shading_toony_factor
        ),
    )

    gi_equalization_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="GI Equalization",  # noqa: F722
        min=0.0,
        default=0.9,
        max=1.0,
        update=lambda self, _context: self.set_value(
            "GiEqualizationFactor", self.gi_equalization_factor
        ),
    )

    matcap_factor: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        size=3,
        subtype="COLOR",  # noqa: F821
        default=(1, 1, 1),
        min=0,
        max=1,
        update=lambda self, _context: self.set_rgb("MatcapFactor", self.matcap_factor),
    )

    matcap_texture: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1MatcapTextureInfoPropertyGroup  # noqa: F722
    )

    parametric_rim_color_factor: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Parametric Rim Color",  # noqa: F722
        size=3,
        subtype="COLOR",  # noqa: F821
        default=(0, 0, 0),
        min=0,
        max=1,
        update=lambda self, _context: self.set_rgb(
            "ParametricRimColorFactor", self.parametric_rim_color_factor
        ),
    )

    rim_multiply_texture: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1RimMultiplyTextureInfoPropertyGroup  # noqa: F722
    )

    rim_lighting_mix_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Rim LightingMix",  # noqa: F722
        soft_min=0,
        soft_max=1,
        update=lambda self, _context: self.set_value(
            "RimLightingMixFactor", self.rim_lighting_mix_factor
        ),
    )

    parametric_rim_fresnel_power_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Parametric Rim Fresnel Power",  # noqa: F722
        min=0.0,
        default=1.0,
        soft_max=100.0,
        update=lambda self, _context: self.set_value(
            "ParametricRimFresnelPowerFactor", self.parametric_rim_fresnel_power_factor
        ),
    )

    parametric_rim_lift_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Parametric Rim Lift",  # noqa: F722
        soft_min=0.0,
        default=1.0,
        soft_max=1.0,
        update=lambda self, _context: self.set_value(
            "ParametricRimLiftFactor", self.parametric_rim_lift_factor
        ),
    )

    OUTLINE_WIDTH_MODE_NONE = "none"
    OUTLINE_WIDTH_MODE_WORLD_COORDINATES = "worldCoordinates"
    OUTLINE_WIDTH_MODE_SCREEN_COORDINATES = "screenCoordinates"
    outline_width_mode_items = [
        (OUTLINE_WIDTH_MODE_NONE, "None", "", "NONE", 0),
        (OUTLINE_WIDTH_MODE_WORLD_COORDINATES, "World Coordinates", "", "NONE", 1),
        (OUTLINE_WIDTH_MODE_SCREEN_COORDINATES, "Screen Coordinates", "", "NONE", 2),
    ]
    OUTLINE_WIDTH_MODE_IDS = [
        outline_width_mode_item[0]
        for outline_width_mode_item in outline_width_mode_items
    ]

    def update_outline_geometry(self, _context: bpy.types.Context) -> None:
        material = self.find_material()
        if material.vrm_addon_extension.mtoon1.is_outline_material:
            return
        bpy.ops.vrm.refresh_mtoon1_outline(material_name=material.name)

    outline_width_mode: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=outline_width_mode_items,
        name="Outline Width Mode",  # noqa: F722
        update=update_outline_geometry,
    )

    def update_outline_width_factor(self, context: bpy.types.Context) -> None:
        self.set_value("OutlineWidthFactor", self.outline_width_factor)
        self.update_outline_geometry(context)

    outline_width_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Outline Width",  # noqa: F722
        min=0.0,
        soft_max=0.05,
        update=update_outline_width_factor,
    )

    outline_width_multiply_texture: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1OutlineWidthMultiplyTextureInfoPropertyGroup  # noqa: F722
    )

    def update_outline_color_factor(self, context: bpy.types.Context) -> None:
        self.set_rgb("OutlineColorFactor", self.outline_color_factor)
        self.update_outline_geometry(context)

    outline_color_factor: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Outline Color",  # noqa: F722
        size=3,
        subtype="COLOR",  # noqa: F821
        default=(0, 0, 0),
        min=0,
        max=1,
        update=update_outline_color_factor,
    )

    def update_outline_lighting_mix_factor(self, context: bpy.types.Context) -> None:
        self.set_value("OutlineLightingMixFactor", self.outline_lighting_mix_factor)
        self.update_outline_geometry(context)

    outline_lighting_mix_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Outline LightingMix",  # noqa: F722
        min=0.0,
        default=1.0,
        max=1.0,
        update=update_outline_lighting_mix_factor,
    )

    uv_animation_mask_texture: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1UvAnimationMaskTextureInfoPropertyGroup  # noqa: F722
    )

    uv_animation_scroll_x_speed_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Translate X",  # noqa: F722
        update=lambda self, _context: self.set_value(
            "UvAnimationScrollXSpeedFactor", self.uv_animation_scroll_x_speed_factor
        ),
    )

    uv_animation_scroll_y_speed_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Translate Y",  # noqa: F722
        update=lambda self, _context: self.set_value(
            "UvAnimationScrollYSpeedFactor", self.uv_animation_scroll_y_speed_factor
        ),
    )

    uv_animation_rotation_speed_factor: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Rotation",  # noqa: F821
        update=lambda self, _context: self.set_value(
            "UvAnimationRotationSpeedFactor", self.uv_animation_rotation_speed_factor
        ),
    )


# https://github.com/KhronosGroup/glTF/blob/d997b7dc7e426bc791f5613475f5b4490da0b099/extensions/2.0/Khronos/KHR_materials_emissive_strength/schema/glTF.KHR_materials_emissive_strength.schema.json
class Mtoon1KhrMaterialsEmissiveStrengthPropertyGroup(MaterialTraceablePropertyGroup):
    material_property_chain: List[str] = [
        "extensions",
        "khr_materials_emissive_strength",
    ]

    emissive_strength: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Strength",  # noqa: F821
        min=0.0,
        default=1.0,
        update=lambda self, _context: self.set_value(
            "EmissiveStrength", self.emissive_strength
        ),
    )


class Mtoon1MaterialExtensionsPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    vrmc_materials_mtoon: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1VrmcMaterialsMtoonPropertyGroup  # noqa: F722
    )
    khr_materials_emissive_strength: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1KhrMaterialsEmissiveStrengthPropertyGroup  # noqa: F722
    )


# https://github.com/vrm-c/vrm-specification/blob/8dc51ec7241be27ee95f159cefc0190a0e41967b/specification/VRMC_materials_mtoon-1.0-beta/schema/VRMC_materials_mtoon.schema.json
class Mtoon1MaterialPropertyGroup(MaterialTraceablePropertyGroup):
    material_property_chain: List[str] = []

    pbr_metallic_roughness: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1PbrMetallicRoughnessPropertyGroup  # noqa: F722
    )

    ALPHA_MODE_OPAQUE = "OPAQUE"
    ALPHA_MODE_OPAQUE_VALUE = 0
    ALPHA_MODE_MASK = "MASK"
    ALPHA_MODE_MASK_VALUE = 1
    ALPHA_MODE_BLEND = "BLEND"
    ALPHA_MODE_BLEND_VALUE = 2
    alpha_mode_items = [
        (ALPHA_MODE_OPAQUE, "Opaque", "", "NONE", ALPHA_MODE_OPAQUE_VALUE),
        (ALPHA_MODE_MASK, "Cutout", "", "NONE", ALPHA_MODE_MASK_VALUE),
        (ALPHA_MODE_BLEND, "Transparent", "", "NONE", ALPHA_MODE_BLEND_VALUE),
    ]
    ALPHA_MODE_IDS = [alpha_mode_item[0] for alpha_mode_item in alpha_mode_items]

    alpha_mode_blend_method_hashed: bpy.props.BoolProperty()  # type: ignore[valid-type]

    def get_alpha_mode(self) -> int:
        # https://docs.blender.org/api/2.93/bpy.types.Material.html#bpy.types.Material.blend_method
        blend_method = self.find_material().blend_method
        if blend_method == "OPAQUE":
            return self.ALPHA_MODE_OPAQUE_VALUE
        if blend_method == "CLIP":
            return self.ALPHA_MODE_MASK_VALUE
        if blend_method in ["HASHED", "BLEND"]:
            return self.ALPHA_MODE_BLEND_VALUE
        raise ValueError(f"Unexpected blend_method: {blend_method}")

    def set_alpha_mode(self, value: int) -> None:
        material = self.find_material()
        if material.blend_method == "HASHED":
            self.alpha_mode_blend_method_hashed = True
        if material.blend_method == "BLEND":
            self.alpha_mode_blend_method_hashed = False

        if value == self.ALPHA_MODE_OPAQUE_VALUE:
            material.blend_method = "OPAQUE"
            shadow_method = "OPAQUE"
        elif value == self.ALPHA_MODE_MASK_VALUE:
            material.blend_method = "CLIP"
            shadow_method = "CLIP"
        elif value == self.ALPHA_MODE_BLEND_VALUE:
            material.blend_method = "HASHED"
            shadow_method = "HASHED"
        else:
            logger.error("Unexpected alpha mode: {value}")
            material.blend_method = "OPAQUE"
            shadow_method = "OPAQUE"

        if material.vrm_addon_extension.mtoon1.is_outline_material:
            material.shadow_method = "NONE"
            return

        material.shadow_method = shadow_method

        outline_material = material.vrm_addon_extension.mtoon1.outline_material
        if not outline_material:
            return
        outline_material.vrm_addon_extension.mtoon1.set_alpha_mode(value)

    alpha_mode: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=alpha_mode_items,
        name="Alpha Mode",  # noqa: F722
        get=get_alpha_mode,
        set=set_alpha_mode,
    )

    def __get_double_sided(self) -> bool:
        return not self.find_material().use_backface_culling

    def __set_double_sided(self, value: bool) -> None:
        self.find_material().use_backface_culling = not value

    double_sided: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Double Sided",  # noqa: F722
        get=__get_double_sided,
        set=__set_double_sided,
    )

    def get_alpha_cutoff(self) -> float:
        return max(0, min(1, float(self.find_material().alpha_threshold)))

    def set_alpha_cutoff(self, value: float) -> None:
        material = self.find_material()
        material.alpha_threshold = max(0, min(1, value))

        if material.vrm_addon_extension.mtoon1.is_outline_material:
            return
        outline_material = material.vrm_addon_extension.mtoon1.outline_material
        if not outline_material:
            return
        outline_material.vrm_addon_extension.mtoon1.set_alpha_cutoff(value)

    alpha_cutoff: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Cutoff",  # noqa: F821
        min=0,
        soft_max=1,
        get=get_alpha_cutoff,
        set=set_alpha_cutoff,
    )

    normal_texture: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1NormalTextureInfoPropertyGroup  # noqa: F722
    )

    emissive_texture: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1EmissiveTextureInfoPropertyGroup  # noqa: F722
    )

    emissive_factor: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        size=3,
        subtype="COLOR",  # noqa: F821
        default=(0, 0, 0),
        min=0,
        max=1,
        update=lambda self, _context: self.set_rgb(
            "EmissiveFactor", self.emissive_factor
        ),
    )

    extensions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Mtoon1MaterialExtensionsPropertyGroup  # noqa: F722
    )

    def get_enabled(self, material: bpy.types.Material) -> bool:
        if self.is_outline_material:
            return False
        if not material.use_nodes:
            return False

        surface_node_name = self.get_node_name("MaterialOutputSurfaceIn")
        surface_node = material.node_tree.nodes.get(surface_node_name)
        if not isinstance(surface_node, bpy.types.NodeReroute):
            # logger.warning(f'No node reroute "{surface_node_name}"')
            return False

        connected = False
        surface_socket = surface_node.outputs[0]
        for link in material.node_tree.links:
            if (
                link.from_socket == surface_socket
                and link.to_socket
                and link.to_socket.node
                and link.to_socket.node.type == "OUTPUT_MATERIAL"
            ):
                connected = True
                break
        if not connected:
            return False

        return bool(self.get("enabled"))

    def __get_enabled(self) -> bool:
        return self.get_enabled(self.find_material())

    def __set_enabled(self, value: bool) -> None:
        material = self.find_material()

        if not value:
            if self.get("enabled") and material.use_nodes:
                bpy.ops.vrm.convert_mtoon1_to_bsdf_principled(
                    material_name=material.name
                )
            self["enabled"] = False
            return

        if not material.use_nodes:
            material.use_nodes = True
        if self.__get_enabled():
            return

        bpy.ops.vrm.convert_material_to_mtoon1(material_name=material.name)
        self["enabled"] = True

    enabled: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Enable VRM MToon Material",  # noqa: F722
        get=__get_enabled,
        set=__set_enabled,
    )

    export_shape_key_normals: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Export Shape Key Normals",  # noqa: F722
    )

    def update_is_outline_material(self, _context: bpy.types.Context) -> None:
        self.set_bool("IsOutlineMaterial", self.is_outline_material)
        self.set_int("NormalScale", -1 if self.is_outline_material else 1)

    is_outline_material: bpy.props.BoolProperty(  # type: ignore[valid-type]
        update=update_is_outline_material,
    )

    outline_material: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Material,
    )

    def all_textures(self) -> List[Mtoon1TextureInfoPropertyGroup]:
        return [
            self.pbr_metallic_roughness.base_color_texture,
            self.normal_texture,
            self.emissive_texture,
            self.extensions.vrmc_materials_mtoon.shade_multiply_texture,
            self.extensions.vrmc_materials_mtoon.shading_shift_texture,
            self.extensions.vrmc_materials_mtoon.matcap_texture,
            self.extensions.vrmc_materials_mtoon.rim_multiply_texture,
            self.extensions.vrmc_materials_mtoon.outline_width_multiply_texture,
            self.extensions.vrmc_materials_mtoon.uv_animation_mask_texture,
        ]

    def link_material_output_surface(self, connect: bool) -> None:
        self.link_reroutes("MaterialOutputSurface", connect)


def reset_shader_node_group(
    context: bpy.types.Context,
    material: bpy.types.Material,
    reset_node_tree: bool = True,
) -> None:
    root = material.vrm_addon_extension.mtoon1
    mtoon = root.extensions.vrmc_materials_mtoon

    base_color_factor = list(root.pbr_metallic_roughness.base_color_factor)
    base_color_texture = root.pbr_metallic_roughness.base_color_texture.backup()
    alpha_mode_blend_method_hashed = root.alpha_mode_blend_method_hashed
    alpha_mode = root.alpha_mode
    double_sided = root.double_sided
    alpha_cutoff = root.alpha_cutoff
    normal_texture = root.normal_texture.backup()
    normal_texture_scale = root.normal_texture.scale
    emissive_texture = root.emissive_texture.backup()
    emissive_factor = list(root.emissive_factor)
    export_shape_key_normals = root.export_shape_key_normals
    emissive_strength = (
        root.extensions.khr_materials_emissive_strength.emissive_strength
    )

    transparent_with_z_write = mtoon.transparent_with_z_write
    render_queue_offset_number = mtoon.render_queue_offset_number
    shade_multiply_texture = mtoon.shade_multiply_texture.backup()
    shade_color_factor = list(mtoon.shade_color_factor)
    shading_shift_texture = mtoon.shading_shift_texture.backup()
    shading_shift_texture_scale = mtoon.shading_shift_texture.scale
    shading_shift_factor = mtoon.shading_shift_factor
    shading_toony_factor = mtoon.shading_toony_factor
    gi_equalization_factor = mtoon.gi_equalization_factor
    matcap_factor = mtoon.matcap_factor
    matcap_texture = mtoon.matcap_texture.backup()
    parametric_rim_color_factor = list(mtoon.parametric_rim_color_factor)
    rim_multiply_texture = mtoon.rim_multiply_texture.backup()
    rim_lighting_mix_factor = mtoon.rim_lighting_mix_factor
    parametric_rim_fresnel_power_factor = mtoon.parametric_rim_fresnel_power_factor
    parametric_rim_lift_factor = mtoon.parametric_rim_lift_factor
    outline_width_mode = mtoon.outline_width_mode
    outline_width_factor = mtoon.outline_width_factor
    outline_width_multiply_texture = mtoon.outline_width_multiply_texture.backup()
    outline_color_factor = list(mtoon.outline_color_factor)
    outline_lighting_mix_factor = mtoon.outline_lighting_mix_factor
    uv_animation_mask_texture = mtoon.uv_animation_mask_texture.backup()
    uv_animation_scroll_x_speed_factor = mtoon.uv_animation_scroll_x_speed_factor
    uv_animation_scroll_y_speed_factor = mtoon.uv_animation_scroll_y_speed_factor
    uv_animation_rotation_speed_factor = mtoon.uv_animation_rotation_speed_factor

    if reset_node_tree:
        shader.load_mtoon1_shader(context, material)
        if root.outline_material:
            shader.load_mtoon1_shader(context, root.outline_material)

    root.is_outline_material = False
    if root.outline_material:
        root.outline_material.vrm_addon_extension.mtoon1.is_outline_material = True

    root.pbr_metallic_roughness.base_color_factor = base_color_factor
    root.pbr_metallic_roughness.base_color_texture.restore(base_color_texture)
    root.alpha_mode_blend_method_hashed = alpha_mode_blend_method_hashed
    root.alpha_mode = alpha_mode
    root.double_sided = double_sided
    root.alpha_cutoff = alpha_cutoff
    root.normal_texture.restore(normal_texture)
    root.normal_texture.scale = normal_texture_scale
    root.emissive_texture.restore(emissive_texture)
    root.emissive_factor = emissive_factor
    root.export_shape_key_normals = export_shape_key_normals
    root.extensions.khr_materials_emissive_strength.emissive_strength = (
        emissive_strength
    )

    mtoon.transparent_with_z_write = transparent_with_z_write
    mtoon.render_queue_offset_number = render_queue_offset_number
    mtoon.shade_multiply_texture.restore(shade_multiply_texture)
    mtoon.shade_color_factor = shade_color_factor
    mtoon.shading_shift_texture.restore(shading_shift_texture)
    mtoon.shading_shift_texture.scale = shading_shift_texture_scale
    mtoon.shading_shift_factor = shading_shift_factor
    mtoon.shading_toony_factor = shading_toony_factor
    mtoon.gi_equalization_factor = gi_equalization_factor
    mtoon.matcap_factor = matcap_factor
    mtoon.matcap_texture.restore(matcap_texture)
    mtoon.parametric_rim_color_factor = parametric_rim_color_factor
    mtoon.rim_multiply_texture.restore(rim_multiply_texture)
    mtoon.rim_lighting_mix_factor = rim_lighting_mix_factor
    mtoon.parametric_rim_fresnel_power_factor = parametric_rim_fresnel_power_factor
    mtoon.parametric_rim_lift_factor = parametric_rim_lift_factor
    mtoon.outline_width_mode = outline_width_mode
    mtoon.outline_width_factor = outline_width_factor
    mtoon.outline_width_multiply_texture.restore(outline_width_multiply_texture)
    mtoon.outline_color_factor = outline_color_factor
    mtoon.outline_lighting_mix_factor = outline_lighting_mix_factor
    mtoon.uv_animation_mask_texture.restore(uv_animation_mask_texture)
    mtoon.uv_animation_scroll_x_speed_factor = uv_animation_scroll_x_speed_factor
    mtoon.uv_animation_scroll_y_speed_factor = uv_animation_scroll_y_speed_factor
    mtoon.uv_animation_rotation_speed_factor = uv_animation_rotation_speed_factor

    bpy.ops.vrm.refresh_mtoon1_outline(material_name=material.name)
