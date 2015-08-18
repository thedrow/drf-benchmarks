#!/usr/bin/env python
# coding: utf-8

import pytest as pytest
from rest_framework import serializers


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
    serializer = serializers.ListSerializer(child=serializer_class(instance=instances_list))

    @benchmark
    def result():
        return serializer.to_representation(instances_list)

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
    serializer = serializers.ListSerializer(child=nested_serializer_class(instance=nested_instances_list))

    @benchmark
    def result():
        return serializer.to_representation(nested_instances_list)

    assert result if nested_instances_list else not result
