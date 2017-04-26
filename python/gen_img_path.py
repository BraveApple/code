#!/usr/bin/env python

import os
import sys
import argparse

def gen_img_path(img_root, txt_file):
  
  img_list = [];
  for root, subdirs, files in os.walk(img_root):
    if len(files) == 0:
      continue
    files = map(lambda x: os.path.join(root, x), files)
    img_list.extend(filter(lambda x: os.path.isfile(x) and x.endswith(".jpg"), files))

  img_list = map(lambda x: x.replace(img_root, "").strip("/"), img_list)
  img_list.sort()
  f = open(txt_file, "w")
  for img_file in img_list:
    f.write(img_file + "\n")

def parse_args():
  """Parse arguments for input parameters"""
  description = "Generate path txt"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("img_root", help="The root of images")
  parser.add_argument("txt_file", help="The path of a txt file")
  
  args = parser.parse_args();
  return args

def main():
  """Main function"""
  args = parse_args()
  img_root = args.img_root
  if not os.path.isdir(img_root):
    print("Not found img_root --> {}".format(img_root))
    sys.exit(1)
  txt_file = args.txt_file
  gen_img_path(img_root, txt_file)

if __name__ == "__main__":
  main()    
