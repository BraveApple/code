#!/usr/bin/env python

import lmdb
from tqdm import *
import numpy as np
import logging
import os
import shutil
import cv2
import caffe
from caffe.proto import caffe_pb2

def write_lmdb(lmdb_dir, txt_array, batch_size):
    '''write images and corresponding labels to lmdb database!'''
    if os.path.exists(lmdb_dir):
        shutil.rmtree(lmdb_dir)
    lmdb_env = lmdb.open(lmdb_dir, map_size=int(1e12))
    lmdb_txn = lmdb_env.begin(write=True)
    datum = caffe_pb2.Datum()
    
    num_simple = txt_array.shape[0]
    label_size = txt_array.shape[1] - 1
    
    item_id = -1
    for i in tqdm(range(num_simple)):
        item_id += 1
        image_path = txt_array[item_id, 0]
        image = cv2.imread(image_path) # shape = (height, width, channels)
        data_shape = (image.shape[2], image.shape[0], image.shape[1])
        data = np.zeros(data_shape) # shape = (chnnels, height, width)
        # fill data with image 
        for channel in range(data.shape[0]):
            data[channel, :] = image[:, :, channel]

        label = int(txt_array[item_id, 1])
        # save in datum
        datum = caffe.io.array_to_datum(data, label)
        keystr = '{:0>8d}'.format(item_id)
        lmdb_txn.put( keystr, datum.SerializeToString() )
        
        # write batch
        if (item_id + 1) % batch_size == 0:
            lmdb_txn.commit()
            lmdb_txn = lmdb_env.begin(write=True)
    # write last batch
    if (item_id + 1) % batch_size != 0:
        lmdb_txn.commit()

if __name__ == "__main__":
    ORIGINAL_DATA_ROOT = "/home/wang/disk_4T/wang_data/original_dataset"
    CONVERT_DATA_ROOT = "/home/wang/disk_4T/wang_data/convert_dataset"
    IMAGE_ROOT = os.path.join(ORIGINAL_DATA_ROOT, "CelebA/Img/img_align_celeba")
    IMAGE_LIST_FILE = os.path.join(ORIGINAL_DATA_ROOT, "CelebA/Anno/list_attr_celeba.txt")
    TRAIN_OUTPUT_ROOT = os.path.join(CONVERT_DATA_ROOT, "train_lmdb")
    TEST_OUTPUT_ROOT = os.path.join(CONVERT_DATA_ROOT, "test_lmdb")

    txt_array = np.loadtxt(IMAGE_LIST_FILE, skiprows=2, usecols=(0, 1), dtype='|S100')
    num_sample = txt_array.shape[0]
    for i in np.arange(num_sample):
        txt_array[i, 0] = os.path.join(IMAGE_ROOT, txt_array[i, 0]) 
        # txt_narray[i, 1:] = map(lambda x: "0" if x == "-1" else "1", txt_narray[i, 1:])
    logging.info("Shuffle dataset!")
    np.random.shuffle(txt_array)
    num_train = int(num_sample * 0.75)
    logging.info("Start to create train lmdb!")
    write_lmdb(TRAIN_OUTPUT_ROOT, txt_array[:num_train], 1000)
    logging.info("End to create train lmdb!")
    
    logging.info("Start to create test lmdb!")
    write_lmdb(TEST_OUTPUT_ROOT, txt_array[num_train:], 1000)
    logging.info("End to create test lmdb!")

    

     
