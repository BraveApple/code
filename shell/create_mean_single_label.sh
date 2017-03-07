#!/usr/bin/en sh

TOOLS_ROOT=$CAFFE_ROOT/build/tools
LMDB_ROOT=$WANG_DATA/convert_dataset/CelebA
LMDB_TRAIN=$LMDB_ROOT/lmdb_train
LMDB_TEST=$LMDB_ROOT/lmdb_test
MEAN_FILE=$LMDB_ROOT/CelebA.binaryproto

if [ ! -d $LMDB_ROOT ];then
    echo "Not found directory ${LMDB_ROOT} !"
    exit 1
fi

if [ ! -d $LMDB_TRAIN ];then
    echo "Not found directory ${LMDB_TRAIN} !"
    exit 1
fi

if [ ! -d $LMDB_TEST ];then
    echo "Not found directory ${LMDB_TEST} !"
    exit 1
fi

if [ -f $MEAN_FILE ];then
    echo "The mean file is existed, so we remove it!"
    rm -rf $MEAN_FILE
fi

echo "Start to create mean binaryproto file!"
$TOOLS_ROOT/compute_image_mean --backend=lmdb \
$LMDB_TRAIN $LMDB_ROOT
echo "End to ctrate mean binaryproto file!"
