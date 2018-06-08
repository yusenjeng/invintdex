import control.helper as Helper
import control.crawler as Crawler
import control.initial_data_loader as InitialDataLoader

from django.http import HttpResponse
from django.template import loader
from control.models import Company, ETF
from control.serializers import CompanySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


taskManager = Helper.TaskManager()


@api_view(['GET'])
def company_list(req):
    if req.method == 'GET':
        coms = Company.objects.all()
        serializer = CompanySerializer(coms, many=True)
        return Response(serializer.data)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def test(req):
    if req.method == 'GET':
        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def upd_nasdaq_nyse_list(req):
    if req.method == 'GET':
        InitialDataLoader.loadNASDAQ_NYSE()
        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def upd_sp500_list(req):
    if req.method == 'GET':
        InitialDataLoader.loadSP500()
        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def import_etf(req):
    if req.method == 'GET':
        InitialDataLoader.loadETF()
        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def upd_ticker_price(req):
    if req.method == 'GET':
        ticker = req.GET['ticker'].upper()
        f = '2007-01-01'
        t = Helper.today()
        if 'f' in req.GET:
            f = req.GET['f']
        if 't' in req.GET:
            t = req.GET['t']

        taskManager.run(Crawler.pullTicker, (ticker, f, t))

        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def upd_etf_tickers(req):
    if req.method == 'GET':
        f = '2007-01-01'
        t = Helper.today()
        if 'f' in req.GET:
            f = req.GET['f']
        if 't' in req.GET:
            t = req.GET['t']

        tickers_etf = [c.ticker for c in ETF.objects.all()]
        taskManager.run(Crawler.pullAllTickers, (tickers_etf, f, t, True))

        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def upd_all_tickers(req):
    if req.method == 'GET':
        f = '2007-01-01'
        t = Helper.today()

        if 'f' in req.GET:
            f = req.GET['f']
        if 't' in req.GET:
            t = req.GET['t']

        tickerFrom = req.GET['tickerFrom'].upper()
        tickers_com = [
            c.ticker for c in Company.objects.all().order_by('ticker')
        ]
        taskManager.run(Crawler.pullAllTickers,
                        (tickers_com, f, t, False, tickerFrom))

        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def upd_ticker_financials(req):
    if req.method == 'GET':
        ticker = req.GET['ticker'].upper()
        taskManager.run(Crawler.MorningstarCrawler.pullFinancials, (ticker, ))
        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def upd_all_financials(req):
    if req.method == 'GET':
        tickerFrom = req.GET['tickerFrom'].upper()
        tickers = [
            c.ticker for c in Company.objects.all() if c.is_etf is False
        ]
        taskManager.run(Crawler.MorningstarCrawler.pullAllFinancials,
                        (tickers, tickerFrom))
        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def gen_ticker_list(req):
    if req.method == 'GET':

        coms = []
        for c in Company.objects.all():
            if c.is_etf is True:
                continue
            doc = {}
            doc['name'] = c.name + ' (' + c.ticker + ')'
            doc['comment'] = c.sector
            doc['ticker'] = c.ticker
            coms.append(doc)

        Helper.dumpjson(coms, 'ticker/static/ticker/ticker_list.json')

        return Response({'msg': 'ok'})
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


def index(req):
    template = loader.get_template('control/dashboard.html')
    context = {}
    return HttpResponse(template.render(context, req))
