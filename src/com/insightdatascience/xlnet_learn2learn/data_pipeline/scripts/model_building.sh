#!/bin/bash

#### local path
SQUAD_DIR=/home/hairong/workspace/squad
INIT_CKPT_DIR=/home/hairong/workspace/xlnet_cased_L-24_H-1024_A-16
PROC_DATA_DIR=/home/hairong/workspace/xlnet/proc_data
MODEL_DIR=/home/hairong/workspace/xlnet/model

#### Use 3 GPUs, each with 8 seqlen-512 samples
# Hairong: since i use fp32 instead of fp16, I need twice the memory per example,
#so I need to reduce batch size by a half from 4 to 2, and reduce learning
#rate by half from 2e-5 to 1e-5 to maintain the same learning momentum.
python3 run_squad_GPU.py \
  --use_tpu=False \
  --num_hosts=1 \
  --num_core_per_host=1 \
  --model_config_path=${INIT_CKPT_DIR}/xlnet_config.json \
  --spiece_model_file=${INIT_CKPT_DIR}/spiece.model \
  --output_dir=${PROC_DATA_DIR} \
  --init_checkpoint=${INIT_CKPT_DIR}/xlnet_model.ckpt \
  --model_dir=${MODEL_DIR} \
  --train_file=${SQUAD_DIR}/train-v2.0.json \
  --predict_file=${SQUAD_DIR}/dev-v2.0.json \
  --uncased=False \
  --max_seq_length=340 \
  --do_train=True \
  --train_batch_size=2 \
  --do_predict=True \
  --predict_batch_size=32 \
  --learning_rate=1e-5 \
  --adam_epsilon=1e-6 \
  --iterations=1000 \
  --save_steps=5000 \
  --train_steps=85000 \
  --warmup_steps=1000 \
  --use_bfloat16=False
