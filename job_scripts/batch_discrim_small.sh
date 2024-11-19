#!/bin/bash
#BSUB -q gpua100
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J evaluate_mistral_discriminate_small
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=10GB]"
#BSUB -W 06:00
#BSUB -o evaluate_mistral_discriminate_small%J.out
#BSUB -e evaluate_mistral_discriminate_small%J.err

# Activate conda environment
source /dtu/blackhole/17/209207/miniconda3/bin/activate
conda activate DL_project

#### Set environment variables ####
export TMPDIR=/dtu/blackhole/17/209207/tmp
export TEMP=/dtu/blackhole/17/209207/tmp
export TMP=/dtu/blackhole/17/209207/tmp

export HF_HOME=/dtu/blackhole/17/209207/huggingface_cache
export HUGGING_FACE_HUB_TOKEN=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  # Replace with your actual token

unset TRANSFORMERS_CACHE

# Run your script with --half_precision
python run_src/do_discriminate.py \
    --model_ckpt microsoft/Phi-3-mini-4k-instruct \
    --root_dir /dtu/blackhole/17/209207/DL_project/rStar/run_outputs/GSM8K/Mistral-7B-v0.1/test_0_29 \
    --dataset_name GSM8K \
    --note default \
