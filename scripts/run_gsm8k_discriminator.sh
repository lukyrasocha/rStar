CUDA_VISIBLE_DEVICES=0 python run_src/do_discriminate.py \
    --model_ckpt microsoft/Phi-3-mini-4k-instruct \
    --root_dir run_outputs/GSM8K/Mistral-7B-v0.1/1060-to-1159-2024-11-16_16-35-17 \
    --dataset_name GSM8K \
    --note default
