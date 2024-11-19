#!/bin/bash
#BSUB -q gpua100
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J mistral_discriminate
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=10GB]"
#BSUB -W 12:00
#BSUB -o mistral_discriminate_%J.out
#BSUB -e mistral_discriminate_%J.err

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

python eval_src/do_eval.py --dataset_name GSM8K --exp_dir_path /dtu/blackhole/17/209207/DL_project/rStar/run_outputs/GSM8K/Mistral-7B-v0.1/test_0_29

