rm -rf release/
mkdir release/
zip -u release/blender.zip blender/*.blend
zip -ru release/printables.zip stl/print_* 3mf/print_*
