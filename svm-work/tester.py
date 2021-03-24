import csvread
import stringer
import plotter
import integrator
import numpy as np

#Get a huge matrix out of the CSV
bighead, bigdat = csvread.read_dlc('skeleton.csv')

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
test_set = head_on_sldr
#Perform tracking analysis
test_string = stringer.make_strings(test_set, prob_floor=0.90)
interped = stringer.linear_interp(test_string, tenacity=15)
smoothed = stringer.smooth_string(interped, rolling_window=20)

#Display results to the user
plotter.plot_joint(test_string)
plotter.plot_joint(interped)
plotter.plot_joint(smoothed)

euclidified = integrator.euclidify(smoothed);
integrated = integrator.integrate(euclidified);
print(integrated)
