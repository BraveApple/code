#!/usr/bin/en sh

TOOLS_ROOT=$CAFFE_M_ROOT/build/tools
IMAGE_ROOT=$WANG_DATA/original_dataset/ILSVRC/Data/CLS-LOC
TRAIN_ROOT=$IMAGE_ROOT/train
VAL_ROOT=$IMAGE_ROOT/val
IMAGE_LIST_ROOT=$WANG_DATA/original_dataset/ILSVRC/ImageSets/CLS-LOC
LMDB_ROOT=$WANG_DATA/convert_dataset/imagenet
LMDB_TRAIN=$LMDB_ROOT/lmdb_train
LMDB_VAL=$LMDB_ROOT/lmdb_val

if [ ! -d $TOOLS_ROOT ];then
    echo "Not found the directory --> ${TOOL_ROOT} !"
    exit 1
fi

if [ ! -d $TRAIN_ROOT ];then
    echo "Not found the directory --> ${TRAIN_ROOT} !"
    exit 1
fi

if [ ! -d $VAL_ROOT ];then
    echo "Not found the directory --> ${VAL_ROOT} !"
    exit 1
fi

if [ ! -d $IMAGE_LIST_ROOT ];then
    echo "Not found the directory --> ${IMAGE_LIST_ROOT} !"
    exit 1
fi

if [ ! -d $LMDB_ROOT ];then
    echo "Create a directory ${LMDB_ROOT} !"
    mkdir $LMDB_ROOT
fi

if [ -d $LMDB_TRAIN ];then
    echo "The directory ${LMDB_TRAIN} is existed, so we remove it!"
    rm -rf $LMDB_TRAIN
fi

if [ -d $LMDB_VAL ];then
    echo "The directory ${LMDB_VAL} is existed, so we remove it!"
    rm -rf $LMDB_VAL
fi

echo "Start to create train lmdb!"
$TOOLS_ROOT/convert_imageset --shuffle=true --encoded=true \
--dim_label=1 --resize_height=256 --resize_width=256 --check_size=false \
$IMAGE_ROOT/train/ $IMAGE_LIST_ROOT/train.txt  $LMDB_TRAIN
echo "End to create train lmdb!"

echo "Start to create val lmdb!"
$TOOLS_ROOT/convert_imageset --shuffle=true --encoded=true \
--dim_label=1 --resize_height=256 --resize_width=256 --check_size=false \
$IMAGE_ROOT/val/ $IMAGE_LIST_ROOT/val.txt  $LMDB_VAL
echo "End to create testing lmdb!"
