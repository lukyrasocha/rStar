#!/bin/bash
#BSUB -q gpua100 
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J phi3mini4k
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=40GB]"
#BSUB -W 14:00
#BSUB -o hpc_outputs/mistral_generate_%J.out
#BSUB -e hpc_outputs/mistral_generate_%J.err


#### Set environment variables #### 
export HUGGING_FACE_HUB_TOKEN=
export HUGGINGFACE_TOKEN=

export HF_HOME=/dtu/blackhole/0a/203690/huggingface_cache

source /dtu/blackhole/0a/203690/miniconda3/bin/activate

conda activate rStar_new

CUDA_VISIBLE_DEVICES=0 python run_src/do_generate.py \
    --dataset_name GSM8K \
    --test_json_filename test_all \
    --model_ckpt mistralai/Mistral-7B-v0.1 \
    --note default \
    --num_rollouts 32 
