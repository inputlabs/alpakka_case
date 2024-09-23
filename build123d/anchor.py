from build123d import (
    BuildPart, BuildSketch, BuildLine, Box, Plane, Polyline, Rectangle, Location, Locations,
    Axis, Rot, Mode, Align, Until, Cylinder, RegularPolygon,
    mirror, make_face, edges, extrude, fillet, chamfer, split, faces, add, loft)


try:
    from ocp_vscode import show_object
except ModuleNotFoundError:
    pass

# top
TOP_WIDTH = 8
TOP_DEPTH = 8
TOP_HEIGHT = 8.3
TOP_PTS = ((0,4),
    (11, 4),
    (TOP_DEPTH, TOP_HEIGHT),
    (0, TOP_HEIGHT),
    (0, 4))
CHAMFER = 1

NUT_THICKNESS = 2.3 # should be 1.75 according to https://www.engineersedge.com/hardware/standard_metric_hex_nuts_13728.htm
NUT_WIDTH = 5 # across flats for M2.5 x 0.45
NUT_TOLERANCE = +0.181

BOLT_HOLE_RAD = 1.3

# bottom
BOTTOM_WIDTH = 7
BOTTOM_HEIGHT = 4
BOTTOM_PTS = ((6, 0),
    (15, 0),
    (11, BOTTOM_HEIGHT),
    (6, BOTTOM_HEIGHT),
    (6, 0))

BOTTOM_CUTOUT_WIDTH = 3
BOTTOM_CUTOUT_PTS = ((6, 0),
    (10, 0),
    (6, 4),
    (6, 0))

FDM_BRIDGE_THICKNESS = 0.2 # only for FDM printing, otherwise set to 0.0


with BuildPart() as anchor:
    with BuildSketch(Plane.YZ):
        with BuildLine():
            Polyline(TOP_PTS)
        make_face()
    extrude(amount=TOP_WIDTH)

    edge_list = edges().filter_by(Axis.Z)
    chamfer(edge_list, CHAMFER)


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

    with BuildSketch(Location((TOP_WIDTH / 2, TOP_DEPTH / 2, TOP_HEIGHT - NUT_THICKNESS))):
        RegularPolygon((NUT_WIDTH + NUT_TOLERANCE) / 2, 6, major_radius=False)
    extrude(amount=NUT_THICKNESS, mode=Mode.SUBTRACT)

    with Locations(Location((TOP_WIDTH / 2, TOP_DEPTH / 2, (TOP_HEIGHT + BOTTOM_HEIGHT) / 2))):
        Cylinder(BOLT_HOLE_RAD, TOP_HEIGHT - BOTTOM_HEIGHT, mode=Mode.SUBTRACT)

    if FDM_BRIDGE_THICKNESS > 0:
        with Locations(Location((TOP_WIDTH / 2, TOP_DEPTH / 2, (TOP_HEIGHT + BOTTOM_HEIGHT) / 2 - 0.25))):
            Box(BOLT_HOLE_RAD * 2, (NUT_WIDTH + NUT_TOLERANCE), FDM_BRIDGE_THICKNESS, mode=Mode.SUBTRACT)



# __main__ => show in VSCode
# temp     => show in CQEditor
if __name__ in ['__main__', 'temp']:
    if __name__ == '__main__':
        from ocp_vscode import show_object

    show_object(anchor)

    print(f"Volume: {anchor.part.volume}")
