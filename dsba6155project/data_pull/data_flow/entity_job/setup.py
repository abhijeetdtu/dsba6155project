import setuptools

from distutils.command.build import build as _build  # type: ignore

import logging
import subprocess

setuptools.setup(
    name='entity-job',
    version='1.0',
    install_requires=[
        "spacy",
        "spacy-lookups-data",
        "apache-beam",
        "apache_beam[gcp]",
        "spacy-data-model @ https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz"
    ],
    packages=setuptools.find_packages()
)


#os.system("pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz")
