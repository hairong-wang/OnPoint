#!/bin/bash

#### local path
INIT_CKPT_DIR=/home/whairong2011/xlnet_cased_L-24_H-1024_A-16

#### google storage path
GS_ROOT=${STORAGE_BUCKET}
GS_INIT_CKPT_DIR=${GS_ROOT}/experiment/squad
GS_PROC_DATA_DIR=${GS_ROOT}/proc_data/amazon
GS_MODEL_DIR=${GS_ROOT}/experiment/amazon_steps8000_warmup1000
SQUAD_DIR=${GS_ROOT}/data/amazon
# TPU name in google cloud
TPU_NAME=whairong2011

python3 run_squad.py \
  --use_tpu=True \
  --tpu=${TPU_NAME} \
  --num_hosts=1 \
  --num_core_per_host=8 \
  --model_config_path=${INIT_CKPT_DIR}/xlnet_config.json \
  --spiece_model_file=${INIT_CKPT_DIR}/spiece.model \
  --output_dir=${GS_PROC_DATA_DIR} \
  --init_checkpoint=${GS_INIT_CKPT_DIR}/model.ckpt-8000 \
  --model_dir=${GS_MODEL_DIR} \
  --train_file=${SQUAD_DIR}/amazonqa_squad_21_train.json \
  --predict_file=${SQUAD_DIR}/amazonqa_squad_6_valid.json \
  --uncased=False \
  --max_seq_length=512 \
  --do_train=False \
  --train_batch_size=48 \
  --do_predict=True \
  --predict_batch_size=32 \
  --learning_rate=3e-5 \
  --adam_epsilon=1e-6 \
  --iterations=1 \
  --save_steps=1 \
  --train_steps=2 \
  --warmup_steps=0 \
  $@
