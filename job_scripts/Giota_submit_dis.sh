#!/bin/bash
#BSUB -q gpua100
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J mistral_discriminate
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=40GB]"
#BSUB -W 12:00
#BSUB -u s223531@dtu.dk
#BSUB -N 
#BSUB -o mistral_discriminate_%J.out
#BSUB -e mistral_discriminate_%J.err


# Activate conda environment
source /dtu/blackhole/04/184612/miniconda3/bin/activate
conda activate DL_PrrojectEleven

#### Set environment variables #### 
export TMPDIR=/dtu/blackhole/04/184612/tmp
export TEMP=/dtu/blackhole/04/184612/tmp
export TMP=/dtu/blackhole/04/184612/tmp

export HF_HOME=/dtu/blackhole/04/184612/huggingface_cache
export HUGGING_FACE_HUB_TOKEN=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  

unset TRANSFORMERS_CACHE

# Navigate to rStar directory
cd rStar

CUDA_VISIBLE_DEVICES=0 python run_src/do_discriminate.py \
    --root_dir  run_outputs/GSM8K/Mistral-7B-v0.1/'2024-11-16_22-43-39---[default]' \
    --model_ckpt microsoft/Phi-3-mini-4k-instruct \
    --dataset_name GSM8K \
    --note default 

