from build123d import (
    BuildPart, BuildSketch, BuildLine, Box, Plane, Polyline, Rectangle, Location, Locations,
    Axis, Rot, Mode, Align, Until, Cylinder, RegularPolygon,
    mirror, make_face, edges, extrude, fillet, chamfer, split, faces, add, loft)


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

BOLT_HOLE_RADIUS = 1.3

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
    #Top
    with BuildSketch(Plane.YZ):
        with BuildLine():
            Polyline(TOP_PTS)
        make_face()
    extrude(amount=TOP_WIDTH)

    edge_list = edges().filter_by(Axis.Z)
    chamfer(edge_list, CHAMFER)

    # Remove cutout for nut
    location = Location((TOP_WIDTH / 2, # align center
        TOP_DEPTH / 2, # align center
        TOP_HEIGHT - NUT_THICKNESS))
    with BuildSketch(location):
        RegularPolygon((NUT_WIDTH + NUT_TOLERANCE) / 2, 6, major_radius=False)
    extrude(amount=NUT_THICKNESS, mode=Mode.SUBTRACT)

    # Remove cutout for bolt
    location = Location((TOP_WIDTH / 2, # align center
        TOP_DEPTH / 2,  # align center
        (TOP_HEIGHT + BOTTOM_HEIGHT) / 2))
    with Locations(location):
        Cylinder(BOLT_HOLE_RADIUS, TOP_HEIGHT - BOTTOM_HEIGHT, mode=Mode.SUBTRACT)

    # Additional cutout to generate bridge for FDP printing
    if FDM_BRIDGE_THICKNESS > 0:
        location = Location((TOP_WIDTH / 2, # align center
            TOP_DEPTH / 2, # align center
            (TOP_HEIGHT + BOTTOM_HEIGHT) / 2 - FDM_BRIDGE_THICKNESS))
        with Locations(location):
            Box(BOLT_HOLE_RADIUS * 2,
                NUT_WIDTH + NUT_TOLERANCE,
                FDM_BRIDGE_THICKNESS,
                mode=Mode.SUBTRACT)


    # Bottom
    plane = Plane.YZ.offset((TOP_WIDTH - BOTTOM_WIDTH) / 2)
    with BuildSketch(plane):
        with BuildLine():
            Polyline(BOTTOM_PTS)
        make_face()
    extrude(amount=BOTTOM_WIDTH)

    with BuildPart(mode=Mode.SUBTRACT):
        plane = Plane.YZ.offset(TOP_WIDTH - BOTTOM_WIDTH + BOTTOM_CUTOUT_WIDTH / 2)
        with BuildSketch(plane):
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

    print(f"Volume: {anchor.part.volume}")
