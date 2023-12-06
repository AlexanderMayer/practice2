from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views as auth_views
from .views import *

urlpatterns = [
    path('', auth_views.index, name='home'),
    path('login/', auth_views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:status>', profile, name='profile'),
    path('app_add/', CreateApplication.as_view(), name='app_add'),
    path('registration/', registration, name='registration'),
    path('delete/<int:request_id>', delete_request, name='delete_request'),
    path('profile/<str:status>', app_filter, name='app_filter'),
    path('app_list/', admin_app, name='app_list'),
    path('handle/<int:id>', AppAdminHandle.as_view(), name='handle'),
    path('category/', category_view, name="category"),
    path('catdelete/<int:id>', delete_category, name='delete_category'),
]
