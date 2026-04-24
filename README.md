# Image Labeling and Dataset Preparation Pipeline

## Overview  
This project provides a pipeline for generating labeled images, organizing them into randomized sets, and consolidating outputs into a single directory. It is useful for dataset preparation tasks such as training machine learning models or conducting user studies. It is further split into sets of 6 images.

---

## Features  

- Add labels (text or image-based) to images  
- Control label size, position, rotation, and opacity  
- Generate multiple labeled variations of each image  
- Flatten nested folder structures into a single directory  
- Randomly group images into fixed-size sets  

---

## Project Structure  
.
├── generateLabel.py    # Adds labels to images
├── randomiseImages.py # Creates random sets of images
├── transferImages.py   # Moves images from nested folders
├── scriptToRun.sh
└── README.md


---

## Installation  

1. Clone the repository or download the files  

## Usage

### Run using Bash Script

1. Linux/ WSL 
Make the script executable:
```
chmod +x runPipelineLinuxWSL.sh
```

Run the script:
```
./runPipelineLinuxWSL.sh
```

Functionality:
- Installs required dependencies (Pillow)
- Runs the labeling script on 6 predefined images in Orignal Image Dataset 


2. Windows 
Run the script:
```
./runPipelineWindows.ps1
```

Functionality:
- Installs required dependencies (Pillow)
- Runs the labeling script on 6 predefined images in Orignal Image Dataset 
---

### Run using image paths 
1. Generate Labeled Images  
```
python3 generateLabel.py image1.jpg image2.jpg
```

### Output Folder Structure Example
Output: Creates a folder labeled_outputs/

For each image:  
- Saves original image  
- Generates labeled versions with:  
 -- Multiple sizes (LABEL_SIZES)  
 -- Multiple positions (top-left, top-right, bottom-left, bottom-right)  

Example: After running on dog.jpg, cat.jpg, etc., your structure will look like:  
labeled_outputs/  
│  
├── dog/  
│   ├── original_dog.jpg  
│   │  
│   ├── 0.1pct/  
│   │   ├── dog_top-left.jpg  
│   │   ├── dog_top-right.jpg  
│   │   ├── dog_bottom-left.jpg  
│   │   └── dog_bottom-right.jpg  
│   │  
│   ├── 0.25pct/  
│   │   ├── dog_top-left.jpg  
│   │   ├── dog_top-right.jpg  
│   │   ├── dog_bottom-left.jpg  
│   │   └── dog_bottom-right.jpg  
│   │  
│   ├── 0.5pct/  
│   │   └── ...  
│   │  
│   └── 1pct/  
│       └── ...  
│  
├── cat/  
│   ├── original_cat.jpg  
│   ├── 0.1pct/  
│   ├── 0.25pct/  
│   ├── 0.5pct/  
│   └── 1pct/  
│  
└── ...  

### Flatten Folder Structure 

Edit paths inside transferImages.py, then run:  
```
python3 transferImages.py  
```
Functionality:  
- Moves all images from nested directories into a single folder  
- Automatically renames duplicates to avoid overwriting  

### Randomize Images into Sets  

Edit paths inside randomiseImages.py, then run:  
```
python3 randomiseImages.py  
```

Functionality:  
- Reads all images from source folder  
- Shuffles them  
- Splits into folders of 6 images each  

## Dependencies  
Python 3.8+  
Pillow 

