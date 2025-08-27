import os
import json
from PIL import Image

FLAGS_DIR = 'state_flags_png_1024/state_flags_png'
THUMBNAIL_DIR = 'thumbnails'
THUMBNAIL_SIZE = (64, 40)
OUTPUT_JSON = 'flags_data.json'

def normalize_rgb(rgb):
    return tuple([v / 255.0 for v in rgb])

def process_flag(flag_path, thumbnail_path):
    img = Image.open(flag_path).convert('RGB')
    pixels = list(img.getdata())
    norm_pixels = [normalize_rgb(p) for p in pixels]
    avg_r = sum([p[0] for p in norm_pixels]) / len(norm_pixels)
    avg_g = sum([p[1] for p in norm_pixels]) / len(norm_pixels)
    avg_b = sum([p[2] for p in norm_pixels]) / len(norm_pixels)
    # Save thumbnail
    img.thumbnail(THUMBNAIL_SIZE)
    img.save(thumbnail_path)
    return avg_r, avg_g, avg_b

def main():
    os.makedirs(THUMBNAIL_DIR, exist_ok=True)
    flags_data = []
    for fname in os.listdir(FLAGS_DIR):
        if fname.endswith('.png'):
            state = fname.replace('.png', '').replace('_', ' ')
            flag_path = os.path.join(FLAGS_DIR, fname)
            thumbnail_path = os.path.join(THUMBNAIL_DIR, fname)
            avg_r, avg_g, avg_b = process_flag(flag_path, thumbnail_path)
            flags_data.append({
                'state': state,
                'avg_rgb': [avg_r, avg_g, avg_b],
                'thumbnail': thumbnail_path
            })
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(flags_data, f, indent=2)

if __name__ == '__main__':
    main()
