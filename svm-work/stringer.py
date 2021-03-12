'''
This script is designed to take the information extracted from a CSV by csvread.py
and create "strings" of movement. As long as a given body part shows up continuously
with breaks no longer than tenacity*frames and with probabilty no lower than
prob_floor, that series of points is designated a movement_string. Computation is
done to determine at each frame of the movement_string how much movement has taken
place since the last frame of the movement_string. Interpolation is performed
along breaks.

After this is done, the resulting signal will be smoothed with a rolling average
technique of length rolling_window.

- How is the interpolation done?
- - Linearly?
- - Sigmoid?
- - Polynomial?
'''

import numpy as np

#tenacity = 10
#prob_floor = 0.95
#rolling_window = 15

'''
data is of type:
    numpy.ndarray
Makes a raw string of coordinate deltas in O(n)

prob_floor is applied here, then probs are forgotten
'''
def make_strings(data, prob_floor=0.95):
    string = []
    last = (-1.0,-1.0) #location of last point
    bl = 0 #break length
    fs = False #Found the start
    for point in data:
        newpoint = np.array([0.0,0.0])
        if point[2] < prob_floor: #Kill the low-probability points
            newpoint[0] = -1.0
            newpoint[1] = -1.0
        elif not fs: #Once we find the first point, set that as reference
            last = (point[0],point[1])
            newpoint[0] = 0.0
            newpoint[1] = 0.0
            fs = True
        else: #From then on, points are in reference to last accepted point
            newpoint[0] = np.abs(point[0] - last[0])
            newpoint[1] = np.abs(point[1] - last[1])
            last = (point[0], point[1])
        string.append(newpoint)
    string = np.array(string)
    return string

'''
interoplates over gaps in the string. Returns a new string with gaps sealed.
gaps are sealed by taking the value of the point immediately after, dividing that
by the length of the gap + 1, and applying that value to the entire gap and to the
point immediately after.

Perhaps this is called "constant interpolation."

tenacity is applied here, and zeroes are inserted where tenacity fails.
'''
def linear_interp(string, tenacity=10):

    #Set up variables pre-loop
    break_markers = [] #list of lists of first and last indices of breaks
    moving_marker = [-1,-1] #constantly overwritten as we switch states
    in_break = False #State for the below state machine

    #Find every break
    for i in range(len(string)):
        delta = string[i]
        bad = False #Determine if this point is real
        if not (delta[0] >= 0.0):
            bad = True
        #State machine that finds indices of all breaks
        if not in_break: #If we're not in break state
            if bad: #Switch if we enter
                in_break = True
                moving_marker[0] = i
        if in_break: #If we are in a break state
            if not bad: #Switch if we leave
                in_break = False
                moving_marker[1] = i-1
                break_markers.append(moving_marker[:]) #Append a copy
            if (i == len(string)-1):
                moving_marker[1] = i
                break_markers.append(moving_marker[:]) #Append a copy

    newstring = np.copy(string)
    #Interpolate over each break
    for marker in break_markers:
        bl = marker[1] - marker[0] + 1
        if (marker[1] == len(newstring)-1):
            for i in range(marker[0], len(newstring)):
                newstring[i,0] = 0.0
                newstring[i,1] = 0.0
            continue
        if (bl > tenacity): #Breaks that are too long are set to all zero
            for i in range(marker[0], marker[1] + 2):
                newstring[i,0] = 0.0
                newstring[i,1] = 0.0
            continue
        postval = string[marker[1]+1]
        avgx = postval[0] / (bl+1.0)
        avgy = postval[1] / (bl+1.0)
        for i in range(marker[0], marker[1] + 2):
            newstring[i,0] = avgx
            newstring[i,1] = avgy
    return newstring

'''
Runs a moving average of window length rolling_window across the string, producing
a new, smoother string.
'''
def smooth_string(string, rolling_window=15):
    newstring = np.copy(string)
    xwindow = np.array([])
    ywindow = np.array([])

    #Across the whole string
    for i in range(len(string)):
        xwindow = np.append(xwindow, string[i,0])
        ywindow = np.append(ywindow, string[i,1])
        np.append(ywindow, string[i,1])
        if np.size(xwindow) > rolling_window:
            xwindow = xwindow[1:]
            ywindow = ywindow[1:]
        newx = xwindow.mean()
        newy = ywindow.mean()
        newstring[i,0] = newx
        newstring[i,1] = newy
    return newstring
