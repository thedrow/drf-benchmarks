#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers

from drf_benchmarks import test_serializer_fields, test_nested_serializer_fields
from drf_benchmarks.models import RegularFieldsModel, RegularFieldsAndFKModel
from drf_benchmarks.serializers.cython_ordered_dict.base import CythonOrderedDictMixin


class TestSerializer(CythonOrderedDictMixin, serializers.ModelSerializer):
    class Meta:
        model = RegularFieldsModel
        fields = test_serializer_fields


class TestNestedSerializer(CythonOrderedDictMixin, serializers.ModelSerializer):
    fk = TestSerializer()

    class Meta:
        model = RegularFieldsAndFKModel
        fields = test_nested_serializer_fields