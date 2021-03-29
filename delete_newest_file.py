import glob
import os
import shutil #to move the .csvfile
import deeplabcut


def new_video():
    video_path = '/home/share'
    list_of_videos = glob.glob(video_path + '/*.mp4')  # * means all if need specific format then *.csv
    latest_file = max(list_of_videos, key=os.path.getctime)
    print(latest_file)

    config_path = '/home/CoffeeOverhead-AllenWilson-2021-02-23/config.yaml'
    deeplabcut.analyze_videos(config_path,[latest_file],
        shuffle=1, save_as_csv=True, videotype=.mp4)

    list_of_csv = glob.glob(video_path + '/*.csv')
    csv_destination = '/home/afww/CSV'

    for file in list_of_csv:
            original = r'' + file
            filename = file.replace(video_path, '')
            target = r'' + csv_destination + filename
            shutil.move(original, target)

    if os.path.isfile(latest_file):
        os.remove(latest_file)
        print("success")
    else:
        print("File doesn't exist!")

    return
