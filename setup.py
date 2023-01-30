
from setuptools import setup
import os
import pkg_resources

setup(
    name="fbstories",
    version="0.1",
    description='Script para descargar stories de facebook',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    author="Leo",
    url="https://github.com/CalumRakk/FBStories",
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    entry_points={
        "console_scripts": ["fbstories=fbstories.cli"],
    },
    packages=['fbstories'],
)
