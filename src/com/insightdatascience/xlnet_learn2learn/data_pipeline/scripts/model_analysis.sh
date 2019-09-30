#### local path
SQUAD_DIR=/home/hairong/workspace/squad
INIT_CKPT_DIR=/home/hairong/workspace/xlnet/model
PROC_DATA_DIR=/home/hairong/workspace/xlnet/proc_data
MODEL_DIR=/home/hairong/workspace/xlnet/model

python3 run_squad_GPU.py \
  --use_tpu=False \
  --num_hosts=1 \
  --num_core_per_host=1 \
  --model_config_path=${INIT_CKPT_DIR}/xlnet_config.json \
  --spiece_model_file=${INIT_CKPT_DIR}/spiece.model \
  --output_dir=${PROC_DATA_DIR} \
  --init_checkpoint=${INIT_CKPT_DIR}/model.ckpt-40000 \
  --model_dir=${MODEL_DIR} \
  --train_file=${SQUAD_DIR}/train-v2.0.json \
  --predict_file=${SQUAD_DIR}/dev-v2.0.json \
  --uncased=False \
  --max_seq_length=340 \
  --do_train=False \
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
