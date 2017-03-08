#!/usr/bin/env python
 
import os
import shutil
import math
import numpy as np
import cv2
import h5py
import logging
from tqdm import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_single_hdf5(hdf5_file, data_shape, label_shape):
    """ create a hdf5 file"""
    logger.info("Start to create a new hdf file called \"{}\"".format(hdf5_file))
    if os.path.exists(hdf5_file):
        os.remove(hdf5_file)
    f = h5py.File(hdf5_file, 'w')
    f.create_dataset("data", data_shape, dtype="float32")
    f.create_dataset("label", label_shape, dtype="int16")
    return f

def write_multiple_hdf5_by_num_output(image_and_label_array, output_root, num_output):
    """write dataset into multiple hdf5 files, and each file must be less than 2GB otherwise Caffe will throw an error"""
    sample_size = image_and_label_array.shape[0]
    logging.info("sample_size = {}".format(sample_size))
    # image_size = (height, width, channels)
    image_size = cv2.imread(image_and_label_array[0, 0]).shape
    # image_size = (channels, height, width)
    image_size = (image_size[2], image_size[0], image_size[1])
    logging.info("image_size = {}".format(image_size))
    label_size = (image_and_label_array.shape[1] - 1, )
    logging.info("label_size = {}".format(label_size))
    batch_size = sample_size / num_output
    for index_output in np.arange(num_output):
        hdf5_file = "{:0>2d}.h5".format(index_output + 1)
        hdf5_file = os.path.join(output_root, hdf5_file)
        # the size of last batch usually is not the same as the previous batch
        start_index = index_output * batch_size
        end_index = (index_output + 1) * batch_size
        if index_output == num_output - 1:
            end_index += sample_size % num_output
        
        length = end_index - start_index
        data_shape = (length, ) + image_size
        label_shape = (length, ) + label_size
        f = create_single_hdf5(hdf5_file, data_shape, label_shape)
        logger.info("Start to write dataset to \"{}\"".format(hdf5_file))
        for i in tqdm(range(length)):
            j = start_index + i
            f["label"][i, :] = image_and_label_array[j, 1:].astype("int16")
            image_array = cv2.imread(image_and_label_array[j, 0]) # shape = (height, width, chennels)
            for channel in np.arange(image_size[0]):
                f["data"][i, channel] = image_array[:, :, channel].astype("float32") / 256
        logger.info("End to write dataset to \"{}\"".format(hdf5_file))

def write_multiple_hdf5_by_max_size(image_and_label_array, output_root, list_file_name, max_size, size_type="GB"):
    """write dataset into multiple hdf5 files, and each file must be less than max_size"""
    list_file_path = os.path.join(output_root, list_file_name)
    write_list_file = open(list_file_path, 'w')
    sample_size = image_and_label_array.shape[0]
    logging.info("sample_size = {}".format(sample_size))
    # image_size = (height, width, channels)
    image_size = cv2.imread(image_and_label_array[0, 0]).shape
    # image_size = (channels, height, width)
    image_size = (image_size[2], image_size[0], image_size[1])
    logging.info("image_size = {}".format(image_size))
    label_size = (image_and_label_array.shape[1] - 1, )
    logging.info("label_size = {}".format(label_size))
    # compute batch_size when data type is "float32" and label type is "int16"
    batch_size = image_size[0] * image_size[1] * image_size[2] * 32 / 8.0 + label_size[0] * 16 / 8.0
    batch_size = batch_size / 1024.0 / 1024.0 / 1024.0
    batch_size = int(max_size / batch_size)
    num_output = sample_size / batch_size
    for index_output in np.arange(num_output):
        hdf5_file = "{:0>2d}.h5".format(index_output + 1)
        hdf5_file = os.path.join(output_root, hdf5_file)
        data_shape = (batch_size, ) + image_size
        label_shape = (batch_size, ) + label_size
        f = create_single_hdf5(hdf5_file, data_shape, label_shape)
        write_list_file.write(hdf5_file + "\n")
        logger.info("Start to write dataset to \"{}\"".format(hdf5_file))
        for i in tqdm(range(batch_size)):
            j = index_output * batch_size + i
            f["label"][i, :] = image_and_label_array[j, 1:].astype("int16")
            image_array = cv2.imread(image_and_label_array[j, 0]) # shape = (height, width, channels)
            for channel in np.arange(image_size[0]):
                f["data"][i, channel] = image_array[:, :, channel].astype("float32") / 255.0
        logger.info("End to write dataset to \"{}\"".format(hdf5_file))
    # for last batch
    if sample_size % batch_size != 0:
        last_batch_size = sample_size % batch_size
        hdf5_file = "{:0>2d}.h5".format(num_output + 1)
        hdf5_file = os.path.join(output_root, hdf5_file)
        data_shape = (last_batch_size, ) + image_size
        label_shape = (last_batch_size, ) + label_size
        f = create_single_hdf5(hdf5_file, data_shape, label_shape)
        write_list_file.write(hdf5_file + "\n")
        logger.info("Start to write dataset to \"{}\"".format(hdf5_file))
        for i in tqdm(range(last_batch_size)):
            j = num_output * batch_size + i
            f["label"][i,:] = image_and_label_array[j, 1:].astype("int16")
            image_array = cv2.imread(image_and_label_array[j, 0]) # shape = (height, width, channels)
            for channel in np.arange(image_size[0]):
                f["data"][i, channel] = image_array[:, :, channel].astype("float32") / 255.0
        logger.info("End to write dataset to \"{}\"".format(hdf5_file))

def select_label(label_list, list_file_name):
    read_file = open(list_file_name, 'r')
    assert read_file != -1, "open {} failed!".format(list_file_name)
    label_line = read_file.readlines()[1]
    label_line.strip()
    labels = label_line.split()
    logger.info("label names: {}".format(labels))
    label_index = []
    for label in label_list:
        if not label in labels:
            logger.info("label = {} not found!".format(label))
            exit(-1)
        label_index.append(labels.index(label) + 1)
    return tuple(label_index)

if __name__ == "__main__":
    
    ORIGINAL_DATA_ROOT = "/home/wang/disk_4T/wang_data/original_dataset"
    CONVERT_DATA_ROOT = "/home/wang/disk_4T/wang_data/convert_dataset"
    IMAGE_ROOT = os.path.join(ORIGINAL_DATA_ROOT, "CelebA/Img/img_align_celeba")
    IMAGE_LIST_FILE = os.path.join(ORIGINAL_DATA_ROOT, "CelebA/Anno/list_attr_celeba.txt")
    TRAIN_OUTPUT_ROOT = os.path.join(CONVERT_DATA_ROOT, "train")
    if os.path.exists(TRAIN_OUTPUT_ROOT):
        shutil.rmtree(TRAIN_OUTPUT_ROOT)
    os.mkdir(TRAIN_OUTPUT_ROOT)
    TEST_OUTPUT_ROOT = os.path.join(CONVERT_DATA_ROOT, "test")
    if os.path.exists(TEST_OUTPUT_ROOT):
        shutil.rmtree(TEST_OUTPUT_ROOT)
    os.mkdir(TEST_OUTPUT_ROOT)

    label_index = select_label(["Smiling", "No_Beard", "Bangs", "Male"], IMAGE_LIST_FILE)
    cols = (0, ) + label_index
    logger.info("cols = {}".format(cols))
    txt_narray = np.loadtxt(IMAGE_LIST_FILE, skiprows=2, usecols=cols, dtype='|S100')
    num_sample = txt_narray.shape[0]
    for i in np.arange(num_sample):
        txt_narray[i, 0] = os.path.join(IMAGE_ROOT, txt_narray[i, 0])
        txt_narray[i, 1:] = map(lambda x: "0" if x == "-1" else "1", txt_narray[i, 1:])
    logger.info("Shuffle dataset!")
    np.random.shuffle(txt_narray)
    num_train = int(num_sample * 0.75)
    logger.info("#"*30 + "Start to create hdf5 dataset!" + "#"*30)
    logger.info("#"*30 + "Start to create train hdf5 dataset!" + "#"*30)
    write_multiple_hdf5_by_max_size(txt_narray[:num_train], TRAIN_OUTPUT_ROOT, "train.txt", 5)
    logger.info("#"*30 + "End to create train hdf5 dataset!" + "#"*30)
    logger.info("#"*30 + "Start to create test hdf5 dataset!" + "#"*30)
    write_multiple_hdf5_by_max_size(txt_narray[num_train:], TEST_OUTPUT_ROOT, "test.txt", 5)
    logger.info("#"*30 + "End to create test hdf5 dataset!" + "#"*30)

