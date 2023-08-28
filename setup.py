from setuptools import setup
import pkg_resources

setup(
    name="fbstories",
    version="0.3",
    description="Script para descargar stories de facebook",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    author="Leo",
    url="https://github.com/CalumRakk/FBStories",
    install_requires=["lxml==4.9.2", "playwright==1.30.0", "requests==2.28.2"],
    entry_points={
        "console_scripts": ["fbstories=fbstories.cli:run_script"],
    },
    packages=["fbstories"],
)
