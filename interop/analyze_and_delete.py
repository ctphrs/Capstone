import glob
import os
import shutil #to move the .csvfile
#import deeplabcut

#TODO: double-check variable names
def find_latest_h264(video_path):
    #For every mp4 video in the specified path
    video_path = '/home/share'
    list_of_videos = glob.glob(video_path + '/*.h264')

    #Discover which is newest
    latest_file = max(list_of_videos, key=os.path.getctime)

    #Return the name
    print("found latest:",latest_file)
    return latest_file

#TODO: write function to re-encode and resize

#TODO: double-check variable names
def analyze_and_delete(video_file):
    #Run all DLC stuff to analyze it.
    config_path = '/home/CoffeeOverhead-AllenWilson-2021-02-23/config.yaml'
    #deeplabcut.analyze_videos(config_path,[video_file], shuffle=1, save_as_csv=True, videotype='.mp4')
    print("wouldve analyzed:", video_file)

    #Delete original video
    if os.path.isfile(video_file):
        os.remove(video_file)
        print("success: deleted original")
    else:
        print("File doesn't exist!")

#TODO: double-check variable names
def move_all_csvs(video_path,csv_destination):
    #Move any and all CSV files from that directory to dest.
    list_of_csv = glob.glob(video_path + '/*.csv')
    for file in list_of_csv:
        original = r'' + file
        filename = file.replace(video_path, '')
        target = r'' + csv_destination + filename
        shutil.move(original, target)
    print('success: moved all CSVs')


if __name__ == '__main__':
    pass
