"""SVG tools for curved crease origami."""

import json
import math
import svg.path as svg
import sys

def read_json_params(param_file):
    with open(param_file, 'r') as f:
        params = json.loads(''.join(f))
    return params

def read_svg(input_svg_file):
    """Reads an svg file and returns a list of svg path objects."""
    svg_paths = None

    # TODO(lycarter): figure out how to do this. probably svg.parse_path?

    return svg_paths

def discretize_path(path, l):
    """Discretizes a single path, with segments of length at least l."""
    total_length = path.length()
    segments = math.floor(total_length/l)
    pct = 1.0/segments

    discrete_path = svg.Path()

    for i in range(segments):
        start_pos = path.point(float(i)*pct)
        end_pos = path.point(float(i+1.0)*pct)
        line_segment = svg.Line(start=start_pos, end=end_pos)
        discrete_path.append(line_segment)

    return discrete_path

def discretize_svg(input_svg, params):
    """Discretizes an svg by the discretization parameters in params."""

    l = params['cut_pattern_length']

    new_paths = svg.Path()
    for path in input_svg:
        new_paths.extend(discretize_path(path, l))
    return new_paths

def modify_cut(line, input_cut):
    # TODO(lycarter): stretch input_cut to the length of line
    # TODO(lycarter): translate and rotate input_cut to match line
    pass

def apply_cut(discrete_svg, input_cut):
    cut_svg = svg.Path()
    for line in discrete_svg:
        cut_svg.append(modify_cut(line, input_cut))

    return cut_svg




if __name__ == '__main__':
    """ Usage: python svg_tools.py params.json in.svg out.svg"""
    cut_param_file = sys.argv[1] if len(sys.argv) > 1 else 'params.json'
    input_svg_file = sys.argv[2] if len(sys.argv) > 2 else 'in.svg'
    output_svg_file = sys.argv[3] if len(sys.argv) > 3 else 'out.svg'


    params = read_json_params(cut_param_file)
    input_cut_file = params['cut_file']

    input_svg = read_svg(input_svg_file)
    input_cut = read_svg(input_cut_file)

    discretized_svg = discretize_svg(input_svg, params)

    output_svg = apply_cut(discretized_svg, input_cut)