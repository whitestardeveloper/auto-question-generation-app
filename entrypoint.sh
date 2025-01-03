#!/bin/bash

# Check if models are installed; if not, install them
MODEL_DIR="/app/models"

install_model() {
    if [ ! -f "$MODEL_DIR/$1.installed" ]; then
        echo "Installing model $1..."
        ollama pull $1 && touch "$MODEL_DIR/$1.installed"
    else
        echo "Model $1 already installed."
    fi
}

# List of models to check/install
# MODELS=("gemma2" "aya-expanse" "mistral-nemo" "llama3.1" "qwen2.5")
MODELS=("gemma2:27b" "aya-expanse:32b" "mistral-small" "llama3.1:70b" "qwen2.5:32b")

for model in "${MODELS[@]}"; do
    install_model $model
done

# Run the main Python script
python q_gen_task_list.py