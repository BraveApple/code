#!/usr/bin/en sh

TOOLS_ROOT=$CAFFE_M_ROOT/build/tools
LMDB_ROOT=$WANG_DATA/convert_dataset/ILSVRC
LMDB_TRAIN=$LMDB_ROOT/lmdb_train
MEAN_FILE=$LMDB_ROOT/ILSVRC.binaryproto

if [ ! -d $LMDB_ROOT ];then
    echo "Not found directory --> ${LMDB_ROOT} !"
    exit 1
fi

if [ ! -d $LMDB_TRAIN ];then
    echo "Not found directory --> ${LMDB_TRAIN} !"
    exit 1
fi

if [ -f $MEAN_FILE ];then
    echo "The mean file is existed, so we remove it! --> ${MEAN_FILE}"
    rm -rf $MEAN_FILE
fi

echo "Start to create mean binaryproto file!"
$TOOLS_ROOT/compute_image_mean --backend=lmdb \
$LMDB_TRAIN $MEAN_FILE
echo "End to ctrate mean binaryproto file!"
