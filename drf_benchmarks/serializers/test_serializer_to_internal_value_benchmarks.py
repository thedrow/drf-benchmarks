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
    group="ModelSerializer deserialization",
    min_rounds=100,
    max_time=120,
    warmup=True
)
@pytest.mark.django_db
def test_object_deserialization(benchmark):
    serializer = TestSerializer(data=data)

    @benchmark
    def result():
        return serializer.to_internal_value(data)

    assert result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    min_rounds=1000,
    disable_gc=True,
    max_time=120,
    warmup=True
)
@pytest.mark.parametrize("number_of_objects", range(2, 100))
def test_object_list_deserialization(number_of_objects, benchmark):
    data_list = [data for _ in range(number_of_objects)]
    serializer = serializers.ListSerializer(child=TestSerializer(), data=data_list)

    @benchmark
    def result():
        return serializer.to_internal_value(data_list)

    gc.collect()  # explicitly garbage collect in order to reduce standard deviation

    assert result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    min_rounds=100,
    max_time=120,
    warmup=True
)
@pytest.mark.django_db
def test_nested_object_deserialization(benchmark):
    serializer = TestNestedSerializer(data=nested_data)

    @benchmark
    def result():
        return serializer.to_representation(nested_data)

    assert result and serializer.is_valid(), serializer.errors


@pytest.mark.benchmark(
    group="ModelSerializer deserialization",
    min_rounds=1000,
    disable_gc=True,
    max_time=120,
    warmup=True
)
@pytest.mark.parametrize("number_of_objects", range(2, 100))
@pytest.mark.django_db
def test_nested_object_list_deserialization(number_of_objects, benchmark):
    data_list_with_nesting = [nested_data for _ in range(number_of_objects)]
    serializer = serializers.ListSerializer(child=TestNestedSerializer(), data=data_list_with_nesting)

    @benchmark
    def result():
        return serializer.to_representation(data_list_with_nesting)

    gc.collect()  # explicitly garbage collect in order to reduce standard deviation

    assert result and serializer.is_valid(), serializer.errors
