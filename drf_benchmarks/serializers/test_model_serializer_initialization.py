#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from rest_framework import serializers


@pytest.mark.benchmark(
    group="ModelSerializer initialization",
    warmup=True
)
def test_serializer_initialization(serializer, data, benchmark):
    @benchmark
    def result():
        return serializer(data=data)


@pytest.mark.benchmark(
    group="ModelSerializer initialization",
    warmup=True
)
def test_nested_serializer_initialization(nested_serializer, nested_data, benchmark):
    @benchmark
    def result():
        return nested_serializer(data=nested_data)


@pytest.mark.benchmark(
    group="ModelSerializer initialization",
    warmup=True
)
def test_list_serializer_initialization(serializer, data_list, benchmark):
    @benchmark
    def result():
        return serializers.ListSerializer(child=serializer(), data=data_list)


@pytest.mark.benchmark(
    group="ModelSerializer initialization",
    warmup=True
)
def test_nested_list_serializer_initialization(nested_serializer, nested_data_list, benchmark):
    @benchmark
    def result():
        return serializers.ListSerializer(child=nested_serializer(), data=nested_data_list)
