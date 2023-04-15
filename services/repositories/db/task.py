from itertools import chain

from django_layer.countries_app.models import City, Country


class TaskDBRepository:

    def merge_models(self):
        query_sets = []
        query_sets.append(City.objects.all())
        query_sets.append(Country.objects.all())
        final_set = list(chain(*query_sets))
        final_set.sort(key=lambda obj: obj.updated_at)
        return final_set
