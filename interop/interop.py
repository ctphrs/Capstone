import sys
import getpass
sys.path.insert(0,'../stat-analysis')
user = getpass.getuser()

import afww_interop_funcs as funcs
import movement_analysis as stats

nfs_dir = '/home/share'
wrk_dir = '/home/'+user+'/afww-interop-working'
config_path = '/home/'+user+'/SOME-DLC/config.yaml'
csv_archive = '/home/'+user+'/CSV'

prob_floor = 0.95
prob_floor_diff = 0.95
tenacity = 15
rolling_window = 20
fps = 30
ppm=1000

if __name__ == '__main__':

    #Loop
    while True:
        
        #Find first video
        vid_on_nfs = funcs.find_latest_file(nfs_dir,'h264')
        if vid_on_nfs == None:
            continue
        
        #move to working directory
        h264_in_wrk = funcs.move(vid_on_nfs, wrk_dir)
        
        #re-encode
        mp4_in_wrk = funcs.encode_960(h264_in_wrk)
        
        #Delete the h264
        funcs.delete(h264_in_wrk)
        
        #analyze video
        funcs.dlc_analyze(mp4_in_wrk, config_path)
        
        #find CSV that was made
        csv_in_wrk = funcs.find_latest_file(wrk_dir, 'csv')
        
        #Do stats analysis
        movement_list = stats.analyze(csv_in_wrk, prob_floor=prob_floor,
            prob_floor_diff=prob_floor_diff, tenacity=tenacity,
            rolling_window=rolling_window, fps=fps, ppm=ppm)
        
        #archive CSV
        csv_in_arch = funcs.move(csv_in_wrk, csv_archive)
        
        #Delete all in wrk
        funcs.delete_all(wrk_dir)
        
        #For now, just print data
        #TODO: send off to Corinne
        print(movement_list)
