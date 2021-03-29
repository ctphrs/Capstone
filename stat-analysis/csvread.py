import csv #Heavy lifting
import numpy as np #We'll use numpy for everything. Might as well start now.

#Read a DeepLabCut CSV file and transform it into useful numpy arrays
def read_dlc(filename):

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        #Read the first three lines as headers
        scorers = reader.__next__()
        joint = reader.__next__()
        attribute = reader.__next__()
        header = np.array((scorers, joint, attribute))

        #Read the rest of the lines as frame records
        contents = np.array([row for row in reader])
        contents = contents.astype(float)

        #Return tuple for unpacking
        return header, contents

#For each string in the list of feature names, extract the three
#corresponding columns. Then, return vertical arrays for each of
#these features, containing columns: x, y, p (confidence)
def extract_features(list_feat_names, header, contents):

    #Governing lists - these are python lists of np arrays of data.
    headers = []
    datas = []
    for name in list_feat_names:
        idx = 0 #Will become the index of the first column commensurate with name
        try:
            while header[1][idx] != name :
                idx = idx + 1
        except Exception: #If we count past the end, quit and warn the user.
            #TODO: Don't print. Use STDERR.
            print('Error determining index of', name)
            print('Most likely',name,'does not exist')
            print('Exiting')
            exit()
        end = idx+2

        #Slice arrays and add the extracted data to governing lists
        feat_head = header[:, idx:end+1]
        feat_cont = contents[:, idx:end+1]
        headers.append(feat_head)
        datas.append(feat_cont)

    #Finall, after all of that iteration and checking is done, return governing lists
    return (headers, datas)

#Main function for testing the library
if __name__ == '__main__':
    (header, frames) = read_dlc('skeleton.csv')
    (fh, fc) = extract_features(['lear','tlbs','tltp'],header,frames)
    print('fh[0]:',fh[0])
    print('fc[0]:',fc[0])
