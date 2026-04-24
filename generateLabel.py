# imports required 
import os
import sys
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# CONFIGURATION 
LABEL_TYPE       = "text"                        # Options: "text" or "image"
IMAGE_LABEL_PATH = "IMAGE.png"                   # Only used if TYPE is "image"
LABEL_TEXT      = "AI Modified"   
FONT_COLOR      = (150, 150, 150) 
BG_COLOR        = (255, 255, 255)                
BG_OPACITY      = 0                              # 0-255
LABEL_SIZES     = [0.1, 0.25, 0.5, 1]            # % of total image area
LABEL_POSITION  = "bottom-right"                 # Options: top-left, bottom-left, top-right, bottom-right, center, custom
CUSTOM_COORDS   = (50, 50)                       # (x, y) pixels - only used if POSITION is "custom"
ROTATION_ANGLE  = 0                              # Degrees to tilt
PADDING         = 0.15           
OUTPUT_FOLDER   = "labeledOutputs"

# Image logo 
if LABEL_TYPE == "image":
    GEMINI_GRAY     = (60, 64, 67)     
    GEMINI_SURFACE  = (241, 243, 244)  
    FONT_COLOR      = (60, 64, 67)     
    BG_COLOR        = (241, 243, 244)  
    BG_OPACITY      = 0                
    OUTPUT_FOLDER   = "imageLabel/labeledOutputs"

# Helper functions

def find_font(target_px):
    '''Tries to find a common bold font on the system. Falls back to default if not found.'''
    font_paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
                  "/System/Library/Fonts/Helvetica.ttc", 
                  "C:/Windows/Fonts/arialbd.ttf"]
    for path in font_paths:
        if os.path.exists(path):
            try: return ImageFont.truetype(path, int(target_px))
            except: continue
    return ImageFont.load_default()

def get_text_size(draw, text, font):
    '''Returns the width and height of the text when drawn with the specified font.'''
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def add_label_fixed_anchor(image_path, size_percent, output_path):
    '''Adds a label (text or image) to the input image at a fixed position, ensuring the label's top-left corner remains anchored even after rotation.'''
    img = Image.open(image_path).convert("RGBA")
    img_w, img_h = img.size
    
    # Calculate Target Area for the Logo/Text
    total_img_area = img_w * img_h
    target_label_area = total_img_area * (size_percent / 100)

    if LABEL_TYPE == "image" and os.path.exists(IMAGE_LABEL_PATH):
        logo = Image.open(IMAGE_LABEL_PATH).convert("RGBA")
        orig_w, orig_h = logo.size
        aspect_ratio = orig_w / orig_h
        
        # Calculate width/height so their product equals target_label_area
        # Area = w * h  AND  w = h * aspect
        # Area = h^2 * aspect  =>  h = sqrt(Area / aspect)
        label_h = int(math.sqrt(target_label_area / aspect_ratio))
        label_w = int(label_h * aspect_ratio)
        
        # Resize logo to the calculated label size
        label_raw = logo.resize((label_w, label_h), Image.Resampling.LANCZOS)
    
    else:
        # TEXT LOGIC 
        aspect = 5.0  
        label_h = int(math.sqrt(target_label_area / aspect))
        label_w = int(target_label_area / label_h)

        label_raw = Image.new("RGBA", (label_w, label_h), (0, 0, 0, 0))
        draw_label = ImageDraw.Draw(label_raw)
        
        font_size = max(int(label_h * (1 - PADDING * 2)), 8)
        font = find_font(font_size)
        tw, th = get_text_size(draw_label, LABEL_TEXT, font)
        draw_label.text(((label_w - tw)//2, (label_h - th)//2), LABEL_TEXT, font=font, fill=(*FONT_COLOR, 255))

    # Rotate the label 
    rotated_label = label_raw.rotate(ROTATION_ANGLE, resample=Image.BICUBIC, expand=True)# type: ignore 
    
    # When we rotate, the new 'rotated_label' is larger than the original.
    # To keep the visual top-left corner in the same spot, we must adjust. 
    if LABEL_POSITION == "custom":
        # Calculate how much the rotation expanded the box. This prevents the label from "moving" as it grows.
        offset_x = (rotated_label.width - label_w) // 2
        offset_y = (rotated_label.height - label_h) // 2
        
        # subtract the expansion so the original top-left stays at CUSTOM_COORDS
        paste_pos = (CUSTOM_COORDS[0] - offset_x, CUSTOM_COORDS[1] - offset_y)
    else:
        # Standard corners logic
        margin = 20
        pos_map = {
            "top-left": (margin, margin),
            "top-right": (img_w - rotated_label.width - margin, margin),
            "bottom-right": (img_w - rotated_label.width - margin, img_h - rotated_label.height - margin),
            "bottom-left": (margin, img_h - rotated_label.height - margin)
        }
        paste_pos = pos_map.get(LABEL_POSITION, pos_map["bottom-left"])

    final_img = Image.alpha_composite(img, Image.new("RGBA", img.size, (0,0,0,0)))
    final_img.paste(rotated_label, paste_pos, rotated_label)
    final_img.convert("RGB").save(output_path, quality=95)


# Define the positions you want to cycle through
POSITIONS_TO_GENERATE = ["top-left", "top-right", "bottom-left", "bottom-right"]

def main():
    if len(sys.argv) < 2: return
    
    # Ensure the root output directory exists
    root_out = Path(OUTPUT_FOLDER)
    root_out.mkdir(parents=True, exist_ok=True)

    for img_path in sys.argv[1:]:
        p = Path(img_path)
        
        # Create the base folder for this specific image
        # Path: labeledOutputs/image_name/
        image_base_dir = root_out / p.stem
        image_base_dir.mkdir(parents=True, exist_ok=True)
        
        # Save the original image in the image base folder
        img_original = Image.open(img_path).convert("RGB")
        img_original.save(image_base_dir / f"original_{p.name}")

        # Loop through sizes
        for size in LABEL_SIZES:
            # CREATE SUB-FOLDER FOR PERCENTAGE
            size_dir = image_base_dir / f"{size}pct"
            size_dir.mkdir(parents=True, exist_ok=True)
            
            # 4. Loop through the 5 positions
            positions = ["top-left", "top-right", "bottom-left", "bottom-right"]
            for pos in positions:
                # Update the global position for the drawing function
                global LABEL_POSITION
                LABEL_POSITION = pos
                
                # Construct filename and save inside the size_dir
                file_name = f"{p.stem}_{pos}.jpg"
                save_path = size_dir / file_name
                
                add_label_fixed_anchor(img_path, size, save_path)
                

    print(f"Done! Check the '{OUTPUT_FOLDER}' directory.")

if __name__ == "__main__":
    main()