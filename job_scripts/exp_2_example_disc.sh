#!/bin/bash
#BSUB -q gpua100 
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J exp_1_discriminate_var_5
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=20GB]"
#BSUB -u s233498@student.dtu.dk
#BSUB -B
#BSUB -N
#BSUB -W 03:00
#BSUB -o hpc_outputs/discriminate_exp_1_v5_%J.out
#BSUB -e hpc_outputs/discriminate_exp_1_v5_%J.err

####gpua100
####c02516

#### Set environment variables #### 
export HUGGING_FACE_HUB_TOKEN=
export HUGGINGFACE_TOKEN=
export HF_HOME=/dtu/blackhole/0a/203690/huggingface_cache

export TMPDIR=/dtu/blackhole/0a/203690/tmp
export TEMP=/dtu/blackhole/0a/203690/tmp
export TMP=/dtu/blackhole/0a/203690/tmp

source /dtu/blackhole/0a/203690/miniconda3/bin/activate

conda activate rStar_new

CUDA_VISIBLE_DEVICES=0 python run_src/do_discriminate.py \
    --model_ckpt microsoft/Phi-3-mini-4k-instruct \
    --root_dir run_outputs/GSM8K/Mistral-7B-v0.1/ExperimentsGenerator/exp_1_names_variation_5 \
    --dataset_name GSM8K \
    --note disc_exp_1_names_variation_5