import numpy as np

'''
Given data on joint movement, possibly integrated and possibly movement_strings,
This script will return a human-interpretable score of how active a dog is
in terms of the part or parts of its body represented in data.
'''

'''
Returns the amount of the time (0. to 1.) that the part is visible.
This is useful for enhancing the score by the inverse of this number.
requires input of a numpy array of a EUCLID STRING
'''
def visible_time(euclid_string):
    zeroes = np.array([x for x in euclid_string if x == 0.0])
    zeroes = zeroes.size

    total = euclid_string.size
    frac = 1.0 - (zeroes / total)

    #We never want to end up dividing by zero!
    if frac == 0.0:
        return 1.0

    return frac

'''
Determine a discount for the score based on the size of objects in the video
'''
def factor_size(ppm):
    return ppm #do no fancy stuff yet

'''
Determine a discount for the score based on the speed and length of the video
Useful for per-minute analysis
'''
def factor_time(num_frames, frame_rate):
    seconds = float(num_frames) / float(frame_rate)
    minutes = seconds / 60.0
    return minutes #simply returns the minute-length of the video
