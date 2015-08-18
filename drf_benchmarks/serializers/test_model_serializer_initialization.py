#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from rest_framework import serializers


@pytest.mark.benchmark(
    group="ModelSerializer initialization",
    warmup=True
)
def test_serializer_initialization(serializer_class, data, benchmark):
    @benchmark
    def result():
        return serializer_class(data=data)


@pytest.mark.benchmark(
    group="ModelSerializer initialization",
    warmup=True
)
def test_nested_serializer_initialization(nested_serializer_class, nested_data, benchmark):
    @benchmark
    def result():
        return nested_serializer_class(data=nested_data)


@pytest.mark.benchmark(
    group="ModelSerializer initialization",
    warmup=True
)
def test_list_serializer_initialization(serializer_class, data_list, benchmark):
    @benchmark
    def result():
        return serializers.ListSerializer(child=serializer_class(), data=data_list)


@pytest.mark.benchmark(
    group="ModelSerializer initialization",
    warmup=True
)
def test_nested_list_serializer_initialization(nested_serializer_class, data_list_with_nesting, benchmark):
    @benchmark
    def result():
        return serializers.ListSerializer(child=nested_serializer_class(), data=data_list_with_nesting)
