from setuptools import setup, find_packages

setup(
    name="pybgproutesapi",
    version="0.1.5",
    description="Python bindings for the bgproutes.io API",
    author="Thomas Holterbach and Thomas Alfroy",
    author_email="contact@bgproutes.io",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
