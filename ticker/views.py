from . import api
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.shortcuts import render
from control import helper as Helper
from control import crawler as Crawler
from control.models import Company, ETF, SP500, Quote, ETFQuote, IS, BS, CF
from datetime import datetime, date, timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

taskManager = Helper.TaskManager()


@api_view(['GET'])
def get_quote(req, ticker):
    ticker = ticker.upper()
    if req.method == 'GET':
        com = Company.objects.get(ticker=ticker)
        f = '2007-01-01'
        t = Helper.today()

        if not com.is_filled:
            Crawler.pullTicker(ticker, f, t)
            com.is_filled = True
            com.save()

        quotes = com.quote_set.filter(date__range=[f, t]).order_by('date')

        # data example:
        # [ [js datatime, open, high, low, close], ]
        # [ [1299110400000,51.03,51.40,50.85,51.37], ]
        data = []
        for q in quotes:
            date = Helper.tojstime(q.date)
            r = [date, q.open, q.high, q.low, q.close]
            data.append(r)

        last_q = quotes.last()

        ctx = {
            'ticker': ticker,
            'data': data,
            'last_close': last_q.close,
            'last_change': last_q.change,
            'last_date': last_q.date
        }
        return Response(ctx)

    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_financials(req, ticker):
    ticker = ticker.upper()
    if req.method == 'GET':
        fis = IS.objects.filter(ticker=ticker).order_by('date')
        fbs = BS.objects.filter(ticker=ticker).order_by('date')
        fcf = CF.objects.filter(ticker=ticker).order_by('date')

        ctx = {
            'ticker': ticker,
            'date': [],
            'revenue': [],
            'eps_diluted': [],
            'receivables': [],
            'inventories': [],
            'payables': [],
            'long_term_debt': [],
            'short_term_debt': [],
            'total_assets': [],
            'operating_cf': [],
            'investing_cf': [],
            'financing_cf': [],
            'fcf': [],
            'cogs': [],
            'op_income': [],
            'net_income': [],
        }
        for data in fis:
            ctx['date'].append(str(data.date))
            ctx['revenue'].append(data.revenue)
            ctx['eps_diluted'].append(data.eps_diluted)
            ctx['cogs'].append(data.cogs)
            ctx['op_income'].append(data.op_income)
            ctx['net_income'].append(data.net_income)

        for data in fbs:
            ctx['receivables'].append(data.receivables)
            ctx['inventories'].append(data.inventories)
            ctx['payables'].append(data.payables)
            ctx['long_term_debt'].append(data.long_term_debt)
            ctx['short_term_debt'].append(data.short_term_debt)
            ctx['total_assets'].append(data.total_assets)

        for data in fcf:
            ctx['operating_cf'].append(data.operating_cf)
            ctx['investing_cf'].append(data.investing_cf)
            ctx['financing_cf'].append(data.financing_cf)
            ctx['fcf'].append(data.fcf)

        return Response(ctx)

    return Response({}, status=status.HTTP_400_BAD_REQUEST)


#
# Pages
#
def index(req, ticker):
    ticker = ticker.upper()
    try:
        com = Company.objects.get(ticker=ticker)
    except ObjectDoesNotExist:
        return HttpResponse({}, status=status.HTTP_404_NOT_FOUND)

    context = {'ticker': ticker, 'name': com.name}
    template = loader.get_template('ticker/ticker.html')
    return HttpResponse(template.render(context, req))


def entrance(req):
    context = {}
    template = loader.get_template('ticker/entrance.html')
    return HttpResponse(template.render(context, req))


def markets(req):

    days = 365 * 10
    t = date.today()
    f = t - timedelta(days=days)

    # Treasury Bonds
    # 'TLT', 'IEF', 'SHY'
    tbonds = api.generateTBondsReturns('TLT', f, t)

    # Emerging/Developed Markets
    # 'EFA', 'EEM'
    emdev = api.generateEmDevReturns('EEM', f, t)

    days = 365 * 5
    t = date.today()
    f = t - timedelta(days=days)

    # Corporate Bonds
    # 'LQD', 'HYG'
    cbonds = api.generateCBondsReturns('HYG', f, t)

    context = {'tbonds': tbonds, 'emdev': emdev, 'cbonds': cbonds}

    template = loader.get_template('ticker/markets.html')
    return HttpResponse(template.render(context, req))
