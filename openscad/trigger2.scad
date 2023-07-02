// Libraries
include <BOSL2/std.scad>

// Project parameters
include <parameters.scad>

// Part parameters

baseWidth = 7;
baseLength = 16;
baseHeight = 4.1;
baseMiddleLength1 = 13;
baseMiddleLength2 = 9.8;
baseMiddleHeight = 5.4;
baseTopWidth = 13;
baseTopLength = 5;
baseTopHeight = 6;
baseTopOffset = 1;

surfaceWidthBottom = 18.4;
surfaceLengthBottom = 14;
surfaceHightBottom = 9.5;

surfaceWidthLower = 12.4;
surfaceLengthLower = 10.9;

surfaceLengthMiddle = 10.9;
surfaceHightMiddle = 6;
surfaceOffsetMiddle = 1.875;

surfaceWidthUpper = 9;

surfaceHightTop = 3;
surfaceLengthTop = 4.5;

surfaceDrafWidth = 4;

chamfer = 0.5;

module _trigger2Base() {
  cube([baseWidth, baseLength, baseHeight], anchor=FRONT+BOTTOM);
  move([0,baseLength-baseMiddleLength1,baseHeight])
    prismoid(
      [baseWidth, baseMiddleLength1],
      [baseWidth, baseMiddleLength2],
      h=baseMiddleHeight, 
      shift=[0, (baseMiddleLength1-baseMiddleLength2)/2],
      anchor=FRONT+BOTTOM
    );
  move([0,baseLength-baseMiddleLength2,baseHeight+baseMiddleHeight])
    prismoid(
      [baseWidth, baseMiddleLength2],
      [baseTopWidth, baseTopLength],
      h=baseTopHeight, 
      shift=[0, (baseMiddleLength2-baseTopOffset-baseTopLength)/2],
      anchor=FRONT+BOTTOM
    );
}

module _trigger2SurfaceBottom() {
  difference() {
    intersection() {
      prismoid(
        [surfaceWidthBottom, surfaceLengthBottom],
        [surfaceWidthBottom, surfaceLengthLower],
        h=surfaceHightBottom,
        shift=[0,(surfaceLengthLower-surfaceLengthBottom)/2],
        chamfer=chamfer,
        anchor=FRONT+BOTTOM
      );
      fwd(1)
        cuboid(
          [surfaceWidthBottom, surfaceLengthBottom+1, surfaceHightBottom+1],
          chamfer=chamfer,
          anchor=FRONT+BOTTOM
        );
    }
    xflip_copy() move([surfaceWidthBottom/2, 0, surfaceHightBottom/2]) zrot(90) 
      linear_extrude(height=surfaceHightBottom+1, center=true)
        mask2d_chamfer(
          x=surfaceDrafWidth,
          angle=adj_opp_to_ang((surfaceWidthBottom-baseWidth)/2, surfaceDrafWidth)
        );
  }
}

module _trigger2SurfaceLower() {
  move([0, surfaceLengthLower, surfaceHightBottom]) {
    prismoid(
      [surfaceWidthBottom, surfaceLengthTop],
      [surfaceWidthLower, surfaceLengthTop],
      h=surfaceHightMiddle,
      shift=[0,-surfaceOffsetMiddle],
      chamfer=chamfer,
      anchor=BACK+BOTTOM
    );
  }
}

module _trigger2SurfaceUpper() {
  move([0, surfaceLengthLower-surfaceOffsetMiddle, surfaceHightBottom+surfaceHightMiddle])
    prismoid(
      [surfaceWidthLower, surfaceLengthTop],
      [surfaceWidthUpper, surfaceLengthTop],
      h=6,
      chamfer=chamfer,
      anchor=BACK+BOTTOM
    );
}

module _trigger2SurfaceTop() {
  move([0, surfaceLengthLower-surfaceOffsetMiddle, surfaceHightBottom+surfaceHightMiddle*2])
    cuboid(
      [surfaceWidthUpper, surfaceLengthTop, surfaceHightTop],
      chamfer=chamfer,
      edges=["Z",TOP],
      anchor=BACK+BOTTOM
    );
}

module _trigger2Surface() {
  _trigger2SurfaceBottom();
  _trigger2SurfaceLower();
  _trigger2SurfaceUpper();
  _trigger2SurfaceTop();
  
  move([0, surfaceDrafWidth, surfaceHightBottom])
    prismoid(
      [surfaceWidthBottom, surfaceLengthTop],
      [9, surfaceLengthTop],
      h=surfaceHightMiddle,
      shift=[0, 0.525],
      anchor=FRONT+BOTTOM
    );
}

module trigger2() {
  _trigger2Base();
  back(baseLength) _trigger2Surface();
}

trigger2();
