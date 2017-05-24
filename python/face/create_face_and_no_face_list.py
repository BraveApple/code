#!/usr/bin/env python

from __future__ import division
import os
import sys
import argparse
import numpy as np

def CreateList(face_txt, no_face_txt, ratio, output_txt):
  """Create face and no-face sample list with a ratio"""
  face_array = np.loadtxt(face_txt, dtype="|S100")
  no_face_array = np.loadtxt(no_face_txt, dtype="|S100")
  
  # Shuffle the order of samples
  np.random.shuffle(face_array)
  np.random.shuffle(no_face_array)
  
  # Get the number of face and no-face samples respectively
  face_num = face_array.shape[0]
  no_face_num = no_face_array.shape[0]
  block_num = int(np.min([face_num / 1, no_face_num / ratio]))
  f = open(output_txt, 'w')
  for i in np.arange(block_num):
    f.write(face_array[i] + "\n")
    for j in np.arange(ratio):
      f.write(no_face_array[i * ratio + j] + "\n")
  f.close()

def ParseArgs():
  """Parse arguments for input parameters"""
  description = "Create face and no-face sample list with a ratio"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("--face_txt", help="The path of face txt")
  parser.add_argument("--no_face_txt", help="The path of no-face txt")
  parser.add_argument("--ratio", type=int, default=3, help="The ratio of no-face VS face samples")
  parser.add_argument("--output_txt", help="The path of output txt")

  args = parser.parse_args()
  return args

def main():
  """Main funtion"""
  args = ParseArgs()
  face_txt = args.face_txt
  assert os.path.isfile(face_txt), "Not found file face_txt --> {}\n".format(face_txt)
  no_face_txt = args.no_face_txt
  assert os.path.isfile(no_face_txt), "Not found file no_face_txt --> {}\n".format(no_face_txt)
  ratio = int(args.ratio)
  output_txt = args.output_txt

  CreateList(face_txt, no_face_txt, ratio, output_txt)

if __name__ == "__main__":
  main()
