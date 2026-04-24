#imports 
import os
import random
import shutil

# CONFIGURATION 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
source_folder = os.path.join(BASE_DIR, "all_images")
output_folder = os.path.join(BASE_DIR, "random_sets_of_6")
images_per_folder = 6

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get all images
images = [f for f in os.listdir(source_folder)
          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Shuffle randomly
random.shuffle(images)

# Split into chunks of 6
for i in range(0, len(images), images_per_folder):
    chunk = images[i:i + images_per_folder]

    # Skip if last folder has less than 6
    if len(chunk) < images_per_folder:
        break

    folder_name = os.path.join(output_folder, f"set_{i//images_per_folder + 1}")
    os.makedirs(folder_name, exist_ok=True)

    for img in chunk:
        src_path = os.path.join(source_folder, img)
        dst_path = os.path.join(folder_name, img)

        # Copy the image to the new folder
        shutil.copy(src_path, dst_path)

print("Done creating folders!")