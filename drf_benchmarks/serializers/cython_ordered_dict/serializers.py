#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect

from cyordereddict import OrderedDict
from rest_framework import serializers

from drf_benchmarks import test_serializer_fields, test_nested_serializer_fields
from drf_benchmarks.models import RegularFieldsModel, RegularFieldsAndFKModel


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularFieldsModel
        fields = test_serializer_fields


class TestNestedSerializer(serializers.ModelSerializer):
    fk = TestSerializer()

    class Meta:
        model = RegularFieldsAndFKModel
        fields = test_nested_serializer_fields


# Inject the cythonized ordered dict to all methods
for f in inspect.getmembers(TestSerializer, lambda m: inspect.ismethod(m)):
    if f[1].im_func.func_globals:
        f[1].im_func.func_globals['OrderedDict'] = OrderedDict

for f in inspect.getmembers(TestNestedSerializer, lambda m: inspect.ismethod(m)):
    if f[1].im_func.func_globals:
        f[1].im_func.func_globals['OrderedDict'] = OrderedDict
