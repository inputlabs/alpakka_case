include <BOSL/constants.scad>
use <BOSL/masks.scad>

function dot_p(v1, v2, idx) =
  v1[idx] * v2[idx] + (idx > 0 ? dot_p(v1, v2, idx-1) : 0);

function dot_product(v1, v2) =
  dot_p(v1, v2, len(v1)-1);

function angle(v1,v2) =
  acos(dot_product(v1, v2) / (norm(v1) * norm(v2)));

module chamfer_through_xy(x,y,chamfer=undef,l=undef) {
  middle = (x+y)/2;
  diff = y-x;
  l = l == undef ? norm(diff) : l;
  
  translate(middle) rotate([0,0,angle(diff,[1,0,0])])
    chamfer_mask_x(l=l, chamfer=chamfer);
}
