"""Refined leather group. Uses R5-C's surface-distance punch coordinates and seam margin."""
import bpy

from leather import FINISH, Graph, punch_group

TONES = {
    "Yoke": (.205, .100, .036), "Lumbar": (.205, .100, .036),
    "Waterfall": (.205, .100, .036), "surrounds": (.150, .066, .023),
    "boxing": (.157, .070, .025), "head restraint": (.150, .066, .023),
    "recessed turn": (.095, .039, .014),
}


def apply_finish():
    g = Graph("AUTOLAB • refined cognac hide", [
        ("Hide tone", "Color", (*TONES["Yoke"], 1)),
        ("Perforation", "Float", 0.), ("Pitch (m)", "Float", .004),
    ], ("Finish", "Shader"))
    m = g.math
    coord = g.node("ShaderNodeTexCoord").outputs["Object"]
    broad = g.noise(coord, 24, 2.1, "Slow changes in dye and gloss").outputs["Fac"]
    warp = g.noise(coord, 235, 2.5, "Break up the shape of the grain").outputs["Color"]
    offset = g.node("ShaderNodeVectorMath")
    offset.operation = "MULTIPLY"
    g.set(offset, 0, warp)
    g.set(offset, 1, (.0015, .0011, .0009))
    warped = g.node("ShaderNodeVectorMath")
    warped.operation = "ADD"
    g.set(warped, 0, coord)
    g.set(warped, 1, offset.outputs[0])
    grain = g.node("ShaderNodeTexVoronoi", "Irregular shallow grain")
    grain.feature = "DISTANCE_TO_EDGE"
    g.set(grain, "Vector", warped.outputs[0])
    g.set(grain, "Scale", 790.)
    plates = g.ramp(grain.outputs["Distance"], .018, .22, 0, 1, "Rounded edges")
    fine = g.noise(coord, 2200, 1.8, "Fine pores").outputs["Fac"]
    relief = m("ADD", m("MULTIPLY", plates, .46), m("MULTIPLY", fine, .54))
    bump = g.node("ShaderNodeBump", "Shallow leather relief")
    g.set(bump, "Height", relief)
    g.set(bump, "Strength", .34)
    g.set(bump, "Distance", .00027)
    gloss = g.noise(coord, 130, 2.8, "Local finish variation").outputs["Fac"]
    rough = m("ADD", .385, m("ADD", m("MULTIPLY", broad, .17), m("MULTIPLY", gloss, .135)))
    pigment = g.node("ShaderNodeVectorMath", "Dyed surface")
    pigment.operation = "SCALE"
    g.set(pigment, 0, g.inputs.outputs["Hide tone"])
    g.set(pigment, "Scale", m("ADD", .82, m("MULTIPLY", broad, .32)))

    field = g.node("ShaderNodeGroup", "Rolled punch rim with unpunched margin")
    field.node_tree = punch_group()
    field.node_tree.name = "AUTOLAB • refined blind impression"
    ramp = next(n for n in field.node_tree.nodes if n.type == "VALTORGB")
    # 4 mm pitch; 1.24 mm dark core, feathering to a 1.68 mm outer lip.
    ramp.color_ramp.elements[0].position = .155
    ramp.color_ramp.elements[1].position = .210
    g.set(field, 0, g.inputs.outputs["Pitch (m)"])
    hole = m("MULTIPLY", field.outputs[0], g.inputs.outputs["Perforation"])
    rim = g.node("ShaderNodeBump", "Pressed edge of impression")
    rim.invert = True
    g.set(rim, "Height", hole)
    g.set(rim, "Normal", bump.outputs[0])
    g.set(rim, "Strength", .60)
    g.set(rim, "Distance", .00045)
    hide = g.node("ShaderNodeBsdfPrincipled", "Satin automotive finish")
    for k, v in {
        "Base Color": pigment.outputs[0], "Normal": rim.outputs[0], "Roughness": rough,
        "Specular IOR Level": .32, "IOR": 1.46, "Coat Weight": .025,
        "Coat Roughness": .53, "Sheen Weight": .045, "Sheen Roughness": .58,
    }.items():
        g.set(hide, k, v)
    # The fibre inside a punch does not reflect the softbox like the coated face.
    interior = g.node("ShaderNodeBsdfDiffuse", "Shadowed leather fibre")
    g.set(interior, "Color", (.009, .0045, .002, 1))
    g.set(interior, "Roughness", .80)
    mix = g.node("ShaderNodeMixShader", "Finish / blind impression")
    g.set(mix, 0, hole)
    g.set(mix, 1, hide.outputs[0])
    g.set(mix, 2, interior.outputs[0])
    group = g.finish(mix.outputs[0])
    for region, rgb in TONES.items():
        mat = bpy.data.materials["Cognac • " + region]
        node = mat.node_tree.nodes[FINISH]
        enabled = node.inputs["Perforation"].default_value
        node.node_tree = group
        node.inputs["Perforation"].default_value = enabled
        node.inputs["Pitch (m)"].default_value = .004
        node.inputs["Hide tone"].default_value = (*rgb, 1)
        mat.diffuse_color = (*rgb, 1)
