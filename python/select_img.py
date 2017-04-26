#!/usr/bin/env python

import os
import sys
import shutil
import argparse

def list_intersection(a, b):
  
  return list(set(a).intersection(set(b)))

def select_img(input_root, output_root):
  
  root_dirs = os.listdir(input_root)
  root_dirs = filter(lambda x: os.path.isdir(x), root_dirs)
  all_img_names = []
  for root_dir in root_dirs:
    input_root_tmp = os.path.join(input_root, root_dir)
    img_names_tmp = os.listdir(input_root_tmp)
    all_img_names.append(img_names_tmp)
  
  img_names = all_img_names[0]
  for names in all_img_names:
    img_names = list_intersection(img_names, names)
  
  for root_dir in root_dirs:
    input_root_tmp = os.path.join(input_root, root_dir)
    output_root_tmp = os.path.join(output_root, root_dir)
    if not os.path.isdir(output_root_tmp):
      os.makedirs(output_root_tmp)
    for img_name in img_names:
      input_img_file = os.path.join(input_root_tmp, img_name)
      output_img_file = os.path.join(output_root_tmp, img_name)
      shutil.copy(input_img_file, output_img_file)

def parse_args():
  
  description = "Select images"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("input_root", help="The root of input")
  parser.add_argument("output_root", help="The root of output")

  args = parser.parse_args()
  return args

def main():

  args = parse_args()
  input_root = args.input_root
  if not os.path.isdir(input_root):
    print("Not found input_root --> {}".format(input_root))
    sys.exit(1)
  output_root = args.output_root
  if os.path.isdir(output_root):
    shutil.rmtree(output_root)
  select_img(input_root, output_root)

if __name__ == "__main__":

  main()
