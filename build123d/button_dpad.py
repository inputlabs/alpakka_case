from build123d import (
    BuildPart, BuildSketch, BuildLine, Plane, Axis, Polyline,
    chamfer, extrude, loft, mirror, make_face, fillet)


TOTAL_BUTTON_HEIGHT = 18.3

LOWER_BUTTON_HEIGHT = 2.4
LOWER_BUTTON_WIDTH = 9.6
LOWER_BUTTON_TIP = 11.54
LOWER_BUTTON_MID = 6.74

BOTTOM_OUTLINE_PTS = ((0,0), (LOWER_BUTTON_WIDTH / 2, 0),
    (LOWER_BUTTON_WIDTH / 2,
    LOWER_BUTTON_MID),
    (0, LOWER_BUTTON_TIP)) # Gets mirrored

TOP_BUTTON_HEIGHT = 13.9
TOP_BUTTON_WIDTH = 7.6
TOP_BUTTON_TIP = 10.54
TOP_BUTTON_MID = 6.74

TOP_OUTLINE_PTS = ((0,0), (TOP_BUTTON_WIDTH / 2, 0),
    (TOP_BUTTON_WIDTH / 2,
    TOP_BUTTON_MID),
    (0, TOP_BUTTON_TIP))

MID_BUTTON_HEIGHT = TOTAL_BUTTON_HEIGHT - TOP_BUTTON_HEIGHT - LOWER_BUTTON_HEIGHT

TOP_CHAMFER_SIZE = 0.5
SIDE_FILLET_SIZE = 1


with BuildPart() as button_dpad:
    with BuildSketch(Plane.XY.offset(LOWER_BUTTON_HEIGHT)) as bottom_sk:
        with BuildLine():
            Polyline(BOTTOM_OUTLINE_PTS)
            mirror(about=Plane.YZ)
        make_face()

    with BuildSketch(Plane.XY.offset(LOWER_BUTTON_HEIGHT + MID_BUTTON_HEIGHT)) as top_sk:
        with BuildLine() as top_outline:
            Polyline(TOP_OUTLINE_PTS)
            mirror(about=Plane.YZ)
        make_face()
        fillet(top_sk.vertices(), SIDE_FILLET_SIZE)

    # Mid section first
    loft()

    # Extrude top and bottom
    extrude(bottom_sk.sketch, amount=-LOWER_BUTTON_HEIGHT)
    extrude(top_sk.sketch, amount=TOP_BUTTON_HEIGHT)

    # Chamfer top
    edges = button_dpad.part.edges().group_by(Axis.Z)[-1]
    chamfer(edges, TOP_CHAMFER_SIZE)


# __main__ => show in VSCode
# temp     => show in CQEditor
if __name__ in ['__main__', 'temp']:
    if __name__ == '__main__':
        from ocp_vscode import show_object

    show_object(button_dpad)

    print(f"Volume: {button_dpad.part.volume}")

