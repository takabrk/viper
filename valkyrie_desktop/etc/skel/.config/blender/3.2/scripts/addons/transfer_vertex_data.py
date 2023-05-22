bl_info = {
    "name": "Transfer Vertex Data",
    "author": "dtk mnr",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar",
    "description": "Transfer vertex data in selected vertices.",
    "warning": "",
    "category": "3D View"}

import bpy
import mathutils
from bpy.types import Panel
from rna_prop_ui import PropertyPanel


class PANEL_PT_transfer_vertex_data(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Misc"
    bl_context = "objectmode"
    bl_idname = "PANEL_PT_transfer_vertex_data"
    bl_label = "Transfer Vertex Data"

    def __init__(self):
        pass

    @classmethod
    def poll(self, context):
        try:
            obj = context.active_object
            return (obj.type == 'MESH')
        except AttributeError:
            return 0

    def draw(self, context):
        layout = self.layout
        active = False
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                active = False
                break
            elif obj == context.active_object:
                active = True;
        if len(bpy.context.selected_objects) != 2 or not active:
            layout.label(text="Select 2 Mesh Objects.")
            layout.label(text="1st Select : Origin")
            layout.label(text="2nd Select : Destination")
        else:
            layout.prop(context.window_manager, "transfer_mode")
            box_mode = layout.box()
            box_mode.prop(context.window_manager, "space", text = "Space")
            if context.window_manager.transfer_mode == "0":
                box_mode.prop(context.window_manager, "max_dist", text = "Max")
            for obj in bpy.context.selected_objects:
                if obj == bpy.context.active_object:
                    dest_v_count = 0
                    for v in obj.data.vertices:
                        if v.select:
                            dest_v_count += 1
                else:
                    orig_v_count = 0
                    for v in obj.data.vertices:
                        if v.select:
                            orig_v_count += 1
            box_info = layout.box()
            box_info.label(text="Origin : " + str(orig_v_count))
            box_info.label(text="Destination : " + str(dest_v_count))
            col_btn = layout.column()
            col_btn.operator("object.transfer_vertex_normals", text = "Transfer Normals")
            col_btn.separator()
            col_btn.prop(context.window_manager, "delete_not_exists")
            col_btn.operator("object.transfer_vertex_weights", text = "Transfer Weights")
            if orig_v_count == 0 or dest_v_count == 0 or (context.window_manager.transfer_mode == "2" and orig_v_count != 1):
                col_btn.enabled = False
            else:
                col_btn.enabled = True


class transfer_vertex_normals(bpy.types.Operator):
    bl_idname = "object.transfer_vertex_normals"
    bl_label = "Transfer Vertex Normals"
    bl_description = "Transfer Vertex Normals"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if len(bpy.context.selected_objects) != 2:
            self.report({'WARNING'}, "Select Two Objects.")
            return {'CANCELLED'}

        if context.window_manager.transfer_mode == "1":
            count = transfer_vertex_normals_indices(context)
        elif context.window_manager.transfer_mode == "2":
            count = transfer_vertex_normals_single(context)
        else:
            count = transfer_vertex_normals_distance(context)

        if "v_normal_list" in context.active_object:
            context.active_object.property_unset("v_normal_list")

        bpy.context.view_layer.objects.active = context.active_object

        if len(context.active_object.modifiers) > 0:
            context.active_object.modifiers[0].show_viewport = not context.active_object.modifiers[0].show_viewport
            context.active_object.modifiers[0].show_viewport = not context.active_object.modifiers[0].show_viewport

        if count > 1:
            result = "Normals Transfered : " + str(count) + " vertices"
        elif count == 1:
            result = "Normals Transfered : " + str(count) + " vertex"
        else:
            result = "Normals do not Transfered"

        self.report({'INFO'}, result)

        return {'FINISHED'}


def transfer_vertex_normals_distance(context):

    dest_vertices = []
    orig_vertices = []

    count = 0

    space    = context.window_manager.space
    max_dist = context.window_manager.max_dist

    for obj in bpy.context.selected_objects:
        if(obj.type == 'MESH'):
            if obj == bpy.context.active_object:
                dest_matrix = obj.matrix_world.inverted_safe()
                for v in obj.data.vertices:
                    if v.select:
                        dest_vertices.append(v)
            else:
                orig_matrix = obj.matrix_world.inverted_safe()
                for v in obj.data.vertices:
                    if v.select:
                        orig_vertices.append(v)

    if space == "0":
        for v in dest_vertices:
            shortest_dist = (orig_vertices[0].co @ orig_matrix - v.co @ dest_matrix).length
            nearest_v_idx = 0

            for i in range(1, len(orig_vertices)):
                dist = (orig_vertices[i].co @ orig_matrix - v.co @ dest_matrix).length
                if dist < shortest_dist:
                    shortest_dist = dist
                    nearest_v_idx = i
                    if dist == 0: break

            if shortest_dist <= max_dist:
                v.normal = list(orig_vertices[nearest_v_idx].normal @ orig_matrix @ dest_matrix.inverted_safe())
                count += 1

    else:
        for v in dest_vertices:
            shortest_dist = (orig_vertices[0].co - v.co).length
            nearest_v_idx = 0

            for i in range(1, len(orig_vertices)):
                dist = (orig_vertices[i].co - v.co).length
                if dist < shortest_dist:
                    shortest_dist = dist
                    nearest_v_idx = i
                    if dist == 0: break

            if shortest_dist <= max_dist:
                v.normal = list(orig_vertices[nearest_v_idx].normal)
                count += 1

    return count


def transfer_vertex_normals_indices(context):

    count = 0

    space    = context.window_manager.space

    for obj in bpy.context.selected_objects:
        if(obj.type == 'MESH'):
            if obj == bpy.context.active_object:
                dest_obj = obj
                dest_matrix = obj.matrix_world.inverted_safe()
            else:
                orig_obj = obj
                orig_matrix = obj.matrix_world.inverted_safe()

    if space == "0":
        for v in orig_obj.data.vertices:
            if v.select and v.index < len(dest_obj.data.vertices) and dest_obj.data.vertices[v.index].select:
                dest_obj.data.vertices[v.index].normal = list(v.normal @ orig_matrix @ dest_matrix.inverted_safe())
                count += 1
    else:
        for v in orig_obj.data.vertices:
            if v.select and v.index < len(dest_obj.data.vertices) and dest_obj.data.vertices[v.index].select:
                dest_obj.data.vertices[v.index].normal = list(v.normal)
                count += 1

    return count


def transfer_vertex_normals_single(context):

    count = 0

    space    = context.window_manager.space

    for obj in bpy.context.selected_objects:
        if(obj.type == 'MESH'):
            if obj == bpy.context.active_object:
                dest_obj = obj
                dest_matrix = obj.matrix_world.inverted_safe()
            else:
                orig_obj = obj
                orig_matrix = obj.matrix_world.inverted_safe()

    if space == "0":
        for v in orig_obj.data.vertices:
            if v.select:
                for dest_v in dest_obj.data.vertices:
                    if dest_v.select:
                        dest_v.normal = list(v.normal @ orig_matrix @ dest_matrix.inverted_safe())
                        count = 1
    else:
        for v in orig_obj.data.vertices:
            if v.select:
                for dest_v in dest_obj.data.vertices:
                    if dest_v.select:
                        dest_v.normal = list(v.normal)
                        count = 1

    return count


class transfer_vertex_weights(bpy.types.Operator):
    bl_idname = "object.transfer_vertex_weights"
    bl_label = "Transfer Vertex Weights"
    bl_description = "Transfer Vertex Weights"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if len(bpy.context.selected_objects) != 2:
            self.report({'WARNING'}, "Select Two Objects.")
            return {'CANCELLED'}

        if context.window_manager.transfer_mode == "1":
            count = transfer_vertex_weights_indices(context)
        elif context.window_manager.transfer_mode == "2":
            count = transfer_vertex_weights_single(context)
        else:
            count = transfer_vertex_weights_distance(context)

        if count > 1:
            result = "Weights Transfered : " + str(count) + " vertices"
        elif count == 1:
            result = "Weights Transfered : " + str(count) + " vertex"
        else:
            result = "Weights do not Transfered"

        self.report({'INFO'}, result)

        bpy.context.view_layer.objects.active = bpy.context.active_object

        return {'FINISHED'}


def transfer_vertex_weights_distance(context):

    dest_vertices = []
    orig_vertices = []

    count = 0

    max_dist = context.window_manager.max_dist
    space    = context.window_manager.space

    for obj in bpy.context.selected_objects:
        if(obj.type == 'MESH'):
            if obj == bpy.context.active_object:
                dest_obj = obj
                dest_matrix = obj.matrix_world.inverted_safe()
                for v in obj.data.vertices:
                    if v.select:
                        dest_vertices.append(v)
            else:
                orig_obj = obj
                orig_matrix = obj.matrix_world.inverted_safe()
                for v in obj.data.vertices:
                    if v.select:
                        orig_vertices.append(v)

    if space == "0":

        for v in dest_vertices:
            shortest_dist = (orig_vertices[0].co @ orig_matrix - v.co @ dest_matrix).length
            nearest_v_idx = 0

            for i in range(1, len(orig_vertices)):
                dist = (orig_vertices[i].co @ orig_matrix - v.co @ dest_matrix).length
                if dist < shortest_dist:
                    shortest_dist = dist
                    nearest_v_idx = i
                    if dist == 0: break

            if shortest_dist <= max_dist:
                transfer_vertex_weights_common(context, dest_obj, orig_obj, v.groups, orig_vertices[nearest_v_idx].groups, v.index)
                count += 1

    else:

        for v in dest_vertices:
            shortest_dist = (orig_vertices[0].co - v.co).length
            nearest_v_idx = 0

            for i in range(1, len(orig_vertices)):
                dist = (orig_vertices[i].co - v.co).length
                if dist < shortest_dist:
                    shortest_dist = dist
                    nearest_v_idx = i
                    if dist == 0: break

            if shortest_dist <= max_dist:
                transfer_vertex_weights_common(context, dest_obj, orig_obj, v.groups, orig_vertices[nearest_v_idx].groups, v.index)
                count += 1

    return count


def transfer_vertex_weights_indices(context):

    count = 0

    for obj in bpy.context.selected_objects:
        if(obj.type == 'MESH'):
            if obj == bpy.context.active_object:
                dest_obj = obj
            else:
                orig_obj = obj

    for v in orig_obj.data.vertices:
        if v.select and v.index < len(dest_obj.data.vertices) and dest_obj.data.vertices[v.index].select:
            transfer_vertex_weights_common(context, dest_obj, orig_obj, dest_obj.data.vertices[v.index].groups, v.groups, v.index)
            count += 1

    return count


def transfer_vertex_weights_single(context):

    count = 0

    for obj in bpy.context.selected_objects:
        if(obj.type == 'MESH'):
            if obj == bpy.context.active_object:
                dest_obj = obj
            else:
                orig_obj = obj

    for v in orig_obj.data.vertices:
        if v.select:
            for dest_v in dest_obj.data.vertices:
                if dest_v.select:
                    transfer_vertex_weights_common(context, dest_obj, orig_obj, dest_v.groups, v.groups, dest_v.index)
                    count = 1

    return count


def transfer_vertex_weights_common(context, dest_obj, orig_obj, dest_groups, orig_groups, index):

    for g in dest_groups:
        if not context.window_manager.delete_not_exists and dest_obj.vertex_groups[g.group].name not in orig_obj.vertex_groups:
            continue
        if not dest_obj.vertex_groups[g.group].lock_weight:
            dest_obj.vertex_groups[g.group].remove([index])

    for g in orig_groups:
        g_name = orig_obj.vertex_groups[g.group].name
        if not g_name in dest_obj.vertex_groups:
            dest_obj.vertex_groups.new(name=g_name)
        if not dest_obj.vertex_groups[g_name].lock_weight:
            dest_obj.vertex_groups[g_name].add([index], g.weight, 'REPLACE')



def init_properties():
    bpy.types.WindowManager.transfer_mode = bpy.props.EnumProperty(
        name="Mode",
        items = (("0", "Distance", ""), ("1", "Indices", ""), ("2", "Single", "")),
        default = "0",
        description = "Tranfer Mode",
        )
    bpy.types.WindowManager.space = bpy.props.EnumProperty(
        name="Space",
        items = (("0", "World", ""), ("1", "Local", "")),
        default = "0",
        description = "Space of Checked",
        )
    bpy.types.WindowManager.max_dist = bpy.props.FloatProperty(
        default=0.001)
    bpy.types.WindowManager.delete_not_exists = bpy.props.BoolProperty(
        name="Delete Where Not Exists",
        default=True,
        description="Delete Where Not Exists")

def clear_properties():
    props = ["max_dist", "space", "delete_not_exists"]
    for p in props:
        if bpy.context.window_manager.get(p) != None:
            del bpy.context.window_manager[p]
        try:
            x = getattr(bpy.types.WindowManager, p)
            del x
        except:
            pass

classes = (
    PANEL_PT_transfer_vertex_data,
    transfer_vertex_normals,
    transfer_vertex_weights,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    init_properties()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    clear_properties()

if __name__ == '__main__':
    register()
