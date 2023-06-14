include <BOSL/constants.scad>
use <BOSL/masks.scad>
use <dotSCAD/src/angle_between.scad>

module chamfer_through_xy(x,y,chamfer=undef,l=undef) {
  middle = (x+y)/2;
  diff = y-x;
  l = l == undef ? norm(diff) : l;
  
  translate(middle) rotate([0,0,-angle_between(diff,[1,0,0])])
    chamfer_mask_x(l=l, chamfer=chamfer);
}
