from setuptools import setup
from fbstories import VERSION

setup(
    name="fbstories",
    version=VERSION,
    description="Script para descargar stories de facebook",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    author="Leo",
    url="https://github.com/CalumRakk/FBStories",
    install_requires=["lxml==4.9.2", "playwright==1.30.0", "requests==2.31.0"],
    entry_points={
        "console_scripts": ["fbstories=fbstories.cli:run_script"],
    },
    packages=["fbstories"],
)
