#!/usr/bin/en sh

IMAGE_ROOT=$WANG_DATA/original_dataset/CelebA/Img/img_align_celeba/
IMAGE_LIST_ROOT=$WANG_DATA/original_dataset/CelebA/Anno
LMDB_ROOT=$WANG_DATA/convert_dataset

rm -rf $LMDB_ROOT/train_lmdb $LMDB_ROOT/test_lmdb

echo "Start to create training lmdb!"
convert_imageset --shuffle --encoded \
--resize_height=100 --resize_width=100 \
$IMAGE_ROOT $IMAGE_LIST_ROOT/train.txt  $LMDB_ROOT/train_lmdb
echo "End to create training lmdb!"

echo "Start to create testing lmdb!"
convert_imageset --shuffle --encoded \
--resize_height=100 --resize_width=100 \
$IMAGE_ROOT $IMAGE_LIST_ROOT/test.txt  $LMDB_ROOT/test_lmdb
echo "End to create testing lmdb!"
