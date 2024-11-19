#!/bin/bash
#BSUB -q gpua100
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J mistral_generate
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=40GB]"
#BSUB -W 12:00
#BSUB -u s223531@dtu.dk
#BSUB -N 
#BSUB -o mistral_generate_%J.out
#BSUB -e mistral_generate_%J.err


# Activate conda environment
source /dtu/blackhole/04/184612/miniconda3/bin/activate
conda activate DL_PrrojectEleven

#### Set environment variables #### 
export TMPDIR=/dtu/blackhole/04/184612/tmp
export TEMP=/dtu/blackhole/04/184612/tmp
export TMP=/dtu/blackhole/04/184612/tmp

export HF_HOME=/dtu/blackhole/04/184612/huggingface_cache
export HUGGING_FACE_HUB_TOKEN=

unset TRANSFORMERS_CACHE

# Navigate to rStar directory
cd rStar

CUDA_VISIBLE_DEVICES=0 python run_src/do_generate.py \
    --dataset_name GSM8K \
    --test_json_filename test_all \
    --model_ckpt mistralai/Mistral-7B-v0.1 \
    --note default \
    --num_rollouts 32 \
    --start_idx 0 \
    --end_idx 29

