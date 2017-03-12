#!/usr/bin/env sh

IMAGENET_ROOT=$WANG_DATA/original_dataset/ILSVRC
TRAIN_XML_ROOT=$IMAGENET_ROOT/Annotations/CLS-LOC/train
VAL_XML_ROOT=$IMAGENET_ROOT/Annotations/CLS-LOC/val
MAP_CLASS_TXT=$IMAGENET_ROOT/ImageSets/CLS-LOC/map_clsloc.txt
OUTPUT_ROOT=$IMAGENET_ROOT/ImageSets/CLS-LOC

./xml_to_txt.py --train_xml_root $TRAIN_XML_ROOT --val_xml_root $VAL_XML_ROOT \
--map_class_txt $MAP_CLASS_TXT --output_root $OUTPUT_ROOT