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

The input svg can be created by any program, but it can be difficult to achieve a good output. I had success using Adobe Illustrator, but had to make sure that stroke width was set to 0 px (in other programs such as Corel Draw, this is called "hairline"). In the default mode, rather than specifying stroke width in the svg with the appropriate stroke-width modifier, Illustrator instead saves a double-line, leading to unexpected results once processed. See [this thread](https://forums.adobe.com/thread/973450) for more details on how to set stroke width to 0 px.

### Offset Cut ###

