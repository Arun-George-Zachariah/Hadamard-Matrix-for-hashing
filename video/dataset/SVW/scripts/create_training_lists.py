# pandas==1.1.5

import pandas as pd
import os
import shutil

ANN_FILE = "/mydata/SVW.csv"
DATA_DIR = "/mydata/SVW"

if __name__ == "__main__":
    df = pd.read_csv(ANN_FILE)

    train_counter = 0
    test_counter = 0

    train_category_dict = {}
    test_category_dict = {}

    # Creating a dictionary of category and associated files.
    for index, row in df.iterrows():
        if not pd.isnull(row['FileName']):
            file_name = row['FileName']
            category = row['Genre']

            if row['Train 1?'] == 0:
                if category in test_category_dict:
                    file_lst = test_category_dict[category]
                    file_lst.append(file_name)
                    test_category_dict[category] = file_lst
                else:
                    test_category_dict[category] = [file_name]
            else:
                if category in train_category_dict:
                    file_lst = train_category_dict[category]
                    file_lst.append(file_name)
                    train_category_dict[category] = file_lst
                else:
                    train_category_dict[category] = [file_name]

    # Creating the list files and moving the video to the data directories
    with open("../raw/list_cvt/train.txt", 'a+') as f:
        counter = 0;
        for index, category in enumerate(train_category_dict):
            for file_name in train_category_dict[category]:
                f.write(str(index) + "	" + str(counter) + "	" + category + "/" + file_name + "\n")
                counter += 1

    with open("../raw/list_cvt/test.txt", 'a+') as f:
        counter = 0;
        for index, category in enumerate(test_category_dict):
            for files in test_category_dict[category]:
                f.write(str(index) + "	" + str(counter) + "	" + category + "/" + files + "\n")
                counter += 1
