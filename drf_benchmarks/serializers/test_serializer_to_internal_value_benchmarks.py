#!/usr/bin/env python
# coding: utf-8

import pytest as pytest
from rest_framework import serializers


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    min_rounds=100,
    max_time=60,
    warmup=True
)
@pytest.mark.django_db
def test_object_deserialization(serializer, data, benchmark):
    serializer = serializer(data=data)

    @benchmark
    def result():
        return serializer.to_internal_value(data)

    assert result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    min_rounds=1000,
    max_time=60,
    warmup=True
)
def test_object_list_deserialization(serializer, data_list, benchmark):
    serializer = serializers.ListSerializer(child=serializer(), data=data_list)

    @benchmark
    def result():
        return serializer.to_internal_value(data_list)

    assert result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    min_rounds=100,
    max_time=60,
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_deserialization(nested_serializer, nested_data, benchmark):
    serializer = nested_serializer(data=nested_data)

    @benchmark
    def result():
        return serializer.to_representation(nested_data)

    assert result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    min_rounds=1000,
    max_time=60,
    warmup=True
)
@pytest.mark.parametrize("number_of_objects", range(2, 10))
@pytest.mark.django_db
def test_nested_object_list_deserialization(nested_serializer, data_list_with_nesting, benchmark):
    serializer = serializers.ListSerializer(child=nested_serializer(), data=data_list_with_nesting)

    @benchmark
    def result():
        return serializer.to_representation(data_list_with_nesting)

    assert result and serializer.is_valid(), serializer.errors
