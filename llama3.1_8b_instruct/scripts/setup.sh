#!/bin/bash

# Fail on errors
set -e

check_and_install() {
    local package=$1
    echo "Checking if '$package' is installed..."
    if python3 -c "import $package" &> /dev/null; then
        echo "'$package' is already installed."
    else
        echo "'$package' not found. Installing now..."
        pip install "$package"
        echo "'$package' installed successfully."
    fi
}

# List of required Python packages
packages=(transformers torch accelerate)

# Install missing packages
for pkg in "${packages[@]}"; do
    check_and_install "$pkg"
done

# Download the model's checkpoint using a Python script
echo "Downloading the model's checkpoint..."
python3 - <<EOF
import transformers
import torch
import yaml
import os

config_path = os.path.join('config', 'config.yml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

from huggingface_hub import login

try:
    token = config['hugging_face']['token']
    login(token)
except KeyError as e:
    print(f"Error: Missing key in the configuration file - {e}")
except Exception as e:
    print(f"Login failed: {e}")

model_id = config['model']['model_name']

transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"dtype": torch.bfloat16},
    device_map="auto",
)
EOF

# Move the downloaded model to the specified folder
echo "Moving model's checkpoints to app/models..."
SOURCE_DIR="$HOME/.cache/huggingface/hub/models--meta-llama--Meta-Llama-3.1-8B-Instruct"
DEST_DIR="./app/models"

if [ -d "$SOURCE_DIR" ]; then
    mkdir -p "$DEST_DIR"
    sudo mv "$SOURCE_DIR" "$DEST_DIR"
    echo "Model moved successfully to $DEST_DIR."
else
    echo "Model source directory not found: $SOURCE_DIR"
    exit 1
fi

echo "Completed setup."

