#!/usr/bin/env python

import os
import sys
import argparse
import shutil
import cv2
import numpy as np

def CropImg(img_root, img_subpath, crop_root, crop_size):
  """Crop image patches from a big image"""  
  img_path = os.path.join(img_root, img_subpath)
  assert os.path.isfile(img_path), "Not found the file img_path --> {}".format(img_path)
  img = cv2.imread(img_path)
  if img == None: return []
  img_h, img_w = img.shape[0:2]
  crop_h, crop_w = crop_size
  num_h = img_h / crop_h
  num_w = img_w / crop_w
  img_subdir, img_file = os.path.split(img_subpath)
  img_prefix, img_ext = os.path.splitext(img_file)
  print "Start to crop a big image --> {}".format(img_path)
  crop_img_list = []
  for i in np.arange(num_h):
    for j in np.arange(num_w):
      y = i * crop_h
      x = j * crop_w
      crop_img = img[y : y + crop_h, x : x + crop_w]
      crop_img_name = "{}_{:0>3d}{}".format(img_prefix, i * num_w + j, img_ext)
      crop_img_root = os.path.join(crop_root, img_subdir)
      if not os.path.isdir(crop_img_root): os.makedirs(crop_img_root)
      crop_img_path = os.path.join(crop_img_root, crop_img_name)
      cv2.imwrite(crop_img_path, crop_img)
      crop_img_list.append(crop_img_path)
      print "Crop a image patch --> {}".format(crop_img_path)

  print "End to crop a big image --> {}\n".format(img_path)
  return crop_img_list

def ParseArgs():
  """Parse arguments for input parameters""" 
  description = "Crop image patches from a big image"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("img_root", help="The root path of big images")
  parser.add_argument("img_list_file", help="The list file of big images")
  parser.add_argument("--crop_size", type=int, nargs="*", help="The size of crop image patches")
  parser.add_argument("--crop_img_list_file", help="The list file of crop image patches")
  parser.add_argument("--crop_root", help="The root of crop image patches")

  args = parser.parse_args()
  return args

def main():
  """Main function"""
  args = ParseArgs()
  img_root = args.img_root
  assert os.path.isdir(img_root), "Not found the directory img_root --> {}".format(img_root)
  img_list_file = args.img_list_file
  assert os.path.isfile(img_list_file), "Not found the file img_list_file --> {}".format(img_list_file)
  crop_img_list_file = args.crop_img_list_file
  crop_size = args.crop_size
  assert len(crop_size) == 2, "The length of crop_size must be 2"
  crop_root = args.crop_root
  if os.path.isdir(crop_root): shutil.rmtree(crop_root)
  os.mkdir(crop_root)
  txt_array = np.loadtxt(img_list_file, dtype="|S100")
  f = open(crop_img_list_file, 'w')
  for img_subpath in txt_array:
    crop_img_list = CropImg(img_root, img_subpath, crop_root, crop_size)
    crop_img_list = map(lambda x: x.replace(crop_root, "").lstrip("./"), crop_img_list)
    for crop_subpath in crop_img_list: f.write(crop_subpath + "\n")

if __name__ == "__main__":
  main()
