#!/usr/bin/en sh

TOOLS_ROOT=$CAFFE_M_ROOT/build/tools
IMAGE_ROOT=$WANG_DATA/original_dataset/CelebA/Img/img_align_celeba/
IMAGE_LIST_ROOT=$WANG_DATA/original_dataset/CelebA/Anno
LMDB_ROOT=$WANG_DATA/convert_dataset/CelebA
LMDB_TRAIN=$LMDB_ROOT/lmdb_train
LMDB_TEST=$LMDB_ROOT/lmdb_test

if [ ! -d $LMDB_ROOT ];then
    echo "Create a directory ${LMDB_ROOT} !"
    mkdir $LMDB_ROOT
fi

if [ -d $LMDB_TRAIN ];then
    echo "The directory ${LMDB_TRAIN} is existed, so we remove it!"
    rm -rf $LMDB_TRAIN
fi

if [ -d $LMDB_TEST ];then
    echo "The directory ${LMDB_TEST} is existed, so we remove it!"
    rm -rf $LMDB_TEST
fi

echo "Start to create training lmdb!"
$TOOLS_ROOT/convert_imageset --shuffle=true --encoded=true \
--dim_label=4 --resize_height=218 --resize_width=178 --check_size=false \
$IMAGE_ROOT $IMAGE_LIST_ROOT/train.txt  $LMDB_TRAIN
echo "End to create training lmdb!"

echo "Start to create testing lmdb!"
$TOOLS_ROOT/convert_imageset --shuffle=true --encoded=true \
--dim_label=4 --resize_height=218 --resize_width=178 --check_size=false \
$IMAGE_ROOT $IMAGE_LIST_ROOT/test.txt  $LMDB_TEST
echo "End to create testing lmdb!"
