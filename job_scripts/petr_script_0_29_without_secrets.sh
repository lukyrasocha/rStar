#!/bin/bash
#BSUB -q gpua100
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J mistral_generate_0_29
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=40GB]"
#BSUB -W 24:00
#BSUB -u s240466@student.dtu.dk
#BSUB -o mistral_generate_0_29%J.out
#BSUB -e mistral_generate_0_29%J.err


# Activate conda environment
source /dtu/blackhole/17/209207/miniconda3/bin/activate
conda activate DL_project


export TMPDIR=/dtu/blackhole/17/209207/tmp
export TEMP=/dtu/blackhole/17/209207/tmp
export TMP=/dtu/blackhole/17/209207/tmp

export HF_HOME=/dtu/blackhole/17/209207/huggingface_cache
export HUGGING_FACE_HUB_TOKEN=

unset TRANSFORMERS_CACHE


CUDA_VISIBLE_DEVICES=0 python run_src/do_generate.py \
    --dataset_name GSM8K \
    --test_json_filename test_0_29 \
    --model_ckpt mistralai/Mistral-7B-v0.1 \
    --note default \
    --num_rollouts 32

