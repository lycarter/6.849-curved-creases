"""SVG tools for curved crease origami."""
# disable warnings about variable names
# pylint: disable=C0103


import json
import math
import sys
import svgpathtools as svg

def read_json_params(param_file):
    with open(param_file, 'r') as f:
        params = json.loads(''.join(f))
    return params

def read_svg(input_svg_file):
    """Reads an svg file and returns a list of svg path objects."""
    paths, attributes = svg.svg2paths(input_svg_file)
    return (paths, attributes)

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

    l = params['cut_length']

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

# def offset_curve(path, offset_distance, steps=300):
#     """Takes in a Path object, `path`, and a distance,
#     `offset_distance`, and outputs an piecewise-linear approximation
#     of the 'parallel' offset curve.

#     From svgpathtools documentation (https://pypi.python.org/pypi/svgpathtools)
#     """
#     nls = []
#     for seg in path:
#         ct = 1
#         for k in range(steps):
#             t = k / steps
#             offset_vector = offset_distance * seg.normal(t)
#             nl = svg.Line(seg.point(t), seg.point(t) + offset_vector)
#             nls.append(nl)
#     connect_the_dots = [svg.Line(nls[k].end, nls[k+1].end) for k in range(len(nls)-1)]
#     if path.isclosed():
#         connect_the_dots.append(svg.Line(nls[-1].end, nls[0].end))
#     offset_path = svg.Path(*connect_the_dots)

#     return offset_path

def partial_offset_curve(path, start_t, end_t, offset_distance, steps=300):
    nls = []
    diff = end_t - start_t
    for k in range(steps):
        t = start_t + diff*k/steps
        offset_vector = offset_distance * path.normal(t)
        nls.append(path.point(t) + offset_vector)
    connect_the_dots = [svg.Line(nls[k], nls[k+1]) for k in range(len(nls) - 1)]
    if path.isclosed():
        connect_the_dots.append(svg.Line(nls[-1], nls[0]))
    offset_path = svg.Path(*connect_the_dots)

    return offset_path

def offset_cut(input_svg, params):
    l = params['cut_length']
    t = params['tab_length']

    positive = svg.Path()
    negative = svg.Path()
    for path in input_svg:
        # calculate number of cuts
        maxcuts = path.length()/(l[0]+t[0])
        mincuts = path.length()/(l[1]+t[1])
        ncuts = int((mincuts + maxcuts)/2)
        ltotal = path.length()/ncuts
        l = max(ltotal - (t[0] + t[1])/2, l[0])
        t = ltotal - l
        for i in range(ncuts - 1):
            cut_start = path.ilength(ltotal*i)
            cut_end = path.ilength(ltotal*(i+1) - t)
            positive.append(partial_offset_curve(path, cut_start, cut_end,
                                                 params['cut_width']/2))
            negative.append(partial_offset_curve(path, cut_start, cut_end,
                                                 -params['cut_width']/2))

    cut_path = []
    for i in range(len(positive)):
        pos_path = positive[i]
        neg_path = negative[i]
        pos_path.append(svg.Line(pos_path[-1].end,neg_path[-1].start))
        pos_path.extend(neg_path[::-1])
        pos_path.extend(neg_path[0].start, pos_path[0].start)



if __name__ == '__main__':
    """ Usage: python svg_tools.py params.json in.svg out.svg"""
    cut_param_file = sys.argv[1] if len(sys.argv) > 1 else 'params.json'
    input_svg_file = sys.argv[2] if len(sys.argv) > 2 else 'in.svg'
    output_svg_file = sys.argv[3] if len(sys.argv) > 3 else 'out.svg'


    params = read_json_params(cut_param_file)
    input_cut_file = params['cut_file']

    (input_svg, svg_attributes) = read_svg(input_svg_file)

    if input_cut_file:
        (input_cut, cut_attributes) = read_svg(input_cut_file)
        discretized_svg = discretize_svg(input_svg, params)
        output_paths = apply_cut(discretized_svg, input_cut)
    else:
        output_paths = offset_cut(input_svg, params)

    svg.wsvg(output_paths, 'r'*len(output_paths), filename=output_svg_file)