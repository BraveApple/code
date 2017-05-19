#!/usr/bin/env python

import os
import sys
import numpy as np
import argparse
import caffe

class CopyParam(object):

  def __init__(self, pair_file):
    self.pair_array_ = np.loadtxt(pair_file, dtype="|S100")

  def SetSourceNet(self, prototxt_file, weight_file):
    self.source_net_files_ = [prototxt_file, weight_file]
    self.source_net_ = caffe.Net(prototxt_file, weight_file, caffe.TEST)

  def SetTargetNet(self, prototxt_file, weight_file):
    self.target_net_files_ = [prototxt_file, weight_file]
    self.target_net_ = caffe.Net(prototxt_file, caffe.TEST)

  def ShowLayer(self):
    """Show layers which have learnable parameters"""
    source_layers = self.source_net_.params.keys()
    print "Source Net: {}".format(source_layers)
    target_layers = self.target_net_.params.keys()
    print "Target Net: {}".format(target_layers)

  def Copy(self):
    pair_num = self.pair_array_.shape[0]
    source_param = self.source_net_.params
    target_param = self.target_net_.params
    print "Start to copy weight\n"
    for pair_id in np.arange(pair_num):
      source_layer, target_layer = self.pair_array_[pair_id]
      print "Start to copy weight from {} to {}".format(source_layer, target_layer)
      assert source_layer != target_layer, "source_layer = {} and target_layer = {} must not be same".format(source_layer, target_layer)
      assert source_layer in source_param, "source_layer = {} must be in source_net".format(source_layer)
      assert target_layer in target_param, "source_layer = {} must be in target_net".format(target_layer)
      param_num = len(source_param[source_layer])
      for param_id in np.arange(param_num):
        source_data_shape = source_param[source_layer][param_id].data.shape
        target_data_shape = target_param[target_layer][param_id].data.shape
        assert source_data_shape == target_data_shape, "source_param[{}][{}].data.shape = {} ==\
          target_param[{}][{}].data.shape = {}".format(source_layer, param_id, source_data_shape,\
          target_layer, param_id, target_data_shape)

        print "source_param[{}][{}].data.shape = {} --> target_param[{}][{}].data.shape = {}".format(
          source_layer, param_id, source_data_shape, target_layer, param_id, target_data_shape)
        try:
          target_param[target_layer][param_id].data[...] = source_param[source_layer][param_id].data[...]
        except Exception as e:
          print e
          sys.exit(1)
    
      print "End to copy weight from {} to {}\n".format(source_layer, target_layer)
    self.target_net_.save(self.target_net_files_[1])
    print "End to copy weight\n"

def ParseArgs():
  """Parse arguments for input parameters"""
  description = "Copy weight from source network to target network"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("--pair_file", help="Path to pair file")
  parser.add_argument("--source_proto", help="Path to source prototxt file")
  parser.add_argument("--source_weight", help="Path to source weight file")
  parser.add_argument("--target_proto", help="Path to target prototxt file")
  parser.add_argument("--target_weight", help="Path to target weight file")
  parser.add_argument("--show_layer", action="store_true", help="Whether to show layers which have learnable parameters")

  args = parser.parse_args()
  return args

def main():
  """Main function"""
  args = ParseArgs()
  pair_file = args.pair_file
  assert os.path.isfile(pair_file), "Not found pair_file --> {}".format(pair_file)
  source_proto = args.source_proto
  assert os.path.isfile(source_proto), "Not found source_proto --> {}".format(source_proto)
  source_weight = args.source_weight
  assert os.path.isfile(source_weight), "Not found source_weight --> {}".format(source_weight)
  target_proto = args.target_proto
  assert os.path.isfile(target_proto), "Not found target_proto --> {}".format(target_proto)
  target_weight = args.target_weight
  if os.path.isfile(target_weight):
    os.remove(target_weight)

  copy_param = CopyParam(pair_file)
  copy_param.SetSourceNet(source_proto, source_weight)
  copy_param.SetTargetNet(target_proto, target_weight)
  if args.show_layer:
    copy_param.ShowLayer()
  else:
    copy_param.Copy()

if __name__ == "__main__":
  main()
