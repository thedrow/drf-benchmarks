#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers


class ImmutableFieldMixin(object):
    def __init__(self, *args, **kwargs):
        self.is_bound = False
        super(ImmutableFieldMixin, self).__init__(*args, **kwargs)

    def bind(self, field_name, parent):
        if self.is_bound:
            return
        super(ImmutableFieldMixin, self).bind(field_name, parent)
        self.is_bound = True


class ImmutableIntegerField(ImmutableFieldMixin, serializers.IntegerField):
    pass


class ImmutableCharField(ImmutableFieldMixin, serializers.CharField):
    pass


class ImmutableDateField(ImmutableFieldMixin, serializers.DateField):
    pass


class ImmutableDateTimeField(ImmutableFieldMixin, serializers.DateTimeField):
    pass


class ImmutableDecimalField(ImmutableFieldMixin, serializers.DecimalField):
    pass


class ImmutableEmailField(ImmutableFieldMixin, serializers.EmailField):
    pass


class ImmutableFileField(ImmutableFieldMixin, serializers.FileField):
    pass


class ImmutableFloatField(ImmutableFieldMixin, serializers.FloatField):
    pass


class ImmutableImageField(ImmutableFieldMixin, serializers.ImageField):
    pass


class ImmutableBooleanField(ImmutableFieldMixin, serializers.BooleanField):
    pass


class ImmutableNullBooleanField(ImmutableFieldMixin, serializers.NullBooleanField):
    pass


class ImmutableSlugField(ImmutableFieldMixin, serializers.SlugField):
    pass


class ImmutableTimeField(ImmutableFieldMixin, serializers.TimeField):
    pass


class ImmutableURLField(ImmutableFieldMixin, serializers.URLField):
    pass


try:
    class ImmutableIPAddressField(ImmutableFieldMixin, serializers.IPAddressField):
        pass
except AttributeError:
    class ImmutableIPAddressField(ImmutableFieldMixin, serializers.CharField):
        pass

try:
    class ImmutableFilePathField(ImmutableFieldMixin, serializers.FilePathField):
        pass
except AttributeError:
    class ImmutableFilePathField(ImmutableFieldMixin, serializers.CharField):
        pass
