// Libraries
include <BOSL/constants.scad>
use <BOSL/shapes.scad>
use <BOSL/transforms.scad>

// Project parameters
include <parameters.scad>
use <common.scad>

wheelDiameter = 21.5;
wheelWidth = 6.75;
wheelContactDiameter = 9;
wheelContactOffset = 0.335;
wheelAxelLength = 4.3;
wheelAxelDiameter = 4;
wheelChamfer = 0.75;

defaultWheelVertices = 24;
defaultWheelSegments = 3;
defaultWheelType = WHEEL_TYPE_STAR;

module _wheel_body_star(vertices=undef, segments=undef) {
  vertices = vertices == undef ? defaultWheelVertices : vertices;
  segments = segments == undef ? defaultWheelSegments : segments;
  assert(vertices > 3, "Vertex count must be more than 3");
  assert(vertices%segments == 0, "Vertex count must be divisible by segment count");
  $fn = vertices/segments; // Cylinder sides per segment
  union() {
    for(i=[0:segments-1]) {
      rotate([0,0,360/vertices*i])
        cyl(d=wheelDiameter, h=wheelWidth, chamfer=wheelChamfer, align=V_ABOVE);
    }
  }
}

module _wheel_body(type=undef, vertices=undef, segments=undef) {
  type = type == undef ? defaultWheelType : type;
  if (type == WHEEL_TYPE_SMOOTH) {
    _wheel_body_star(128, 1);
  }
  if (type == WHEEL_TYPE_POLYGON) {
    _wheel_body_star(vertices, 1);
  }
  if (type == WHEEL_TYPE_STAR) {
    _wheel_body_star(vertices, segments);
  }
}

wheelShaftBodyWidthShort = 6;
wheelShaftBodyWidthLong = 11.75;
wheelShaftBodyHeight = 5.15;
wheelShaftContactWidth = 5;
wheelShaftContactHeight = 1.5;
wheelShaftHexDiameter = 2;
wheelShaftHexHeight = 3;
wheelShaftHexWidth = (sqrt(3)/2)*wheelShaftHexDiameter;

// Vertical tolerance is doubled to compensate for bridge sagging
module _wheelShaftBody(tolerance=0) {
  hull() {
    down(wheelShaftBodyHeight/2) {
      cube([
        wheelShaftBodyWidthShort+2*tolerance, 
        wheelShaftBodyWidthLong+2*tolerance, 
        wheelShaftBodyHeight+4*tolerance
      ], true);
      cube([
        wheelShaftBodyWidthLong+2*tolerance, 
        wheelShaftBodyWidthShort+2*tolerance, 
        wheelShaftBodyHeight+4*tolerance
      ], true);
    }
  }
}

module wheelShaft() {
  difference() {
    union() {
      _wheelShaftBody();
      // Contact Pad
      up(wheelShaftContactHeight/2)
        cube([wheelShaftContactWidth, wheelShaftContactWidth, wheelShaftContactHeight], true);
      // Shaft Hex
      up(wheelShaftContactHeight)
        cylinder(h=wheelShaftHexHeight, d=wheelShaftHexDiameter, $fn=6);
    }
    back(wheelShaftBodyWidthLong+wheelShaftHexWidth/2)
      cube(wheelShaftBodyWidthLong*2, true);
  }
}

module wheelShaftPrint() {
  up(wheelShaftBodyHeight)
    wheelShaft();
}

module _wheelShaftCutout() {
  difference() {
    _wheelShaftBody(Tolerance);
    back(wheelShaftBodyWidthLong+wheelShaftHexWidth/2+Tolerance)
      cube(wheelShaftBodyWidthLong*2, true);
  }
}

module wheel(type=undef, vertices=undef, segments=undef) {
  difference() {
    union() {
      _wheel_body(type, vertices, segments);
      // Contact interface
      up(wheelWidth)
        cylinder(d=wheelContactDiameter, h=wheelContactOffset, $fn=64);
      // Axle
      up(wheelWidth+wheelContactOffset)
        cylinder(d=wheelAxelDiameter, h=wheelAxelLength, $fn=64);
    }
    rotate([0,180,0])
      _wheelShaftCutout();
  }
}

module wheelAssembly(type=undef, vertices=undef, segments=undef) {
  wheel(type, vertices, segments);
  rotate([0,180,0]) wheelShaft();
}

wheelHolderWidth = 7;
wheelHolderHeight = 13;
wheelHolderTopDepth = 9.8;
wheelHolderBottomDepth = 13;
wheelHolderCutSize = 4.2;

module wheelHolder() {
  difference() {
    prismoid(
      size1=[wheelHolderWidth, wheelHolderBottomDepth],
      size2=[wheelHolderWidth, wheelHolderTopDepth],
      h=wheelHolderHeight
    );
    up(wheelHolderHeight-wheelHolderCutSize/2+Tolerance/2)
      cube([wheelHolderWidth+Tolerance, wheelHolderCutSize, wheelHolderCutSize+Tolerance], true);
  }
}
