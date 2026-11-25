"""Editable Cycles materials. No image textures, displacement modifier or baking."""
from collections import defaultdict

import bpy

PATTERN = "Insert arc length (m)"
MARGIN = "Unpunched margin (m)"
FINISH = "Cognac finish"
SURROUND = (.197, .085, .037, 1)
CENTRE = (.237, .110, .049, 1)


class Graph:
    def __init__(self, name, inputs, output):
        self.tree = bpy.data.node_groups.new(name, "ShaderNodeTree")
        for key, kind, default in inputs:
            s = self.tree.interface.new_socket(name=key, in_out="INPUT", socket_type="NodeSocket"+kind)
            s.default_value = default
            if key == "Perforation":
                s.min_value, s.max_value = 0, 1
        self.tree.interface.new_socket(name=output[0], in_out="OUTPUT", socket_type="NodeSocket"+output[1])
        self.inputs = self.node("NodeGroupInput")
        self.out = self.node("NodeGroupOutput")

    def node(self, kind, label=""):
        n = self.tree.nodes.new(kind)
        n.label = label
        return n

    def set(self, node, key, val):
        if isinstance(val, bpy.types.NodeSocket):
            self.tree.links.new(val, node.inputs[key])
        else:
            node.inputs[key].default_value = val

    def math(self, op, *args, label=""):
        n = self.node("ShaderNodeMath", label)
        n.operation, n.hide = op, True
        for i,val in enumerate(args):
            self.set(n, i, val)
        return n.outputs[0]

    def noise(self, vec, scale, detail, label):
        n = self.node("ShaderNodeTexNoise", label)
        self.set(n, "Scale", scale)
        self.set(n, "Detail", detail)
        self.set(n, "Vector", vec)
        return n

    def ramp(self, value, lo, hi, dark, light, label):
        n = self.node("ShaderNodeValToRGB", label)
        n.color_ramp.interpolation = "EASE"
        for e, x, f in zip(n.color_ramp.elements, (lo, hi), (dark, light)):
            e.position, e.color = x, (f, f, f, 1)
        self.set(n, 0, value)
        return n.outputs[0]

    def finish(self, val):
        self.set(self.out, 0, val)
        levels, occupied = {}, defaultdict(int)
        def depth(n):
            if n.name not in levels:
                levels[n.name] = max((depth(l.from_node)+1 for s in n.inputs for l in s.links), default=0)
            return levels[n.name]
        for n in self.tree.nodes:
            d = depth(n)
            n.location = (d*215, -occupied[d])
            occupied[d] += 85 if n.hide else 360
        return self.tree


def punch_group():
    g = Graph("AUTOLAB • staggered punch field", [("Pitch (m)", "Float", .0040)], ("Impression","Float"))
    m = g.math
    uv = g.node("ShaderNodeUVMap", "Surface distance, not bounding-box projection")
    uv.uv_map = PATTERN
    sep = g.node("ShaderNodeSeparateXYZ")
    g.set(sep, 0, uv.outputs["UV"])
    pitch = m("MAXIMUM", g.inputs.outputs[0], .0005)
    x = m("DIVIDE", sep.outputs[0], pitch)
    y = m("DIVIDE", sep.outputs[1], m("MULTIPLY", pitch, .8660254))
    row = m("FLOOR", y)
    dx = m("SUBTRACT", m("FRACT", m("ADD", x, m("MULTIPLY", row, .5))), .5)
    dy = m("MULTIPLY", m("SUBTRACT", m("FRACT", y), .5), .8660254)
    r = m("SQRT", m("ADD", m("MULTIPLY", dx, dx), m("MULTIPLY", dy, dy)))
    cup = g.ramp(r, .095, .170, 1, 0, "Rolled rim and dark blind impression")
    edge = g.node("ShaderNodeAttribute", "Stop punching before the cut edge")
    edge.attribute_name = MARGIN
    return g.finish(m("MULTIPLY", cup, m("GREATER_THAN", edge.outputs["Fac"], .0045)))


def finish_group():
    g = Graph("AUTOLAB • finished hide", [("Hide tone", "Color", CENTRE),
              ("Perforation", "Float", 0.), ("Pitch (m)", "Float", .0040)], ("Finish","Shader"))
    m = g.math
    coord = g.node("ShaderNodeTexCoord").outputs["Object"]
    broad = g.noise(coord, 20, 2.5, "Slow finish / roughness variation").outputs["Fac"]
    fine = g.noise(coord, 2100, 1.5, "Fine follicle breakup").outputs["Fac"]
    warp = g.noise(coord, 370, 2, "Disrupt the straight cell walls").outputs["Color"]
    scaled = g.node("ShaderNodeVectorMath")
    scaled.operation = "SCALE"
    g.set(scaled, 0, warp)
    g.set(scaled, "Scale", .00067)
    dist = g.node("ShaderNodeVectorMath")
    dist.operation = "ADD"
    g.set(dist, 0, coord)
    g.set(dist, 1, scaled.outputs[0])
    grain = g.node("ShaderNodeTexVoronoi", "Broken hide grain in object metres")
    grain.feature = "DISTANCE_TO_EDGE"
    g.set(grain, "Vector", dist.outputs[0])
    g.set(grain, "Scale", 640.)
    cells = g.ramp(grain.outputs["Distance"], .012, .165, 0, 1, "Rounded grain plateaus")
    punch = g.node("ShaderNodeGroup", "Optional centre-insert treatment")
    punch.node_tree = punch_group()
    g.set(punch, 0, g.inputs.outputs["Pitch (m)"])
    hole = m("MULTIPLY", punch.outputs[0], g.inputs.outputs["Perforation"])
    height = m("ADD", m("MULTIPLY", cells, .70), m("MULTIPLY", fine, .30))
    bump = g.node("ShaderNodeBump", "Embossed grain")
    g.set(bump, "Height", height)
    g.set(bump, "Distance", .00024)
    g.set(bump, "Strength", .43)
    peel = g.node("ShaderNodeBump", "Low relief under the smaller grain")
    g.set(peel, "Height", g.noise(coord, 93., 2.0, "Soft hide undulation").outputs["Fac"])
    g.set(peel, "Strength", .32)
    g.set(peel, "Distance", .00042)
    g.set(bump, "Normal", peel.outputs[0])
    pit = g.node("ShaderNodeBump", "Recess without cutting the mesh")
    pit.invert = True
    g.set(pit, "Height", hole)
    g.set(pit, "Distance", .00055)
    g.set(pit, "Strength", .70)
    g.set(pit, "Normal", bump.outputs[0])
    tone = m("MULTIPLY", m("ADD", .874, m("MULTIPLY", broad, .22)),
             m("SUBTRACT", 1., m("MULTIPLY", hole, .90)))
    pigment = g.node("ShaderNodeVectorMath", "Dyed hide beneath clear finish")
    pigment.operation = "SCALE"
    g.set(pigment, 0, g.inputs.outputs["Hide tone"])
    g.set(pigment, "Scale", tone)
    rough = m("ADD", m("ADD", .344, m("MULTIPLY", broad, .20)),
              m("ADD", m("MULTIPLY", fine, .056), m("MULTIPLY", hole, .23)))
    bs = g.node("ShaderNodeBsdfPrincipled", "Semi-matte topcoat")
    for k,val in {"Base Color":pigment.outputs[0], "Roughness":rough, "Normal":pit.outputs[0],
                  "Coat Weight":.075, "Coat Roughness":.42, "Sheen Weight":.08,
                  "Sheen Roughness":.48, "IOR":1.46}.items():
        g.set(bs, k, val)
    return g.finish(bs.outputs[0])


def hide(group, name, tone, perforation=0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = tone
    nodes = mat.node_tree.nodes
    nodes.remove(nodes.get("Principled BSDF"))
    n = nodes.new("ShaderNodeGroup")
    n.name, n.label, n.node_tree = FINISH, "Editable region finish", group
    n.inputs["Hide tone"].default_value = tone
    n.inputs["Perforation"].default_value = perforation
    n.width, n.location = 240, (-280, 280)
    out = nodes.get("Material Output")
    out.location = (40, 280)
    mat.node_tree.links.new(n.outputs[0], out.inputs["Surface"])
    return mat
