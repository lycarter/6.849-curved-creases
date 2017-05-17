# 6.849 Curved Creases #
Curved crease origami svg tools

## Installation/Requirements ##

1. Start a new [Python Virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)
2. Install requirements: `pip install -r requirements.txt`
3. Done!

## Usage ##

`python svg_tools.py params.json in.svg out.svg`

There are two modes: offset cut and cut from file. In offset cut, svg paths are traced with an offset. This leads to properly curved creases, but tabs are limited to straight tabs with right angles. When specifying a cut pattern from a file, a cut pattern can be supplied, which is then applied around each path. Unfortunately, the cut pattern nis interpolated, not curved to match the input file. In general, I've had good results with both, and for a sufficiently fine cut pattern, the interpolation is not very noticable.

### Input Files ###

See [`sample_params_offset.json`](sample_params_offset.json) for sample parameters for making an offset cut, and [`sample_params_cutfile.json`](sample_params_cutfile.json) for sample parameters for making a cut specified by an external file.

The input svg can be created by any program, but it can be difficult to achieve a good input. I had success using Adobe Illustrator, but had to make sure that stroke width was set to 0 px (in other programs such as Corel Draw, this is called "hairline"). In the default mode, rather than specifying stroke width in the svg with the appropriate stroke-width modifier, Illustrator instead saves a double-line, leading to unexpected results once processed (eg, a double-cut pattern). See [this thread](https://forums.adobe.com/thread/973450) for more details on how to set stroke width to 0 px. Finally, my code currently only supports svg paths - not other tags, such as `<circle>` and `<line>`. The workaround is to select all paths in Illustrator and make each a "compound path". See [this thread](http://stackoverflow.com/questions/7378742/use-adobe-illustrator-to-create-svg-path-using-move-to-commands) for more info. This actually took quite a while to figure out, since I started with trying to add support for non-path svg tags. Unfortunately, I couldn't find a Python library that supported this, and in general, working directly with paths seems to be preferrable for modularity. I don't really understand why svg's specification even includes non-path tags, since all non-path tags can be represented very easily by paths.

### Offset Cut ###

Input (stroke-width and stroke attributes have been modified manually to make it show up well on Github)

![](https://lycarter.github.io/6.849-curved-creases/circle.svg)

Output (stroke-width has been modified manually to make it show up well on Github)

![](https://lycarter.github.io/6.849-curved-creases/circle_out.svg)

A more complex example:

Input (stroke-width and stroke attributes have been modified manually to make it show up well on Github)

![](https://lycarter.github.io/6.849-curved-creases/circles.svg)

Output (stroke-width has been modified manually to make it show up well on Github)

![](https://lycarter.github.io/6.849-curved-creases/circles_out.svg)


### External File Cut ###

For both examples, the cut file used is (stroke-width and stroke attributes have been modified manually to make it show up well on Github)

![](https://lycarter.github.io/6.849-curved-creases/cut_spec.svg)

Input (stroke-width and stroke attributes have been modified manually to make it show up well on Github)

![](https://lycarter.github.io/6.849-curved-creases/circle.svg)

Output (stroke-width has been modified manually to make it show up well on Github)

![](https://lycarter.github.io/6.849-curved-creases/circle_cutfile.svg)

A more complex example:

Input (stroke-width and stroke attributes have been modified manually to make it show up well on Github)

![](https://lycarter.github.io/6.849-curved-creases/circles.svg)

Output (stroke-width has been modified manually to make it show up well on Github)

![](https://lycarter.github.io/6.849-curved-creases/circles_cutfile.svg)
