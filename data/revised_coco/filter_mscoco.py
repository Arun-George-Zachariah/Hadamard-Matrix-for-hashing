TRAIN_DATA_FILE = "/mydata/CSQ_Space/Hadamard-Matrix-for-hashing/data/coco/train.txt"
TEST_DATA_FILE = "/mydata/CSQ_Space/Hadamard-Matrix-for-hashing/data/coco/test.txt"
DATABASE_FILE = "/mydata/CSQ_Space/Hadamard-Matrix-for-hashing/data/coco/database.txt"
EVAL_DATA = "/mydata/CSQ_Space/15K_Dataset.txt"
TRAIN_OUT_FILE = "/mydata/CSQ_Space/Hadamard-Matrix-for-hashing/data/revised_coco/train.txt"
TEST_OUT_FILE = "/mydata/CSQ_Space/Hadamard-Matrix-for-hashing/data/revised_coco/test.txt"
DB_OUT_FILE = "/mydata/CSQ_Space/Hadamard-Matrix-for-hashing/data/revised_coco/database.txt"

def load_data():
    with open(TRAIN_DATA_FILE, 'r') as train_file, open(TEST_DATA_FILE, 'r') as test_file, open(DATABASE_FILE, 'r') as db_file :
        train_file_lst = train_file.readlines()
        test_file_lst = test_file.readlines()
        db_file_lst = db_file.readlines()

        return train_file_lst, test_file_lst, db_file_lst

if __name__ == '__main__':
    train_file_lst, test_file_lst, db_file_lst = load_data()

    with open(EVAL_DATA, 'r') as eval_file:
        # eval_file_lst = eval_file.readline()
        for eval_item in eval_file:

            for item in db_file_lst:
                if eval_item.replace("\n", "") in item:
                    db_file_lst.remove(item)
                    break

            for item in train_file_lst:
                if eval_item.replace("\n", "") in item:
                    train_file_lst.remove(item)
                    break

            for item in test_file_lst:
                if eval_item.replace("\n", "") in item:
                    test_file_lst.remove(item)
                    break

    with open(TRAIN_OUT_FILE, 'w') as f:
        for item in train_file_lst:
            f.write("%s\n" % item.replace("\n", ""))

    with open(TEST_OUT_FILE, 'w') as f:
        for item in test_file_lst:
            f.write("%s\n" % item.replace("\n", ""))

    with open(DB_OUT_FILE, 'w') as f:
        for item in db_file_lst:
            f.write("%s\n" % item.replace("\n", ""))
