// Libraries
include <BOSL/constants.scad>
use <BOSL/transforms.scad>

// Project parameters
include <parameters.scad>

// Project modules
use <trigger1.scad>
use <trigger4.scad>
use <wheel.scad>

// Wheel
wheel(WheelType);
back(30) wheel(WHEEL_TYPE_SMOOTH);
back(60) wheel(WHEEL_TYPE_POLYGON);
back(90) wheel(WHEEL_TYPE_STAR);
right(20) wheelShaftPrint();
right(35) wheelHolder();

// R1
right(50) trigger1(TriggerFit);
right(50) back(30) trigger1(FIT_TIGHT);
right(50) back(60) trigger1(FIT_LOOSE);

// L1
right(70) mirror([1,0,0]) trigger1(TriggerFit);
right(70) back(30) mirror([1,0,0]) trigger1(FIT_TIGHT);
right(70) back(60) mirror([1,0,0]) trigger1(FIT_LOOSE);

// R4
right(95) trigger4(TriggerFit);
right(95) back(30) trigger4(FIT_TIGHT);
right(95) back(60) trigger4(FIT_LOOSE);

// L4
right(110) mirror([1,0,0]) trigger4(TriggerFit);
right(110) back(30) mirror([1,0,0]) trigger4(FIT_TIGHT);
right(110) back(60) mirror([1,0,0]) trigger4(FIT_LOOSE);
