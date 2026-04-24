#!/bin/bash

# Exit on error
set -e

echo "Installing dependencies..."
pip install --upgrade pip
pip install Pillow

echo "Running labeling script on 6 images..."

# Replace these with your actual image paths, currently set to images availaible in Original Image Dataset 
IMAGES=(
    "./Original Image Dataset/AVENGERS_AI_MODIFIED.jpeg"
    "./Original Image Dataset/CHAK_DE_INDIA_AI_MODIFIED.png"
    "./Original Image Dataset/MENS_CRICKET_AI_MODIFIED.jpg"
    "./Original Image Dataset/WOMENS_CRICKET_AI_MODIFIED.jpeg"
    "./Original Image Dataset/ZNMD_AI_MODIFIED.png"
    "./Original Image Dataset/F1_AI_MODIFIED.png"
)

# Run script for each image individually
for img in "${IMAGES[@]}"
do
    echo "Processing $img"
    python3 generateLabel.py "$img"
done

echo "Done!"