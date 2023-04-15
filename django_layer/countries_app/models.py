from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    country = models.ForeignKey('Country', on_delete=models.PROTECT, verbose_name=_('country'), related_name='cities')
    longitude = models.FloatField(verbose_name=_('longitude'))
    latitude = models.FloatField(verbose_name=_('latitude'))
    is_capital = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')
        ordering = ['name']

    def __str__(self):
        return self.name


class Country(models.Model):
    iso_code = models.CharField(
        max_length=50, primary_key=True, verbose_name=_('ISO code'))
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))
    population = models.PositiveIntegerField(verbose_name=_('population'))
    area_size = models.PositiveIntegerField(verbose_name=_('area size'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        ordering = ['name']

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'), unique=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    country = models.ManyToManyField('Country', related_name='languages')

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')
        ordering = ['name']

    def __str__(self):
        return self.name


class Currency(models.Model):
    iso_code = models.CharField(
        max_length=30, primary_key=True, verbose_name=_('ISO code'))
    name = models.CharField(max_length=30, verbose_name=_('name'), unique=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    country = models.ManyToManyField('Country', related_name='currencies')

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')
        ordering = ['name']

    def __str__(self):
        return self.name
