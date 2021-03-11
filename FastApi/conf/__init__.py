#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    desc: init文件,用于定位PROJECT_ROOT
    author: liukun
    date: 2020-05-01
'''
import os
_project_root = os.path.dirname(
    os.path.dirname(
            os.path.realpath(__file__)
    )
)