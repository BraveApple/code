#!/usr/bin/env python

import os
import sys
import argparse


def ListPath(input_root, path_txt):
  
  img_list = []
  for root, subdirs, files in os.walk(input_root):
    if len(files) == 0:
      continue
    files = map(lambda x: os.path.join(root, x), files)
    img_list.extend(filter(lambda x: os.path.isfile(x) and x.endswith(".jpg"), files))
  
  img_list = map(lambda x: x.replace(input_root, "").lstrip("./"), img_list)
  f = open(path_txt, 'w')
  for img_path in img_list:
    f.write(img_path + '\n')
  f.close()

def ParseArgs():
  """Parse arguments for input parameters"""
  description = "List path for a directory"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("input_root", help="Path to the root directory")
  parser.add_argument("path_txt", help="Path to the path txt")

  args = parser.parse_args()
  return args

def main():
  """Main function"""
  args = ParseArgs()
  input_root = args.input_root
  assert os.path.isdir(input_root), "Not found the directory input_root --> {}".format(input_root)
  path_txt = args.path_txt
  ListPath(input_root, path_txt)

if __name__ == "__main__":
  main()
  

