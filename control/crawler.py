import io
import os
import csv
import time
import pandas
import platform
import threading
import urllib.request
import fix_yahoo_finance as yf
import pandas_datareader
import pandas_datareader.data as web

from pprint import pprint
from control import helper as Helper
from control.models import Company, ETF, SP500, Quote, ETFQuote, IS, BS, CF
from control.AccountingDict import DictIS, DictBS, DictCF

# Enable the fix
yf.pdr_override()


def pullAllTickers(tickers, f, t, isETF=False, ticker_from=''):
    toSkip = ticker_from != ''
    print('pullAllTickers ticker_from=', ticker_from)

    first_fail_idx = -1

    fail_count = 0
    i = 0
    while i < len(tickers):
        ticker = tickers[i]
        if toSkip is True:
            if ticker != ticker_from:
                i += 1
                continue
            else:
                toSkip = False

        size = pullTicker(ticker, f, t, isETF)
        print(i + 1, '/', len(tickers), 'is done')

        if size < 3:
            fail_count += 1
            if fail_count == 1:
                first_fail_idx = i
        else:
            fail_count = 0
            first_fail_idx = -1
            # time.sleep(1)

        i += 1

        if fail_count > 20:
            i = first_fail_idx
            fail_count = 0
            first_fail_idx = -1
            print('Sleep 2 minutes...')
            time.sleep(60 * 2)

    pass


def pullTicker(ticker, f, t, isETF=False):
    df = yf.download(ticker, start=f, end=t, auto_adjust=True)
    print('[pullTickerYahoo]', ticker, f, t, ' size=', len(df.index))
    last_close = None
    for i in df.index:
        Date = Helper.todate(i)
        Close = float(df['Close'][i])
        High = float(df['High'][i])
        Low = float(df['Low'][i])
        Open = float(df['Open'][i])
        Volume = int(df['Volume'][i])
        if Volume < 1 or Close < 1:
            continue

        if isETF:
            doc, created = ETFQuote.objects.get_or_create(
                ticker_id=ticker, date=Date)
        else:
            doc, created = Quote.objects.get_or_create(
                ticker_id=ticker, date=Date)

        doc.open = Open
        doc.high = High
        doc.low = Low
        doc.close = Close
        doc.adjclose = Close
        doc.volume = Volume

        if last_close is not None:
            change = ((Close / last_close) - 1) * 100
            doc.change = change  # as %

        doc.save()
        last_close = Close
    return len(df.index)


def pullTickerMorningstar(ticker, f, t):
    print('[pullTickerMorningstar]', ticker, f, t, ':)')
    df = web.DataReader(ticker, 'morningstar', f, t)
    last_close = None
    for i in df.index:
        Date = Helper.todate(i[1])
        Close = float(df['Close'][i])
        High = float(df['High'][i])
        Low = float(df['Low'][i])
        Open = float(df['Open'][i])
        Volume = int(df['Volume'][i])
        if Volume < 1:
            continue

        doc, created = Quote.objects.get_or_create(ticker_id=ticker, date=Date)
        doc.open = Open
        doc.high = High
        doc.low = Low
        doc.close = Close
        doc.adjclose = Close
        doc.volume = Volume

        if last_close is not None:
            change = ((Close / last_close) - 1) * 100
            doc.change = change  # as %

        doc.save()
        last_close = Close
    pass


# Deprecated:
# Google Finance as data source is not that reliable
def pullTickerGoogle(ticker, f, t):
    print('[pullTicker]', ticker, f, t, ':)')
    try:
        df = web.DataReader(ticker, 'google', f, t)
    except:
        return pullTickerMorningstar(ticker, f, t)

    last_close = None
    for i in df.index:
        Date = Helper.todate(i)
        Close = float(df['Close'][i])
        High = float(df['High'][i])
        Low = float(df['Low'][i])
        Open = float(df['Open'][i])
        Volume = int(df['Volume'][i])

        if Volume < 1:
            continue

        doc, created = Quote.objects.get_or_create(ticker_id=ticker, date=Date)
        doc.open = Open
        doc.high = High
        doc.low = Low
        doc.close = Close
        doc.adjclose = Close
        doc.volume = Volume

        if last_close is not None:
            change = ((Close / last_close) - 1) * 100
            doc.change = change  # as %

        doc.save()
        last_close = Close
    pass


#
# download financial data from morningstar
#
class MorningstarCrawler():
    def __init__():
        pass

    @staticmethod
    def pullAllFinancials(tickers, fromTicker):
        toSkip = fromTicker != ''
        for t in tickers:
            if toSkip is True:
                if t != fromTicker:
                    continue
                else:
                    t = fromTicker
                    toSkip = False

            print("[pullAllFinancials]", t)
            MorningstarCrawler.pullFinancials(t)
            time.sleep(60)
        pass

    @staticmethod
    def pullFinancials(ticker):
        print('pullFinancialData', ticker)
        cols = MorningstarCrawler.query(ticker, 'is')
        rows = MorningstarCrawler.transpose(cols)
        ISs = MorningstarCrawler.toIS(rows)

        try:
            for data in ISs:
                if 'date' not in data:
                    continue
                doc, created = IS.objects.get_or_create(
                    ticker_id=ticker, date=data['date'])
                Helper.assign(data, doc)
                doc.save()
        except Exception as e:
            print('Pulling IS fail,', ticker, e)

        cols = MorningstarCrawler.query(ticker, 'bs')
        rows = MorningstarCrawler.transpose(cols)
        BSs = MorningstarCrawler.toBS(rows)
        try:
            for data in BSs:
                if 'date' not in data:
                    continue

                doc, created = BS.objects.get_or_create(
                    ticker_id=ticker, date=data['date'])
                Helper.assign(data, doc)
                doc.save()
        except Exception as e:
            print('Pulling BS fail,', ticker, e)

        cols = MorningstarCrawler.query(ticker, 'cf')
        rows = MorningstarCrawler.transpose(cols)
        CFs = MorningstarCrawler.toCF(rows)
        try:
            for data in CFs:
                if 'date' not in data:
                    continue
                doc, created = CF.objects.get_or_create(
                    ticker_id=ticker, date=data['date'])
                Helper.assign(data, doc)
                doc.save()
        except Exception as e:
            print('Pulling CF fail,', ticker, e)

    def query(ticker='AAPL', report_type='is'):
        s = 'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?period=3&dataType=A&order=asc&columnYear=10&number=3&t=' + ticker + '&reportType=' + report_type
        fp = urllib.request.urlopen(s)

        cols = {}

        s = fp.read().decode("utf8")
        reader = csv.DictReader(io.StringIO(s))
        for line in reader:
            k, values = line.popitem()
            try:
                k2, fieldname = line.popitem()
            except KeyError:
                continue

            # Hack:
            # morningstar's data format could be inconsistent.
            if isinstance(values, str):
                fieldname, values = values, fieldname

            if Helper.hasNumbers(fieldname):
                continue
            if fieldname == '':
                continue
            if values is None:
                continue

            if isinstance(values, list) is True:
                if fieldname.startswith('Fiscal year ends'):
                    cols['Date'] = values[:5]
                elif fieldname not in cols:
                    cols[fieldname] = values[:5]
            else:
                if fieldname.startswith('Fiscal year ends'):
                    cols['Date'] = [values]
                elif fieldname not in cols:
                    cols[fieldname] = [values]

        fp.close()
        return cols

    def transpose(cols):
        if 'Date' not in cols:
            w = 0
        else:
            w = len(cols['Date'])

        rows = []
        for i in range(w):
            r = {}
            for k in cols:
                r[k] = cols[k][i]
            rows.append(r)
        return rows

    def toIS(rows):
        docs = []
        for r in rows:
            doc = {
                'revenue': 0,
                'cogs': 0,
                'rd': 0,
                'sgna': 0,
                'op_expenses': 0,
                'op_income': 0,
                'interest_expense': 0,
                'ebit': 0,
                'net_income': 0,
                'eps': 0,
                'eps_diluted': 0
            }

            for k in r:
                if k == 'Date':
                    doc['date'] = r['Date'] + "-01"
                elif k in DictIS:
                    doc[DictIS[k]] = Helper.toFloat(r[k])

            docs.append(doc)
        return docs

    def toBS(rows):
        docs = []
        for r in rows:
            doc = {
                'cash': 0,
                'inventories': 0,
                'receivables': 0,
                'payables': 0,
                'ppne': 0,
                'goodwill': 0,
                'total_assets': 0,
                'long_term_debt': 0,
                'short_term_debt': 0,
                'total_liabilities': 0,
                'total_equity': 0
            }

            for k in r:
                if k == 'Date':
                    doc['date'] = r['Date'] + "-01"
                elif k in DictBS:
                    doc[DictBS[k]] = Helper.toFloat(r[k])

            docs.append(doc)
        return docs

    def toCF(rows):
        docs = []
        for r in rows:
            doc = {
                'net_income': 0,
                'depreciation_amortization': 0,
                'operating_cf': 0,
                'investing_cf': 0,
                'financing_cf': 0,
                'fcf': 0,
                'net_change_cash': 0,
                'capex': 0
            }

            for k in r:
                if k == 'Date':
                    doc['date'] = r['Date'] + "-01"
                elif k in DictCF:
                    doc[DictCF[k]] = Helper.toFloat(r[k])

            docs.append(doc)
        return docs

    pass


#
# Periodic Tasks
#
TM_UPDATE_QUOTES = 60 * 60 * 8
taskManager = Helper.TaskManager()


def foo():
    threading.Timer(TM_UPDATE_QUOTES, foo).start()
    f = Helper.lastweek()
    t = Helper.today()
    tickers = [c.ticker for c in Company.objects.all()]
    taskManager.run(pullAllTickers, (tickers, f, t))
