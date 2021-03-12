import csvread
import stringer
import plotter

bighead, bigdat = csvread.read_dlc('skeleton.csv')
littlehead, littledat = csvread.extract_features(['sldr'], bighead, bigdat)
lear = littledat[0]
#print(lear)

string_lear = stringer.make_strings(lear, prob_floor=0.90)
#print(string_lear)

interped = stringer.linear_interp(string_lear, tenacity=10)
#print(interped)

smoothed = stringer.smooth_string(interped, rolling_window=15)
#print(smoothed)

plotter.plot_joint(string_lear)
plotter.plot_joint(interped)
plotter.plot_joint(smoothed)
