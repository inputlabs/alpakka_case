from build123d import (
    BuildPart, BuildSketch, Plane, Axis, Rectangle,
    chamfer, extrude, loft, fillet)


TOTAL_BUTTON_HEIGHT = 16.3

BUTTON_DEPTH = 7.6

LOWER_BUTTON_HEIGHT = 2.3
LOWER_BUTTON_WIDTH = 9.6

TOP_BUTTON_HEIGHT = 12
TOP_BUTTON_WIDTH = 7.6

MID_BUTTON_HEIGHT = TOTAL_BUTTON_HEIGHT - TOP_BUTTON_HEIGHT - LOWER_BUTTON_HEIGHT

TOP_CHAMFER_SIZE = 0.5
SIDE_FILLET_SIZE = 1

with BuildPart() as button_select:
    with BuildSketch(Plane.XY.offset(LOWER_BUTTON_HEIGHT)) as bottom_sk:
        Rectangle(LOWER_BUTTON_WIDTH, BUTTON_DEPTH)

    with BuildSketch(Plane.XY.offset(LOWER_BUTTON_HEIGHT + MID_BUTTON_HEIGHT)) as top_sk:
        Rectangle(TOP_BUTTON_WIDTH, BUTTON_DEPTH)
        fillet(top_sk.vertices(), SIDE_FILLET_SIZE)

    # Mid section first
    loft()

    # Extrude top and bottom
    extrude(bottom_sk.sketch, amount=-LOWER_BUTTON_HEIGHT)
    extrude(top_sk.sketch, amount=TOP_BUTTON_HEIGHT)

    # Chamfer top
    edges = button_select.part.edges().group_by(Axis.Z)[-1]
    chamfer(edges, TOP_CHAMFER_SIZE)


# __main__ => show in VSCode
# temp     => show in CQEditor
if __name__ in ['__main__', 'temp']:
    if __name__ == '__main__':
        from ocp_vscode import show_object

    show_object(button_select)

    print(f"Volume: {button_select.part.volume}")
