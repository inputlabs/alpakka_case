import bpy
from pathlib import Path

context = bpy.context
scene = context.scene
viewlayer = context.view_layer


obs = [o for o in scene.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')    

path = Path(bpy.path.abspath("//")).parent
print(path)

for ob in obs:
    if (ob.visible_get()):
        viewlayer.objects.active = ob
        ob.select_set(True)

stl_path = path / "STL" / f"{ob.name}.stl"
bpy.ops.export_mesh.stl(
filepath=str(stl_path),
axis_up='-Z',
use_selection=True)
