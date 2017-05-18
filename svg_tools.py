"""SVG tools for curved crease origami."""
# disable warnings about variable names
# pylint: disable=C0103

import json
import cmath
import math
import sys
import svgpathtools as svg

def memodict(f):
    """ Memoization decorator for a function taking a single argument.
    From http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/
    """
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret 
    return memodict().__getitem__

def read_json_params(param_file):
    with open(param_file, 'r') as f:
        params = json.loads(''.join(f))
    return params

def read_svg(input_svg_file):
    """Reads an svg file and returns a list of svg path objects."""
    paths, attributes = svg.svg2paths(input_svg_file)
    return (paths, attributes)

def partial_offset_curve(path, start_t, end_t, offset_distance, steps=10):
    nls = []
    diff = end_t - start_t
    for k in range(steps):
        t = start_t + diff*k/steps
        offset_vector = offset_distance * path.normal(t)
        p = path.point(t)
        # print(p)
        nls.append(p + offset_vector)
    connect_the_dots = [svg.Line(nls[k], nls[k+1]) for k in range(len(nls) - 1)]
    offset_path = svg.Path(*connect_the_dots)

    return offset_path

@memodict
def scale_cut_file(input_tuple):
    (scale, cut_file) = input_tuple
    new_file = svg.Path()
    for path in cut_file:
        new_file.append(type(path)(*[point*scale for point in path]))
    return new_file

def scale_cut(start_pos, end_pos, cut_file):
    print(type(start_pos))
    print(start_pos)
    vec = end_pos - start_pos
    r, theta = cmath.polar(vec)
    (xmin, xmax, ymin, ymax) = cut_file.bbox()
    R = xmax - xmin
    scale = float(r)/R

    mid_pos = (start_pos + end_pos)/2.0

    new_file = scale_cut_file((scale, cut_file))

    center = (scale*(xmin+xmax)/2.0) + (scale*(ymin+ymax)/2.0)*1j

    new_file = new_file.rotated((180/math.pi)*theta, center)
    new_file = new_file.translated(mid_pos - center)

    return new_file

def cut(input_svg, params, cut_file=None):
    print('beginning cuts')
    l_range = params['cut_length']
    t_range = params['tab_length']

    if cut_file is None:
        positive = svg.Path()
        negative = svg.Path()
    else:
        cut_paths = []

    for path in input_svg:
        print('starting a path')
        # calculate number of cuts
        pathlength = float(path.length(error=1e-3))
        maxcuts = pathlength/(l_range[0]+t_range[0])
        mincuts = pathlength/(l_range[1]+t_range[1])
        ncuts = int((mincuts + maxcuts)/2)
        if ncuts == 0:
            print path
            print pathlength
        ltotal = pathlength/ncuts
        l = max(ltotal - (t_range[0] + t_range[1])/2, l_range[0])
        t = ltotal - l
        print('there are %s cuts' % ncuts)

        # accumulate segments
        for i in range(ncuts):
            print("%s/%s" % (ltotal*i, pathlength))
            cut_start = path.ilength(ltotal*i, s_tol=1e-3, error=1e-3)
            cut_end = path.ilength(ltotal*(i+1) - t, s_tol=1e-3, error=1e-3)
            if cut_file is None:
                positive.append(partial_offset_curve(path, cut_start, cut_end,
                                                     params['cut_width']/2))
                negative.append(partial_offset_curve(path, cut_start, cut_end,
                                                     -params['cut_width']/2))
            else:
                cut_start = path.point(cut_start)
                cut_end = path.point(cut_end)
                cut_paths.append(scale_cut(cut_start, cut_end, cut_file))
        print('cut a path')

    if cut_file is None:
        print('number of segments: %s' % len(positive))
    else:
        print('number of segments: %s' % len(cut_paths))

    if cut_file is None:
        cut_paths = []
        for i in range(len(positive)):
            pos_path = positive[i]
            neg_path = negative[i]
            pos_path.append(svg.Line(pos_path[-1].end, neg_path[-1].end))
            pos_path.extend(neg_path[::-1])
            pos_path.append(svg.Line(neg_path[0].start, pos_path[0].start))
            cut_paths.append(svg.Path(*pos_path))

    return cut_paths


if __name__ == '__main__':
    """ Usage: python svg_tools.py params.json in.svg out.svg"""
    cut_param_file = sys.argv[1] if len(sys.argv) > 1 else 'params.json'
    input_svg_file = sys.argv[2] if len(sys.argv) > 2 else 'in.svg'
    output_svg_file = sys.argv[3] if len(sys.argv) > 3 else 'out.svg'


    params = read_json_params(cut_param_file)
    input_cut_file = params['cut_file']

    (input_svg, svg_attributes) = read_svg(input_svg_file)
    print input_svg

    if input_cut_file:
        (input_cut, cut_attributes) = read_svg(input_cut_file)
        print input_cut[0]
        output_paths = cut(input_svg, params, input_cut[0])
    else:
        output_paths = cut(input_svg, params)

    svg.wsvg(output_paths, 'r'*len(output_paths), filename=output_svg_file)
