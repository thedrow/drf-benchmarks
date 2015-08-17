#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal

import pytest

from drf_benchmarks.models import RegularFieldsModel, RegularFieldsAndFKModel
from drf_benchmarks.serializers import serializer_ids, serializers_to_test, nested_serializers_to_test, \
    nested_serializer_ids


@pytest.fixture(scope='session')
def data():
    return {
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


@pytest.fixture(scope='session')
def nested_data(data):
    return {
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


@pytest.fixture(scope='session', params=range(1, 10), ids=[' %d objects' if n > 1 else ' %d object' % n for n in range(1, 10)])
def number_of_objects(request):
    return request.param


@pytest.fixture(scope='session')
def data_list(number_of_objects, data):
    return [data for _ in range(number_of_objects)]


@pytest.fixture(scope='session')
def data_list_with_nesting(number_of_objects, data):
    return [data for _ in range(number_of_objects)]


@pytest.fixture(params=serializers_to_test, ids=serializer_ids)
def serializer(request):
    return request.param


@pytest.fixture(params=nested_serializers_to_test, ids=nested_serializer_ids)
def nested_serializer(request):
    return request.param


@pytest.fixture(scope='session')
def instance(data):
    return RegularFieldsModel.objects.create(**data)


@pytest.fixture(scope='session')
def instances_list(data_list):
    return RegularFieldsModel.objects.bulk_create([RegularFieldsModel(**d) for d in data_list])


@pytest.fixture(scope='session')
def nested_instance(instance, data):
    return RegularFieldsAndFKModel.objects.create(fk=instance, **data)


@pytest.fixture(scope='session')
def nested_instances_list(data_list, instance):
    return RegularFieldsAndFKModel.objects.bulk_create([RegularFieldsAndFKModel(fk=instance, **d) for d in data_list])
