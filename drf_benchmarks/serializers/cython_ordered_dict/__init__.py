#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import platform

if platform.python_implementation() != 'PyPy':
    from drf_benchmarks.serializers.cython_ordered_dict.serializers import *
