from django.db import models
from drf_benchmarks.fields import CustomField


class RegularFieldsModel(models.Model):
    """
    A model class for testing regular flat fields.
    """
    auto_field = models.AutoField(primary_key=True)
    big_integer_field = models.BigIntegerField()
    boolean_field = models.BooleanField(default=False)
    char_field = models.CharField(max_length=100)
    comma_separated_integer_field = models.CommaSeparatedIntegerField(max_length=100)
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    decimal_field = models.DecimalField(max_digits=3, decimal_places=1)
    email_field = models.EmailField(max_length=100)
    float_field = models.FloatField()
    integer_field = models.IntegerField()
    null_boolean_field = models.NullBooleanField()
    positive_integer_field = models.PositiveIntegerField()
    positive_small_integer_field = models.PositiveSmallIntegerField()
    slug_field = models.SlugField(max_length=100)
    small_integer_field = models.SmallIntegerField()
    text_field = models.TextField()
    time_field = models.TimeField()
    url_field = models.URLField(max_length=100)

    def method(self):
        return 'method'


class RegularFieldsModel2(models.Model):
    """
    A model class for testing regular flat fields.
    """
    auto_field = models.AutoField(primary_key=True)
    big_integer_field = models.BigIntegerField()
    boolean_field = models.BooleanField(default=False)
    char_field = models.CharField(max_length=100)
    comma_separated_integer_field = models.CommaSeparatedIntegerField(max_length=100)
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    decimal_field = models.DecimalField(max_digits=3, decimal_places=1)
    email_field = models.EmailField(max_length=100)
    float_field = models.FloatField()
    integer_field = models.IntegerField()
    null_boolean_field = models.NullBooleanField()
    positive_integer_field = models.PositiveIntegerField()
    positive_small_integer_field = models.PositiveSmallIntegerField()
    slug_field = models.SlugField(max_length=100)
    small_integer_field = models.SmallIntegerField()
    text_field = models.TextField()
    time_field = models.TimeField()
    url_field = models.URLField(max_length=100)

    def method(self):
        return 'method'


class RegularFieldsAndFKModel(models.Model):
    """
    A model class for testing regular flat fields.
    """
    auto_field = models.AutoField(primary_key=True)
    big_integer_field = models.BigIntegerField()
    boolean_field = models.BooleanField(default=False)
    char_field = models.CharField(max_length=100)
    comma_separated_integer_field = models.CommaSeparatedIntegerField(max_length=100)
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    decimal_field = models.DecimalField(max_digits=3, decimal_places=1)
    email_field = models.EmailField(max_length=100)
    float_field = models.FloatField()
    integer_field = models.IntegerField()
    null_boolean_field = models.NullBooleanField()
    positive_integer_field = models.PositiveIntegerField()
    positive_small_integer_field = models.PositiveSmallIntegerField()
    slug_field = models.SlugField(max_length=100)
    small_integer_field = models.SmallIntegerField()
    text_field = models.TextField()
    time_field = models.TimeField()
    url_field = models.URLField(max_length=100)
    fk = models.ForeignKey(RegularFieldsModel)

    def method(self):
        return 'method'


class RegularFieldsAndFKModel2(models.Model):
    """
    A model class for testing regular flat fields.
    """
    auto_field = models.AutoField(primary_key=True)
    big_integer_field = models.BigIntegerField()
    boolean_field = models.BooleanField(default=False)
    char_field = models.CharField(max_length=100)
    comma_separated_integer_field = models.CommaSeparatedIntegerField(max_length=100)
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    decimal_field = models.DecimalField(max_digits=3, decimal_places=1)
    email_field = models.EmailField(max_length=100)
    float_field = models.FloatField()
    integer_field = models.IntegerField()
    null_boolean_field = models.NullBooleanField()
    positive_integer_field = models.PositiveIntegerField()
    positive_small_integer_field = models.PositiveSmallIntegerField()
    slug_field = models.SlugField(max_length=100)
    small_integer_field = models.SmallIntegerField()
    text_field = models.TextField()
    time_field = models.TimeField()
    url_field = models.URLField(max_length=100)
    fk = models.ForeignKey(RegularFieldsModel2)

    def method(self):
        return 'method'
