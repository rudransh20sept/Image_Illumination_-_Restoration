# setup.py
from setuptools import setup, find_packages

setup(
    name="image-illumination-restoration",
    version="0.1.3",
    author="Rudransh Joshi",
    author_email="rudransh20septmber@gmail.com",
    description="Image_Illumination_&_Restoration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
  # optional
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "opencv-python",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
