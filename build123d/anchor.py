from build123d import (
    BuildPart, BuildSketch, BuildLine, Box, Plane, Polyline, Rectangle, Location, Locations,
    Axis, Rot, Mode, Align, Until,
    mirror, make_face, extrude, fillet, chamfer, split, faces, add, loft)

try:
    from ocp_vscode import show_object
except ModuleNotFoundError:
    pass

# top
TOP_WIDTH = 8
TOP_PTS = ((0,4),
    (11, 4),
    (8, 8.3),
    (0, 8.3),
    (0, 4))

# bottom
BOTTOM_WIDTH = 7
BOTTOM_PTS = ((6, 0),
    (15, 0),
    (11, 4),
    (6, 4),
    (6, 0))

BOTTOM_CUTOUT_WIDTH = 3
BOTTOM_CUTOUT_PTS = ((6, 0),
    (10, 0),
    (6, 4),
    (6, 0))


with BuildPart() as anchor:
    with BuildSketch(Plane.YZ):
        with BuildLine():
            Polyline(TOP_PTS)
        make_face()
    extrude(amount=TOP_WIDTH)

    with BuildSketch(Plane.YZ.offset((TOP_WIDTH - BOTTOM_WIDTH) / 2)):
        with BuildLine():
            Polyline(BOTTOM_PTS)
        make_face()
    extrude(amount=BOTTOM_WIDTH)

    with BuildPart(mode=Mode.SUBTRACT):
        with BuildSketch(Plane.YZ.offset(TOP_WIDTH - BOTTOM_WIDTH + BOTTOM_CUTOUT_WIDTH / 2)):
            with BuildLine():
                Polyline(BOTTOM_CUTOUT_PTS)
            make_face()
        extrude(amount=BOTTOM_CUTOUT_WIDTH)


# __main__ => show in VSCode
# temp     => show in CQEditor
if __name__ in ['__main__', 'temp']:
    if __name__ == '__main__':
        from ocp_vscode import show_object
        show_object(anchor)