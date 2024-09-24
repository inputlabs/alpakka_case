from build123d import (
    BuildPart, BuildSketch, BuildLine, Box, Plane, Polyline, Rectangle, Location, Locations,
    Axis, Rot, Mode, Align, Until,
    mirror, make_face, extrude, fillet, chamfer, split, faces, add)


# bottom box
COVER_BOTTOM_WIDTH = 62
COVER_BOTTOM_DEPTH = 37
COVER_BOTTOM_HEIGHT = 2

# the two trapezoids
TRAPEZ_WIDTH = 25
TRAPEZ_PTS = ((0, 0), (TRAPEZ_WIDTH, 0), (20, 5), (5, 5), (0, 0))

# the two boxes
BOX_WIDTH = 6
BOX_DEPTH = 6
BOX_HEIGHT = 8
BOX_INSET = 8 # from outside

# friction tabs on the poyhedrons and boxes
TAB_WIDTH = 4
TAB_HEIGHT = 2
TAB_ANGLE = 5 # degrees

USE_TABS = True # only for friction hold of 3d-printed parts

FILLET_SIZE = 2


with BuildPart() as cover:
    # Bottom box
    with BuildSketch():
        Rectangle(COVER_BOTTOM_WIDTH, COVER_BOTTOM_DEPTH)
    extrude(amount=COVER_BOTTOM_HEIGHT)
    split(bisect_by=Plane.YZ)  # keep only half, since everything will be mirrored in the end

    # Front trapezoid
    plane = Plane.XZ.offset(-COVER_BOTTOM_DEPTH / 2)
    with BuildSketch(plane) as poly_sk:
        with BuildLine(Location((COVER_BOTTOM_WIDTH / 2 - TRAPEZ_WIDTH, COVER_BOTTOM_HEIGHT))):
            Polyline(TRAPEZ_PTS)
        make_face()
    extrude(amount=COVER_BOTTOM_HEIGHT)

    if USE_TABS:
        trapezoid_face = poly_sk.sketch.face().center()
        plane = Plane(
            origin=(trapezoid_face.X, trapezoid_face.Y, COVER_BOTTOM_HEIGHT + 2), x_dir=(-1, 0, 0), z_dir=(0, 1, 0)
        ) # manually construct a plane with some of the face center coordinates
        with BuildSketch(plane.rotated((TAB_ANGLE, 0, 0))): # create sketch on plane rotated about local y-axis
            Rectangle(TAB_WIDTH, TAB_HEIGHT, align=(Align.CENTER, Align.MAX)) # align top edge to y-axis
        extrude(until=Until.PREVIOUS)

    # Rear box
    with BuildPart(mode=Mode.PRIVATE) as box_pt: # construct private box on the origin and transform later
        with BuildSketch() as s:
            Rectangle(BOX_WIDTH, BOX_DEPTH)
        extrude(amount=BOX_HEIGHT)

        if USE_TABS:
            box_face = faces().filter_by(Axis.X)[-1]
            plane = Plane(box_face).rotated((0, -TAB_ANGLE, 0)) # rotate about local y-axis
            with BuildSketch(plane):
                Rectangle(TAB_WIDTH, TAB_HEIGHT, align=(Align.CENTER, Align.MAX)) # align top edge to y-axis
            extrude(until=Until.PREVIOUS)
        mirror(about=Plane.YZ) # leverage local centerline symmetry to mirror the tab

    loc = Location(
        (COVER_BOTTOM_WIDTH / 2 - BOX_INSET - BOX_WIDTH / 2, -COVER_BOTTOM_DEPTH / 2 - BOX_WIDTH / 2, 0)
    )
    with Locations(loc):
        add(box_pt.part)

    # Create fillets
    edges = cover.part.edges().filter_by(Axis.X).group_by(Axis.Y)[2][0]
    fillet(edges, FILLET_SIZE)
    edges = cover.part.edges().filter_by(Axis.X).group_by(Axis.Y)[1][1]
    fillet(edges, FILLET_SIZE)

    mirror(about=Plane.YZ)


# __main__ => show in VSCode
# temp     => show in CQEditor
if __name__ in ['__main__', 'temp']:
    if __name__ == '__main__':
        from ocp_vscode import show_object

    show_object(cover)

    print(f"Volume: {cover.part.volume}")
