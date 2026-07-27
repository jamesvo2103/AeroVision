# Training the airfoil airflow model

The web app needs a trained pix2pix-turbo checkpoint (`.pkl`) to produce real
airflow images. Training needs an **NVIDIA GPU**, so it does not run on the
CPU-only dev machine — use Google Colab (free GPU) or any cloud GPU.

## Easiest path: Colab
Open `train_airfoil_colab.ipynb` in Google Colab, set the runtime to GPU, and
run the cells top to bottom. It clones the repo, installs deps, trains, and
downloads the checkpoint.

## What the training does
- Input (`train_A`): clean airfoil images.
- Target (`train_B`): the same airfoil with airflow drawn around it.
- Text prompt per image: `data/Aerovision_data/train_prompts.json`.
- 193 training pairs / 21 test pairs.

## Manual command (any GPU box)
```bash
cd ml_model
pip install -r requirements.txt accelerate
export WANDB_MODE=offline   # skip Weights & Biases login

accelerate launch --mixed_precision=fp16 src/train_pix2pix_turbo.py \
  --pretrained_model_name_or_path "stabilityai/sd-turbo" \
  --dataset_folder "data/Aerovision_data" \
  --output_dir "outputs/airfoil_airflow" \
  --resolution 512 --train_batch_size 4 \
  --max_train_steps 3000 --checkpointing_steps 500 \
  --learning_rate 5e-6 \
  --lambda_lpips 5 --lambda_l2 1 --lambda_gan 0.5 --lambda_clipsim 5 \
  --report_to "wandb" --tracker_project_name "aerovision" \
  --enable_xformers_memory_efficient_attention --gradient_checkpointing
```
Checkpoints land in `outputs/airfoil_airflow/checkpoints/model_<step>.pkl`.
Start low (e.g. 500 steps) to sanity-check, then train longer for quality.

## Plugging the checkpoint into the app
```bash
export AEROVISION_MODEL_PATH=ml_model/checkpoints/airfoil_airflow.pkl
export AEROVISION_DEVICE=cuda
uvicorn backend.main:app --port 8000
```
With no checkpoint set, the backend runs in **STUB mode** (placeholder output)
so the frontend and backend can be developed without a GPU.
