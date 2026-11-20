"""GROK MEME MILLION V1.8.4 - real 3D coin turntable (Blender, Cycles CPU).

Run:  blender -b -P src/blender_coin.py -- <out_dir> [frames=72] [res=512] [samples=48]
Outputs <out_dir>/coin_00.png ... (RGBA, transparent), one frame per 360/frames degrees.
The face carries an original embossed Grok Bot mark (ring + slash), not a third-party logo.
"""
import bpy, math, sys, os

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(argv[0] if argv else "assets/coins")
FR = int(argv[1]) if len(argv) > 1 else 72
RES = int(argv[2]) if len(argv) > 2 else 512
SPP = int(argv[3]) if len(argv) > 3 else 48
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SPP
try:
    sc.cycles.use_denoising = False
except Exception:
    pass
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGBA"
sc.view_settings.view_transform = "Standard"

# ---------------- material: polished gold with reeded rim bump
gold = bpy.data.materials.new("Gold")
gold.use_nodes = True
nt = gold.node_tree
bsdf = nt.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (1.0, 0.70, 0.26, 1)
bsdf.inputs["Metallic"].default_value = 1.0
bsdf.inputs["Roughness"].default_value = 0.24
tc = nt.nodes.new("ShaderNodeTexCoord")
sep = nt.nodes.new("ShaderNodeSeparateXYZ")
at2 = nt.nodes.new("ShaderNodeMath"); at2.operation = "ARCTAN2"
mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 60.0
sinn = nt.nodes.new("ShaderNodeMath"); sinn.operation = "SINE"
bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35
nt.links.new(tc.outputs["Object"], sep.inputs[0])
nt.links.new(sep.outputs["X"], at2.inputs[0]); nt.links.new(sep.outputs["Z"], at2.inputs[1])
nt.links.new(at2.outputs[0], mul.inputs[0]); nt.links.new(mul.outputs[0], sinn.inputs[0])
nt.links.new(sinn.outputs[0], bump.inputs["Height"])
rim_mask = nt.nodes.new("ShaderNodeMath"); rim_mask.operation = "GREATER_THAN"; rim_mask.inputs[1].default_value = 0.93
lenn = nt.nodes.new("ShaderNodeVectorMath"); lenn.operation = "LENGTH"
comb = nt.nodes.new("ShaderNodeCombineXYZ")
nt.links.new(sep.outputs["X"], comb.inputs["X"]); nt.links.new(sep.outputs["Z"], comb.inputs["Z"])
nt.links.new(comb.outputs[0], lenn.inputs[0]); nt.links.new(lenn.outputs["Value"], rim_mask.inputs[0])
nt.links.new(rim_mask.outputs[0], bump.inputs["Strength"])
nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

dark = bpy.data.materials.new("GoldDeep")
dark.use_nodes = True
d = dark.node_tree.nodes["Principled BSDF"]
d.inputs["Base Color"].default_value = (0.85, 0.52, 0.14, 1)
d.inputs["Metallic"].default_value = 1.0
d.inputs["Roughness"].default_value = 0.38

# ---------------- coin body (axis = Y so the face looks at the camera)
bpy.ops.mesh.primitive_cylinder_add(vertices=160, radius=1.0, depth=0.15, location=(0, 0, 0), rotation=(math.pi / 2, 0, 0))
coin = bpy.context.object
coin.data.materials.append(gold)
bev = coin.modifiers.new("bevel", "BEVEL"); bev.width = 0.03; bev.segments = 4
bpy.ops.object.shade_smooth()
# inner recessed field ring (both faces)
for side in (-1, 1):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.86, minor_radius=0.035, location=(0, side * 0.075, 0), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object; o.data.materials.append(gold); bpy.ops.object.shade_smooth()
    # embossed mark: ring + slash
    bpy.ops.mesh.primitive_torus_add(major_radius=0.36, minor_radius=0.075, location=(0, side * 0.08, 0), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object; o.data.materials.append(dark); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, side * 0.085, 0), rotation=(0, math.radians(45), 0))
    o = bpy.context.object; o.scale = (0.11, 0.05, 1.25); o.data.materials.append(dark)
    bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.03; bv.segments = 3
# parent everything to an empty for the turntable
bpy.ops.object.empty_add(location=(0, 0, 0))
pivot = bpy.context.object
for o in list(bpy.data.objects):
    if o.type == "MESH":
        o.parent = pivot

# ---------------- camera + studio lights (key, fill, green rim like the app accent)
bpy.ops.object.camera_add(location=(0, -6.2, 0.35), rotation=(math.radians(86.8), 0, 0))
cam = bpy.context.object; cam.data.lens = 85; sc.camera = cam
for name, loc, energy, size, col in (("key", (-3.5, -4.0, 4.0), 1400, 3.5, (1, .97, .9)),
                                     ("fill", (4.5, -3.0, 0.5), 380, 4.0, (.9, .95, 1)),
                                     ("rim", (0.5, 4.0, 2.5), 700, 2.0, (.45, 1, .75)),
                                     ("top", (0, -1.0, 6.0), 300, 6.0, (1, 1, 1))):
    bpy.ops.object.light_add(type="AREA", location=loc)
    L = bpy.context.object; L.data.energy = energy; L.data.size = size; L.data.color = col
    tr = L.constraints.new("TRACK_TO"); tr.target = pivot; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"
# world: vertical gradient so the metal has something to reflect
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
wn = w.node_tree
tcw = wn.nodes.new("ShaderNodeTexCoord"); grad = wn.nodes.new("ShaderNodeSeparateXYZ")
ramp = wn.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.02, 0.025, 0.03, 1)
ramp.color_ramp.elements[1].color = (0.55, 0.55, 0.5, 1)
mapr = wn.nodes.new("ShaderNodeMapRange"); mapr.inputs["From Min"].default_value = -0.3; mapr.inputs["From Max"].default_value = 1.0
wn.links.new(tcw.outputs["Generated"], grad.inputs[0])
wn.links.new(grad.outputs["Z"], mapr.inputs["Value"]); wn.links.new(mapr.outputs["Result"], ramp.inputs["Fac"])
wn.links.new(ramp.outputs["Color"], wn.nodes["Background"].inputs["Color"])
wn.nodes["Background"].inputs["Strength"].default_value = 0.9

for i in range(FR):
    pivot.rotation_euler = (0, 0, 2 * math.pi * i / FR)
    sc.render.filepath = os.path.join(OUT, f"coin_{i:02d}.png")
    bpy.ops.render.render(write_still=True)
    print("COIN FRAME", i, flush=True)
