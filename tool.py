import os
import numpy as np
import SimpleITK as sitk
import shutil


def copy_data(src_path, store_path):
    for file in os.listdir(src_path):
        file_path = os.path.join(src_path, file)
        shutil.copy(file_path, store_path)

def get_roi_index(roi_all):
    roi_sum = np.sum(roi_all, axis=(0, 1))
    roi_index = list(np.where(roi_sum != 0)[0])
    if roi_index[0] != 0:
        roi_index.insert(0, roi_index[0] - 1)
    if roi_index[-1] != roi_sum.shape[0] - 1:
        roi_index.append(roi_index[-1] + 1)
    return roi_index


def get_crop_shape(roi_all):

    h_roi = np.sum(roi_all, axis=0)  # shape(height, channels)
    h_roi = np.sum(h_roi, axis=1)  # 将数据加和到高这个维度上，shape(heights,)
    h_corp = np.where(h_roi != 0)[0]
    h_left, h_right = np.min(h_corp) - 1, np.max(h_corp) + 2

    w_roi = np.sum(roi_all, axis=1)
    w_roi = np.sum(w_roi, axis=1)
    w_crop = np.where(w_roi != 0)[0]
    w_top, w_bottom = np.min(w_crop) - 1, np.max(w_crop) + 2
    return h_left, h_right, w_top, w_bottom


def crop_data_array(roi_all, data_array):
    h_left, h_right, w_top, w_bottom = get_crop_shape(roi_all=roi_all)
    index_roi = get_roi_index(roi_all=roi_all)
    crop_array = data_array[w_top - 15: w_bottom + 15, h_left - 15: h_right + 15, :]
    return crop_array


def get_case_roi_dict(self, case_path):
    roi_list = []
    index_list = []
    for i in range(1, 9):
        index_list.append("roi_" + str(i))
    for file in os.listdir(case_path):
        if file != 'data.nii':
            roi_path = os.path.join(case_path, file)
            roi_array = DataProcess.get_array(roi_path)
            roi_list.append(roi_array)
    roi_dict = dict(zip(index_list, roi_list))
    return roi_dict


class FolderProcess:
    def __init__(self):
        pass

    @staticmethod
    def make_folder(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    @staticmethod
    def remove_folder(folder_path):
        if len(os.listdir(folder_path)) != 0:
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                os.remove(file_path)
        else:
            os.remove(folder_path)


class DataProcess:
    def __init__(self):
        pass

    @staticmethod
    def standard(data_array):
        data_array = (data_array - np.min(data_array)) / ((np.max(data_array) - np.min(data_array)))
        return data_array

    @staticmethod
    def get_array(data_path):
        data = sitk.ReadImage(data_path)
        data_array = sitk.GetArrayFromImage(data)
        data_array = np.transpose(data_array, (1, 2, 0))
        return data_array

