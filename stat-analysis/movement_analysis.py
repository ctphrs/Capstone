import csvread
import stringer
import plotter
import integrator
import scorer

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
given a processed track, score the thing.
'''
def score_track(track, fps=30, ppm=1000):
    #First, euclidify and integrate.
    euclidified = integrator.euclidify(track)
    integrated = integrator.integrate(euclidified)

    vid_frames = euclidified.size
    vid_framerate = fps

    #Calculate various discounts for the things that change between videos and setups
    visible_discount = scorer.visible_time(euclidified)
    time_discount = scorer.factor_time(vid_frames, vid_framerate)
    size_discount = scorer.factor_size(ppm)

    #Factor in all of the different discounts
    score = integrated / (time_discount * size_discount * visible_discount)

    return score

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

def analyze1(filename, prob_floor = 0.95, prob_floor_diff = 0.95,
            tenacity = 15, rolling_window = 20, fps = 30, ppm = 1000):
    #read the file
    main_header, main_data = csvread.read_dlc(filename)

    #Joints representing activity
    act_header, act_data = csvread.extract_features(['sldr','hnch','tlbs','rfpw',
        'lfpw','rrpw','lrpw'], main_header, main_data)
    joint_sldr = act_data[0]
    joint_hnch = act_data[1]
    joint_tlbs = act_data[2]
    joint_rfpw = act_data[3]
    joint_lfpw = act_data[4]
    joint_rrpw = act_data[5]
    joint_lrpw = act_data[6]
    #Differences
    rfpw_on_sldr = joint_diff(joint_sldr, joint_rfpw)
    lfpw_on_sldr = joint_diff(joint_sldr, joint_lfpw)
    rrpw_on_hnch = joint_diff(joint_hnch, joint_rrpw)
    lrpw_on_hnch = joint_diff(joint_hnch, joint_lrpw)
    #Start stringin'
    sldr_track = make_and_process_string(joint_sldr,
        prob_floor, tenacity, rolling_window)
    hnch_track = make_and_process_string(joint_hnch,
        prob_floor, tenacity, rolling_window)
    tlbs_track = make_and_process_string(joint_tlbs,
        prob_floor, tenacity, rolling_window)
    rfpw_track = make_and_process_string(rfpw_on_sldr,
        prob_floor_diff, tenacity, rolling_window)
    lfpw_track = make_and_process_string(lfpw_on_sldr,
        prob_floor_diff, tenacity, rolling_window)
    rrpw_track = make_and_process_string(rrpw_on_hnch,
        prob_floor_diff, tenacity, rolling_window)
    lrpw_track = make_and_process_string(lrpw_on_hnch,
        prob_floor_diff, tenacity, rolling_window)

    #Joints representing alertness
    alt_header, alt_data = csvread.extract_features(['head','lear','rear','tltp'],
        main_header, main_data)
    joint_head = alt_data[0]
    joint_lear = alt_data[1]
    joint_rear = alt_data[2]
    joint_tltp = alt_data[3]
    #differences
    head_on_sldr = joint_diff(joint_sldr, joint_head)
    lear_on_head = joint_diff(joint_head, joint_lear)
    rear_on_head = joint_diff(joint_head, joint_rear)
    tltp_on_tlbs = joint_diff(joint_tlbs, joint_tltp)
    #Start stringin'
    head_track = make_and_process_string(head_on_sldr,
        prob_floor_diff, tenacity, rolling_window)
    lear_track = make_and_process_string(lear_on_head,
        prob_floor_diff, tenacity, rolling_window)
    rear_track = make_and_process_string(rear_on_head,
        prob_floor_diff, tenacity, rolling_window)
    tltp_track = make_and_process_string(tltp_on_tlbs,
        prob_floor_diff, tenacity, rolling_window)

    #Start Scorin' everything
    score_sldr = score_track(sldr_track, fps, ppm)
    score_hnch = score_track(hnch_track, fps, ppm)
    score_tlbs = score_track(tlbs_track, fps, ppm)
    score_rfpw = score_track(rfpw_track, fps, ppm)
    score_lfpw = score_track(lfpw_track, fps, ppm)
    score_rrpw = score_track(rrpw_track, fps, ppm)
    score_lrpw = score_track(lrpw_track, fps, ppm)
    activity_scores = [score_sldr, score_hnch, score_tlbs, score_rfpw,
        score_lfpw, score_rrpw, score_lrpw]
    score_head = score_track(head_track, fps, ppm)
    score_lear = score_track(lear_track, fps, ppm)
    score_rear = score_track(rear_track, fps, ppm)
    score_tltp = score_track(tltp_track, fps, ppm)
    alertness_scores = [score_head, score_lear, score_rear, score_tltp]

    return (activity_scores, alertness_scores)

def analyze2(filename, prob_floor = 0.95, prob_floor_diff = 0.95,
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
    score_sldr = score_track_novis(sldr_track, fps, ppm)
    score_hnch = score_track_novis(hnch_track, fps, ppm)
    score_head = score_track_novis(head_track, fps, ppm)
    score_nose = score_track_novis(nose_track, fps, ppm)

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
    results = analyze2(sys.argv[1])
    print(results)

    #I'd return, but this isn't actually a function.
    exit()
