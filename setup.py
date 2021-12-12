#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import os
from os.path import join as pjoin

from setuptools import setup

from setupbase import (
    create_cmdclass, ensure_targets, combine_commands, HERE, install_npm
)

# Get our version

nb_path = pjoin(HERE, 'src', 'evidently', 'nbextension', 'static')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    # pjoin(HERE, 'lib', 'plugin.js'),
]

package_data_spec = {
    'evidently': [
        'nbextension/static/*.*js*',
        'nbextension/static/*.woff2',
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/evidently', nb_path, '*.js*'),
    ('share/jupyter/nbextensions/evidently', nb_path, '*.woff2'),
    ('etc/jupyter/nbconfig/notebook.d', HERE, 'evidently.json')
]

cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
                           data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(os.path.join(HERE, "ui"), build_cmd='build'),
    ensure_targets(jstargets),
)

with open("requirements.txt", encoding="utf-8") as dep_file:
    dependencies = dep_file.readlines()
with open("dev_requirements.txt", encoding="utf-8") as dev_dep_file:
    dev_dependencies = dev_dep_file.readlines()
setup_args = dict(
    cmdclass=cmdclass,
    keywords=[],
    classifiers=[],
    include_package_data=True,
    install_requires=dependencies,
    extras_require={
        "dev": dev_dependencies,
    },
    entry_points={
    },
)

if __name__ == '__main__':
    setup(**setup_args)
