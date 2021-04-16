import os
import time

import sys
import getpass
sys.path.insert(0,'../stat-analysis')
user = getpass.getuser()

import afww_interop_funcs as funcs
import movement_analysis as stats

nfs_dir = '/home/share'
wrk_dir = '/home/'+user+'/afww-interop-working'
config_path = '/home/'+user+'/alfonso-net/alfonso-wd-team-2021-04-14/config.yaml'
csv_archive = '/home/'+user+'/ARCH-04-16-NODELETE'

prob_floor = 0.95
prob_floor_diff = 0.95
tenacity = 5
rolling_window = 8 
fps = 30
ppm = 300

if __name__ == '__main__':

    #Loop
    while True:
        files_avail = len(os.listdir(nfs_dir))
        if files_avail < 2:
            print('no video available!')
            time.sleep(5)
            continue

        #Find oldest video
        vid_on_nfs,ctime = funcs.find_oldest_file(nfs_dir,'h264')
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

        #Also make labeled video!!
        funcs.dlc_label(mp4_in_wrk, config_path)
        
        #find CSV that was made
        csv_in_wrk,*ignore = funcs.find_latest_file(wrk_dir, 'csv')
        
        #Do stats analysis
        movement_list = stats.analyze2(csv_in_wrk, prob_floor=prob_floor,
            prob_floor_diff=prob_floor_diff, tenacity=tenacity,
            rolling_window=rolling_window, fps=fps, ppm=ppm)
        
        #archive CSV
        csv_in_arch = funcs.move(csv_in_wrk, csv_archive)
        
        #Delete all in wrk
        #funcs.delete_all(wrk_dir)

        #Instead of deleting, archive all in wrk.
        funcs.archive_all(wrk_dir, csv_archive)
        
        #PRINT to user
        print('RESULTS')
        print(movement_list)

        #Send data off to Corinne
        head = movement_list[2][1]
        nose = movement_list[3][1]
        hnch = movement_list[1][1]
        sldr = movement_list[0][1]
        funcs.insert_data(head=head, nose=nose, haunches=hnch,
                shoulder=sldr, timestamp = ctime)
