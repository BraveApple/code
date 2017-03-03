#!/usr/bin/en sh

IMAGE_ROOT=$WANG_DATA/original_dataset/CelebA/Img/img_align_celeba
IMAGE_LIST_ROOT=$WANG_DATA/original_dataset/CelebA
LMDB_ROOT=$WANG_DATA/convert_dataset

rm -rf $LMDB_ROOT/lmdb_train $LMDB_ROOT/lmdb_test

echo "Start to create training lmdb!"
convert_imageset --shuffle \
--resize_height=256 --resize_width=256 \
$IMAGE_ROOT $IMAGE_LIST_ROOT/train.txt  $LMDB/train_lmdb
echo "End to create training lmdb!"

echo "Start to create testing lmdb!"
convert_imageset --shuffle \
--resize_height=256 --resize_width=256 \
$IMAGE_ROOT $IMAGE_LIST_ROOT/test.txt  $LMDB/train_lmdb
echo "End to create testing lmdb!"
