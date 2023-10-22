from django.shortcuts import render

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

from .models import Ad, Offer
from .forms import AdForm, OfferForm
from .filters import OfferFilter

# Create your views here.


class AdList(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-posted']
    paginate_by = 10


class MyAdList(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-posted']

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user)


class AdDetailView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'ads/ad_detail.html'
    queryset = Ad.objects.all()
    form_class = OfferForm

    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(AdDetailView, self).get_context_data(**kwargs)
        context['offers'] = Offer.objects.filter(ad=self.object)
        context['form'] = OfferForm(
            {'user': self.request.user, 'ad': self.object}
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        send_mail(
            subject='На Ваше объявление откликнулись!',
            message=f'На Ваше объявление откликнулся пользователь {self.request.user}!',
            from_email=None,
            recipient_list=[self.object.author.email]
        )
        return super(AdDetailView, self).form_valid(form)


class AdCreateView(LoginRequiredMixin, CreateView):
    template_name = 'ads/ad_create.html'
    form_class = AdForm
    success_url = reverse_lazy('ads_list')

    def get_context_data(self, **kwargs):
        context = super(AdCreateView, self).get_context_data(**kwargs)
        context['form'] = AdForm(
            {'author': self.request.user}
        )
        return context


class AdEditView(LoginRequiredMixin, UpdateView):
    template_name = 'ads/ad_create.html'
    form_class = AdForm
    success_url = reverse_lazy('ads_list')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        ad = self.get_object()
        if not (ad.author == user or user.is_superuser):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AdDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'ads/ad_delete.html'
    queryset = Ad.objects.all()
    success_url = reverse_lazy('ads_list')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        ad = self.get_object()
        if not (ad.author == user or user.is_superuser):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class OfferListView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'ads/offers.html'
    context_object_name = 'offers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = OfferFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

    def get_queryset(self):
        context = Offer.objects.filter(ad__author=self.request.user)
        return context

    def accept(request, pk):
        offer = Offer.objects.get(pk=pk)
        offer.is_accepted = not offer.is_accepted
        offer.save()

        send_mail(
            subject='Ваш отклик принят!',
            message='Ваш отклик принят!',
            from_email=None,
            recipient_list=[offer.user.email]
        )

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class OfferDeleteView(LoginRequiredMixin, DeleteView):
    model = Offer
    success_url = reverse_lazy('offers')

