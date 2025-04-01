from build123d import *

TOTAL_HEIGHT = 8.75

HEAD_RADIUS = 4
HEAD_TALL = 2
HEAD_CHAMFER = 0.4
NECK_RADIUS = 2.5

DOME_RADIUS = 12
DOME_TOP_HEIGHT = 1.85

HOLE_TOLERANCE_XY_MID = 0.1
HOLE_TOLERANCE_XY_TIGHT = 0.075
HOLE_TOLERANCE_Z = 0.5


def Thumbstick(HOLE_TOLERANCE_XY):
    HOLE_RADIUS = 2 + HOLE_TOLERANCE_XY
    HOLE_CUT = 1.5 + HOLE_TOLERANCE_XY
    HOLE_DEPTH = 5 + HOLE_TOLERANCE_Z

    with BuildPart() as thumbstick_right:
        # Dome.
        with BuildSketch(Plane.XZ) as dome:
            with Locations((0, -DOME_RADIUS + DOME_TOP_HEIGHT)):
                Circle(radius=DOME_RADIUS)
                split(bisect_by=Plane.XZ, keep=Keep.BOTTOM)
                split(bisect_by=Plane.YZ)

        # Neck and head.
        with BuildSketch(Plane.XZ) as shaft:
            # Neck.
            Rectangle(NECK_RADIUS, TOTAL_HEIGHT, align=Align.MIN)
            # Head.
            with BuildLine():
                Polyline(
                    (0,           TOTAL_HEIGHT),
                    (HEAD_RADIUS, TOTAL_HEIGHT),
                    (HEAD_RADIUS, TOTAL_HEIGHT - HEAD_TALL),
                    (0,           TOTAL_HEIGHT - HEAD_TALL - HEAD_RADIUS),
                )
            make_face()

        # Make 3D.
        revolve(axis=Axis.Z)

        # Remove hole.
        with BuildSketch(Plane.XY) as hole:
            Circle(radius=HOLE_RADIUS)
            Rectangle(HOLE_RADIUS * 2, HOLE_CUT * 2, mode=Mode.INTERSECT)
        extrude(amount=HOLE_DEPTH, mode=Mode.SUBTRACT)

        # Chamfer top edge.
        top_edge = edges().sort_by(Axis.Z)[-1]
        chamfer(top_edge, HEAD_CHAMFER)

    return thumbstick_right


thumbstick_right_mid = Thumbstick(HOLE_TOLERANCE_XY_MID)
thumbstick_right_tight = Thumbstick(HOLE_TOLERANCE_XY_TIGHT)


if __name__ == '__main__':
    from common.vscode import show_object
    show_object(thumbstick_right_mid, name='Thumbstick')
    # export_stl(thumbstick_right.part, 'stl/test_thumbstick_right.stl')
