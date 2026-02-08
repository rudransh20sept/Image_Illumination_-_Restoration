
# Image_Illumination_&_Restoration (IDR)

IDR is a lightweight Python library to automatically enhance dark or overly exposed images.
It automatically adjusts brightness and contrast


![logo.png](https://i.postimg.cc/Wbm0P3Dk/logo.png)

## Features

- Automatic detection and enhancement of dark images.
- Brightness and contrast correction.
- Simple one-line usage.
- Adaptive histogram equalization (CLAHE).

## File Formats Supported

- **.png**
- **.jpg**
- **.jpeg**
- **.bmp**
- **.tif**
- **.tiff**




## Installation



```python
pip install image-illumination-restoration

```
    
## Usage

```python
import idr

# Enhance a dark image
idr.em("dark.jpg")
print("done")

```
or 
```python
import idr

idr.em(
    input_path="dark.jpg",
    output_dir="./enhanced",
    verbose=True  # Enable to check min/max values and diagnose black output
)
```

## Demo

before using the lib

![App Screenshot](https://i.postimg.cc/J7Kv2Kfp/dark.jpg)

after using the lib

![App Screenshot](https://i.postimg.cc/Qtdk9gfN/dark-colors.jpg)

before using the lib

![App Screenshot](https://i.postimg.cc/RZ87gfrB/2.jpg)

after using the lib

![App Screenshot](https://i.postimg.cc/tCjmzK3w/2-final.jpg_++)


## Authors

- [@Rudransh joshi](https://rudransh.kafalfpc.com/)


## Acknowledgements

The name **IDR** was also chosen as a small tribute to a person who inspired me.


## License

[MIT](https://choosealicense.com/licenses/mit/)

