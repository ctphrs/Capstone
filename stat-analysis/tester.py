import csvread
import stringer
import plotter
import integrator
import scorer
import heuristics
import numpy as np

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('please specify file')
        exit()
    fname = sys.argv[1]

    #Get a huge matrix out of the CSV
    bighead, bigdat = csvread.read_dlc(fname)

    #Get a smaller matrix containing only head and sldr data
    littlehead, littledat = csvread.extract_features(['head','sldr','hnch','nose'], bighead, bigdat)
    #Extract head data (as np.array)
    headpos = np.array(littledat[0])
    #Extract sldr data (as np.array)
    sldrpos = np.array(littledat[1])
    #Extract hnch data (as np.array)
    hnchpos = np.array(littledat[2])
    #Extract nose data (as np.array)
    nosepos = np.array(littledat[3])

    #Rename for consistency
    test_set = nosepos


    #Perform tracking analysis
    test_string = stringer.make_strings(test_set, prob_floor=0.20)
    capped = heuristics.delta_threshold(test_string, 15)
    interped = stringer.linear_interp(capped, tenacity=5)
    smoothed = stringer.smooth_string(interped, rolling_window=15)

    '''
    test_set = stringer.make_strings(test_set, prob_floor=0.95)
    #print('set1')
    #print(test_set)
    test_set = stringer.linear_interp(test_set, tenacity=15)
    #print('set2')
    #print(test_set)
    test_set = stringer.smooth_string(test_set, rolling_window=20)
    #print('set3')
    #print(test_set)
    '''


    #Display results to the user
    plotter.plot_joint(test_string)
    plotter.plot_joint(capped)
    plotter.plot_joint(interped)
    plotter.plot_joint(smoothed)


    euclidified = integrator.euclidify(smoothed)
    integrated = integrator.integrate(euclidified)
    print('integrated:', integrated)


    visible_discount = scorer.visible_time(euclidified)
    size_discount = scorer.factor_size(300) #assume pixels/meter
    vid_frames = euclidified.size
    vid_framerate = 24 #assume 30 fps
    time_discount = scorer.factor_time(vid_frames, vid_framerate)

    if visible_discount < 0.5:
        print('visible time was:',visible_discount)
        visible_discount = float('inf')
    score = integrated / visible_discount #always less than 1 - this enhances the score
    print('visible time:', visible_discount)
    
    score = score / size_discount #Assuming size_discount is ppm still, converts to meters.
    print('size discount:', size_discount)
    
    score = score / time_discount # t>1 minute: discount t<1minute: enhance. per-minute score.
    print('time discount:', time_discount)
    
    print('corrected score:', score)
