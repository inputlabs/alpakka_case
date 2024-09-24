from build123d import (
    BuildPart, BuildSketch, Rectangle, Circle, Mode, Plane, Axis,
    chamfer, extrude, loft)


TOTAL_BUTTON_HEIGHT = 18.3

LOWER_BUTTON_HEIGHT = 2.4
LOWER_BUTTON_RAD = 5.8
LOWER_BUTTON_WIDTH = 9.6

TOP_BUTTON_HEIGHT = 13.9
MID_BUTTON_HEIGHT = TOTAL_BUTTON_HEIGHT - TOP_BUTTON_HEIGHT - LOWER_BUTTON_HEIGHT
MID_BUTTON_RAD = 4.8

CHAMFER_SIZE = 0.5


with BuildPart() as button_abxy:
    with BuildSketch(Plane.XY.offset(LOWER_BUTTON_HEIGHT)) as bottom_sk:
        Circle(LOWER_BUTTON_RAD)
        Rectangle(2 * LOWER_BUTTON_RAD, LOWER_BUTTON_WIDTH, mode=Mode.INTERSECT)

    with BuildSketch(Plane.XY.offset(LOWER_BUTTON_HEIGHT + MID_BUTTON_HEIGHT)) as top_sk:
        Circle(MID_BUTTON_RAD)

    # Mid section first
    loft()

    # Extrude top and bottom
    extrude(bottom_sk.sketch, amount=-LOWER_BUTTON_HEIGHT)
    extrude(top_sk.sketch, amount=TOP_BUTTON_HEIGHT)

    # Chamfer top
    edges = button_abxy.part.edges().group_by(Axis.Z)[-1]
    chamfer(edges, CHAMFER_SIZE)


# __main__ => show in VSCode
# temp     => show in CQEditor
if __name__ in ['__main__', 'temp']:
    if __name__ == '__main__':
        from ocp_vscode import show_object

    show_object(button_abxy)
