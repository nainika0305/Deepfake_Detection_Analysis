import os
import shutil

# CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
source_root = os.path.join(BASE_DIR, "labeledOutputs")
destination = os.path.join(BASE_DIR, "all_images")

os.makedirs(destination, exist_ok=True)

for root, dirs, files in os.walk(source_root):
    for file in files:
        src = os.path.join(root, file)
        dst = os.path.join(destination, file)

        # Avoid overwriting duplicate names
        if os.path.exists(dst):
            base, ext = os.path.splitext(file)
            count = 1
            while os.path.exists(dst):
                dst = os.path.join(destination, f"{base}_{count}{ext}")
                count += 1

        shutil.move(src, dst)

print("All files from nested folders moved!")