import glob
import sys
import os
import shutil #to move the .csv file
import deeplabcut
import subprocess
import pyodbc
import datetime

#Given a directory and a file extension
#Return latest file of that type in dir
#Do not include . in ext
def find_latest_file(video_dir, ext):
    #For every mp4 video in the specified path
    list_of_videos = glob.glob(video_dir + '/*.' + ext)

    if len(list_of_videos) == 0 :
        print('No such files:', ext)
        return None

    #Discover which is newest
    latest_file = max(list_of_videos, key=os.path.getctime)

    #remember its creation time
    ctime = os.path.getctime(latest_file)

    #Return the name
    return (latest_file, ctime)


def find_oldest_file(video_dir, ext):
    #For every mp4 video in the specified path
    list_of_videos = glob.glob(video_dir + '/*.' + ext)

    if len(list_of_videos) == 0 :
        print('No such files:', ext)
        return None

    #Discover which is newest
    latest_file = min(list_of_videos, key=os.path.getctime)

    #remember its creation time
    ctime = os.path.getctime(latest_file)

    #Return the name
    return (latest_file, ctime)


#Given a video file (assumed h264)
#Return path to newly-encoded mp4
def encode_960(h264_file):
    #Find proper name for if video were mp4
    name = h264_file.strip('.h264')
    mp4name = name + '.mp4'

    #re-encode. this IS a blocking function, thanks!
    subprocess.run(['ffmpeg', '-i', h264_file, '-vf', 'scale=-1:720', '-b:v', '15M',  mp4name])

    #Return name of new video
    return mp4name


#Run DeepLabCut Analysis on a video file
#using the network referenced in config_path
def dlc_analyze(video_file, config_path):
    #Run all DLC stuff to analyze it.
    deeplabcut.analyze_videos(config_path,[video_file], shuffle=1, save_as_csv=True, videotype='.mp4')

def dlc_label(video_file, config_path):
    #Make labeled video
    deeplabcut.create_labeled_video(config_path, [video_file])


#Check for file existence, then delete.
def delete(a_file):
    #Check for existence
    if os.path.isfile(a_file):
        os.remove(a_file)
    else:
        print("File doesn't exist:", file)


#Check for file existence, then move
def move(file, new_directory):
    #Check for existence
    if os.path.isfile(file) and os.path.isdir(new_directory):
        new_file = shutil.move(file, new_directory)
        return new_file
    else:
        print("File doesn't exist:", file)
        print("OR")
        print("Directory doesn't exist:", new_directory)


#delete every file in a specified directory
def delete_all(dir_name):
    list_of_files = glob.glob(dir_name + '/*')
    for file_or_dir in list_of_files:
        os.remove(file_or_dir)
    return

def archive_all(dir_name, dest_name):
    list_of_files = glob.glob(dir_name + '/*')
    for file_or_dir in list_of_files:
        new_file = shutil.move(file_or_dir, dest_name)
    return

#insert movement data into SPCA database
def insert_data(head, nose, haunches, shoulder, timestamp):
    server = 'afww-desktop'
    database = 'SPCA'
    uid = 'sa'
    pw = 'CNU1$cool'

    dt = datetime.datetime.fromtimestamp(timestamp)

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+uid+';PWD='+pw)

    cursor = conn.cursor()

    cursor.execute('''
                   INSERT INTO SPCA.dbo.Movement (Dog_ID, Head, Nose, Haunches, Shoulder, Time_Stamp)
                   VALUES (3, ?, ?, ?, ?, ?);
                   ''', head, nose, haunches, shoulder, dt)

    conn.commit()
    return
