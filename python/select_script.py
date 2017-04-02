#!/usr/bin/env python

import os
import sys
import shutil
import argparse

def find_words(script, words):
    """
    Find whether a script contain words

    Input:
    - script --> A path of the script
    - words --> A list of words which we are interesed

    Output:
    - find_word --> Whether a script contain words   
    """
    find_word = False
    f = open(script, 'r')
    for line in f.readlines():
        for word in words:
            if word in line:
                find_word = True
            if find_word:
                break
        if find_word:
            break
    return find_word

def find_all_scripts(dir_root, words):
    """
    Find all scripts containing words under dir_root

    Input:
    - dir_root --> A root of searching directory
    - words --> A list of words which we are interested

    Output:
    - scripts --> A list of scripts path we find
    """

    scripts = []
    for root, subdirs, files in os.walk(dir_root):
        if len(files) == 0:
            continue
        files = map(lambda x: os.path.join(root, x), files)
        scripts.extend(filter(lambda x: os.path.isfile(x) and find_words(x, words), files))
    return scripts

def parse_args():
    """Parse arguments for input parameters"""
    description = "Split a txt into training and testing txt!"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("dir_root", help="Path to the root of searching directory")
    parser.add_argument("output_root", help="Directory which all finded scripts is copyed to")
    parser.add_argument("--words", action="store", type=str, nargs='*', default=None, help="The words we want to find")
    
    args = parser.parse_args()
    return args

def main():
    """ The main function"""
    args = parse_args()
    print("args = {}".format(args))
    dir_root = args.dir_root
    if not os.path.isdir(dir_root):
        print("Not found the dir_root --> {}".format(dir_root))
        sys.exit(1)
    output_root = args.output_root
    if os.path.isdir(output_root):
        print("Find the output_root --> {}".format(output_root))
        shutil.rmtree(output_root)
    print("Create a new output_root --> {}".format(output_root))
    os.mkdir(output_root)
    words = args.words
    if not words:
        print("The parameter \"words\" is empty")
        sys.exit(1)
    scripts = find_all_scripts(dir_root, words)
    print("scripts = {}".format(scripts))
    for script in scripts:
        script_root, script_name = os.path.split(script)
        # print("script_root = {}".format(script_root))
        script_root = os.path.join(output_root, script_root.replace(dir_root, ''))
        # print("script_root = {}".format(script_root))
        if not os.path.exists(script_root):
            os.makedirs(script_root)
        script_path = os.path.join(script_root, script_name)
        # print("script_path = {}".format(script_path))
        shutil.copy(script, script_path)

if __name__ == "__main__":
    main()

