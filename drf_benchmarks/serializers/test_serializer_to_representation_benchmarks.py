#!/usr/bin/env python
# coding: utf-8
try:
    from line_profiler import LineProfiler
except ImportError:
    LineProfiler = None
import os

import pytest as pytest
from rest_framework import serializers


def profile_list_serialization(serializer, child_serializer, instances_list):
    if os.environ.get('CI', None) != 'true' or not LineProfiler:
        return
    profile = LineProfiler(serializer.instances_list, child_serializer.instances_list)
    profile.enable()
    serializer.to_representation(instances_list)
    profile.disable()
    profile.print_stats()


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    warmup=True
)
@pytest.mark.django_db
def test_object_serialization(instance, serializer_class, benchmark):
    serializer = serializer_class(instance=instance)

    @benchmark
    def result():
        return serializer.to_representation(instance)

    assert result


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    warmup=True
)
@pytest.mark.django_db
def test_object_list_serialization(instances_list, serializer_class, benchmark):
    child_serializer = serializer_class(instance=instances_list)
    serializer = serializers.ListSerializer(child=child_serializer)

    @benchmark
    def result():
        return serializer.to_representation(instances_list)

    profile_list_serialization(serializer, child_serializer, instances_list)

    assert result if instances_list else not result


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_serialization(nested_instance, nested_serializer_class, benchmark):
    serializer = nested_serializer_class(instance=nested_instance)

    @benchmark
    def result():
        return serializer.to_representation(nested_instance)

    assert result


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_list_serialization(nested_instances_list, nested_serializer_class, benchmark):
    child_serializer = nested_serializer_class(instance=nested_instances_list)
    serializer = serializers.ListSerializer(child=child_serializer)

    @benchmark
    def result():
        return serializer.to_representation(nested_instances_list)

    profile_list_serialization(serializer, child_serializer, nested_instances_list)

    assert result if nested_instances_list else not result
