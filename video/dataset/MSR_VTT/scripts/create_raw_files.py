# Imports
import json
import pickle
import os
import shutil

# Constants
ANN_FILE = "/mydata/MSR_VTT_Dataset/train_val_videodatainfo.json"
OUT_FILE = "train.txt"
VIDEO_DIR = "/mydata/MSR_VTT_Dataset/TrainValVideo"
DEST_DIR = "/mydata/MSR_VTT_Dataset/data"

if __name__ == '__main__':
    # Initializing the ground truth dictionary
    category_dict = {}

    # Reading the annotations
    with open(ANN_FILE) as file:
        data = json.load(file)

        # Obtaining all the videos
        videos = data["videos"]

        # Iterating over the videos
        for video in videos:
            video_id = video["video_id"]
            video_category = video["category"]

            # Creating the ground truth based on the category
            if video_category in category_dict:
                lst = category_dict[video_category]
                lst.append(video_id)
                category_dict[video_category] = lst
            else:
                category_dict[video_category] = [video_id]

    # Initialing the counter
    counter = 0

    # Iterating over the categories
    for category in sorted(category_dict):
        # Creating the directory for the respective category
        if not os.path.exists("Category_" + str(category)):
            os.makedirs(DEST_DIR + "/Category_" + str(category))

        # Obtaining all videos belonging to the category
        video_lst = category_dict[category]

        # Iterating over the videos
        for video in video_lst:
            # Adding the details to the file
            with open(OUT_FILE, 'a+') as f:
                f.write(str(counter) + "	" + str(category) + "	" + "Category_" + str(category) + "/" + video + ".mp4\n")
            counter += 1

            # Copying the video to the directory
            shutil.copy(VIDEO_DIR + "/" + video + ".mp4", DEST_DIR + "/Category_" + str(category))



