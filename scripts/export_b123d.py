from build123d import Axis, Plane, export_stl, export_step

# Import parts.
import sys
sys.path.insert(1, './build123d')
from wheel import wheel, core, holder
from trigger_r1 import trigger_r1
from cover import cover
from anchor import anchor


STL_DIR = 'stl/'
STEP_DIR = 'step/'

def export(obj, filename):
    export_stl(obj, STL_DIR + filename + '.stl')
    export_step(obj, STEP_DIR + filename + '.step')

# Scroll wheel.
export(wheel.part, 'secondary_015mm_wheel')
export(core.part.rotate(Axis.X, 90), 'secondary_007mm_wheel_core')
export(holder.part, 'any_015mm_wheel_holder')

# Trigger L1/R1.
export(trigger_r1.part, 'primary_015mm_trigger_R1')
export(trigger_r1.part.mirror(Plane.YZ), 'primary_015mm_trigger_L1')

# Battery Cover.
export(cover.part, 'secondary_015mm_cover')

# Anchor.
export(anchor.part, 'any_015mm_anchors_2x')
