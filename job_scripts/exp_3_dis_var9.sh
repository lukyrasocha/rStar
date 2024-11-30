#!/bin/bash
#BSUB -q gpua100
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J exp_3_discriminate_var_9
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=40GB]"
#BSUB -u s223531@dtu.dk
#BSUB -N
#BSUB -W 04:00
#BSUB -o exp_3_discriminate_var_9%J.out
#BSUB -e exp_3_discriminate_var_9%J.err

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

CUDA_VISIBLE_DEVICES=0 python run_src/do_discriminate.py \
    --dataset_name GSM8K \
    --root_dir run_outputs/GSM8K/Mistral-7B-v0.1/ExperimentsGenerator/exp_3_names_numbers_variation_9 \
    --model_ckpt microsoft/Phi-3-mini-4k-instruct \
    --note exp_3_names_numbers_variation_9