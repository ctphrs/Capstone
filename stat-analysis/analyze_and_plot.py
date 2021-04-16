import csvread
import stringer
import plotter
import integrator
import scorer

import numpy as np
import sys

import movement_analysis as ma

if __name__ == '__main__':
    filename = sys.argv[1]
    framerate = int(sys.argv[2])
    ppm = int(sys.argv[3])
    result = ma.threestep(filename, prob_floor = 0.0, tenacity=framerate+2, rolling_window=framerate+4, fps=framerate, ppm=ppm) 
    print(result)
