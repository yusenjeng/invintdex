from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [

    # url(r'^<str:ticker>/get_quote/$', views.get_quote),

    path('<str:ticker>', views.index, name='index'),
    path('markets/', views.markets, name='markets'),
    path('<str:ticker>/get_quote/', views.get_quote, name='get_quote'),
    path('<str:ticker>/get_financials/', views.get_financials, name='get_financials'),
]