#!/usr/bin/env python

import os
import sys
import numpy as np
import argparse
from tqdm import *
import xml.etree.ElementTree as ET

class XMLToTXT(object):

    def __init__(self, train_xml_root, val_xml_root, map_class_txt, output_root):
        self.train_xml_root_ = train_xml_root
        self.val_xml_root_ = val_xml_root
        self.map_class_txt_ = map_class_txt
        self.output_root_ = output_root
        self.train_txt_ = "train.txt"
        self.val_txt_ = "val.txt"
        self.map_class(map_class_txt)

    def map_class(self, map_class_txt):
        txt_array = np.loadtxt(map_class_txt, dtype="|S100")
        num_class = txt_array.shape[0]
        self.map_dict_ = {}
        for i in np.arange(num_class):
            class_dir = txt_array[i, 0]
            class_id = int(txt_array[i, 1]) - 1
            self.map_dict_[class_dir] = class_id

    def adjust_folder(self, folder):
        adjust_folder = folder
        if folder.find("n") != 0:
            adjust_folder = "n" + folder
        return adjust_folder

    def parse_train_xml(self):
        train_txt_root = os.path.join(self.output_root_, self.train_txt_)
        f = open(train_txt_root, 'w')
        print "Create train.txt --> {}".format(train_txt_root)
        xml_list = []
        for root, subdirs, files in os.walk(self.train_xml_root_):
            if len(files) == 0:
                continue
            files = map(lambda x: os.path.join(root, x), files)
            xml_list.extend(filter(lambda x: os.path.isfile(x) and ".xml" in x, files))
        if len(xml_list) == 0:
            print "Not find any xml files under the directory {}".format(self.train_xml_root_)
            sys.exit(1)

        for item_id in tqdm(range(len(xml_list))):
            xml_file = xml_list[item_id]
            tree = ET.parse(xml_file)
            folder = tree.find("folder").text
            folder = self.adjust_folder(folder)
            image_name = tree.find("filename").text + ".JPEG"
            class_dir = tree.find("object").find("name").text
            class_id = self.map_dict_[class_dir]
            print_line = folder + "/" + image_name + " " + str(class_id)
            f.write(print_line + "\n")
        f.close()

    def parse_val_xml(self):
        val_txt_root = os.path.join(self.output_root_, self.val_txt_)
        f = open(val_txt_root, 'w')
        print "Create val.txt --> {}".format(val_txt_root)
        xml_list = []
        for root, subdirs, files in os.walk(self.val_xml_root_):
            if len(files) == 0:
                continue
            files = map(lambda x: os.path.join(root, x), files)
            xml_list.extend(filter(lambda x: os.path.isfile(x) and ".xml" in x, files))
        if len(xml_list) == 0:
            print "Not find any xml files under the directory {}".format(self.val_xml_root_)
            sys.exit(1)

        for item_id in tqdm(range(len(xml_list))):
            xml_file = xml_list[item_id]
            xml_path = os.path.join(self.val_xml_root_, xml_file)
            tree = ET.parse(xml_path)
            image_name = tree.find("filename").text + ".JPEG"
            class_dir = tree.find("object").find("name").text
            class_id = self.map_dict_[class_dir]
            print_line = image_name + " " + str(class_id)
            f.write(print_line + "\n")
        f.close()

    def parse_xml(self):
        self.parse_train_xml()
        self.parse_val_xml()

# End to define class XMLTOTXT

def parse_args():
    """Read xml files to create train.txt and val.txt"""
    description = "Read xml files to create train.txt and val.txt !"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--train_xml_root", help="Path to train xml root")
    parser.add_argument("--val_xml_root", help="Path to val xml root")
    parser.add_argument("--map_class_txt", help="Path to txt file which maps classes")
    parser.add_argument("--output_root", help="Path to output")
    args = parser.parse_args()
    return args

def main():
    """Main Method"""
    args = parse_args()
    train_xml_root = args.train_xml_root
    if not os.path.isdir(train_xml_root):
        print "Not found train_xml_root --> {}".format(train_xml_root)
        sys.exit(1)

    val_xml_root = args.val_xml_root
    if not os.path.isdir(val_xml_root):
        print "Not found val_xml_root --> {}".format(val_xml_root)
        sys.exit(1)

    map_class_txt = args.map_class_txt
    if not os.path.isfile(map_class_txt):
        print "Not found map_class_txt --> {}".format(map_class_txt)
        sys.exit(1)

    output_root = args.output_root
    if not os.path.isdir(output_root):
        print "Not found output_root --> {}".format(output_root)
        sys.exit(1)
    xml_to_txt = XMLToTXT(train_xml_root, val_xml_root, map_class_txt, output_root)
    xml_to_txt.parse_xml()

if __name__ == "__main__":
    main() 
    
