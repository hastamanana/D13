from django.urls import path
from .views import (AdList, MyAdList, AdDetailView, AdCreateView, AdEditView, AdDeleteView, OfferListView, OfferDeleteView)


urlpatterns = [
    path('', AdList.as_view(), name='ads_list'),
    path('my-ads', MyAdList.as_view(), name='my_ads'),
    path('<int:pk>', AdDetailView.as_view(), name='ad_detail'),
    path('create/', AdCreateView.as_view(), name='ad_create'),
    path('update/<int:pk>/', AdEditView.as_view(), name='ad_edit'),
    path('delete/<int:pk>/', AdDeleteView.as_view(), name='ad_delete'),
    path('offers', OfferListView.as_view(), name='offers'),
    path('offers/accept/<int:pk>', OfferListView.accept, name='offer_accept'),
    path('offers/delete/<int:pk>', OfferDeleteView.as_view(), name='offer_delete'),
]
