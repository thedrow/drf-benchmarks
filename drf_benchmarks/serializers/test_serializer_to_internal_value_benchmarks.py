#!/usr/bin/env python
# coding: utf-8
try:
    from line_profiler import LineProfiler
except ImportError:
    LineProfiler = None
import os
import pytest as pytest
from rest_framework import serializers

try:
    from cProfile import Profile
except ImportError:
    from profile import Profile


def profile_list_deserialization(serializer, child_serializer, data_list):
    if os.environ.get('CI', None) != 'true' or not LineProfiler:
        return
    profile = LineProfiler(serializer.to_internal_value, child_serializer.to_internal_value)
    profile.enable()
    serializer.to_internal_value(data_list)
    profile.disable()
    profile.print_stats()


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
    child_serializer = serializer_class()
    serializer = serializers.ListSerializer(child=child_serializer, data=data_list)

    @benchmark
    def result():
        return serializer.to_internal_value(data_list)

    profile_list_deserialization(serializer, child_serializer, data_list)

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
        return serializer.to_internal_value(nested_data)

    assert result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_list_deserialization(nested_serializer_class, data_list_with_nesting, benchmark):
    child_serializer = nested_serializer_class()
    serializer = serializers.ListSerializer(child=child_serializer, data=data_list_with_nesting)

    @benchmark
    def result():
        return serializer.to_internal_value(data_list_with_nesting)

    profile_list_deserialization(serializer, child_serializer, data_list_with_nesting)

    assert result if data_list_with_nesting else not result and serializer.is_valid(), serializer.errors
