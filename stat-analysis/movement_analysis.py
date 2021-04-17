import csvread
import stringer
import plotter
import integrator
import scorer
import heuristics

import numpy as np
import sys

'''
given two joints, find the difference
and minimum of probability
'''
def joint_diff(joint1, joint2):
    #Subtract position deltas
    diff = np.subtract(joint2, joint1)
    #choose minimum of probability
    diff[:,2] = np.minimum(joint1[:,2], joint2[:,2])
    return diff

'''
given a joint, do all of the necessary track processing things.
'''
def make_and_process_string(joint_or_diff, prob_floor, tenacity, rolling_window):
    #Drop unlikely candidates and format
    track = stringer.make_strings(joint_or_diff, prob_floor)
    #Interpolate linearly (constant in first derivative) over gaps
    track = stringer.linear_interp(track,tenacity)
    #Smooth using a rolling average
    track = stringer.smooth_string(track,rolling_window)
    return track

'''
THREE
A new process for analysis type 3
'''
def proc3(joint, prob_floor, tenacity, rolling_window, delta_max):
    #Drop unlikely candidates and format
    track = stringer.make_strings(joint, prob_floor)

    #Drop obvious errors prior to interp
    track = heuristics.delta_threshold(track, delta_max*tenacity)

    #Interpolate linearly (constant in first derivative) over gaps
    track = stringer.linear_interp(track, tenacity)

    #Drop obvious errors after interp
    track = heuristics.delta_threshold(track, delta_max)

    #Smooth using a rolling average
    track = stringer.smooth_string(track, rolling_window)
    return track

'''
given a processed track, score the thing WITHOUT VISIBILITY ACCOUNTING
'''
def score_track_novis(track, fps=30, ppm=1000):
    #First, euclidify and integrate.
    euclidified = integrator.euclidify(track)
    integrated = integrator.integrate(euclidified)

    vid_frames = euclidified.size
    vid_framerate = fps

    #Calculate various discounts for the things that change between videos and setups
    time_discount = scorer.factor_time(vid_frames, vid_framerate)
    size_discount = scorer.factor_size(ppm)

    #Factor in all of the different discounts
    score = integrated / (time_discount * size_discount)

    return score

'''
given a processed track, score the thing WITH NEW VISIBILITY ACCOUNTING
'''
def score_track_newvis(track, fps=30, ppm=1000):
    #First, euclidify and integrate.
    euclidified = integrator.euclidify(track)
    integrated = integrator.integrate(euclidified)

    vid_frames = euclidified.size
    vid_framerate = fps

    #Calculate various discounts for the things that change between videos and setups
    visible_discount = scorer.visible_time(euclidified)
    time_discount = scorer.factor_time(vid_frames, vid_framerate)
    size_discount = scorer.factor_size(ppm)

    if visible_discount < 0.5:
        return 0.0

    #Factor in all of the different discounts
    score = integrated / (time_discount * size_discount * visible_discount)

    return score


'''
THREE
Scoring mechanism for analysis type 3
'''
def score3(track, fps=30, ppm=1000):
    #First, euclidify and integrate.
    euclidified = integrator.euclidify(track)
    integrated = integrator.integrate(euclidified)

    vid_frames = euclidified.size
    vid_framerate = fps

    #Calculate various discounts for the things that change between videos and setups
    visible_discount = scorer.visible_time(euclidified)
    time_discount = scorer.factor_time(vid_frames, vid_framerate)
    size_discount = scorer.factor_size(ppm)

    if visible_discount < 0.5:
        visible_discount = float('inf')

    #Factor in all of the different discounts
    score = integrated / (time_discount * size_discount * visible_discount)

    return score

'''
Given a file, do a complete analysis on certain joints.
'''
def analyze2(filename, prob_floor = 0.90, prob_floor_diff = 0.90,
            tenacity = 5, rolling_window = 15, fps = 24, ppm = 300):
    #read the file
    main_header, main_data = csvread.read_dlc(filename)

    #Joints representing activity
    act_header, act_data = csvread.extract_features(['sldr','hnch','head',
        'nose'], main_header, main_data)
    joint_sldr = act_data[0]
    joint_hnch = act_data[1]
    joint_head = act_data[2]
    joint_nose = act_data[3]

    #Track
    sldr_track = make_and_process_string(joint_sldr,
        prob_floor, tenacity, rolling_window)
    hnch_track = make_and_process_string(joint_hnch,
        prob_floor, tenacity, rolling_window)
    head_track = make_and_process_string(joint_head,
        prob_floor, tenacity, rolling_window)
    nose_track = make_and_process_string(joint_nose,
        prob_floor, tenacity, rolling_window)

    #Score
    score_sldr = score_track_newvis(sldr_track, fps, ppm)
    score_hnch = score_track_newvis(hnch_track, fps, ppm)
    score_head = score_track_newvis(head_track, fps, ppm)
    score_nose = score_track_newvis(nose_track, fps, ppm)

    return([('sldr',score_sldr),('hnch',score_hnch),('head',score_head),
        ('nose',score_nose)])

'''
THREE
Third and likely final attempt at analysis
Should be fairly similar to second attempt
Calls new core process involving new heuristics
'''
def analyze3(filename, prob_floor = 0.90, prob_floor_diff = 0.90,
            tenacity = 5, rolling_window = 15, fps = 24, ppm = 300,
            delta_max = 10):

    #read the file
    main_header, main_data = csvread.read_dlc(filename)

    #Joints representing activity
    act_header, act_data = csvread.extract_features(['sldr','hnch','head',
        'nose'], main_header, main_data)
    joint_sldr = act_data[0]; joint_hnch = act_data[1]; joint_head = act_data[2]; joint_nose = act_data[3]

    #Track
    sldr_track = proc3(joint_sldr, prob_floor, tenacity, rolling_window, delta_max)
    hnch_track = proc3(joint_hnch, prob_floor, tenacity, rolling_window, delta_max)
    head_track = proc3(joint_head, prob_floor, tenacity, rolling_window, delta_max)
    nose_track = proc3(joint_nose, prob_floor, tenacity, rolling_window, delta_max)

    #Score
    score_sldr = score3(sldr_track, fps, ppm)
    score_hnch = score3(hnch_track, fps, ppm)
    score_head = score3(head_track, fps, ppm)
    score_nose = score3(nose_track, fps, ppm)

    return([('sldr',score_sldr),('hnch',score_hnch),('head',score_head),
        ('nose',score_nose)])

def threestep(filename, prob_floor = 0.95, prob_floor_diff = 0.95,
            tenacity = 15, rolling_window = 20, fps = 30, ppm = 1000):
    #read the file
    main_header, main_data = csvread.read_dlc(filename)

    #Joints representing activity
    act_header, act_data = csvread.extract_features(['sldr','hnch','head',
        'nose'], main_header, main_data)
    joint_sldr = act_data[0]
    joint_hnch = act_data[1]
    joint_head = act_data[2]
    joint_nose = act_data[3]

    sldr_raw = stringer.make_strings(joint_sldr, prob_floor=prob_floor)
    sldr_int = stringer.linear_interp(sldr_raw, tenacity=tenacity)
    sldr_smt = stringer.smooth_string(sldr_int, rolling_window = rolling_window)
    plotter.plot_joint(sldr_raw)
    #plotter.plot_joint(sldr_int)
    #plotter.plot_joint(sldr_smt)

    hnch_raw = stringer.make_strings(joint_hnch, prob_floor=prob_floor)
    hnch_int = stringer.linear_interp(hnch_raw, tenacity=tenacity)
    hnch_smt = stringer.smooth_string(hnch_int, rolling_window = rolling_window)
    plotter.plot_joint(hnch_raw)
    #plotter.plot_joint(hnch_int)
    #plotter.plot_joint(hnch_smt)

    head_raw = stringer.make_strings(joint_head, prob_floor=prob_floor)
    head_int = stringer.linear_interp(head_raw, tenacity=tenacity)
    head_smt = stringer.smooth_string(head_int, rolling_window = rolling_window)
    plotter.plot_joint(head_raw)
    #plotter.plot_joint(head_int)
    #plotter.plot_joint(head_smt)

    nose_raw = stringer.make_strings(joint_nose, prob_floor=prob_floor)
    nose_int = stringer.linear_interp(nose_raw, tenacity=tenacity)
    nose_smt = stringer.smooth_string(nose_int, rolling_window = rolling_window)
    plotter.plot_joint(nose_raw)
    #plotter.plot_joint(nose_int)
    #plotter.plot_joint(nose_smt)

    #Score
    print()
    print('sldr')
    score_sldr = score_track_newvis(sldr_smt, fps, ppm)
    print()
    print('hnch')
    score_hnch = score_track_newvis(hnch_smt, fps, ppm)
    print()
    print('head')
    score_head = score_track_newvis(head_smt, fps, ppm)
    print()
    print('nose')
    score_nose = score_track_newvis(nose_smt, fps, ppm)

    return([('sldr',score_sldr),('hnch',score_hnch),('head',score_head),
        ('nose',score_nose)])

if __name__ == '__main__':

    #Ensure that command-line users are appropraitely chastized
    if len(sys.argv) != 2:
        print("Please provide exactly one argument when calling from command line")
        print("Please make sure that argument is the correct path to a CSV file")
        print("Please make sure that the CSV file was produced by DeepLabCut")
        exit()

    #Perform correct services for command-line users.
    #TODO: not accepting parameters like tenacity or ppm
    #CLI users may want this.
    results = analyze2(sys.argv[1],prob_floor=0.60)
    print('analyze2')
    print(results)
    results = analyze3(sys.argv[1],prob_floor=0.60)
    print('analyze3')
    print(results)

    #I'd return, but this isn't actually a function.
    exit()
