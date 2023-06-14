# Alpakka Controller: OpenSCAD Source

This folder contains the source code that generates the files needed
to print the controller case.

These files don't produce printable output:
- [`constants.scad`](constants.scad) defines constants used for parametric design
- [`parameters.scad`](parameters.scad) defines most of the important variables
  (parameters) used in the design
- [`common.scad`](common.scad) contains handy functions and modules used
  throughout the project

Parts of the controller:
- [`r4.scad`](r4.scad) defines R4 trigger

Libraries:
- [`BOSL`](https://github.com/revarbat/BOSL) The Belfry OpenSCAD Library -
  A library of tools, shapes, and helpers to make OpenSCAD easier to use
- [`dotSCAD`](https://github.com/JustinSDK/dotSCAD)
  Reduce the burden of mathematics when playing OpenSCAD
