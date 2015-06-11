#!/usr/bin/env python
# coding: utf-8
from datetime import datetime
from decimal import Decimal
import gc
import pytest as pytest
from rest_framework import serializers
from drf_benchmarks.models import RegularFieldsModel, RegularFieldsAndFKModel

data = {
    'big_integer_field': 100000,
    'char_field': 'a',
    'comma_separated_integer_field': '1,2',
    'date_field': datetime.now().date(),
    'datetime_field': datetime.now(),
    'decimal_field': Decimal('1.5'),
    'email_field': 'somewhere@overtherainbow.com',
    'float_field': 0.443,
    'integer_field': 55,
    'null_boolean_field': True,
    'positive_integer_field': 1,
    'positive_small_integer_field': 1,
    'slug_field': 'slug-friendly-text',
    'small_integer_field': 1,
    'text_field': 'lorem ipsum',
    'time_field': datetime.now().time(),
    'url_field': 'https://overtherainbow.com'
}

nested_data = {
    'big_integer_field': 100000,
    'char_field': 'a',
    'comma_separated_integer_field': '1,2',
    'date_field': datetime.now().date(),
    'datetime_field': datetime.now(),
    'decimal_field': Decimal('1.5'),
    'email_field': 'somewhere@overtherainbow.com',
    'float_field': 0.443,
    'integer_field': 55,
    'null_boolean_field': True,
    'positive_integer_field': 1,
    'positive_small_integer_field': 1,
    'slug_field': 'slug-friendly-text',
    'small_integer_field': 1,
    'text_field': 'lorem ipsum',
    'time_field': datetime.now().time(),
    'url_field': 'https://overtherainbow.com',
    'fk': data
}

data_list = [data for _ in range(100)]

data_list_with_nesting = [nested_data for _ in range(100)]


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularFieldsModel
        fields = list(data.keys()) + ['method']


class TestNestedSerializer(serializers.ModelSerializer):
    fk = TestSerializer()

    class Meta:
        model = RegularFieldsAndFKModel
        fields = list(data.keys()) + ['method', 'fk']


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    min_rounds=100,
    warmup=True
)
def test_object_serialization(benchmark):
    instance = RegularFieldsModel(**data)
    serializer = TestSerializer(instance=instance)

    @benchmark
    def result():
        return serializer.to_representation(instance)

    assert result


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    min_rounds=1000,
    disable_gc=True,
    warmup=True
)
@pytest.mark.parametrize("number_of_objects", range(2, 100))
def test_object_list_serialization(number_of_objects, benchmark):
    instances_list = [RegularFieldsModel(**data) for _ in range(number_of_objects)]
    serializer = serializers.ListSerializer(child=TestSerializer(instance=instances_list))

    @benchmark
    def result():
        return serializer.to_representation(instances_list)

    gc.collect()  # explicitly garbage collect in order to reduce standard deviation

    assert result


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    min_rounds=100,
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_serialization(benchmark):
    nested_instance = RegularFieldsModel(**data)
    nested_instance.save()
    instance = RegularFieldsAndFKModel(fk=nested_instance, **data)
    serializer = TestNestedSerializer(instance=instance)

    @benchmark
    def result():
        return serializer.to_representation(instance)

    assert result


@pytest.mark.benchmark(
    group="ModelSerializer serialization",
    min_rounds=1000,
    disable_gc=True,
    warmup=True
)
@pytest.mark.parametrize("number_of_objects", range(2, 100))
def test_nested_object_list_serialization(number_of_objects, benchmark):
    nested_instance = RegularFieldsModel(**data)
    nested_instance.save()
    instances_list = [RegularFieldsAndFKModel(fk=nested_instance, **data) for _ in range(number_of_objects)]
    serializer = serializers.ListSerializer(child=TestSerializer(instance=instances_list))

    @benchmark
    def result():
        return serializer.to_representation(instances_list)

    gc.collect()  # explicitly garbage collect in order to reduce standard deviation

    assert result
