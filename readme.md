# Alpakka 3D-print

*Alpakka controller 3D-printed case and buttons (reference designs)*

## Project links
- [Alpakka Manual](https://inputlabs.io/devices/alpakka/manual).
- [Alpakka Firmware](https://github.com/inputlabs/alpakka_firmware).
- [Alpakka PCB](https://github.com/inputlabs/alpakka_pcb).
- [Alpakka 3D-print](https://github.com/inputlabs/alpakka_case). _(you are here)_
- [Input Labs Roadmap](https://github.com/orgs/inputlabs/projects/2/views/2).

## Previews
<span><img width='250px' src='./preview/print_A.png'/></span>
<span><img width='250px' src='./preview/print_B.png'/></span>
<span><img width='250px' src='./preview/print_C.png'/></span>
<span><img width='250px' src='./preview/print_D.png'/></span>
<span><img width='250px' src='./preview/print_E.png'/></span>
<span><img width='250px' src='./preview/print_F.png'/></span>

## LFS and file download
If you only want to download the Blender and STL files **DO NOT USE download ZIP** GitHub button, since it is not compatible with LFS (Large File Storage), but instead get the files from the [latest release](https://github.com/inputlabs/alpakka_case/releases/latest) package.

To use Git with this project it is required to install Git [Large File Storage](https://git-lfs.github.com).


## Repeated and mirrored parts
Some parts require to print 2x or 4x units, and some of them are mirrored. For simplicity, and to avoid mistakes, we export the STL files with these repetitions and mirroring baked in.

If you want to split these to arrange them better in the printer bed:

**In PrusaSlicer**
- Right click in object.
- Split > To objects.

**In Cura**
- Open Marketplace.
- Install `Mesh Tools` plugin.
- Right click in object.
- Mesh Tools > Split model into parts.

## File labels
- `primary`: Primary color or material according to Alpakka reference design color pattern.
- `secondary`: Primary color or material according to Alpakka reference design color pattern.
- `any`: Non visible part or tool that can be printed in any material, even recycled ;)
- `015mm`: 0.15mm layer height, default for most prints.
- `007mm`: 0.07mm layer height, for parts that require extra finesse.
- `020mm`: 0.20mm layer height, for tools that we want to print fast.
- `(brim)`: Consider using a brim for improved bed adhesion.
- `(support)` Requires support material, check the manual!.

Except for the colors (which is up to you how to combine), it is very recommended to follow these indications, and to check the [Manual](https://inputlabs.io/devices/alpakka/manual/diy_case) for more details.
