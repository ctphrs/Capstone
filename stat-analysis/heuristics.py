'''
Some additional heuristics that I want to add to the process
'''

import numpy as np

'''
given track data (string of deltas)
return a new track with all frames with a delta above a specified threshold THROWN OUT
'''
def delta_threshold(track_data, dth):
    tr = np.copy(track_data)
    rows = tr.shape[0]

    for i in range(0,rows):
        if tr[i,0] > dth or tr[i,1] > dth:
            tr[i] = 0

    return tr

'''
Same as delta_threshold, but instead drops points where the second derivative
of position is too high.
'''
def accel_dropper(track_data, ath):
    pass

