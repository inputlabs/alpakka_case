include <BOSL/constants.scad>
use <BOSL/masks.scad>
use <BOSL/shapes.scad>

include <parameters.scad>
use <common.scad>

module r4() {
  leverWidth = 5;
  leverDepth = 21.5;
  leverHeight = 13.5;
  draftWidth = 2.7;
  draftDepth = 7.5;
  protrusionHeight = 4.5;

  // Center on screw hole
  translate([-leverWidth/2,-leverDepth+leverWidth/2]) {
    // Lever
    difference() {
      // Lever body
      cube([leverWidth,leverDepth,leverHeight]);
      // Screw hole
      translate([leverWidth/2,leverDepth-leverWidth/2,-1])
        cylinder(h=leverHeight+2, d=ScrewDiameter+Tolerance, $fn=64);
      // Lever draft
      translate([draftWidth,0,-1]) rotate([0,0,180-atan(draftDepth/draftWidth)])
          cube([2*draftDepth,2*draftWidth,leverHeight+2]);
      // Chamfers
      translate([0,leverDepth])
        chamfer_mask_z(l=leverHeight, chamfer=Chamfer, align=V_ABOVE);
      translate([leverWidth,leverDepth])
        chamfer_mask_z(l=leverHeight, chamfer=Chamfer, align=V_ABOVE);
    }

    // Switch contact protrusion
    translate([leverWidth,protrusionHeight/2,6.75]) rotate([0,90,0])
      prismoid(
        size1=[leverHeight,protrusionHeight],
        size2=[3.5,protrusionHeight],
        h=2.6,
        shift=[-leverWidth/2,0]
      );

    // Trigger surface
    triggerPoints = [
      // Bottom points
      [0,0,0],         // 0
      [-0,9.6,0],      // 1
      [-4.5,12.6,0],   // 2
      [-8,-6,0],       // 3
      [-4.5,-6,0],     // 4
      [-3.1,0,0],      // 5

      // Top points
      [0,0,17],        // 6
      [0,9.6,17],      // 7
      [-4.5,12.6,17],  // 8
      [-14.5,-6,17],   // 9
      [-11,-6,17],     // 10
      [-7.5,0,17],     // 11
    ];
    // Points in each face MUST be defined in clock-wise order when looking from outside
    // in order to have correct normals and to form a valid object
    triggerFaces = [
      [0,1,2,3,4,5],      // top face
      [11,10,9,8,7,6],    // bottom face
      [6,7,1,0],
      [7,8,2,1],
      [8,9,3,2],
      [9,10,4,3],
      [10,11,5,4],
      [11,6,0,5]
    ];
    translate([0,draftDepth]) difference() {
      // Convexity is required to render correctly
      polyhedron(points = triggerPoints, faces = triggerFaces, convexity = 10);
      // Chamfers
      chamfer_through_xy(triggerPoints[3], triggerPoints[4], Chamfer, 10);
      chamfer_through_xy(triggerPoints[9], triggerPoints[10], Chamfer, 10);
      chamfer_through_xy(triggerPoints[1], triggerPoints[2], Chamfer, 10);
      chamfer_through_xy(triggerPoints[7], triggerPoints[8], Chamfer, 10);
    }
  }
}

r4();
