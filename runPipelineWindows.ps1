Write-Host "Installing dependencies..."
python -m pip install --upgrade pip
pip install Pillow

Write-Host "Running labeling script on 6 images..."

$images = @(
    "./Original Image Dataset/AVENGERS_AI_MODIFIED.jpeg"
    "./Original Image Dataset/CHAK_DE_INDIA_AI_MODIFIED.png"
    "./Original Image Dataset/MENS_CRICKET_AI_MODIFIED.jpg"
    "./Original Image Dataset/WOMENS_CRICKET_AI_MODIFIED.jpeg"
    "./Original Image Dataset/ZNMD_AI_MODIFIED.png"
    "./Original Image Dataset/F1_AI_MODIFIED.png"
)

foreach ($img in $images) {
    Write-Host "Processing $img"
    python generateLabel.py $img
}

Write-Host "Done!"