import bpy
import math
from pathlib import Path

context = bpy.context
scene = context.scene
viewlayer = context.view_layer

class Entry:
    def __init__(
            self,
            col_name,
            stl_name,
            axis_up='Z',
            axis_forward='Y',
            merge=False,
            split=False,
            multiple=False,
            rotate=False,
            tolerance=False,
            mirror=False,
        ):
        self.col_name = col_name  # Collection name.
        self.stl_name_base = stl_name
        self.stl_name = stl_name
        self.axis_up = axis_up
        self.axis_forward = axis_forward
        self.merge = merge  # Export all the objects in the collection merged.
        self.multiple = multiple  # Multiple individual exports in the collection.
        self.split = split
        self.rotate = rotate
        self.tolerance = tolerance
        self.tight = tolerance  # Export tight variant.
        self.loose = tolerance  # Export loose variant.
        self.mirror = mirror

    @staticmethod
    def find(name):
        for entry in entries:
            if entry.col_name == name:
                return entry

    @property
    def objects(self):
        return [o for o in scene.objects if o.type == 'MESH']

    def process(self, variant=False):
        bpy.ops.object.select_all(action='DESELECT')
        if not variant and self.tolerance:
            if self.tight:
                self.process_tight()
            if self.loose:
                self.process_loose()
        for ob in self.objects:
            if not ob.visible_get(): continue
            viewlayer.objects.active = ob
            ob.select_set(True)
            if self.rotate:
                self.do_rotate(ob)
            if self.split:
                self.do_split(ob)
            if not self.merge:
                if self.multiple:
                    subentry = Entry.find(ob.name)
                    subentry.export()
                else:
                    self.export()
                ob.select_set(False)
        if self.merge:
            self.export()
        if not variant and self.mirror:
            self.process_mirror()

    def do_rotate(self, ob):
        for mod in ob.modifiers:
            if 'rotation' in mod.name:
                mod.show_viewport = True

    def do_split(self, ob):
        for mod in ob.modifiers:
            if 'instance' in mod.name:
                mod.show_viewport = False

    def process_tight(self):
        for ob in self.objects:
            for mod in ob.modifiers:
                if 'loose' in mod.name:
                    mod.show_viewport = False
                if 'tight' in mod.name:
                    mod.show_viewport = True
        self.stl_name = f'{entry.stl_name_base}_tight'
        self.tight = False
        self.process(True)

    def process_loose(self):
        for ob in self.objects:
            for mod in ob.modifiers:
                if 'loose' in mod.name:
                    mod.show_viewport = True
                if 'tight' in mod.name:
                    mod.show_viewport = False
        self.stl_name = f'{entry.stl_name_base}_loose'
        self.loose = False
        self.process(True)

    def process_mirror(self):
        for ob in self.objects:
            for mod in ob.modifiers:
                if 'Mirror print' in mod.name:
                    mod.show_viewport = True
        self.stl_name = self.stl_name.replace('R', 'L')
        self.mirror = False
        self.process(True)

    def export(self):
        root = Path(bpy.path.abspath("//")).parent
        path = root / 'stl' / f'{self.stl_name}.stl'
        bpy.ops.export_mesh.stl(
            filepath=str(path),
            use_selection=True,
            axis_up=self.axis_up,
            axis_forward=self.axis_forward)


entries = [
    Entry('Case front',       'primary_015mm_front'),
    Entry('R1',               'primary_015mm_trigger_R1', split=True, mirror=True),
    Entry('R2',               'primary_015mm_trigger_R2', '-Z', split=True, mirror=True),
    Entry('R4',               'primary_015mm_trigger_R4', '-Y', '-Z', split=True, mirror=True),
    Entry('DHat',             'primary_015mm_dhat'),
    Entry('Select',           'primary_007mm_select_4x', split=True),
    Entry('Case back',        'secondary_015mm_back', '-Z'),
    Entry('Case cover',       'secondary_015mm_cover'),
    Entry('Wheel',            'secondary_015mm_wheel', 'X'),
    Entry('Wheel shaft R',    'secondary_015mm_wheelshaft'),
    Entry('Abxy',             'secondary_007mm_abxy_4x', split=True),
    Entry('Dpad',             'secondary_007mm_dpad_4x', split=True),
    Entry('Home',             'secondary_007mm_home', rotate=True),
    Entry('Thumbstick',       'secondary_007mm_thumbstick', tolerance=True),
    Entry('Hexagon',          'conductive_015mm_hexagon', '-Z', tolerance=True),
    Entry('Wheel support',    'any_015mm_wheelholder', '-X'),
    Entry('Anchor',           'any_015mm_anchors_2x', '-Z', split=True),
    Entry('Soldering helper', 'any_020mm_solderstand', '-Z', merge=True),
    Entry('Scrollwheel', None, multiple=True),
]

for collection in bpy.data.collections:
    entry = Entry.find(collection.name)
    entry.process()
    break
