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

