"""Owned baked 2-over/2-under twill. Appearance estimates, not OEM material data."""
import bpy
import numpy as np

YARN_PITCH_METRES = .0014
TILE_METRES = YARN_PITCH_METRES * 32


def make_carbon(out):
    material = bpy.data.materials.new('MAT_Console_Carbon')
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    shader = nodes.get('Principled BSDF')
    shader.inputs['Metallic'].default_value = 0
    shader.inputs['Roughness'].default_value = .28
    shader.inputs['Coat Weight'].default_value = .85
    shader.inputs['Coat Roughness'].default_value = .12
    size = 1024
    y, x = np.mgrid[0:size, 0:size] * (32 / size)
    # The shift of one yarn per row forms diagonal twill, never a checkerboard.
    warp = (np.floor(y) - np.floor(x)) % 4 < 2
    across = np.where(warp, x % 1, y % 1)
    along = np.where(warp, y % 2, x % 2)
    crown = np.sin(np.pi * across) ** .55
    tuck = .70 + .30 * np.sin(np.pi * along / 2) ** 2
    filaments = .5 + .5 * np.sin(across * np.pi * 24)
    height = .000018 * crown * tuck + .0000015 * filaments
    # Periodic central differences preserve continuity at tile boundaries.
    dx = (np.roll(height, -1, 1) - np.roll(height, 1, 1)) / (2 * TILE_METRES / size)
    dy = (np.roll(height, -1, 0) - np.roll(height, 1, 0)) / (2 * TILE_METRES / size)
    normal = np.dstack((-dx, -dy, np.ones_like(dx)))
    normal /= np.linalg.norm(normal, axis=2, keepdims=True)
    tone = (.018 + .038 * crown * tuck) * np.where(warp, 1.0, .65) + .002 * filaments
    for role in ['base', 'normal', 'roughness']:
        pixels = np.ones((size, size, 4), dtype=np.float32)
        if role == 'base':
            pixels[:, :, :3] = tone[:, :, None]
        elif role == 'normal':
            pixels[:, :, :3] = normal * .5 + .5
        else:
            # The delivery manifest applies a .28 factor: .86..1 becomes .24..28.
            pixels[:, :, :3] = (.86 + .14 * (1-crown))[:, :, None]
        image = bpy.data.images.new('front-cabin-carbon-' + role, width=size, height=size, alpha=True)
        if role != 'base': image.colorspace_settings.name = 'Non-Color'
        image.pixels.foreach_set(pixels.ravel())
        image.filepath_raw = str(out / ('front-cabin-carbon-' + role + '.png'))
        image.file_format = 'PNG'; image.save()
        tex = nodes.new('ShaderNodeTexImage'); tex.image = image
        if role == 'normal':
            bump = nodes.new('ShaderNodeNormalMap'); bump.inputs['Strength'].default_value = .45
            links.new(tex.outputs['Color'], bump.inputs['Color'])
            links.new(bump.outputs['Normal'], shader.inputs['Normal'])
        else:
            links.new(tex.outputs['Color'], shader.inputs['Base Color' if role == 'base' else 'Roughness'])
    return material


def physical_uvs(obj):
    """Fixed metre scale, projected per face on the existing thin trim surfaces."""
    for face in obj.data.polygons:
        if obj.data.materials[face.material_index].name != 'MAT_Console_Carbon': continue
        axis = max(range(3), key=lambda i: abs(face.normal[i]))
        axes = [(1, 2), (0, 2), (0, 1)][axis]
        for index in face.loop_indices:
            point = obj.data.vertices[obj.data.loops[index].vertex_index].co
            obj.data.uv_layers.active.data[index].uv = (point[axes[0]] / TILE_METRES, point[axes[1]] / TILE_METRES)
