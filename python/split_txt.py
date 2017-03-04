#!/usr/bin/env python

import numpy as np
import logging
import argparse
import os

logging.basicConfig(level=logging.DEBUG)

def split_txt(txt_file, output_root, split_rate, skiprows, usecols):
    """
        Split a txt into two txts, which are training and testing part. 
        Training part is (split_rate), and testing part is (1 - split_rate)
    
    """
    txt_array = np.loadtxt(txt_file, skiprows=skiprows, usecols=usecols, dtype="|S100")
    num_sample = txt_array.shape[0]
    num_train = int(num_sample * split_rate)
    logging.info("Shuffle dataset!")
    np.random.shuffle(txt_array)
    # write to train.txt
    train_txt = os.path.join(output_root, "train.txt")
    logging.info("Create train.txt --> {}".format(train_txt))
    f_train = open(train_txt, 'w')
    for line in txt_array[:num_train]:
        print_line = " ".join(map(str, line))
        f_train.write(print_line + "\n")
    f_train.close()

    # write to test.txt
    test_txt = os.path.join(output_root, "test.txt")
    logging.info("Create test.txt --> {}".format(test_txt))
    f_test = open(test_txt, 'w')
    for line in txt_array[num_train:]:
        print_line = " ".join(map(str, line))
        f_test.write(print_line + "\n")
    f_test.close()

def parse_args():
    """Parse arguments for input parameters"""
    description = "Split a txt into training and testing txt!"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("txt_file", help="Path to txt")
    parser.add_argument("output_root", help="Directory in which to place train.txt and test.txt")
    parser.add_argument("--rate", action="store", type=float, default=0.75, help="Split rate")
    parser.add_argument("--skiprows", action="store", type=int, default=0, help="The number of skipped lines")
    parser.add_argument("--usecols", action="store", type=int, nargs='*', default=None, help="The index of used columns")

    args = parser.parse_args()
    return args

def main():
    """A main fuction for this script"""
    args = parse_args()
    logging.info("args = {}".format(args))
    txt_file = args.txt_file
    if not os.path.exists(txt_file):
        logging.error("Not found txt \"{}\"".format(txt_file))
        exit(-1)
    output_root = args.output_root
    if not os.path.exists(output_root):
        logging.error("Not found output_root \"{}\"".format(output_root))
        exit(-1)
    split_rate = args.rate
    if split_rate < 0 or split_rate > 1.0:
        logging.error("split_rate must be in [0, 1.0]")
        exit(-1)
    skiprows = args.skiprows
    if skiprows < 0:
        logging.error("skiprows must be positive")
        exit(-1)
    usecols = args.usecols
    
    split_txt(txt_file, output_root, split_rate, skiprows, usecols)

if __name__ == "__main__":
    main()
    
