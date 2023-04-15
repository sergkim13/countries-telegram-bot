from django.contrib import admin

from django_layer.countries_app.models import City, Country, Currency, Language


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """
    City model class for django admin site
    """
    list_display = ('id', 'name', 'is_capital', 'country', 'longitude', 'latitude', 'updated_at')
    search_fields = ['name', 'country__name']
    list_filter = (
        ('country', admin.RelatedOnlyFieldListFilter),
        ('updated_at', admin.DateFieldListFilter),
        ('is_capital', admin.BooleanFieldListFilter),
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """
    Country model class for django admin site
    """
    list_display = ('iso_code', 'name', 'population', 'area_size', 'updated_at')
    search_fields = ['iso_code', 'name']
    list_filter = (('updated_at', admin.DateFieldListFilter),)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """
    Language model class for django admin site
    """
    list_display = ('id', 'name', 'countries', 'updated_at')
    search_fields = ['name', 'country__name']
    list_filter = (
        ('country', admin.RelatedOnlyFieldListFilter),
        ('updated_at', admin.DateFieldListFilter),
    )

    def countries(self, obj: Language):
        """
        Method for `ManyToMany` related countries display in `list_display`

        :return: list of related country entities
        """
        return [c.name for c in obj.country.all()]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """
    Currency model class for django admin site
    """
    list_display = ('iso_code', 'name', 'countries', 'updated_at')
    search_fields = ['iso_code', 'name', 'country__name']
    list_filter = (
        ('country', admin.RelatedOnlyFieldListFilter),
        ('updated_at', admin.DateFieldListFilter),
    )

    def countries(self, obj: Currency):
        """
        Method for `ManyToMany` related countries display in `list_display`

        :return: list of related country entities
        """
        return [c.name for c in obj.country.all()]
