# idr/__main__.py
import sys
from .enhancer import em

if len(sys.argv) < 2:
    print("Usage: python -m idr <image_path>")
else:
    image_path = sys.argv[1]
    em(image_path)
    print(" Enhancement finished. Check 'output_final.jpg'.")
