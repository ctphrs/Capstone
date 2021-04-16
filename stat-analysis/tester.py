import csvread
import stringer
import plotter
import integrator
import scorer
import numpy as np

#Get a huge matrix out of the CSV
bighead, bigdat = csvread.read_dlc('/home/afww/Capstone/stat-analysis/video1DLC_resnet_50_alfonsoApr14shuffle1_350000.csv')

#Get a smaller matrix containing only head and sldr data
littlehead, littledat = csvread.extract_features(['head','sldr'], bighead, bigdat)
#Extract head data (as np.array)
headpos = np.array(littledat[0])
#Extract sldr data (as np.array)
sldrpos = np.array(littledat[1])

#subtract to get relative position
head_on_sldr = np.subtract(headpos, sldrpos)
#probability needs to be a minimum, not a difference.
head_on_sldr[:,2] = np.minimum(headpos[:,2],sldrpos[:,2])

#Rename for consistency
test_set = headpos

#Perform tracking analysis
test_string = stringer.make_strings(test_set, prob_floor=0.95)
interped = stringer.linear_interp(test_string, tenacity=15)
smoothed = stringer.smooth_string(interped, rolling_window=20)

test_set = stringer.make_strings(test_set, prob_floor=0.95)
#print('set1')
#print(test_set)
test_set = stringer.linear_interp(test_set, tenacity=15)
#print('set2')
#print(test_set)
test_set = stringer.smooth_string(test_set, rolling_window=20)
#print('set3')
#print(test_set)

#Display results to the user
plotter.plot_joint(test_string)
plotter.plot_joint(interped)
plotter.plot_joint(smoothed)


euclidified = integrator.euclidify(smoothed)
integrated = integrator.integrate(euclidified)


visible_discount = scorer.visible_time(euclidified)
size_discount = scorer.factor_size(1000) #assume 1000 pixels/meter
vid_frames = euclidified.size
vid_framerate = 30 #assume 30 fps
time_discount = scorer.factor_time(vid_frames, vid_framerate)

score = integrated / visible_discount #always less than 1 - this enhances the score
score = score / size_discount #Assuming size_discount is ppm still, converts to meters.
score = score / time_discount # t>1 minute: discount t<1minute: enhance. per-minute score.
print('integrated:', integrated)
print('visible time:', visible_discount)
print('size discount:', size_discount)
print('time discount:', time_discount)
print('final score:', score)
