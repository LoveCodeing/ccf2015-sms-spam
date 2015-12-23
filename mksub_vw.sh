#!/bin/sh

DATA_DIR=data
TRAIN_FILE=$DATA_DIR/train.seg.cnt.vw
TEST_FILE=$DATA_DIR/test.seg.cnt.vw
VW=/root/work/dl/vowpal_wabbit.7.7/vowpalwabbit/vw


MODEL_FILE=$DATA_DIR/model.vw
PRED_FILE=$DATA_DIR/preds.txt
SUBM_FILE=$DATA_DIR/subm.csv

loss_func=hinge
VW_PARAMS="-l 0.16 --ngram 2 --loss_function $loss_func --l2 0.0001 -b 30"
threshold=0.34

$VW $TRAIN_FILE -f $MODEL_FILE $VW_PARAMS
$VW $TEST_FILE -t --quiet -i $MODEL_FILE -p $PRED_FILE
python code/vw_to_subm.py $PRED_FILE $SUBM_FILE --loss_func $loss_func --threshold $threshold

