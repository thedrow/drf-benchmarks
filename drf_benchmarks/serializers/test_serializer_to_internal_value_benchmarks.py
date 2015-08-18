#!/usr/bin/env python
# coding: utf-8

import pytest as pytest
from rest_framework import serializers


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    warmup=True
)
@pytest.mark.django_db
def test_object_deserialization(serializer_class, data, benchmark):
    serializer = serializer_class(data=data)

    @benchmark
    def result():
        return serializer.to_internal_value(data)

    assert result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    warmup=True
)
def test_object_list_deserialization(serializer_class, data_list, benchmark):
    serializer = serializers.ListSerializer(child=serializer_class(), data=data_list)

    @benchmark
    def result():
        return serializer.to_internal_value(data_list)

    assert result if data_list else not result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_deserialization(nested_serializer_class, nested_data, benchmark):
    serializer = nested_serializer_class(data=nested_data)

    @benchmark
    def result():
        return serializer.to_representation(nested_data)

    assert result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_list_deserialization(nested_serializer_class, data_list_with_nesting, benchmark):
    serializer = serializers.ListSerializer(child=nested_serializer_class(), data=data_list_with_nesting)

    @benchmark
    def result():
        return serializer.to_representation(data_list_with_nesting)

    assert result if data_list_with_nesting else not result and serializer.is_valid(), serializer.errors
