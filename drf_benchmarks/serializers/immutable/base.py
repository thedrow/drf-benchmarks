#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields import FieldDoesNotExist
from django.utils import timezone
import rest_framework
from rest_framework.compat import OrderedDict
from django.db import models
from rest_framework.fields import HiddenField, empty, ChoiceField, ModelField, CharField, ReadOnlyField, \
    CreateOnlyDefault
from rest_framework.relations import HyperlinkedRelatedField, HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer
from rest_framework.settings import api_settings
from rest_framework.utils.field_mapping import get_field_kwargs, get_nested_relation_kwargs, get_relation_kwargs, \
    get_url_kwargs
from rest_framework.utils import model_meta

from drf_benchmarks.serializers.immutable.fields import *


class ImmutableModelSerializer(ImmutableFieldMixin, ModelSerializer):
    serializer_field_mapping = {
        models.AutoField: ImmutableIntegerField,
        models.BigIntegerField: ImmutableIntegerField,
        models.BooleanField: ImmutableBooleanField,
        models.CharField: ImmutableCharField,
        models.CommaSeparatedIntegerField: ImmutableCharField,
        models.DateField: ImmutableDateField,
        models.DateTimeField: ImmutableDateTimeField,
        models.DecimalField: ImmutableDecimalField,
        models.EmailField: ImmutableEmailField,
        models.FileField: ImmutableFileField,
        models.FloatField: ImmutableFloatField,
        models.ImageField: ImmutableImageField,
        models.IntegerField: ImmutableIntegerField,
        models.NullBooleanField: ImmutableNullBooleanField,
        models.PositiveIntegerField: ImmutableIntegerField,
        models.PositiveSmallIntegerField: ImmutableIntegerField,
        models.SlugField: ImmutableSlugField,
        models.SmallIntegerField: ImmutableIntegerField,
        models.TextField: ImmutableCharField,
        models.TimeField: ImmutableTimeField,
        models.URLField: ImmutableURLField,
        models.GenericIPAddressField: ImmutableIPAddressField,
        models.FilePathField: ImmutableFilePathField,
    }
    if rest_framework.VERSION.startswith("3.0"):
        def get_fields(self):
            declared_fields = self._declared_fields

            ret = OrderedDict()
            model = getattr(self.Meta, 'model')
            fields = getattr(self.Meta, 'fields', None)
            exclude = getattr(self.Meta, 'exclude', None)
            depth = getattr(self.Meta, 'depth', 0)
            extra_kwargs = getattr(self.Meta, 'extra_kwargs', {})

            assert not (fields and exclude), "Cannot set both 'fields' and 'exclude'."

            extra_kwargs = self._include_additional_options(extra_kwargs)

            # Retrieve metadata about fields & relationships on the model class.
            info = model_meta.get_field_info(model)

            # Use the default set of field names if none is supplied explicitly.
            if fields is None:
                fields = self._get_default_field_names(declared_fields, info)
                exclude = getattr(self.Meta, 'exclude', None)
                if exclude is not None:
                    for field_name in exclude:
                        fields.remove(field_name)

            # Determine the set of model fields, and the fields that they map to.
            # We actually only need this to deal with the slightly awkward case
            # of supporting `unique_for_date`/`unique_for_month`/`unique_for_year`.
            model_field_mapping = {}
            for field_name in fields:
                if field_name in declared_fields:
                    field = declared_fields[field_name]
                    source = field.source or field_name
                else:
                    try:
                        source = extra_kwargs[field_name]['source']
                    except KeyError:
                        source = field_name
                # Model fields will always have a simple source mapping,
                # they can't be nested attribute lookups.
                if '.' not in source and source != '*':
                    model_field_mapping[source] = field_name

            # Determine if we need any additional `HiddenField` or extra keyword
            # arguments to deal with `unique_for` dates that are required to
            # be in the input data in order to validate it.
            hidden_fields = {}
            unique_constraint_names = set()

            for model_field_name, field_name in model_field_mapping.items():
                try:
                    model_field = model._meta.get_field(model_field_name)
                except FieldDoesNotExist:
                    continue

                # Include each of the `unique_for_*` field names.
                unique_constraint_names |= set([
                    model_field.unique_for_date,
                    model_field.unique_for_month,
                    model_field.unique_for_year
                ])

            unique_constraint_names -= set([None])

            # Include each of the `unique_together` field names,
            # so long as all the field names are included on the serializer.
            for parent_class in [model] + list(model._meta.parents.keys()):
                for unique_together_list in parent_class._meta.unique_together:
                    if set(fields).issuperset(set(unique_together_list)):
                        unique_constraint_names |= set(unique_together_list)

            # Now we have all the field names that have uniqueness constraints
            # applied, we can add the extra 'required=...' or 'default=...'
            # arguments that are appropriate to these fields, or add a `HiddenField` for it.
            for unique_constraint_name in unique_constraint_names:
                # Get the model field that is refered too.
                unique_constraint_field = model._meta.get_field(unique_constraint_name)

                if getattr(unique_constraint_field, 'auto_now_add', None):
                    default = CreateOnlyDefault(timezone.now)
                elif getattr(unique_constraint_field, 'auto_now', None):
                    default = timezone.now
                elif unique_constraint_field.has_default():
                    default = unique_constraint_field.default
                else:
                    default = empty

                if unique_constraint_name in model_field_mapping:
                    # The corresponding field is present in the serializer
                    if unique_constraint_name not in extra_kwargs:
                        extra_kwargs[unique_constraint_name] = {}
                    if default is empty:
                        if 'required' not in extra_kwargs[unique_constraint_name]:
                            extra_kwargs[unique_constraint_name]['required'] = True
                    else:
                        if 'default' not in extra_kwargs[unique_constraint_name]:
                            extra_kwargs[unique_constraint_name]['default'] = default
                elif default is not empty:
                    # The corresponding field is not present in the,
                    # serializer. We have a default to use for it, so
                    # add in a hidden field that populates it.
                    hidden_fields[unique_constraint_name] = HiddenField(default=default)

            # Now determine the fields that should be included on the serializer.
            for field_name in fields:
                if field_name in declared_fields:
                    # Field is explicitly declared on the class, use that.
                    ret[field_name] = declared_fields[field_name]
                    continue

                elif field_name in info.fields_and_pk:
                    # Create regular model fields.
                    model_field = info.fields_and_pk[field_name]
                    field_cls = self._field_mapping[model_field]
                    kwargs = get_field_kwargs(field_name, model_field)
                    if 'choices' in kwargs:
                        # Fields with choices get coerced into `ChoiceField`
                        # instead of using their regular typed field.
                        field_cls = ChoiceField
                    if not issubclass(field_cls, ModelField):
                        # `model_field` is only valid for the fallback case of
                        # `ModelField`, which is used when no other typed field
                        # matched to the model field.
                        kwargs.pop('model_field', None)
                    if not issubclass(field_cls, CharField):
                        # `allow_blank` is only valid for textual fields.
                        kwargs.pop('allow_blank', None)

                elif field_name in info.relations:
                    # Create forward and reverse relationships.
                    relation_info = info.relations[field_name]
                    if depth:
                        field_cls = self._get_nested_class(depth, relation_info)
                        kwargs = get_nested_relation_kwargs(relation_info)
                    else:
                        field_cls = self._related_class
                        kwargs = get_relation_kwargs(field_name, relation_info)
                        # `view_name` is only valid for hyperlinked relationships.
                        if not issubclass(field_cls, HyperlinkedRelatedField):
                            kwargs.pop('view_name', None)

                elif hasattr(model, field_name):
                    # Create a read only field for model methods and properties.
                    field_cls = ReadOnlyField
                    kwargs = {}

                elif field_name == api_settings.URL_FIELD_NAME:
                    # Create the URL field.
                    field_cls = HyperlinkedIdentityField
                    kwargs = get_url_kwargs(model)

                else:
                    raise ImproperlyConfigured(
                        'Field name `%s` is not valid for model `%s`.' %
                        (field_name, model.__class__.__name__)
                    )

                # Check that any fields declared on the class are
                # also explicity included in `Meta.fields`.
                missing_fields = set(declared_fields.keys()) - set(fields)
                if missing_fields:
                    missing_field = list(missing_fields)[0]
                    raise ImproperlyConfigured(
                        'Field `%s` has been declared on serializer `%s`, but '
                        'is missing from `Meta.fields`.' %
                        (missing_field, self.__class__.__name__)
                    )

                # Populate any kwargs defined in `Meta.extra_kwargs`
                extras = extra_kwargs.get(field_name, {})
                if extras.get('read_only', False):
                    for attr in [
                        'required', 'default', 'allow_blank', 'allow_null',
                        'min_length', 'max_length', 'min_value', 'max_value',
                        'validators', 'queryset'
                    ]:
                        kwargs.pop(attr, None)

                if extras.get('default') and kwargs.get('required') is False:
                    kwargs.pop('required')

                kwargs.update(extras)

                # Create the serializer field.
                ret[field_name] = field_cls(**kwargs)

            for field_name, field in hidden_fields.items():
                ret[field_name] = field

            return ret
    else:
        def get_fields(self):
            """
            Return the dict of field names -> field instances that should be
            used for `self.fields` when instantiating the serializer.
            """
            assert hasattr(self, 'Meta'), (
                'Class {serializer_class} missing "Meta" attribute'.format(
                    serializer_class=self.__class__.__name__
                )
            )
            assert hasattr(self.Meta, 'model'), (
                'Class {serializer_class} missing "Meta.model" attribute'.format(
                    serializer_class=self.__class__.__name__
                )
            )
            if model_meta.is_abstract_model(self.Meta.model):
                raise ValueError(
                    'Cannot use ModelSerializer with Abstract Models.'
                )

            declared_fields = self._declared_fields
            model = getattr(self.Meta, 'model')
            depth = getattr(self.Meta, 'depth', 0)

            if depth is not None:
                assert depth >= 0, "'depth' may not be negative."
                assert depth <= 10, "'depth' may not be greater than 10."

            # Retrieve metadata about fields & relationships on the model class.
            info = model_meta.get_field_info(model)
            field_names = self.get_field_names(declared_fields, info)

            # Determine any extra field arguments and hidden fields that
            # should be included
            extra_kwargs = self.get_extra_kwargs()
            extra_kwargs, hidden_fields = self.get_uniqueness_extra_kwargs(
                field_names, declared_fields, extra_kwargs
            )

            # Determine the fields that should be included on the serializer.
            fields = OrderedDict()

            for field_name in field_names:
                # If the field is explicitly declared on the class then use that.
                if field_name in declared_fields:
                    fields[field_name] = declared_fields[field_name]
                    continue

                # Determine the serializer field class and keyword arguments.
                field_class, field_kwargs = self.build_field(
                    field_name, info, model, depth
                )

                # Include any kwargs defined in `Meta.extra_kwargs`
                extra_field_kwargs = extra_kwargs.get(field_name, {})
                field_kwargs = self.include_extra_kwargs(
                    field_kwargs, extra_field_kwargs
                )

                # Create the serializer field.
                fields[field_name] = field_class(**field_kwargs)

            # Add in any hidden fields.
            fields.update(hidden_fields)

            return fields
