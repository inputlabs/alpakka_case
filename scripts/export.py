import bpy
import math
from pathlib import Path

context = bpy.context
scene = context.scene
viewlayer = context.view_layer

obs = [o for o in scene.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
root = Path(bpy.path.abspath("//")).parent

class Entry:
    def __init__(self, name, stl_name, axis_up='Z', axis_forward='Y',
            collection=False, transformation=None):
        self.name = name
        self.stl_name = stl_name
        self.axis_up = axis_up
        self.axis_forward = axis_forward
        self.collection = collection
        self.transformation = transformation

    def export(self):
        path = root / 'stl' / f'{self.stl_name}.stl'
        bpy.ops.export_mesh.stl(
            filepath=str(path),
            use_selection=True,
            axis_up=self.axis_up,
            axis_forward=self.axis_forward)


def get_entry(name, collection=False):
    for entry in entries:
        if entry.name == name and entry.collection == collection:
            return entry

def rotation(ob, x=0, y=0, z=0):
    if x: ob.rotation_euler.x = math.radians(x)
    if y: ob.rotation_euler.y = math.radians(y)
    if z: ob.rotation_euler.z = math.radians(z)

entries = [
    Entry('Case front',       'primary_015mm_front'),
    Entry('Case back',        'secondary_015mm_back', '-Z'),
    Entry('R1',               'primary_015mm_triggersR1'),
    Entry('R2',               'primary_015mm_triggersR2', '-Z'),
    Entry('R4',               'primary_015mm_triggersR4', '-Y', '-Z'),
    Entry('Anchor',           'any_015mm_anchors_(brim)', '-Z'),
    Entry('DHat',             'primary_015mm_dhat_(brim)'),
    Entry('Wheel',            'secondary_015mm_wheel', 'X'),
    Entry('Wheel shaft R',    'secondary_015mm_wheelshaft'),
    Entry('Wheel support',    'any_015mm_wheelholder'),
    Entry('Abxy',             'secondary_007mm_abxy'),
    Entry('Dpad',             'secondary_007mm_dpad'),
    Entry('Select',           'primary_007mm_select'),
    Entry('Thumbstick',       'secondary_007mm_thumbstick_(support)'),
    Entry('Home',             'secondary_007mm_home_(support)', transformation=lambda ob: rotation(ob, -8.4)),
    Entry('Case cover',       'secondary_015mm_cover'),
    Entry('Hexagon R',        'conductive_015mm_hexagon', '-Z'),
    Entry('Soldering helper', 'any_020mm_solderstand', '-Z', collection=True),
]

for collection in bpy.data.collections:
    collection = get_entry(collection.name, True)
    for ob in obs:
        if (ob.visible_get()):
            entry = collection or get_entry(ob.name)
            if not entry: break
            viewlayer.objects.active = ob
            ob.select_set(True)
            if entry.transformation:
                entry.transformation(ob)
            if not collection:
                entry.export()
                ob.select_set(False)
    if collection:
        collection.export()
