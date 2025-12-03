from build123d import (
    BuildPart, BuildSketch, BuildLine, Polyline, Plane, Rectangle, Locations,
    Mode, Circle, Align, extrude, mirror, make_face, export_stl
)

THICKNESS_AROUND = 1.2
THICKNESS_END = 0.5

PCB_WIDTH = 21.8
PCB_DEPTH = 46.9
PCB_THICKNESS = 1.65

DONGLE_HEIGHT = 4.12 # @ button
INSET = DONGLE_HEIGHT - PCB_THICKNESS

TOLERANCE_WIDTH = +0.35
TOLERANCE_HEIGHT = +0.1

ANTENNA_WIDTH = 13.2 + 0.75 # measured + tolerance
ANTENNA_DEPTH = 5.2 + 0.1

EJECTION_HOLE_SIZE = 2.3 # slightly larger than hex-key

CUT_WIDTH = 0.3
CUT_LONG = 31.2
CUT_SHORT = 15.6

BUMP_WIDTH = 4
BUMP_OFFSET = 1

MAIN_PTS_OUTER = (
    (0, 0),
    (PCB_WIDTH/2 + TOLERANCE_WIDTH + THICKNESS_AROUND, 0),
    (PCB_WIDTH/2 + TOLERANCE_WIDTH + THICKNESS_AROUND, THICKNESS_AROUND + PCB_THICKNESS + 2 * TOLERANCE_HEIGHT),
    (PCB_WIDTH/2 + TOLERANCE_WIDTH - INSET, DONGLE_HEIGHT + 2 * TOLERANCE_HEIGHT + 2 * THICKNESS_AROUND),
    (0, DONGLE_HEIGHT + 2 * TOLERANCE_HEIGHT + 2 * THICKNESS_AROUND)
)

# Not symmetric due to button => Need to specify all points
MAIN_PTS_INNER = (
    (-PCB_WIDTH/2 - TOLERANCE_WIDTH, THICKNESS_AROUND),
    ( PCB_WIDTH/2 + TOLERANCE_WIDTH, THICKNESS_AROUND),
    ( PCB_WIDTH/2 + TOLERANCE_WIDTH, PCB_THICKNESS + THICKNESS_AROUND + 2 * TOLERANCE_HEIGHT),
    ( PCB_WIDTH/2 - INSET/2 + TOLERANCE_WIDTH, DONGLE_HEIGHT + THICKNESS_AROUND - INSET/2 + 2 * TOLERANCE_HEIGHT),
    ( PCB_WIDTH/2 - INSET*1.5, DONGLE_HEIGHT + THICKNESS_AROUND + 2 * TOLERANCE_HEIGHT),
    (-PCB_WIDTH/2 - TOLERANCE_WIDTH + INSET, DONGLE_HEIGHT + THICKNESS_AROUND + 2 * TOLERANCE_HEIGHT),
    (-PCB_WIDTH/2 - TOLERANCE_WIDTH, PCB_THICKNESS + THICKNESS_AROUND + 2 * TOLERANCE_HEIGHT),
    (-PCB_WIDTH/2 - TOLERANCE_WIDTH, THICKNESS_AROUND - TOLERANCE_HEIGHT)
)

SUPPORT_PTS = (
    (0, 0),
    (10, 0),
    (10, 20),
    (0, 20)
)

SUPPORT_WIDTH = 0.4
SUPPORT_INTERFACE_INTERVAL = 0.4
LAYER_HEIGHT = 0.2

BUTTON_INSET = 14.3

with BuildPart() as dongle_case:
    # Main body
    with BuildSketch(Plane.XZ):
        with BuildLine():
            Polyline(MAIN_PTS_OUTER)
            mirror(about=Plane.YZ)
        make_face()
    total_depth = PCB_DEPTH + ANTENNA_DEPTH + THICKNESS_END
    extrude(amount=total_depth)

    # Remove interior
    with BuildSketch(Plane.XZ):
        with BuildLine():
            Polyline(MAIN_PTS_INNER)
        make_face()
    extrude(amount=PCB_DEPTH, mode=Mode.SUBTRACT)

    # Remove space for Antenna
    with BuildSketch(Plane.XZ.offset(PCB_DEPTH)):
        z = THICKNESS_AROUND + DONGLE_HEIGHT/2 + TOLERANCE_HEIGHT
        with Locations((0, z)):
            Rectangle(ANTENNA_WIDTH, DONGLE_HEIGHT + 2 * TOLERANCE_HEIGHT)
    extrude_amount = ANTENNA_DEPTH
    extrude(amount=extrude_amount, mode=Mode.SUBTRACT)

    # Ejection holes
    with BuildSketch(Plane.XZ.offset(PCB_DEPTH)):
        z = THICKNESS_AROUND + EJECTION_HOLE_SIZE / 2 + 0.1
        location1 = (-ANTENNA_WIDTH / 2 - 1.5, z)
        location2 = ( ANTENNA_WIDTH / 2 + 1.5, z)
        with Locations(location1, location2):
            Rectangle(EJECTION_HOLE_SIZE, EJECTION_HOLE_SIZE + 0.2)
    extrude_amount = -ANTENNA_DEPTH - THICKNESS_END
    extrude(amount=extrude_amount, both=True, mode=Mode.SUBTRACT)

    # Cuts to make bottom flexible => can press PCB + button against top
    x = PCB_WIDTH/2 + TOLERANCE_WIDTH
    with BuildSketch(Plane.XZ):  # Short cut.
        with Locations((x, 0)):
            Rectangle(CUT_WIDTH, THICKNESS_AROUND, align=(Align.MAX, Align.MIN))
    extrude(amount=CUT_SHORT, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XZ):  # Long cut.
        with Locations((-x, 0)):
            Rectangle(CUT_WIDTH, THICKNESS_AROUND, align=(Align.MIN, Align.MIN))
    extrude(amount=CUT_LONG, mode=Mode.SUBTRACT)

    # Bump to hold PCB in place.
    with BuildSketch(Plane.YZ):
        y = -PCB_THICKNESS/2 - BUMP_WIDTH/2 + BUMP_OFFSET
        z = THICKNESS_AROUND
        with Locations((y, z)):
            Circle(PCB_THICKNESS/2)
    extrude_amount = PCB_WIDTH/2 + TOLERANCE_WIDTH - CUT_WIDTH
    extrude(amount=extrude_amount, both=True)

    # Bump cut with the PCB shape.
    with BuildSketch(Plane.XY.offset(THICKNESS_AROUND)) as xxx1:
        with BuildLine():
            x = PCB_WIDTH/2 + TOLERANCE_WIDTH - BUMP_WIDTH
            y = -BUMP_WIDTH/2 - PCB_THICKNESS + BUMP_OFFSET
            Polyline(
                ( x + PCB_THICKNESS, y),
                (-x - PCB_THICKNESS, y),
                (-x,                 y + PCB_THICKNESS),
                ( x,                 y + PCB_THICKNESS),
                ( x + PCB_THICKNESS, y)
            )
        make_face()
    extrude(amount=PCB_THICKNESS/2, mode=Mode.SUBTRACT)

    # Support
    with BuildSketch(Plane.YZ):
        with BuildLine():
            Polyline(SUPPORT_PTS)
            mirror(about=Plane.YZ)
        make_face()
    extrude(amount=SUPPORT_WIDTH)



if __name__ == '__main__':
    from common.vscode import show_object
    show_object(dongle_case)
    print(f"Volume: {dongle_case.part.volume}")

export_stl(dongle_case.part, "dongle_case_support.stl")