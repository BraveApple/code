#!/usr/bin/env python

import os
import sys
import shutil
import argparse
import numpy as np

def copy_img(raw_img_root, align_img_root, txt_file, output_raw_root, output_align_root):
  """Copy all images and change their names according to a txt file"""
  txt_array = np.loadtxt(txt_file, dtype="|S100")
  img_id = 0
  for img in txt_array:
    raw_img = os.path.join(raw_img_root, img)
    if not os.path.isfile(raw_img):
      print("Not found raw_img --> {}".format(raw_img))
      sys.exit(1)
    
    align_img = os.path.join(align_img_root, img)
    if not os.path.isfile(align_img):
      print("Not found align_img --> {}".format(align_img))
      sys.exit(1)
    
    img_name = "{:0>4d}.jpg".format(img_id)
    img_id += 1
    output_raw_img = os.path.join(output_raw_root, img_name)
    shutil.copy(raw_img, output_raw_img)
    output_align_img = os.path.join(output_align_root, img_name)
    shutil.copy(align_img, output_align_img)

def parse_args():
  """Parse arguments for input parameters"""
  description = "Copy all images an change their names according to a txt file"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("raw_img_root", help="The root of raw_img_root")
  parser.add_argument("align_img_root", help="The root of align_img_root")
  parser.add_argument("txt_file", help="The path of txt_file")
  parser.add_argument("output_root", help="The root of output")

  args = parser.parse_args()
  return args

def main():
  """A main function"""
  args = parse_args()
  raw_img_root = args.raw_img_root
  if not os.path.isdir(raw_img_root):
    print("Not found raw_img_root --> {}".format(raw_img_root))
    sys.exit(1)
  align_img_root = args.align_img_root
  if not os.path.isdir(align_img_root):
    print("Not found aling_img_root --> {}".format(align_img_root))
    sys.exit(1)
  txt_file = args.txt_file
  if not os.path.isfile(txt_file):
    print("Not found txt_file --> {}".format(align_img_root))
    sys.exit(1)
  output_root = args.output_root
  if os.path.isdir(output_root):
    print("Found output_root --> {} <--, you must remove it".format(output_root))
    sys.exit(1)
  os.mkdir(output_root)
  output_raw_root = os.path.join(output_root, "raw_img")
  output_align_root = os.path.join(output_root, "align_img")
  os.mkdir(output_raw_root)
  os.mkdir(output_align_root)

  copy_img(raw_img_root, align_img_root, txt_file, output_raw_root, output_align_root)

if __name__ == "__main__":
  main()
    
