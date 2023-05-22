import datetime
from typing import Dict, Set, Tuple, cast

import bpy


class WM_OT_vrm_io_scene_gltf2_disabled_warning(bpy.types.Operator):  # type: ignore[misc]
    bl_label = "glTF 2.0 add-on is disabled"
    bl_idname = "wm.vrm_gltf2_addon_disabled_warning"
    bl_options = {"REGISTER"}

    def execute(self, _context: bpy.types.Context) -> Set[str]:
        return {"FINISHED"}

    def invoke(self, context: bpy.types.Context, _event: bpy.types.Event) -> Set[str]:
        return cast(
            Set[str], context.window_manager.invoke_props_dialog(self, width=500)
        )

    def draw(self, _context: bpy.types.Context) -> None:
        self.layout.label(
            text='Official add-on "glTF 2.0 format" is required. Please enable it.'
        )


def image_to_image_bytes(
    image: bpy.types.Image, export_settings: Dict[str, object]
) -> Tuple[bytes, str]:
    from io_scene_gltf2.blender.exp.gltf2_blender_image import (
        ExportImage,
    )  # pyright: reportMissingImports=false

    export_image = ExportImage.from_blender_image(image)

    if image.file_format == "JPEG":
        mime_type = "image/jpeg"
    else:
        mime_type = "image/png"

    if bpy.app.version < (3, 3, 0):
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/518b6466032534c4be4a4c50ca72d37c169a5ebf/addons/io_scene_gltf2/blender/exp/gltf2_blender_image.py
        return export_image.encode(mime_type), mime_type

    if bpy.app.version < (3, 5, 0):
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/b8901bb58fa29d78bc2741cadb3f01b6d30d7750/addons/io_scene_gltf2/blender/exp/gltf2_blender_image.py
        image_bytes, _specular_color_factor = export_image.encode(mime_type)
        return image_bytes, mime_type

    # https://github.com/KhronosGroup/glTF-Blender-IO/blob/e662c281fc830d7ad3ea918d38c6a1881ee143c5/addons/io_scene_gltf2/blender/exp/gltf2_blender_image.py#L139
    image_bytes, _specular_color_factor = export_image.encode(
        mime_type, export_settings
    )
    return image_bytes, mime_type


def init_extras_export() -> None:
    # https://github.com/KhronosGroup/glTF-Blender-IO/blob/6f9d0d9fc1bb30e2b0bb019342ffe86bd67358fc/addons/io_scene_gltf2/blender/com/gltf2_blender_extras.py#L20-L21
    try:
        from io_scene_gltf2.blender.com.gltf2_blender_extras import (
            BLACK_LIST,
        )  # pyright: reportMissingImports=false
    except ImportError:
        return

    value = "vrm_addon_extension"
    if value not in BLACK_LIST:
        BLACK_LIST.append(value)


def create_export_settings() -> Dict[str, object]:
    return {
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L522
        "timestamp": datetime.datetime.now(datetime.timezone.utc),
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L258-L268
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L552
        "gltf_materials": True,
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L120-L137
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L532
        "gltf_format": "GLB",
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L154-L168
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L533
        "gltf_image_format": "AUTO",
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L329-L333
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L569
        "gltf_extras": True,
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L611-L633
        "gltf_user_extensions": [],
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L606
        "gltf_binary": bytearray(),
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L176-L184
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/67b2ed150b0eba08129b970dbe1116c633a77d24/addons/io_scene_gltf2/__init__.py#L530
        "gltf_keep_original_textures": False,
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/bfe4ff8b1b5c26ba17b0531b67798376147d9fa7/addons/io_scene_gltf2/__init__.py#L273-L279
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/bfe4ff8b1b5c26ba17b0531b67798376147d9fa7/addons/io_scene_gltf2/__init__.py#L579
        "gltf_original_specular": False,
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/e662c281fc830d7ad3ea918d38c6a1881ee143c5/addons/io_scene_gltf2/__init__.py#L208-L214
        # https://github.com/KhronosGroup/glTF-Blender-IO/blob/e662c281fc830d7ad3ea918d38c6a1881ee143c5/addons/io_scene_gltf2/__init__.py#L617
        "gltf_jpeg_quality": 75,
    }
