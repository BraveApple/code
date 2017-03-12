#!/usr/bin/env python

import multiprocessing
from multiprocessing import Process, freeze_support, Pool
import os
import sys
import caffe
import numpy as np
import scipy
import h5py

class ExtractFeature(object):

    def __init__(self, model_file, weight_file, image_list, num_task, output_root):
        self.num_task_ = num_task
        self.model_file_ = model_file
        self.weight_file_ = model_file
        self.output_root_ = output_root

    def create_net(self):
        net = caffe.Net(self.model_file_, self.weight_file_, caffe.TEST)
        net.forward()
        return net

    def split_task(self, image_list):
        batch_size = len(image_list) / self.num_task_
        split_task = [batch_size] * self.num_task_
        for task_id in range(len(image_list) % self.num_task):
            self.split_task[task_id] += 1

        if sum(split_task) != len(image_list):
            print "Fail to split task!"
            sys.exit(1)
        self.split_images_ = []
        start_id = 0
        for task_size in split_task:
            self.split_images.append(image_list[start_id: start_id + task_size])
            start_id += task_size

    def single_task(self, taks_id):
        hdf5_file = os.path.join(self.output_root_, "{:0>2d}.hdf5".format(task_id))
        if os.path.isfile(hdf5_file):
            os.remove(hdf5_file)
        f = h5py.File(hdf5_file, 'w')
        for image in self.split_images_[task_id]:



