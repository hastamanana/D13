from django.urls import path
from .views import UserDetailView, UserEditView


urlpatterns = [
    path('profile', UserDetailView.as_view(), name='user_detail'),
    path('profile/edit', UserEditView.as_view(), name='user_edit')
]
