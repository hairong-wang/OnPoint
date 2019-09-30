#### local path
#### Need to change the directory to your directory containing model
#### checkpoint and processed data
INIT_CKPT_DIR=/home/hairong/workspace/xlnet/model
PROC_DATA_DIR=/home/hairong/workspace/xlnet/proc_data
MODEL_DIR=/home/hairong/workspace/xlnet/model

CONTEXT=$1
OUTPUT_PATH=$2

python3 data_pipeline/run_squad_GPU.py \
  --use_tpu=False \
  --num_hosts=1 \
  --num_core_per_host=1 \
  --model_config_path=${INIT_CKPT_DIR}/xlnet_config.json \
  --spiece_model_file=${INIT_CKPT_DIR}/spiece.model \
  --output_dir=${PROC_DATA_DIR} \
  --init_checkpoint=${INIT_CKPT_DIR}/model.ckpt-40000 \
  --model_dir=${MODEL_DIR} \
  --predict_file=${CONTEXT} \
  --predict_dir=${OUTPUT_PATH} \
  --uncased=False \
  --max_seq_length=340 \
  --do_train=False \
  --do_predict=True \
  --predict_batch_size=32 \
  --use_bfloat16=False
