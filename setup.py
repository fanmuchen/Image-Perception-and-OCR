import setuptools
from pathlib import Path

setuptools.setup(
    name="fmcimage",
    version=0.24,
    # long_description=Path("README.md").read_text(),
    long_description="A lightweight python package that contains necessary modules for perceiving images and using ocr.",
    packages=setuptools.find_packages(exclude=["data","tests"]),
)