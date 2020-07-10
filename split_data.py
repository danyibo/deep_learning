import os
import shutil
import numpy as np
import random
from Ankle.tool import FolderProcess


class SplitData:
    def __init__(self, src_folder_path='', train_test_path=''):
        self.__src_folder_path = src_folder_path
        self.train_test_path = train_test_path
        self.copy_path = train_test_path

    def set_src_folder(self, src_folder_path):
        self.__src_folder_path = src_folder_path

    def set_train_test(self, trian_test_path):
        self.train_test_path = trian_test_path

    def copy_src_data(self):
        data_folder_name = os.path.basename(self.__src_folder_path)
        store_copy_data_folder = os.path.join(self.train_test_path, data_folder_name)
        FolderProcess.make_folder(store_copy_data_folder)
        for case in os.listdir(self.__src_folder_path):
            store_copy_case_path = os.path.join(store_copy_data_folder, case)
            FolderProcess.make_folder(store_copy_case_path)
            case_path = os.path.join(self.__src_folder_path, case)
            for file in os.listdir(case_path):
                file_path = os.path.join(case_path, file)
                shutil.copy(file_path, store_copy_case_path)

    def move_data(self, copy_data_path, set_name, set_size):
        all_data = os.listdir(copy_data_path)
        random.seed(12)
        set_index = random.sample(all_data, set_size)
        set_path = os.path.join(self.train_test_path, set_name)
        FolderProcess.make_folder(set_path)
        for case in set_index:
            shutil.move(os.path.join(copy_data_path, case), os.path.join(set_path, case))
            all_data.remove(case)

    def move_test_data(self, copy_data_path, set_name):
        set_path = os.path.join(self.train_test_path, set_name)
        FolderProcess.make_folder(set_path)
        for case in os.listdir(copy_data_path):
            shutil.move(os.path.join(copy_data_path, case), os.path.join(set_path, case))

    def split_data(self):
        data_folder_name = os.path.basename(self.__src_folder_path)
        copy_data_path = os.path.join(self.train_test_path, data_folder_name)
        while len(os.listdir(copy_data_path)) != 0:
            total_number = len(os.listdir(copy_data_path))
            train_size = int(np.floor(total_number * 0.7))
            val_size = int(np.floor(total_number * 0.1))
            self.move_data(copy_data_path, 'train', train_size)
            self.move_data(copy_data_path, 'val', val_size)
            self.move_test_data(copy_data_path, 'test')
        os.rmdir(copy_data_path)


def run_split_data(src_folder_path, train_test_path):
    split_data = SplitData()
    split_data.set_src_folder(src_folder_path)
    split_data.set_train_test(train_test_path)
    split_data.copy_src_data()
    split_data.split_data()
    folder_name = os.path.basename(src_folder_path)
    print("split {} data finished!".format(folder_name))


if __name__ == "__main__":
    src_folder_path = r"E:\Data\doctor tao\data\Ankle instability"
    train_test_path = r"E:\Data\doctor tao\data\lesions split"
    run_split_data(src_folder_path, train_test_path)



