// Libraries
include <BOSL/constants.scad>
use <BOSL/masks.scad>
use <BOSL/shapes.scad>
use <dotSCAD/src/loft.scad>

// Project parameters
include <parameters.scad>
use <common.scad>

leverWidth = 5;
leverDepth = 21.5;
leverHeight = 13.5;
draftWidth = 2.7;
draftDepth = 7.5;
protrusionHeight = 4.5;
chamfer = 1;

defaultFit = FIT_TIGHT;

module _trigger4_lever(fit=undef) {
  fit = fit == undef ? defaultFit : fit;
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
      chamfer_mask_z(l=leverHeight, chamfer=chamfer, align=V_ABOVE);
    translate([leverWidth,leverDepth])
      chamfer_mask_z(l=leverHeight, chamfer=chamfer, align=V_ABOVE);
  }

  // Switch contact protrusion
  translate([leverWidth,protrusionHeight/2,6.75]) rotate([0,90,0])
    prismoid(
      size1 = [leverHeight,protrusionHeight],
      size2 = [3.5,protrusionHeight],
      h = fit == FIT_TIGHT ? 2.6 : 2.5,
      shift = [-leverWidth/2,0]
    );
}

module _trigger4_trigger_surface() {
  // Points in each polygon MUST be defined in counter-clockwise
  // order to form a valid object
  triggerPoints = [
    // Bottom points
    [
      [-3.1,0,0],      
      [-4.5,-6,0],     
      [-8,-6,0],      
      [-4.5,12.6,0],  
      [-0,9.6,0],     
      [0,0,0],        
    ],
    // Top points
    [
      [-7.5,0,17],     
      [-11,-6,17],     
      [-14.5,-6,17],   
      [-4.5,12.6,17],  
      [0,9.6,17],      
      [0,0,17],        
    ]
  ];
  
  translate([0,draftDepth])
    difference() {
      loft([triggerPoints[0], triggerPoints[1]], 16);
      chamfer_through_xy(triggerPoints[0][3], triggerPoints[0][4], chamfer, 10);
      chamfer_through_xy(triggerPoints[1][3], triggerPoints[1][4], chamfer, 10);
      chamfer_through_xy(triggerPoints[0][1], triggerPoints[0][2], chamfer, 10);
      chamfer_through_xy(triggerPoints[1][1], triggerPoints[1][2], chamfer, 10);
    }
}

module trigger4(fit=undef) {
  // Center on screw hole
  translate([-leverWidth/2,-leverDepth+leverWidth/2]) {
    _trigger4_lever(fit);
    _trigger4_trigger_surface();
  }
}
