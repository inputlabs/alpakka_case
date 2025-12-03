from build123d import *
import math

BASE_X_LEN = 36
BASE_Y_LEN = 40
BASE_Z_LEN = 1.9
BASE_Y_SIDE = 20

HOLE_RADIUS = 5
HOLE_DISTANCE_FROM_CENTER = 12

TRAPEZ_THICKNESS = 2.758  ## Tight version was 2.8.
TRAPEZ_X_LEN = math.sqrt(10**2 + 10**2)  # Diagonal of 10x10 (Blender legacy).
TRAPEZ_Z_LEN = 18
TRAPEZ_TIP = 2.2

TABS_Z_LEN = 4


with BuildPart() as chex:
    # Base.
    with BuildSketch():
        with BuildLine():
            Polyline([
                (0,            BASE_Y_LEN/2),
                (BASE_X_LEN/2, BASE_Y_SIDE/2),
                (BASE_X_LEN/2, 0),
            ])
            mirror(about=Plane.YZ)
            mirror(about=Plane.XZ)
        make_face()
        # Holes.
        locations = [
            (0, HOLE_DISTANCE_FROM_CENTER),
            (0, -HOLE_DISTANCE_FROM_CENTER),
            (HOLE_DISTANCE_FROM_CENTER, 0),
            (-HOLE_DISTANCE_FROM_CENTER, 0),
        ]
        with Locations(locations):
            Circle(HOLE_RADIUS, mode=Mode.SUBTRACT)
    extrude(amount=BASE_Z_LEN)

    # Trapezoid.
    with BuildPart(mode=Mode.PRIVATE) as trapezoid_pt:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                points = (
                    (0,            0),
                    (TRAPEZ_X_LEN, 0),
                    (TRAPEZ_TIP,   TRAPEZ_Z_LEN - BASE_Z_LEN),
                    (0,            TRAPEZ_Z_LEN - BASE_Z_LEN),
                )
                Polyline(points)
                mirror(about=Plane.YZ)
            make_face()
        extrude(amount=TRAPEZ_THICKNESS/2, both=True)
    with Locations((0, 0, BASE_Z_LEN)):
        add(trapezoid_pt, rotation=(0, 0, -45))
        add(trapezoid_pt, rotation=(0, 0, 45))

    # Tabs (to prevent wrong insertion).
    tab_z = TRAPEZ_Z_LEN - TABS_Z_LEN
    normal = Axis(origin=(0,0,0), direction=(1,1,0))
    face1 = (chex.faces()
        .filter_by(normal)[1]
        .split(Plane.XY.offset(tab_z), keep=Keep.TOP)
    )
    face2 = (chex.faces()
        .filter_by(normal)[3]
        .split(Plane.XY.offset(tab_z), keep=Keep.TOP)
    )
    extrude(face1, until=Until.NEXT, dir=(0,1,0))
    extrude(face2, until=Until.NEXT, dir=(0,-1,0))

    with Locations((0, 0, 8)):
        Sphere(radius = 2)


if __name__ == '__main__':
    from common.vscode import show_object
    show_object(chex)
    print(f"Volume: {chex.part.volume}")
    # export_stl(chex.part, 'stl/test_hex.stl')
