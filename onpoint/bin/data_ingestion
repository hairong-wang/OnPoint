#!/bin/bash

#### local path
SQUAD_DATA_S3_BUCKET='squad-data'
SQUAD_DATA_TRAIN_S3_KEY='squad2.0/train-v2.0.json'
SQUAD_DATA_DEV_S3_KEY='squad 2.0/dev-v2.0.json'
LOCAL_SQUAD_DATA_TRAIN_PATH=./squad2.0_train.json
LOCAL_SQUAD_DATA_DEV_PATH=./squad2.0_dev.json

python3 data_downloader.py \
--s3_bucket=SQUAD_DATA_S3_BUCKET \
--s3_key=SQUAD_DATA_TRAIN_S3_KEY \
--local_path=LOCAL_SQUAD_DATA_TRAIN_PATH \
$@

python3 data_downloader.py \
--s3_bucket=SQUAD_DATA_S3_BUCKET \
--s3_key=SQUAD_DATA_DEV_S3_KEY \
--local_path=LOCAL_SQUAD_DATA_DEV_PATH \
$@
