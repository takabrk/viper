bl_info = {
    "name" : "Vertex Groups Utilities",
    "author": "dtk mnr",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "location": "Properties > Data > Vertex Groups > Menu",
    "description" : "Utilities for Vertex Groups",
    "warning": "",
    "category" : "Object"
}

import bpy
import mathutils


class AddSymmetricalVertexGroups(bpy.types.Operator):
    bl_idname = "object.vertex_group_add_symmetrical"
    bl_label = "Add Symmetrical Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if (obj):
            if (obj.type == 'MESH'):
                if len(obj.vertex_groups) > 0:
                    return True
        return False

    def execute(self, context):
        count = add_symmetrical_vertex_groups()

        if count > 1:
            result = "Added : " + str(count) + " groups"
        elif count == 1:
            result = "Added : " + str(count) + " group"
        else:
            result = "Not Added"

        self.report({'INFO'}, result)

        return {'FINISHED'}


class RemoveDisusedVertexGroups(bpy.types.Operator):
    bl_idname = "object.vertex_group_remove_disused"
    bl_label = "Remove Disused Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if (obj):
            if (obj.type == 'MESH'):
                if len(obj.vertex_groups) > 1:
                    return True
        return False

    def execute(self, context):
        count = remove_disused_vertex_groups()

        if count > 1:
            result = "Deleted : " + str(count) + " groups"
        elif count == 1:
            result = "Deleted : " + str(count) + " group"
        else:
            result = "Not Deleted"

        self.report({'INFO'}, result)

        return {'FINISHED'}


def get_vertex_groups_callback(self, context):
    items = []
    obj = bpy.context.active_object
    item = (str(-1), "None", "")
    items.append(item)
    for i, g in enumerate(obj.vertex_groups):
        if g == obj.vertex_groups.active:
            continue
        item = (str(i), g.name, "")
        items.append(item)
    return items

class MergeVertexGroups(bpy.types.Operator):
    bl_idname = "object.vertex_group_merge"
    bl_label = "Merge Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    from_count = 5

    from_groups = []
    for i in range(from_count):
        from_groups.append(
            bpy.props.EnumProperty(
                name="From " + str(i + 1),
                items = get_vertex_groups_callback,
                description = "From Group " + str(i + 1),
                )
        )

    from_group_1: from_groups[0]
    from_group_2: from_groups[1]
    from_group_3: from_groups[2]
    from_group_4: from_groups[3]
    from_group_5: from_groups[4]

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if (obj and obj.type == 'MESH') and len(obj.vertex_groups) > 2:
            return True
        return False

    def draw(self, context):
        obj = context.active_object
        self.layout.prop(self, "from_group_1")
        for i in range(self.from_count - 1):
            if (len(obj.vertex_groups) > i + 2):
                self.layout.prop(self, "from_group_" + str(i + 2))
        self.layout.label(text="To: >>>>>>>>> " + bpy.context.active_object.vertex_groups.active.name)

    def invoke(self, context, event):
        obj = context.active_object
        default = str(0)
        if obj.vertex_groups.active.index == 0:
            default = str(1)
        self.from_group_1 = default

        for i in range(self.from_count - 1):
            setattr(self, "from_group_" + str(i + 2), str(-1))

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        prop = {}
        prop["from_groups"] = []
        for i in range(self.from_count):
            prop["from_groups"].append(int(getattr(self, "from_group_" + str(i + 1))))
        merge_vertex_groups(prop)

        return {'FINISHED'}



def add_symmetrical_vertex_groups():
    obj = bpy.context.active_object
    mesh = obj.data

    vertex_groups = [vgroup.name for vgroup in obj.vertex_groups]

    count = 0

    for vgroup in obj.vertex_groups:
        new_name = ""
        if vgroup.name[-2:] == ".L" and vgroup.name[:-2] + ".R" not in vertex_groups:
           new_name = vgroup.name[:-2] + ".R"
        elif vgroup.name[-2:] == ".R" and vgroup.name[:-2] + ".L" not in vertex_groups:
           new_name = vgroup.name[:-2] + ".L"
        elif vgroup.name[-2:] == ".l" and vgroup.name[:-2] + ".r" not in vertex_groups:
           new_name = vgroup.name[:-2] + ".r"
        elif vgroup.name[-2:] == ".r" and vgroup.name[:-2] + ".l" not in vertex_groups:
           new_name = vgroup.name[:-2] + ".l"

        if new_name != "":
            obj.vertex_groups.active_index = vgroup.index
            bpy.ops.object.vertex_group_copy()
            new_vgroup = obj.vertex_groups.active
            mirror_weights(obj, new_vgroup)
            new_vgroup.name = new_name
            print("Added :", new_name)
            count += 1

    return count


def mirror_weights(obj, vgroup):

    weights = {}

    for v in obj.data.vertices:
        for g in v.groups:
            if g.group == vgroup.index:
                weights[v.index] = vgroup.weight(v.index)

    for v in obj.data.vertices:
        mirror_co = mathutils.Vector((-v.co[0], v.co[1], v.co[2]))

        nearest_index = -1
        nearest_dist = 0.1
        for target_v in obj.data.vertices:
            if v.index == target_v.index:
                continue
            dist = (target_v.co - mirror_co).length
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_index = target_v.index
                if dist == 0:
                    break

        if nearest_index != -1 and nearest_index in weights:
            vgroup.add([v.index], weights[nearest_index], 'REPLACE')
        else:
            vgroup.remove([v.index])


def remove_disused_vertex_groups():
    obj = bpy.context.active_object
    mesh = obj.data
    vertex_groups = []
    remove_candidate = []

    mirror_modifier_used = False
    for modi in obj.modifiers:
        if modi.type == 'MIRROR' and modi.use_x and modi.use_mirror_vertex_groups:
            mirror_modifier_used = True

    for vgroup in obj.vertex_groups:
        remove_flag = True
        vertex_groups.append(vgroup.name.upper())
        for index in range(len(mesh.vertices)):
            try:
                if vgroup.weight(index) > 0:
                    remove_flag = False
                    break
            except RuntimeError:
                continue
        if remove_flag:
            remove_candidate.append(vgroup.name.upper())

    count = 0

    for vgroup in obj.vertex_groups:
        name = vgroup.name.upper()
        if name in remove_candidate:
            if (
                (name[-2:] != ".L" and name[-2:] != ".R") or
                (name[-2:] == ".L" and name[:-2] + ".R" in remove_candidate) or
                (name[-2:] == ".R" and name[:-2] + ".L" in remove_candidate) or
                (name[-2:] == ".L" and name[:-2] + ".R" not in vertex_groups) or
                (name[-2:] == ".R" and name[:-2] + ".L" not in vertex_groups) or
                not mirror_modifier_used
               ):
                print("Deleted :", vgroup.name)
                count += 1
                obj.vertex_groups.remove(vgroup)

    return count


def merge_vertex_groups(prop):
    obj = bpy.context.active_object
    mesh = obj.data
    from_groups = []
    for i in prop["from_groups"]:
        if i == -1:
            continue
        from_groups.append(obj.vertex_groups[i])
    to_group = obj.vertex_groups.active

    for v in mesh.vertices:
        add_weight = False
        from_val = 0
        for from_group in from_groups:
            for g in v.groups:
                if g.group == from_group.index:
                    from_val += g.weight
                    break
        if from_val == 0:
            continue

        to_group.add([v.index], from_val, 'ADD')

    while len(from_groups) > 0:
        obj.vertex_groups.remove(from_groups[0])
        from_groups.pop(0)

    obj.vertex_groups.active = to_group



def menu_func(self,context):
    self.layout.separator()
    self.layout.operator(AddSymmetricalVertexGroups.bl_idname, icon='ADD', text="Add Symmetrical Vertex Groups")
    self.layout.operator(RemoveDisusedVertexGroups.bl_idname, icon='X', text="Remove Disused Vertex Groups")
    self.layout.operator(MergeVertexGroups.bl_idname, icon='MOD_BOOLEAN', text="Merge Vertex Groups")

classes = (
    AddSymmetricalVertexGroups,
    RemoveDisusedVertexGroups,
    MergeVertexGroups,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.remove(menu_func)

if __name__ == '__main__':
    register()
