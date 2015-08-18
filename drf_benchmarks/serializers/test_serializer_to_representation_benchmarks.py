#!/usr/bin/env python
# coding: utf-8

import pytest as pytest
from rest_framework import serializers


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    warmup=True
)
@pytest.mark.django_db
def test_object_serialization(instance, serializer, benchmark):
    serializer = serializer(instance=instance)

    @benchmark
    def result():
        return serializer.to_representation(instance)

    assert result


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    warmup=True
)
@pytest.mark.django_db
def test_object_list_serialization(instances_list, serializer, benchmark):
    serializer = serializers.ListSerializer(child=serializer(instance=instances_list))

    @benchmark
    def result():
        return serializer.to_representation(instances_list)

    assert result if instances_list else not result


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_serialization(nested_instance, nested_serializer, benchmark):
    serializer = nested_serializer(instance=nested_instance)

    @benchmark
    def result():
        return serializer.to_representation(nested_instance)

    assert result


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_list_serialization(nested_instances_list, nested_serializer, benchmark):
    serializer = serializers.ListSerializer(child=nested_serializer(instance=nested_instances_list))

    @benchmark
    def result():
        return serializer.to_representation(nested_instances_list)

    assert result if nested_instances_list else not result
