#!/usr/bin/env python

import os
import sys
import re
import copy
import argparse
import logging
from abc import ABCMeta, abstractmethod

logging.basicConfig(level=logging.DEBUG)

'''
I0305 17:04:46.986999  9448 solver.cpp:331] Iteration 13000, Testing net (#0)
I0305 17:04:54.289549  9455 data_layer.cpp:85] Restarting data prefetching from start.
I0305 17:04:57.071898  9448 blocking_queue.cpp:49] Waiting for data
I0305 17:05:29.136428  9448 solver.cpp:398]     Test net output #0: accuracy_1 = 0.890842
I0305 17:05:29.136467  9448 solver.cpp:398]     Test net output #1: accuracy_2 = 0.76478
I0305 17:05:29.136472  9448 solver.cpp:398]     Test net output #2: accuracy_3 = 0.74938
I0305 17:05:29.136474  9448 solver.cpp:398]     Test net output #3: accuracy_4 = 0.801021
I0305 17:05:29.136479  9448 solver.cpp:398]     Test net output #4: loss_1 = 0.274614 (* 1 = 0.274614 loss)
I0305 17:05:29.136482  9448 solver.cpp:398]     Test net output #5: loss_2 = 0.466634 (* 1 = 0.466634 loss)
I0305 17:05:29.136485  9448 solver.cpp:398]     Test net output #6: loss_3 = 0.508843 (* 1 = 0.508843 loss)
I0305 17:05:29.136488  9448 solver.cpp:398]     Test net output #7: loss_4 = 0.436861 (* 1 = 0.436861 loss)
I0305 17:05:29.382328  9448 solver.cpp:219] Iteration 13000 (1.45414 iter/s, 68.769s/100 iters), loss = 1.6711
I0305 17:05:29.382369  9448 solver.cpp:238]     Train net output #0: loss_1 = 0.304902 (* 1 = 0.304902 loss)
I0305 17:05:29.382374  9448 solver.cpp:238]     Train net output #1: loss_2 = 0.410657 (* 1 = 0.410657 loss)
I0305 17:05:29.382376  9448 solver.cpp:238]     Train net output #2: loss_3 = 0.458894 (* 1 = 0.458894 loss)
I0305 17:05:29.382380  9448 solver.cpp:238]     Train net output #3: loss_4 = 0.496642 (* 1 = 0.496642 loss)
I0305 17:05:29.382385  9448 sgd_solver.cpp:105] Iteration 13000, lr = 1e-07
'''


class BaseParse(object):
    __metaclass__ = ABCMeta

    def __init__(self, log_path):
        self.lines_ = open(log_path, 'r').readlines()
        self.length_ = len(self.lines_)
        self.regex_begin_iteration_ = None
        self.regex_end_iteration_ = None
        self.regex_output_ = None
        self.begin_item_id_ = 0
        self.match_begin_ = False
        self.end_item_id_ = 0
        self.match_end_ = False
        self.match_dict_list = []

    def check_item_id(self):
        return self.begin_item_id_ < self.length_ and self.end_item_id_ < self.length_

    def is_valid_to_begin(self):
        return not self.match_begin_ and not self.match_end_

    def is_valid_to_end(self):
        return self.match_begin_ and self.match_end_

    def match_block(self):
        if not self.is_valid_to_begin():
            return False
        if not self.check_item_id():
            return False
        for begin_id in range(self.begin_item_id_, self.length_):
            begin_iteration_match = self.regex_begin_iteration_.search(self.lines_[begin_id])
            if begin_iteration_match:
                self.match_begin_ = True
                self.begin_item_id_ = begin_id
                break
        if not self.check_item_id():
            return False
        self.end_item_id_ = self.begin_item_id_
        for end_id in range(self.end_item_id_, self.length_):
            end_iteration_match = self.regex_end_iteration_.search(self.lines_[end_id])
            if end_iteration_match:
                self.match_end_ = True
                self.end_item_id_ = end_id
                break
        if not self.is_valid_to_end():
            return False
        return True

    def next_block(self):
        self.match_begin_ = False
        self.begin_item_id_ = self.end_item_id_ + 1
        self.match_end_ = False
        self.end_item_id_ = self.end_item_id_ + 1

    @abstractmethod
    def find_iteration_regex(self):
        pass

    def find_output_regex(self):
        match_key_list = []
        match_value_list = []
        is_match = False
        if not self.is_valid_to_end():
            return (is_match, match_key_list, match_value_list)
        for item_id in range(self.begin_item_id_, self.end_item_id_):
            output_match = self.regex_output_.search(self.lines_[item_id])
            if output_match:
                match_key_list.append(str(output_match.group(2)))
                match_value_list.append(float(output_match.group(3)))
                is_match = True
        return (is_match, match_key_list, match_value_list)

    @abstractmethod
    def find_block_regex(self):
        pass

    def find_all_regex(self):
        is_match_exist = True
        while is_match_exist:
            is_match_exist = self.match_block()
            if not is_match_exist:
                is_match_exist = False
                break
            match_dict = self.find_block_regex()
            self.match_dict_list.append(copy.deepcopy(match_dict))
            self.next_block()

    def write_to_txt(self, txt_file):
        with open(txt_file, 'w') as f:
            key_list = self.match_dict_list[0].keys()
            f.write(" ".join(key_list) + "\n")             
            for line_dict in self.match_dict_list:
                if len(line_dict) != len(key_list):
                    print "The number of keys is not matched!"
                    sys.exit(1)
                print_line = ""
                for key in key_list:
                    print_line += str(line_dict[key]) + " "
                print_line = print_line.strip()
                f.write(print_line + "\n")
            f.close()

class ParseTest(BaseParse):
    def __init__(self, log_path):
        super(ParseTest, self).__init__(log_path)
        self.regex_begin_iteration_ = re.compile('Iteration (\d+), Testing net')
        self.regex_end_iteration_ = re.compile(
            'Iteration (\d+) \(([\.\deE+-]+) iter/s, (\S+) iters\), loss = ([\.\deE+-]+)')
        self.regex_output_ = re.compile('Test net output #(\d+): (\S+) = ([\.\deE+-]+)')

    def find_iteration_regex(self):
        match_key = None
        match_value = None
        is_match = False
        if not self.is_valid_to_end():
            return (is_match, match_key, match_value)
        for item_id in range(self.begin_item_id_, self.end_item_id_):
            iteration_match = self.regex_begin_iteration_.search(self.lines_[item_id])
            if iteration_match:
                match_key = "iteration"
                match_value = int(iteration_match.group(1))
                is_match = True
                break
        return (is_match, match_key, match_value)

    def find_block_regex(self):
        match_dict = {}
        is_iteration_match, iteration_key, iteration_value = self.find_iteration_regex()
        if not is_iteration_match:
            print "Fali to match iteration!"
            sys.exit(1)
        match_dict[iteration_key] = iteration_value
        is_output_match, output_key_list, output_value_list = self.find_output_regex()
        if not is_output_match:
            print "Fail to match output!"
            sys.exit(1)
        for output_key, output_value in zip(output_key_list, output_value_list):
            match_dict[output_key] = output_value
        return match_dict


class ParseTrain(BaseParse):
    def __init__(self, log_path):
        super(ParseTrain, self).__init__(log_path)
        self.regex_begin_iteration_ = re.compile(
            'Iteration (\d+) \(([\.\deE+-]+) iter/s, (\S+) iters\), loss = ([\.\deE+-]+)')
        self.regex_end_iteration_ = re.compile('Iteration (\d+), lr = ([\.\deE+-]+)')
        self.regex_output_ = re.compile('Train net output #(\d+): (\S+) = ([\.\deE+-]+)')

    def find_iteration_regex(self):
        match_key_list = []
        match_value_list = []
        is_match = False
        if not self.is_valid_to_end():
            return (is_match, match_key_list, match_value_list)
        for item_id in range(self.begin_item_id_, self.end_item_id_):
            iteration_match = self.regex_begin_iteration_.search(self.lines_[item_id])
            if iteration_match:
                match_key_list.append("iteration")
                match_value_list.append(int(iteration_match.group(1)))

                match_key_list.append("speed")
                match_value_list.append(float(iteration_match.group(2)))

                match_key_list.append("run_time_per_iter")  # 68.0066s/100
                str_run_time = str(iteration_match.group(3)).strip()
                run_time_per_iter = float(str_run_time[0: str_run_time.find("s")]) \
                                    / float(str_run_time[str_run_time.find("/") + 1:])
                match_value_list.append(run_time_per_iter)

                match_key_list.append("sum_of_loss")
                match_value_list.append(float(iteration_match.group(4)))

                is_match = True
                break
        return (is_match, match_key_list, match_value_list)

    def find_learning_rate_regex(self):
        match_key = None
        match_value = None
        is_match = False
        if not self.is_valid_to_end():
            return (is_match, match_key, match_value)
        for item_id in range(self.begin_item_id_, self.end_item_id_ + 1):
            learning_rate_match = self.regex_end_iteration_.search(self.lines_[item_id])
            if learning_rate_match:
                match_key = "learing_rate"
                match_value = float(learning_rate_match.group(2))
                is_match = True
                break
        return (is_match, match_key, match_value)

    def find_block_regex(self):
        match_dict = {}

        is_iteration_match, iteration_key_list, iteration_value_list = self.find_iteration_regex()
        if not is_iteration_match:
            print "Fali to match iteration!"
            sys.exit(1)
        for iteration_key, iteration_value in zip(iteration_key_list, iteration_value_list):
            match_dict[iteration_key] = iteration_value

        is_output_match, output_key_list, output_value_list = self.find_output_regex()
        if not is_output_match:
            print "Fail to match output!"
            sys.exit(1)
        for output_key, output_value in zip(output_key_list, output_value_list):
            match_dict[output_key] = output_value

        is_learning_rate_match, learing_rate_key, learning_rate_value = self.find_learning_rate_regex()
        if not is_learning_rate_match:
            print "Fail to match learing rate!"
            sys.exit(1)
        match_dict[learing_rate_key] = learning_rate_value
        return match_dict

def parse_args():
    """Parse arguments for input parameters"""
    description = "Parse a caffe log file into train and test txt!"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("log_file", help="Path to log")
    parser.add_argument("output_dir", help="Directory to output train and test txt")
    args = parser.parse_args()
    return args

def print_help():
    """Print some helpful information"""
    print "USE EXAMPLE: ./parse_log.py [LOG_FILE] [OUTPUT_DIR] \n"

def absolute_path(output_dir):
    abs_path = None
    script_root = os.getcwd()
    if output_dir.find(".") == 0:
        abs_path = os.path.join(script_root, output_dir.strip("./"))
    elif output_dir.find("/") == 0:
        abs_path = output_dir
    else:
        abs_path = os.path.join(script_root, output_dir)
    return abs_path

def main():
    '''Main method'''
    args = parse_args()
    log_file = args.log_file
    if not os.path.exists(log_file):
        print "Not found log_file {}".format(log_file)
        sys.exit(1)
    output_dir = args.output_dir
    if not os.path.exists(output_dir):
        print "Not found output_dir {}".format(output_dir)
        sys.exit(1)
    output_dir = absolute_path(output_dir)
    train_paser = ParseTrain(log_file)
    train_paser.find_all_regex()
    logging.info("Write to train txt --> {}".format(os.path.join(output_dir, "train.log.txt")))
    train_paser.write_to_txt(os.path.join(output_dir, "train.log.txt"))

    test_paser = ParseTrain(log_file)
    test_paser.find_all_regex()
    logging.info("Write to test txt --> {}".format(os.path.join(output_dir, "test.log.txt")))
    test_paser.write_to_txt(os.path.join(output_dir, "test.log.txt"))

if __name__ == "__main__":
    main()