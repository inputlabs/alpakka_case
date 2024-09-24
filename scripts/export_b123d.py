from build123d import Axis, Plane, Compound, Location, export_stl, export_step

# Import parts.
import sys
sys.path.insert(1, './build123d')
from wheel import wheel, core, holder
from trigger_r1 import trigger_r1
from button_select import button_select
from button_dpad import button_dpad
from cover import cover
from anchor import anchor
from button_abxy import button_abxy

STL_DIR = 'stl/'
STEP_DIR = 'step/'

def export(obj, filename):
    export_stl(obj, STL_DIR + filename + '.stl')
    export_step(obj, STEP_DIR + filename + '.step')

# Buttons.
export(button_abxy.part, 'secondary_007mm_abxy_4x')
export(button_dpad.part, 'secondary_007mm_dpad_4x')
export(button_select.part, 'primary_007mm_select_4x')

# Trigger L1/R1.
export(trigger_r1.part, 'primary_015mm_trigger_R1')
export(trigger_r1.part.mirror(Plane.YZ), 'primary_015mm_trigger_L1')

# Scroll wheel.
export(wheel.part, 'secondary_015mm_wheel')
export(core.part.rotate(Axis.X, 90), 'secondary_007mm_wheel_core')
export(holder.part, 'any_015mm_wheel_holder')

# Battery Cover.
export(cover.part, 'secondary_015mm_cover')

# Anchor.
export(anchor.part, 'any_015mm_anchors_2x')
