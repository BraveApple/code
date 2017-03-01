#!/usr/bin/env sh

g++ blob_demo.cpp -o app -I $CAFFE_ROOT/include/ -D CPU_ONLY \
-I $CAFFE_ROOT/.build_release/src/ -L $CAFFE_ROOT/build/lib -lcaffe -lglog -lboost_system
