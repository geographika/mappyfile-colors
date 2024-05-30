import re
from setuptools import setup
from io import open

(__version__,) = re.findall('__version__ = "(.*)"', open("mappyfile_colors.py").read())


def readme():
    with open("README.rst", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="mappyfile-colors",
    version=__version__,
    description="A mappyfile plugin to convert between RGB and Hex colors, and to add human readable names",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
    ],
    url="http://github.com/geographika/mappyfile-colors",
    author="Seth Girvin",
    author_email="sethg@geographika.co.uk",
    license="MIT",
    py_modules=["mappyfile_colors"],
    install_requires=["mappyfile>=1.0.2", "webcolors"],
    entry_points={"mappyfile.plugins": "mappyfile_colors = mappyfile_colors"},
    zip_safe=False,
)
