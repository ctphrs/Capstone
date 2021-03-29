import glob
import os
import shutil #to move the .csvfile
import deeplabcut


def new_video():
    video_path = 'home/project_location/videos'
    list_of_files = glob.glob(video_path + '/*.mp4')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)

    config_path = '/home/Capstone/config.yaml'
    deeplabcut.analyze_videos(config_path,[latest_file],
        shuffle=1, save_as_csv=True, videotype=.mp4)

    list_of_files = glob.glob(video_path + '/*.csv')
    csv_destination = '/home/where/do/you/want/it/lol'

    for file in list_of_files:
            original = r'' + file
            filename = file.replace(video_path, '')
            target = r'' + csv_destination + filename
            shutil.move(original, target)

    if os.path.isfile(latest_file):
        os.remove(latest_file)
        print("success")
    else:
        print("File doesn't exists!")

    return
