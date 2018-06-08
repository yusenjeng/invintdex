from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'company', views.CompanyViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^test/', views.test),
    url(r'^tickers/$', views.company_list),
    url(r'^upd_sp500_list/$', views.upd_sp500_list),
    url(r'^upd_nasdaq_nyse_list/$', views.upd_nasdaq_nyse_list),
    url(r'^import_etf/$', views.import_etf),

    url(r'^upd_etf_tickers/$', views.upd_etf_tickers),
    url(r'^upd_ticker_price/$', views.upd_ticker_price),

    url(r'^upd_all_tickers/$', views.upd_all_tickers),
    url(r'^upd_ticker_financials/$', views.upd_ticker_financials),
    url(r'^upd_all_financials/$', views.upd_all_financials),
    url(r'^gen_ticker_list/$', views.gen_ticker_list),
    path('', views.index, name='index'),
]