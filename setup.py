from setuptools import setup, find_packages

setup(
    name='carDetection',
    version='1.0',
    description='Car Detection and Counting!',
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "streamlit",
        "torch",
        "ultralytics"]
)
