
bl_info = {
    "name": "Import TMC(PC) (.TMC)",
    "author": "dtk mnr",
    "version": (1, 0, 3),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import TMC(PC)",
    "warning": "",
    "category": "Import-Export",
}

import bpy
import os
import math
import mathutils
from mathutils import Vector, Matrix
import binascii
import struct
import array
from bpy.props import *
from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        orientation_helper,
        axis_conversion,
        unpack_list,
        unpack_face_list,
        )
from bpy.types import (
        Operator,
        OperatorFileListElement,
        )



error_message = ""

prop = {}



class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    check_use_material_node: bpy.props.BoolProperty(
            name="Set \"Use Material Node\" option to be check by default",
            default=False
            )
    check_blend_mode: EnumProperty(
            name="Set \"Blend Mode\" option to be check by default",
            items = (("0", "Alpha Hashed", ""), ("1", "Alpha Blend", "")),
            default = "0",
            )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "check_use_material_node")

        row_blend_mode = layout.row()
        row_blend_mode.alignment = 'LEFT'
        row_blend_mode.scale_x = 0.6
        row_blend_mode.prop(self, "check_blend_mode", expand=True)


class DialogOperator(Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "A problem occurred."
    def execute(self, context):
        self.report({'ERROR'}, error_message)
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class Float16Compressor:
    def __init__(self):
        self.temp = 0

    def compress(self,float32):
        F16_EXPONENT_BITS = 0x1F
        F16_EXPONENT_SHIFT = 10
        F16_EXPONENT_BIAS = 15
        F16_MANTISSA_BITS = 0x3ff
        F16_MANTISSA_SHIFT =  (23 - F16_EXPONENT_SHIFT)
        F16_MAX_EXPONENT =  (F16_EXPONENT_BITS << F16_EXPONENT_SHIFT)

        a = struct.pack('>f',float32)
        b = binascii.hexlify(a)

        f32 = int(b,16)
        f16 = 0
        sign = (f32 >> 16) & 0x8000
        exponent = ((f32 >> 23) & 0xff) - 127
        mantissa = f32 & 0x007fffff
                
        if exponent == 128:
            f16 = sign | F16_MAX_EXPONENT
            if mantissa:
                f16 |= (mantissa & F16_MANTISSA_BITS)
        elif exponent > 15:
            f16 = sign | F16_MAX_EXPONENT
        elif exponent > -15:
            exponent += F16_EXPONENT_BIAS
            mantissa >>= F16_MANTISSA_SHIFT
            f16 = sign | exponent << F16_EXPONENT_SHIFT | mantissa
        else:
            f16 = sign
        return f16

    def decompress(self,float16):
        s = int((float16 >> 15) & 0x00000001)    # sign
        e = int((float16 >> 10) & 0x0000001f)    # exponent
        f = int(float16 & 0x000003ff)            # fraction

        if e == 0:
            if f == 0:
                return int(s << 31)
            else:
                while not (f & 0x00000400):
                    f = f << 1
                    e -= 1
                e += 1
                f &= ~0x00000400
        elif e == 31:
            if f == 0:
                return int((s << 31) | 0x7f800000)
            else:
                return int((s << 31) | 0x7f800000 | (f << 13))

        e = e + (127 -15)
        f = f << 13
        return int((s << 31) | (e << 23) | f)


fglb = {'ENDIAN':'<'}#'file' = filehandle
def fread(offset = -1, fmt = 'L', extractifsingle = True):
    global fglb
    if type(offset) is str:
        if type(fmt) is bool:
            extractifsingle = fmt
        fmt = offset
    elif offset != -1:
        fglb['FILE'].seek(offset)
    result = struct.unpack(fglb['ENDIAN'] + fmt, fglb['FILE'].read(struct.calcsize("!"+fmt)))
    if extractifsingle and len(result) == 1:
        return result[0]
    return result

def freadstring(offset = -1, maxbytes = 255):
    global fglb
    if offset != -1:
        fglb['FILE'].seek(offset)
    mahbytes = b''
    count = 0
    while True:
        count += 1
        chr = fglb['FILE'].read(1)
        mahbytes += chr
        if len(chr) == 0 or count == maxbytes:
            return mahbytes[:].decode('ASCII')
        elif mahbytes[-1] == 0:
            return mahbytes[:-1].decode('ASCII')


class TmcHead():
    global fglb
    name = ''
    Size = Count1 = Count2 = Offset1 = Offset2 = Offset3 = base = 0
    offsets = []
    sizes = []
    def __init__(self, base):
        fglb['FILE'].seek(base)
        self.name = freadstring(base)
        if fread(base + 8, 'L') !=  0x01010000:
            return

        self.Size, self.Count1, self.Count2, self.Count3, self.Offset1, self.Offset2, self.Offset3 = fread(base + 0x10, '7L')
        self.base = base
        fglb['FILE'].seek(base + self.Offset1)
        self.offsets = [fread('L') for i in range(self.Count1)]
        if self.Offset2 != 0:
            fglb['FILE'].seek(base + self.Offset2)
            self.sizes = [fread('L') for i in range(self.Count1)]


class TmcData():
    __slots__ = ("HieLay",
                 "HieMtxLayered",
                 "maxBoneLevel",
                 "MtxGrp",
                 "BnOfsMtxGrp",
                 "Nodes",
                 "MeshNodes",
                 "ObjGrp",
                 "VtxGrp",
                 "IdxGrp",
                 "MtrCol",
                 "matecp",
                 "itable",
                 "offset_l",
                 "textures",
                 "armature",
                 "parent")

    indices = []

    icount = 0
    global prop

    def __init__(self, h):
        self.textures = []
        self.matecp = []
        self.itable = []
        if prop["set_texture_settings"]:
            self.parseCpf(h.offsets[11]);
            self.parseLHeader(h.offsets[7]);
            self.parseTextures(h.offsets[1]);
        self.parseHieLay(h.offsets[6])
        self.parseGlblMtx(h.offsets[9])
        self.parseBnOfsMtx(h.offsets[10])
        self.parseNodeLay(h.offsets[8])
        self.parseMdlGeo(h.offsets[0])
        self.parseVertices(h.offsets[2])
        self.parseIndices(h.offsets[3])
        if prop["apply_material"]: self.parseMtrCol(h.offsets[4])

    def parseCpf(self, base):
        if base == 0:
            return
        h = TmcHead(base)
        if h.name != "cpf" or h.Count2 < 2:
            return
        matecp_h = TmcHead(base + h.offsets[1])
        for offs in matecp_h.offsets:
            cp = []
            cp_h = TmcHead(matecp_h.base + offs)
            for i, cp_offs in enumerate(cp_h.offsets):
                param = fread(cp_h.base + cp_h.Offset3 + 8 * i, 'L')
                cp.append(param)
            self.matecp.append(cp)
        itable_h = TmcHead(matecp_h.base + matecp_h.Offset3)
        for offs in itable_h.offsets:
            row = []
            count = fread(itable_h.base + offs, 'L')
            fglb['FILE'].seek(itable_h.base + offs + 4)
            for i in range(count):
                row.append(fread('L'))
            self.itable.append(row)

    def parseLHeader(self, base):
        h = TmcHead(base)
        self.offset_l = h.offsets[0]

    def parseTextures(self, base):
        if not prop["set_texture_settings"]:
            return
        ttdm_h = TmcHead(base)
        ttdh_h = TmcHead(base + 0x30)
        ttdl_h = TmcHead(base + ttdm_h.Offset3)

        for i in range(ttdh_h.Count1):
            tex = Texture(ttdh_h.base + ttdh_h.offsets[i], i)

            if tex.in_l:
                tex.address = self.offset_l + ttdl_h.offsets[tex.rel_index]
                tex.size    = ttdl_h.sizes[tex.rel_index]
            else:
                tex.address = base + ttdm_h.offsets[tex.rel_index]
                tex.size    = ttdm_h.sizes[tex.rel_index]

            self.textures.append(tex)

    def parseHieLay(self, base):
        self.HieLay = []
        self.HieMtxLayered = {}
        self.maxBoneLevel = 0
        h = TmcHead(base)
        self.maxBoneLevel = 0;
        for offs in h.offsets:
            fglb['FILE'].seek(base + offs)
            hmatrix = Matrix([fread('4f') for i in range(4)]).transposed()
            parent, chlidrencount, bonelevel, bone_ukn02 = fread(base + offs + 16 * 4, 'i3L')
            bchildren = fread(base + offs + 0x40 + 0x10, '%dL'%chlidrencount, False)
            self.HieLay.append((parent, bchildren, bonelevel, hmatrix));
            if bonelevel > self.maxBoneLevel: self.maxBoneLevel = bonelevel

    def parseGlblMtx(self, base):
        self.MtxGrp = []
        h = TmcHead(base)
        for offs in h.offsets:
            fglb['FILE'].seek(base + offs)
            gmatrix = Matrix([fread('4f') for i in range(4)]).transposed()
            self.MtxGrp.append(gmatrix)

    def parseBnOfsMtx(self, base):
        self.BnOfsMtxGrp = []
        h = TmcHead(base)
        for offs in h.offsets:
            fglb['FILE'].seek(base + offs)
            gmatrix = Matrix([fread('4f') for i in range(4)]).transposed()
            self.BnOfsMtxGrp.append(gmatrix)

    def parseNodeLay(self, base):
        self.Nodes = []
        self.MeshNodes = {}
        h = TmcHead(base)
        for offidx ,offs in enumerate(h.offsets):
            nodebase = base + offs
            unk0_0, master, index, unk0_1 = fread(nodebase + 0x30, '4l')
            original_nodename = freadstring(nodebase + 0x40)
            nodename = change_nodename(original_nodename)
            self.Nodes.append(nodename)
            mtxdataoffs = fread(nodebase + fread(nodebase + 0x20), '%dL'%fread(nodebase + 0x14), False)
            #parent, bChildren, boneLevel, hMatrix = self.HieLay[index]
            gmatrix = self.MtxGrp[index]
            if master == -1:
                for mtxoffs in mtxdataoffs:
                    objidx, childrennum, nodeidx, unk00 = fread(nodebase + mtxoffs, '4L')
                    fglb['FILE'].seek(nodebase + mtxoffs + 0x10)
                    #nMatrix = Matrix([fread('4f') for i in range(4)]).transposed()
                    bonegroups = fread(nodebase + mtxoffs + 0x10 + 0x40, '%dL'%childrennum, False)
                    self.MeshNodes[objidx] = (nodename, gmatrix, bonegroups, original_nodename)

    def parseMdlGeo(self, base):
        self.ObjGrp = []
        h = TmcHead(base)
        for idx, offs in enumerate(h.offsets):
            objbase = base + offs
            self.ObjGrp.append(ObjectGroup(objbase, idx, self.MeshNodes, self.Nodes))

    def parseVertices(self, base):
        self.VtxGrp = []
        h = TmcHead(base)
        for idx, offs in enumerate(h.offsets):
            self.VtxGrp.append(VertexGroup(base + offs, idx, self))

    def parseIndices(self, base):
        self.IdxGrp = []
        h = TmcHead(base)
        for idx, offs in enumerate(h.offsets):
            self.IdxGrp.append(IndexGroup(base + offs, idx, self))

    def parseMtrCol(self, base):
        self.MtrCol = []
        h = TmcHead(base)
        for idx, offs in enumerate(h.offsets):
            colors = []
            fglb['FILE'].seek(base + h.offsets[idx])
            for i in range(12):
                color = fread('4f')
                colors.append(color)
            self.MtrCol.append(colors)

    def setArmature(self, armature):
        self.armature = armature

    def setParent(self, parent):
        self.parent = parent


class Texture():
    __slots__ = ("index",
                 "in_l",
                 "rel_index",
                 "address",
                 "size")
    def __init__(self, base, index):
        self.address = self.size = 0
        self.index = index
        self.in_l = True if fread(base, 'L') == 1 else False
        self.rel_index = fread(base + 4, 'L')

class ObjectGroup():
    __slots__ = ("index",
                 "name",
                 "Decl",
                 "Obj")
    def __init__(self, base, idx, meshnodes, nodes):
        self.Obj = []
        idxcounts = {}
        h = TmcHead(base)
        self.index = fread(base + 0x34, 'L')
        self.name = fread(base + 0x50, '16s').decode('ASCII').rstrip("\0")
        if idx in meshnodes:
            self.name = meshnodes[idx][3]
        elif "*" in self.name:
            for node in nodes:
                if node[len(node) - len(self.name) + 1:] == self.name[1:]:
                    self.name = node
        self.parseGeoDecl(base + h.Offset3)
        for offs in h.offsets:
            obj = Object(base + offs)
            self.Obj.append(obj)

            # for idxcount problem
            if obj.declindex in idxcounts:
                if obj.idxstart + obj.idxcount > idxcounts[obj.declindex]:
                    idxcounts[obj.declindex] = obj.idxstart + obj.idxcount
            else:
                idxcounts[obj.declindex] = obj.idxstart + obj.idxcount

        # for idxcount problem
        for key, val in idxcounts.items():
            if val > self.Decl[key].idxcount:
                self.Decl[key].idxcount = val

    def parseGeoDecl(self, base):
        self.Decl = []
        h = TmcHead(base)
        for offs in h.offsets:
            self.Decl.append(Decl(base + offs))

class Decl():
    __slots__ = ("idxbuffer",
                 "idxcount",
                 "vtxcount",
                 "uvcount",
                 "vtxbuffer",
                 "vtxsize",
                 "vdatalaycount",
                 "fvfdata")
    def __init__(self, base):
        self.idxbuffer, self.idxcount, self.vtxcount = fread(base + 0xC, '3L')
        self.vtxbuffer, self.vtxsize, self.vdatalaycount = fread(base + 0x30, '3L')
        self.fvfdata = []
        for i in range(self.vdatalaycount):
            self.fvfdata.append(FVFData(base + 0x40 + i * 8))
        self.uvcount = 0
        for fvf in self.fvfdata:
            if fvf.Usage == 5 and fvf.Type == 0xB:
                self.uvcount += 2
            if fvf.Usage == 5 and fvf.Type == 0xA:
                self.uvcount += 1

class FVFData():
    Offset = Type = Usage = Layer = 0
    def __init__(self, base):
        self.Offset, self.Type, self.Usage, self.Layer = fread(base, '2xBxBx2B')

class Object():
    __slots__ = ("index",
                 "mtrcol",
                 "texcount",
                 "declindex",
                 "transparent1",
                 "transparent2",
                 "twosided",
                 "idxstart",
                 "idxcount",
                 "vtxstart",
                 "vtxcount",
                 "textures")
    def __init__(self, base):
        self.textures = []
        self.index, self.mtrcol, self.texcount = fread(base, '2L4xL')
        for i in range(self.texcount):
            texoffs = fread(base + 0x10 + (4 * i), 'L')
            self.textures.append(TextureGeo(base + texoffs))
        self.declindex, self.transparent1, self.transparent2 = fread(base + 0x38, 'L4xL4xL')
        self.twosided, self.idxstart, self.idxcount, self.vtxstart, self.vtxcount = fread(base + 0x6C, '5L')

class TextureGeo():
    type = index = 0
    def __init__(self, base):
        self.type, self.index = fread(base, '4x2L')

class VertexGroup():
    __slots__ = ("vertices",
                 "normals",
                 "blend_weights",
                 "blend_indices",
                 "v_colors",
                 "tangents",
                 "bitangent_signs",
                 "uvs")
    fcomp = Float16Compressor()

    def __init__(self, base, idx, tmcdata):
        self.vertices = []
        self.normals = []
        self.blend_weights = []
        self.blend_indices = []
        self.v_colors = []
        self.tangents = []
        self.bitangent_signs = []
        self.uvs = []
        for objGrp in tmcdata.ObjGrp:
            for d in objGrp.Decl:
                if d.vtxbuffer == idx:
                    decl = d
                    break
        if not "decl" in locals():
            return
        for vindex in range(decl.vtxcount):
            uv = []
            for i in range(len(decl.fvfdata)):
                fglb['FILE'].seek(base + (decl.vtxsize * vindex) + decl.fvfdata[i].Offset)
                if decl.fvfdata[i].Usage == 0:
                    self.vertices.append(list(fread('3f')))
                elif decl.fvfdata[i].Usage == 3:
                    self.normals.append(list(fread('3f')))
                elif decl.fvfdata[i].Usage == 1:
                    if decl.fvfdata[i].Type == 3:
                        self.blend_weights.append(list(fread('4f')))
                    else:
                        self.blend_weights.append(list(fread('4B')))
                elif decl.fvfdata[i].Usage == 2:
                    self.blend_indices.append(list(fread('4B')))
                elif decl.fvfdata[i].Usage == 10:
                    self.v_colors.append(list(fread('4B')))
                elif decl.fvfdata[i].Usage == 6:
                    self.tangents.append(list(fread('3f')))
                    self.bitangent_signs.append(fread('f'))
                elif decl.fvfdata[i].Usage == 5:
                    if decl.fvfdata[i].Type == 0xB:
                        uv.append(self.parseUV())
                        uv.append(self.parseUV())
                    else:
                        uv.append(self.parseUV())
            self.uvs.append(uv)

    def parseUV(self):
        uv = []
        h = fread('H')
        str = struct.pack('I',self.fcomp.decompress(h))
        f = struct.unpack('f',str)[0]
        uv.append(f)
        h = fread('H')
        str = struct.pack('I',self.fcomp.decompress(h))
        f = struct.unpack('f',str)[0]
        uv.append(1 - f)
        return uv

class IndexGroup():
    __slots__ = ("indices")
    def __init__(self, base, idx, tmcdata):
        self.indices = []
        for objGrp in tmcdata.ObjGrp:
            for d in objGrp.Decl:
                if d.idxbuffer == idx:
                    decl = d
                    break
        self.indices = fread(base, str(decl.idxcount) + 'H')


def build_faces(obj, indices, offset):
    faces = []
    clockwise = True
    for i in range(obj.idxstart, obj.idxstart + obj.idxcount - 2):
        if len(indices[i:i+3]) != len(set(indices[i:i+3])):
            clockwise = not clockwise
            continue
        if clockwise:
            faces.append((indices[i] - offset, indices[i+1] - offset, indices[i+2] - offset))
        else:
            faces.append((indices[i] - offset, indices[i+2] - offset, indices[i+1] - offset))
        clockwise = not clockwise
    return faces


def create_object(filename, tmcdata, collection):
    global prop
    global_matrix = axis_conversion(to_forward='Z', to_up='-Y').to_4x4()

    images = {}
    textures = {}
    tex_digit = 2 if len(tmcdata.textures) <= 100 else 3

    def set_material(tmcdata, objgrp, obj, meshname):
        global prop

        mtrcol = tmcdata.MtrCol[obj.mtrcol]
        mat = bpy.data.materials.new(meshname)
        mat.diffuse_color  = (mtrcol[1][0], mtrcol[1][1], mtrcol[1][2], 0)
        mat.specular_color = mtrcol[2][0:3]
        mat.specular_intensity = sum(mtrcol[2][0:3]) / 3
        mat.roughness = 1 / mtrcol[2][3] * 5

        return mat

    def set_material_node(tmcdata, objgrp, obj, meshname):
        global prop

        normal_map = None
        tex_diffuse = None

        diffuse_added = False
        specular_added = False
        normal_added = False
        disable_alpha = False
        disable_normal = False
        disable_spe = False
        disable_dirt = False
        if len(tmcdata.itable) > 0 and tmcdata.itable[objgrp.index][obj.index] < len(tmcdata.matecp):
            matecp = tmcdata.matecp[tmcdata.itable[objgrp.index][obj.index]]
            if 0xEB53FEEF in matecp or 0x60121B1E in matecp:
                disable_alpha = True
                disable_normal = True
                disable_spe = True
                disable_dirt = True
            #if 0xE8347F43 in matecp:
            #    disable_spe = True

        mat = bpy.data.materials.new(meshname)
        mat.use_nodes = True
        if len(mat.node_tree.nodes) > 0:
            mat.node_tree.nodes.clear()

        if not obj.twosided:
            mat.show_transparent_back = False

        output = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')

        add = mat.node_tree.nodes.new('ShaderNodeAddShader')
        add.location = (-360, 0)

        diffuse = mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
        diffuse.location = (-560, 0)
        specular = mat.node_tree.nodes.new('ShaderNodeBsdfGlossy')
        specular.location = (-560, -260)

        mix_rgb_diffuse = mat.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_rgb_diffuse.location = (-760, 0)
        mix_rgb_specular = mat.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_rgb_specular.location = (-760, -260)

        mat.node_tree.links.new(add.inputs[0], diffuse.outputs[0])
        mat.node_tree.links.new(add.inputs[1], specular.outputs[0])
        mat.node_tree.links.new(diffuse.inputs[0], mix_rgb_diffuse.outputs[0])
        mat.node_tree.links.new(specular.inputs[0], mix_rgb_specular.outputs[0])

        if not disable_alpha and (obj.transparent1 != 0 or obj.transparent2 != 0):
            if prop["blend_mode"] == 0:
                mat.blend_method = 'HASHED'
            else:
                mat.blend_method = 'BLEND'
            transparent = mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
            transparent.location = (-360, -140)
            mix = mat.node_tree.nodes.new('ShaderNodeMixShader')
            mix.location = (-180, 0)
            mat.node_tree.links.new(output.inputs[0], mix.outputs[0])
            mat.node_tree.links.new(mix.inputs[1], transparent.outputs[0])
            mat.node_tree.links.new(mix.inputs[2], add.outputs[0])
        else:
            mat.node_tree.links.new(output.inputs[0], add.outputs[0])

        if tmcdata.MtrCol[obj.mtrcol][2][3] == 0:
            specular.inputs[1].default_value = 1
        else:
            specular.inputs[1].default_value = 1 / tmcdata.MtrCol[obj.mtrcol][2][3] * 5

        mix_rgb_diffuse.blend_type = 'MULTIPLY'
        mix_rgb_diffuse.inputs[0].default_value = 1.0
        mix_rgb_diffuse.inputs[1].default_value = tmcdata.MtrCol[obj.mtrcol][1]

        mix_rgb_specular.blend_type = 'DARKEN'
        mix_rgb_specular.inputs[1].default_value = tmcdata.MtrCol[obj.mtrcol][2]
        mix_rgb_specular.inputs[1].default_value[3] = 1

        for i, tex in enumerate(obj.textures):
            if (tex.type == 0 and diffuse_added) or (tex.type == 1 and normal_added) or (tex.type == 2 and specular_added):
                continue
            fmt_str = "Tex_{0:0>" + str(tex_digit) + "}"
            image_name = fmt_str.format(tex.index)

            if prop["set_texture_settings"]:
                if image_name not in images:
                    images[image_name] = bpy.data.images.new(name=image_name, width=64, height=64)
                    images[image_name].source = 'FILE'
                    images[image_name].filepath = prop["tex_dir"] + image_name + ".dds"

            if tex.type == 0:
                diffuse_added = True

                tex_diffuse = mat.node_tree.nodes.new('ShaderNodeTexImage')
                tex_diffuse.location = (-1060, 0)
                uv_map_diffuse = mat.node_tree.nodes.new('ShaderNodeUVMap')
                uv_map_diffuse.location = (-1260, 0)
                if i < len(mesh.uv_layers):
                    uv_map_diffuse.uv_map = mesh.uv_layers[i].name
                if prop["set_texture_settings"]:
                    tex_diffuse.image = images[image_name]

                if not disable_alpha and (obj.transparent1 != 0 or obj.transparent2 != 0):
                    mat.node_tree.links.new(tex_diffuse.inputs[0], uv_map_diffuse.outputs[0])

                    if prop["set_texture_settings"]:
                        mat.node_tree.links.new(mix.inputs[0], tex_diffuse.outputs[1])
                        mat.node_tree.links.new(mix_rgb_diffuse.inputs[2], tex_diffuse.outputs[0])
                else:
                    mat.node_tree.links.new(tex_diffuse.inputs[0], uv_map_diffuse.outputs[0])

                    if prop["set_texture_settings"]:
                        mat.node_tree.links.new(mix_rgb_diffuse.inputs[2], tex_diffuse.outputs[0])

            elif tex.type == 1:
                normal_added = True

                normal_map = mat.node_tree.nodes.new('ShaderNodeNormalMap')
                normal_map.location = (-760, -520)
                tex_normal = mat.node_tree.nodes.new('ShaderNodeTexImage')
                tex_normal.location = (-1060, -520)
                uv_map_normal = mat.node_tree.nodes.new('ShaderNodeUVMap')
                uv_map_normal.location = (-1260, -520)

                mat.node_tree.links.new(normal_map.inputs[1], tex_normal.outputs[0])
                mat.node_tree.links.new(tex_normal.inputs[0], uv_map_normal.outputs[0])

                if prop["set_texture_settings"]:
                    tex_normal.image = images[image_name]
                    if not disable_normal:
                        mat.node_tree.links.new(diffuse.inputs[2], normal_map.outputs[0])
                        mat.node_tree.links.new(specular.inputs[2], normal_map.outputs[0])

                if i < len(mesh.uv_layers):
                    uv_map_normal.uv_map = mesh.uv_layers[i].name

            elif tex.type == 2:
                specular_added = True

                if not disable_spe:
                    tex_specular = mat.node_tree.nodes.new('ShaderNodeTexImage')
                    tex_specular.location = (-1060, -260)
                    uv_map_specular = mat.node_tree.nodes.new('ShaderNodeUVMap')
                    uv_map_specular.location = (-1260, -260)

                    mat.node_tree.links.new(tex_specular.inputs[0], uv_map_specular.outputs[0])

                    if i < len(mesh.uv_layers):
                        uv_map_specular.uv_map = mesh.uv_layers[i].name

                if prop["set_texture_settings"]:
                    if not disable_spe:
                        tex_specular.image = images[image_name]
                        mat.node_tree.links.new(mix_rgb_specular.inputs[0], tex_specular.outputs[1])
                        mat.node_tree.links.new(mix_rgb_specular.inputs[2], tex_specular.outputs[0])
                    elif tex_diffuse is not None:
                        mat.node_tree.links.new(mix_rgb_specular.inputs[0], tex_diffuse.outputs[1])
                        mix_rgb_specular.blend_type = 'ADD'
                        mix_rgb_specular.inputs[1].default_value = (0,0,0,1)
                        mix_rgb_specular.inputs[2].default_value = tmcdata.MtrCol[obj.mtrcol][2]
                        mix_rgb_specular.inputs[2].default_value[3] = 1

            elif tex.type == 3:
                diffuse_env = mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
                diffuse_env.location = (-560, -780)
                tex_env = mat.node_tree.nodes.new('ShaderNodeTexImage')
                tex_env.location = (-1060, -780)
                normal_map_env = mat.node_tree.nodes.new('ShaderNodeNormalMap')
                normal_map_env.location = (-1260, -780)
                vector_transform = mat.node_tree.nodes.new('ShaderNodeVectorTransform')
                vector_transform.location = (-1460, -780)
                tex_coord = mat.node_tree.nodes.new('ShaderNodeTexCoord')
                tex_coord.location = (-1660, -780)

                normal_map_env.space = 'WORLD'
                vector_transform.convert_from = 'WORLD'
                vector_transform.convert_to = 'CAMERA'

                if normal_map is not None:
                    mat.node_tree.links.new(diffuse_env.inputs[2], normal_map.outputs[0])

                mat.node_tree.links.new(add.inputs[1], diffuse_env.outputs[0])
                mat.node_tree.links.new(diffuse_env.inputs[0], tex_env.outputs[0])
                mat.node_tree.links.new(tex_env.inputs[0], normal_map_env.outputs[0])
                mat.node_tree.links.new(normal_map_env.inputs[1], vector_transform.outputs[0])
                mat.node_tree.links.new(vector_transform.inputs[0], tex_coord.outputs[1])

                if prop["set_texture_settings"]:
                    tex_env.image = images[image_name]

        return mat

    for objgrp in tmcdata.ObjGrp:
        if prop["skip_sweat_object"] and "_sweat_" in objgrp.name: continue

        if prop["auto_zerofill_id"]:
            id_digit = len("{0:x}".format(len(objgrp.Obj) - 1))
        else:
            id_digit = prop["min_digit_id"]

        for obj in objgrp.Obj:
            if prop["skip_empty_object"] and obj.vtxcount < 2:
                continue

            faces = build_faces(obj, tmcdata.IdxGrp[objgrp.Decl[obj.declindex].idxbuffer].indices, obj.vtxstart)
            vtxgrp = tmcdata.VtxGrp[objgrp.Decl[obj.declindex].vtxbuffer]
            meshname = objgrp.name + "_" + "{0:x}".format(obj.index).zfill(id_digit)

            mesh = bpy.data.meshes.new(meshname)
            mesh.from_pydata(vtxgrp.vertices[obj.vtxstart:obj.vtxstart + obj.vtxcount], [], faces)
            mesh.update()

            if len(vtxgrp.v_colors) > 0:
                color_layer = mesh.vertex_colors.new(name="Color")
                alpha_layer = mesh.vertex_colors.new(name="Alpha")
                for poly in mesh.polygons:
                    for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                        col = vtxgrp.v_colors[mesh.loops[loop_index].vertex_index + obj.vtxstart]
                        color_layer.data[loop_index].color = [col[0]/255, col[1]/255, col[2]/255]
                        alpha_layer.data[loop_index].color = [col[3]/255, col[3]/255, col[3]/255]

            for i in range(objgrp.Decl[obj.declindex].uvcount):
                mesh.uv_layers.new(name="UV Maps %d" % (i + 1))
                for poly in mesh.polygons:
                    for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                        mesh.uv_layers[i].data[loop_index].uv = vtxgrp.uvs[mesh.loops[loop_index].vertex_index + obj.vtxstart][i]

            mesh.polygons.foreach_set("use_smooth", [True] * len(mesh.polygons))

            newobj = bpy.data.objects.new(meshname, mesh)
            newobj.parent = tmcdata.parent

            collection.objects.link(newobj)

            if prop["apply_material"]:
                if prop["use_material_node"]:
                    mat = set_material_node(tmcdata, objgrp, obj, meshname)
                else:
                    mat = set_material(tmcdata, objgrp, obj, meshname)
                mesh.materials.append(mat)

            try:
                if tmcdata.MeshNodes is not None:

                    if objgrp.index in tmcdata.MeshNodes:
                        meshnode = tmcdata.MeshNodes[objgrp.index]
                    else:
                        changed_name = change_nodename(objgrp.name)
                        if changed_name in tmcdata.Nodes:
                            meshnode = [objgrp.name, None, [tmcdata.Nodes.index(changed_name)], objgrp.name]
                        else:
                            temp_name = changed_name.replace("*", "")
                            for i, node in enumerate(tmcdata.Nodes):
                                if temp_name in node:
                                    meshnode = [tmcdata.Nodes[i], None, [i], tmcdata.Nodes[i]]
                                    meshname = tmcdata.Nodes[i] + "_" + "{0:x}".format(obj.index).zfill(id_digit)
                                    mesh.name = newobj.name = meshname
                                    break

                    if not prop["transform_matrix"] and meshnode[1] is not None:
                        newobj.matrix_world = global_matrix @ meshnode[1]
                    else:
                        newobj.matrix_world = global_matrix

                    if prop["transform_matrix"] and meshnode[1] is not None:
                        transform_matrix = meshnode[1]
                        if len(vtxgrp.normals) != 0:
                            for i in range(obj.vtxcount):
                                mesh.vertices[i].normal = Vector(vtxgrp.normals[obj.vtxstart + i]) @ transform_matrix.inverted_safe()
                        mesh.transform(transform_matrix)
                    elif len(vtxgrp.normals) != 0:
                        for i in range(obj.vtxcount):
                            mesh.vertices[i].normal = vtxgrp.normals[obj.vtxstart + i]

                    for bonegroup in meshnode[2]:
                        group_name = tmcdata.Nodes[bonegroup]
                        newobj.vertex_groups.new(name=group_name)

                    if len(vtxgrp.blend_indices) != 0:
                        if isinstance(vtxgrp.blend_weights[obj.vtxstart][0], float):
                            for i in range(obj.vtxcount):
                                for j in range(4):
                                    if vtxgrp.blend_weights[obj.vtxstart + i][j] == 0:
                                        continue
                                    newobj.vertex_groups[tmcdata.Nodes[meshnode[2][vtxgrp.blend_indices[obj.vtxstart + i][j]]]].add([i], vtxgrp.blend_weights[obj.vtxstart + i][j], 'ADD')
                        else:
                            blendbase = 1 / 255
                            for i in range(obj.vtxcount):
                                for j in range(4):
                                    if vtxgrp.blend_weights[obj.vtxstart + i][j] == 0:
                                        continue
                                    elif vtxgrp.blend_weights[obj.vtxstart + i][j] == 0xFF:
                                        weight = 1.0
                                    else:
                                        weight = blendbase * vtxgrp.blend_weights[obj.vtxstart + i][j]
                                    newobj.vertex_groups[tmcdata.Nodes[meshnode[2][vtxgrp.blend_indices[obj.vtxstart + i][j]]]].add([i], weight, 'ADD')
                    else:
                        if not objgrp.name in newobj.vertex_groups:
                            newobj.vertex_groups.new(name=objgrp.name)
                        for i in range(obj.vtxcount):
                            newobj.vertex_groups[objgrp.name].add([i], 1.0, 'REPLACE')

                    bpy.context.view_layer.objects.active = newobj
                    if len(newobj.vertex_groups) > 1:
                        bpy.ops.object.vertex_group_sort(sort_type='NAME')

                    modi = newobj.modifiers.new("Armature", 'ARMATURE')
                    modi.object = bpy.data.objects[tmcdata.armature.name]
                    modi.use_bone_envelopes = False
                    modi.use_vertex_groups = True
                    if not prop["show_armature_modi"]: modi.show_viewport = False

            except IndexError:
                newobj.vertex_groups.clear()


def create_armature(filename, tmcdata, collection):
    # Create Armature
    view_layer = bpy.context.view_layer

    if view_layer.objects.active:
        if view_layer.objects.active.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action = 'DESELECT')

    amt = bpy.data.armatures.new(filename + "_armature")
    obj = bpy.data.objects.new(amt.name, amt)
    obj.show_in_front = True
    amt.display_type = 'STICK' #'OCTAHEDRAL','STICK','BBONE','ENVELOPE','WIRE'
    global_matrix = axis_conversion(to_forward='Z', to_up='-Y').to_4x4()

    collection.objects.link(obj)

    view_layer.objects.active = obj

    mat_rot_z180 = mathutils.Matrix.Rotation(math.radians(180.0), 4, 'Z')
    mat_rot_z90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
    mat_rot_z270 = mathutils.Matrix.Rotation(math.radians(270.0), 4, 'Z')
    mat_rot_x90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X')

    OffsetMatrix = {}

    # Create Bones
    bpy.ops.object.mode_set(mode='EDIT')
    for i in range(tmcdata.maxBoneLevel + 1):
        for hidx, (parentidx, bchildren, bonelevel, hmatrix) in enumerate(tmcdata.HieLay):
            if bonelevel == i:
                bonename = tmcdata.Nodes[hidx]
                bone = amt.edit_bones.new(bonename)
                bone.tail += Vector((0,0,0.02))

                if parentidx != -1:
                    if tmcdata.Nodes[parentidx] in amt.edit_bones:
                        parent = amt.edit_bones[tmcdata.Nodes[parentidx]]
                        bone.parent = parent
                        if prop["bone_by"] == 0:
                            bone.matrix = tmcdata.MtxGrp[hidx]
                        elif prop["bone_by"] == 1:
                            bone.matrix = parent.matrix @ hmatrix
                            tmcdata.HieMtxLayered[hidx] = bone.matrix
                        else:
                            bone.matrix = tmcdata.BnOfsMtxGrp[hidx].inverted_safe()
                    if prop["bring_close"]:
                        for childidx in bchildren:
                            if "Shoulder" in tmcdata.Nodes[childidx]:
                                continue
                            if ("MOT" in bonename and "MOT" in tmcdata.Nodes[childidx]) or ("OPT_Hand_" in bonename and not ("_Metacarpal" in bonename or "_Root" in bonename)):
                                OffsetMatrix[bonename] = tmcdata.HieLay[childidx][3]
                else:
                    if prop["bone_by"] == 0:
                        bone.matrix = tmcdata.MtxGrp[hidx]
                    elif prop["bone_by"] == 1:
                        bone.matrix = hmatrix
                        tmcdata.HieMtxLayered[hidx] = hmatrix
                    else:
                        bone.matrix = tmcdata.BnOfsMtxGrp[hidx].inverted_safe()

    for bone in amt.edit_bones:
        part = ""
        if bone.name != "MOT00_Hips" and bone.name != "MOT16_Waist" and bone.name != "MOT02_Chest" and bone.name != "MOT15_Neck" and bone.name != "MOT01_Head":
            parent = bone.parent
            while parent is not None and parent.name != "MOT00_Hips":
                if parent.name == "MOT_*Shoulder.1.L" or bone.name == "MOT_*Shoulder.1.L":
                    part = "LeftArm"
                    break
                elif parent.name == "MOT_*Shoulder.1.R" or bone.name == "MOT_*Shoulder.1.R":
                    part = "RightArm"
                    break
                elif ("MOT_*Arm" in bone.name or "MOT_*Arm" in parent.name) and ".1.L" in bone.name:
                    part = "LeftArm"
                    break
                elif ("MOT_*Arm" in bone.name or "MOT_*Arm" in parent.name) and ".1.R" in bone.name:
                    part = "RightArm"
                    break
                elif "WGT_acs_" in parent.name:
                    break;
                elif "MOT15_Neck" in parent.name:
                    break;
                elif "OPT_Face_" in bone.name:
                    part = "Face"
                    break
                elif "OPT_Breast_" in bone.name:
                    part = "Breast"
                    break
                else:
                    parent = parent.parent
            if part == "LeftArm":
                bone.matrix = bone.matrix @ mat_rot_z270
            elif part == "RightArm":
                bone.matrix = bone.matrix @ mat_rot_z90
            elif part == "Breast":
                bone.matrix = bone.matrix @ mat_rot_x90
            elif part == "Face":
                bone.matrix = bone.matrix @ mat_rot_x90
                bone.length *= 0.25
            else:
                bone.matrix = bone.matrix @ mat_rot_z180
        if bone.name in OffsetMatrix:
            if part == "LeftArm":
                OffsetMatrix[bone.name][1][3] = OffsetMatrix[bone.name][0][3]
            elif part == "RightArm":
                OffsetMatrix[bone.name][1][3] = - OffsetMatrix[bone.name][0][3]
            elif OffsetMatrix[bone.name][1][3] < 0:
                OffsetMatrix[bone.name][1][3] *= -1
            if OffsetMatrix[bone.name][1][3] != 0:
                OffsetMatrix[bone.name][0][3] = 0
                OffsetMatrix[bone.name][2][3] = 0
                bone.tail = (bone.matrix @ OffsetMatrix[bone.name]).decompose()[0]
        if bone.parent is not None and bone.head == bone.parent.tail:
            bone.use_connect = True

    bpy.ops.object.mode_set(mode='OBJECT')
    obj.matrix_world = global_matrix


def posebone_convert_to_euler(obj):

    for bone in obj.pose.bones:

        if posebone_check_skip(bone.name):
            continue

        if "OPT_Face_" in bone.name:
            bone.rotation_mode = 'ZXY'
        elif "OPT_Hand_*_Root" in bone.name:
            bone.rotation_mode = 'ZYX'
        elif "Shoulder.1" in bone.name or "Arm.1" in bone.name or "Hand.1" in bone.name:
            bone.rotation_mode = 'YXZ'
        else:
            bone.rotation_mode = 'XYZ'


def posebone_check_skip(name):
    if name[:3] == "MOT" or "OPT_Face_" in name or "OPT_Hand_" in name or "OPT_wing" in name:
        return False
    return True


def set_offset_matrix(tmcdata):

    bpy.ops.object.mode_set(mode='POSE')

    for bone in bpy.context.visible_pose_bones:
        if bone.name in tmcdata.Nodes:
            idx = tmcdata.Nodes.index(bone.name)
            bone.matrix = tmcdata.BnOfsMtxGrp[idx] @ tmcdata.HieMtxLayered[idx] @ bone.matrix
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.poselib.new()
    bpy.ops.poselib.pose_add()
    bpy.ops.poselib.pose_rename(name="BnOfsMtx")


def import_tmc(filepath):

    global prop

    with open(filepath, 'rb') as f:

        fglb['FILE'] = f
        view_layer = bpy.context.view_layer

        filename = os.path.splitext((os.path.basename(filepath)))[0]

        tmcH = TmcHead(0)
        if tmcH.name != "TMC":
            return

        tmcdata = TmcData(tmcH)


        if prop["set_texture_settings"]:

            tex_dir = "//"

            if prop["tex_dir_type"] == 1:
                tex_dir = bpy.context.user_preferences.filepaths.texture_directory
                if tex_dir != "//" and tex_dir[-1:] != "\\":
                    tex_dir += "\\"

            if prop["tex_in_subdir"]:
                tex_dir += filename + "_tex\\"

            prop["tex_dir"] = tex_dir

            if prop["ext_textures"]:
                if prop["tex_dir_type"] == 2:
                    prop["tex_save_dir"] = os.path.dirname(bpy.data.filepath) +  "\\" + tex_dir[2:]
                elif tex_dir[:2] == "//":
                    prop["tex_save_dir"] = os.path.dirname(filepath) + "\\" + tex_dir[2:]
                else:
                    prop["tex_save_dir"] = tex_dir

        if view_layer.objects.active != None:
            hidden = False
            if view_layer.objects.active.hide_viewport:
                view_layer.objects.active.hide_viewport = False
                hidden = True
            if view_layer.objects.active.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            if hidden:
                view_layer.objects.active.hide_viewport = True
        bpy.ops.object.add(type='EMPTY', location=(0.0, 0.0, 0.0))
        empty = view_layer.objects.active
        tmcdata.setParent(empty)
        parentname = filename
        count = 1
        while parentname in bpy.data.objects:
            parentname = filename + "." + str(count).zfill(3)
            count += 1
        tmcdata.parent.name = parentname

        if prop["add_collection"]:
            collection = bpy.data.collections.new(name=parentname)
            bpy.context.scene.collection.children.link(collection)
            collection.objects.link(empty)
            view_layer.active_layer_collection.collection.objects.unlink(empty)
        else:
            collection = bpy.context.scene.collection

        create_armature(filename, tmcdata, collection)
        tmcdata.setArmature(view_layer.objects.active)
        tmcdata.armature.parent = tmcdata.parent

        posebone_convert_to_euler(tmcdata.armature)

        if prop["test_offset_matrix"] and prop["bone_by"] == 1:
            set_offset_matrix(tmcdata)

        create_object(filename, tmcdata, collection)

        view_layer.objects.active = tmcdata.armature

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if space.overlay.normals_length >= 0.1:
                            space.overlay.normals_length = 0.01
                        break
                break

        bpy.ops.object.mode_set(mode='OBJECT')

        if prop["tex_save_dir"] is not None:
            extract_textures(filepath, tmcdata)


def change_nodename(nodename):
    s = nodename

    if s == "MOT18_right_upleg_MobA_Tiger":
        return "MOT_*_leg_MobA_Tiger.1.r"
    elif s == "MOT19_right_shin_MobA_Tiger":
        return "MOT_*_foot_MobA_Tiger.1.r"
    elif s == "MOT20_right_foot_MobA_Tiger":
        return "MOT_*_toe_MobA_Tiger.1.r"

    if "_Instance" in s:
        s = s.replace("_Instance", ">")
    if ">" not in s and s[:3] == "MOT" and ("Right" in s or "Left" in s or "right" in s or "left" in s):
        if s[4] == "_":
            s = "MOT_" + s[5:]
        else:
            s = "MOT" + s[5:]
    if "Right" in s:
        s = s.replace("Right", "*") + ".1.R"
    elif "Left" in s:
        s = s.replace("Left", "*") + ".1.L"
    elif "right" in s:
        s = s.replace("right", "*") + ".1.r"
    elif "left" in s:
        s = s.replace("left", "*") + ".1.l"
    elif "_R_" in s:
        s = s.replace("_R_", "_*_") + ".0.R"
    elif "_L_" in s:
        s = s.replace("_L_", "_*_") + ".0.L"
    elif "_r_" in s:
        s = s.replace("_r_", "_*_") + ".0.r"
    elif "_l_" in s:
        s = s.replace("_l_", "_*_") + ".0.l"
    else:
        s = s

    return s


def extract_textures(filepath, tmcdata):

    global prop

    if not os.path.exists(prop["tex_save_dir"]):
        os.makedirs(prop["tex_save_dir"])

    filepath_l = filepath + "L"
    exists_l = os.path.exists(filepath_l)

    tex_digit = 2 if len(tmcdata.textures) <= 100 else 3
    fmt_str = "Tex_{0:0>" + str(tex_digit) + "}.dds"

    for tex in tmcdata.textures:
        if not tex.in_l:
            save_path = prop["tex_save_dir"] + "\\" + fmt_str.format(tex.index)
            if os.path.exists(save_path):
                continue
            fglb['FILE'].seek(tex.address)
            bin = fglb['FILE'].read(tex.size)
            with open(save_path, 'wb') as f:
                f.write(bin)

    if exists_l:
        with open(filepath_l, 'rb') as f_l:
            for tex in tmcdata.textures:
                if tex.in_l:
                    if not exists_l:
                        continue
                    save_path = prop["tex_save_dir"] + "\\" + fmt_str.format(tex.index)
                    if os.path.exists(save_path):
                        continue
                    f_l.seek(tex.address)
                    bin = f_l.read(tex.size)
                    with open(save_path, 'wb') as f:
                        f.write(bin)



class Import_tmc_pc(Operator, ImportHelper):
    """Import to tmc pc"""
    bl_idname = "import.tmc_pc"
    bl_label = "Import TMC(PC)"
    bl_options = {'UNDO'}
    filename_ext = ".TMC"

    filter_glob: StringProperty(
            default="*.TMC",
            options={'HIDDEN'},
            )

    files: CollectionProperty(
            name="File Path",
            type=OperatorFileListElement,
            )

    directory: StringProperty(
            subtype='DIR_PATH',
            )

    add_collection: BoolProperty(
            name="Add Collection",
            description="Add Collection and Objects Link to Added Collection",
            default=True,
            )

    auto_zerofill_id: BoolProperty(
            name="Auto Zero Fill ID",
            description="Auto Zero Fill ID Number",
            default=True,
            )

    min_digit_id: IntProperty(
            name="Min Zero Fill ID",
            description="Minimum Digit Zero Fill ID Number",
            default=1,
            min=1,
            max=4,
            )

    transform_matrix: BoolProperty(
            name="Transform by Matrix Data",
            description="Transform by Matrix data",
            default=False,
            )

    skip_sweat_object: BoolProperty(
            name="Skip Sweat Object",
            description="Skip Sweat Object",
            default=False,
            )

    skip_empty_object: BoolProperty(
            name="Skip Empty Object",
            description="Skip Empty Object",
            default=True,
            )

    show_armature_modi: BoolProperty(
            name="Show Armature Modifier",
            description="Show Armature Modifier",
            default=True,
            )

    apply_material: BoolProperty(
            name="Apply Material",
            description="Apply Material",
            default=False,
            )

    use_material_node: BoolProperty(
            name="Use Material Node",
            description="Use Material Node",
            default=True,
            )

    blend_mode: EnumProperty(
            name="Blend Mode",
            items = (("0", "Alpha Hashed", ""), ("1", "Alpha Blend", "")),
            default = "0",
            description = "Blend Mode",
            )

    set_texture_settings: BoolProperty(
            name="Set Texture Settings",
            description="Set Texture Settings",
            default=False,
            )

    tex_dir_type: EnumProperty(
            name="Texture Directory",
            items = (("0", "TMC", "Same Directory As TMC"), ("1", "User", "User Directory")),
            default = "0",
            description = "Texture Directory",
            )

    tex_dir_type_current: EnumProperty(
            name="Texture Directory",
            items = (("0", "TMC", "Same Directory As TMC"), ("1", "User", "User Directory"), ("2", "Current", "Current Directory")),
            default = "2",
            description = "Texture Directory",
            )

    tex_in_subdir: BoolProperty(
            name="Textures in Sub Directory",
            description="Set Textures in Sub Directory",
            default=False,
            )

    ext_textures: BoolProperty(
            name="Extract Textures",
            description="Extract Textures",
            default=False,
            )

    bone_by: EnumProperty(
            name="Bone by",
            items = (("0", "GlblMtx", ""), ("1", "HieLay", ""), ("2", "BnOfsMtx", "")),
            default = "1",
            description = "Bone by",
            )

    bring_close: BoolProperty(
            name="Bring tail close to child",
            description="Bring tail of major bone close to child",
            default=True,
            )

    test_offset_matrix: BoolProperty(
            name="BnOfsMtx Test",
            description="BnOfsMtx Test",
            default=False,
            )

    def __init__(self):
        preferences = bpy.context.preferences.addons[__name__].preferences
        if preferences.check_use_material_node:
            self.use_material_node = preferences.check_use_material_node
        if preferences.check_blend_mode == "1":
            self.blend_mode = preferences.check_blend_mode

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "add_collection")

        layout.separator()

        layout.prop(self, "auto_zerofill_id")
        col_digit = layout.column()
        col_digit.prop(self, "min_digit_id")
        if self.auto_zerofill_id:
            col_digit.enabled = False

        layout.separator()

        layout.prop(self, "transform_matrix")
        layout.prop(self, "skip_sweat_object")
        layout.prop(self, "skip_empty_object")
        layout.prop(self, "show_armature_modi")

        layout.separator()

        layout.prop(self, "apply_material")

        col_use_material_node = layout.column()
        col_use_material_node.prop(self, "use_material_node")

        row_blend_mode = layout.row()
        row_blend_mode.prop(self, "blend_mode", expand=True)

        col_set_tex = layout.column()
        col_set_tex.prop(self, "set_texture_settings")

        box_tex = layout.box()
        row = box_tex.row()

        if bpy.context.blend_data.filepath == "":
            row.prop(self, "tex_dir_type", expand=True)
        else:
            row.prop(self, "tex_dir_type_current", expand=True)

        box_tex.prop(self, "tex_in_subdir")
        box_tex.prop(self, "ext_textures")

        if not self.apply_material:
            col_use_material_node.enabled = False
            #self.use_material_node = False
            row_blend_mode.enabled = False
            col_set_tex.enabled = False
        if not self.use_material_node:
            row_blend_mode.enabled = False
            col_set_tex.enabled = False
            self.set_texture_settings = False
        if not self.set_texture_settings:
            box_tex.enabled = False

        layout.separator()

        layout.prop(self, "bone_by")
        layout.prop(self, "bring_close")
        layout.prop(self, "test_offset_matrix")

    def execute(self, context):
        global prop

        prop = {}

        prop["add_collection"] = True

        prop["auto_zerofill_id"] = self.auto_zerofill_id
        prop["min_digit_id"] = self.min_digit_id

        prop["transform_matrix"] = self.transform_matrix
        prop["skip_sweat_object"] = self.skip_sweat_object
        prop["skip_empty_object"] = self.skip_empty_object
        prop["show_armature_modi"] = self.show_armature_modi

        prop["apply_material"] = self.apply_material
        prop["use_material_node"] = self.use_material_node
        prop["blend_mode"] = int(self.blend_mode)
        prop["set_texture_settings"] = self.set_texture_settings
        prop["tex_in_subdir"] = self.tex_in_subdir
        prop["ext_textures"] = self.ext_textures

        if bpy.context.blend_data.filepath == "":
            prop["tex_dir_type"] = int(self.tex_dir_type)
        else:
            prop["tex_dir_type"] = int(self.tex_dir_type_current)

        prop["tex_dir"] = None
        prop["tex_save_dir"] = None

        prop["bone_by"] = int(self.bone_by)
        prop["bring_close"] = self.bring_close
        prop["test_offset_matrix"] = self.test_offset_matrix

        if len(self.files) > 1 and prop["set_texture_settings"]:
            prop["tex_in_subdir"] = True


        paths = [os.path.join(self.directory, name.name) for name in self.files]

        if not paths:
            paths.append(self.filepath)

        for path in paths:
            import_tmc(path)


        return {"FINISHED"}



classes = (
    AddonPreferences,
    Import_tmc_pc,
)

def menu_func(self, context):
    self.layout.operator(Import_tmc_pc.bl_idname, text="TMC(PC) (.TMC)", icon='PLUGIN')

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)

if __name__ == "__main__":
    register()
