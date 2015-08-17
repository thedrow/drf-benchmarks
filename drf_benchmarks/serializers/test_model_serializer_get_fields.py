#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


@pytest.mark.benchmark(
    group="ModelSerializer get_fields",
    warmup=True
)
def test_serializer_get_fields(serializer, data, benchmark):
    serializer = serializer(data=data)

    @benchmark
    def result():
        return serializer.get_fields()


@pytest.mark.benchmark(
    group="ModelSerializer get_fields",
    warmup=True
)
def test_nested_serializer_get_fields(nested_serializer, nested_data, benchmark):
    serializer = nested_serializer(data=nested_data)

    @benchmark
    def result():
        return serializer.get_fields()


@pytest.mark.benchmark(
    group="ModelSerializer get_fields",
    warmup=True
)
def test_serializer_get_fields_twice(serializer, data, benchmark):
    serializer = serializer(data=data)

    @benchmark
    def result():
        serializer.get_fields()
        return serializer.get_fields()


@pytest.mark.benchmark(
    group="ModelSerializer get_fields",
    warmup=True
)
def test_nested_serializer_get_fields_twice(nested_serializer, nested_data, benchmark):
    serializer = nested_serializer(data=nested_data)

    @benchmark
    def result():
        serializer.get_fields()
        return serializer.get_fields()
