#!/bin/bash
#BSUB -q gpua100
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J exp_1_names_variation_5
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=40GB]"
#BSUB -u s233498@dtu.dk
#BSUB -B
#BSUB -N
#BSUB -W 04:00
#BSUB -o hpc_outputs/exp_1_names_variation_5%J.out
#BSUB -e hpc_outputs/exp_1_names_variation_5%J.err


#### Set environment variables #### 
export HUGGING_FACE_HUB_TOKEN=
export HUGGINGFACE_TOKEN=
export HF_HOME=/dtu/blackhole/0a/203690/huggingface_cache

export TMPDIR=/dtu/blackhole/0a/203690/tmp
export TEMP=/dtu/blackhole/0a/203690/tmp
export TMP=/dtu/blackhole/0a/203690/tmp

source /dtu/blackhole/0a/203690/miniconda3/bin/activate

conda activate rStar_new

CUDA_VISIBLE_DEVICES=0 python run_src/do_generate.py \
    --dataset_name GSM8K \
    --test_json_filename GSMSymbolic/variations/exp_1_names/variation_5 \
    --model_ckpt mistralai/Mistral-7B-v0.1 \
    --note exp_1_names_variation_5 \
    --num_rollouts 32 \
    --num_subquestions 5 \
    --num_a1_steps 5 \
    --disable_a5