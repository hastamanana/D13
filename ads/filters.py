from django_filters import FilterSet, CharFilter
from django.db.models import Q
from .models import Offer


class OfferFilter(FilterSet):
    search_by_ad = CharFilter(method='search_content_and_title', label='')

    class Meta:
        model = Offer
        fields = ['search_by_ad']

    def search_content_and_title(self, queryset, name, value):
        return Offer.objects.filter(
            Q(ad__title__icontains=value) | Q(ad__content__icontains=value)
        )
