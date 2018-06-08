from control import helper as Helper
from control.models import Quote, ETFQuote


def generateTBondsReturns(target, f, t):
    tickers = ['TLT', 'IEF', 'SHY']
    title1, series1, dates = generateReturnsSeries(tickers, f, t, True)
    stream1 = Helper.toCsvString(title1, dates, series1)

    quotes = ETFQuote.objects.filter(
        ticker=target, date__range=[f, t]).order_by('date')

    title2 = ['Date', target]
    series2 = [[q.close for q in quotes]]
    stream2 = Helper.toCsvString(title2, dates, series2)

    return {
        'title': 'Comparison of US Bonds',
        'subtitle': '',
        'subtitle': title1,
        'subtitle2': title2,
        'yLabel': 'Returns %',
        'yLabel2': target,
        'data1': stream1.getvalue(),
        'data2': stream2.getvalue(),
        'signals': [],
        'annotation': 'B',
        'from': dates[0],
        'to': dates[-1],
        'range': 0
    }


def generateEmDevReturns(target, f, t):
    tickers = ['EEM', 'EFA']
    title1, series1, dates = generateReturnsSeries(tickers, f, t, True)
    stream1 = Helper.toCsvString(title1, dates, series1)

    quotes = ETFQuote.objects.filter(
        ticker=target, date__range=[f, t]).order_by('date')

    title2 = ['Date', target]
    series2 = [[q.close for q in quotes]]
    stream2 = Helper.toCsvString(title2, dates, series2)

    return {
        'title': 'Comparison of Emerging/Developed Market',
        'subtitle': '',
        'subtitle': title1,
        'subtitle2': title2,
        'yLabel': 'Returns %',
        'yLabel2': target,
        'data1': stream1.getvalue(),
        'data2': stream2.getvalue(),
        'signals': [],
        'annotation': 'B',
        'from': dates[0],
        'to': dates[-1],
        'range': 0
    }


def generateCBondsReturns(target, f, t):
    tickers = ['HYG', 'LQD']
    title1, series1, dates = generateReturnsSeries(tickers, f, t, True)
    stream1 = Helper.toCsvString(title1, dates, series1)

    quotes = ETFQuote.objects.filter(
        ticker=target, date__range=[f, t]).order_by('date')

    title2 = ['Date', target]
    series2 = [[q.close for q in quotes]]
    stream2 = Helper.toCsvString(title2, dates, series2)

    return {
        'title': 'Comparison of Corporate Bonds',
        'subtitle': '',
        'subtitle': title1,
        'subtitle2': title2,
        'yLabel': 'Returns %',
        'yLabel2': target,
        'data1': stream1.getvalue(),
        'data2': stream2.getvalue(),
        'signals': [],
        'annotation': 'B',
        'from': dates[0],
        'to': dates[-1],
        'range': 0
    }


def generateReturnsSeries(tickers, f, t, isETF=False):
    titles = ['Date']
    series = []
    dates = []
    for ticker in tickers:
        titles.append(ticker)

        if isETF:
            quotes = ETFQuote.objects.filter(
                ticker=ticker, date__range=[f, t]).order_by('date')
        else:
            quotes = Quote.objects.filter(
                ticker=ticker, date__range=[f, t]).order_by('date')

        first = quotes[0].adjclose
        s = [(q.adjclose / first) * 100 for q in quotes]
        series.append(s)

        if len(dates) == 0:
            dates = [q.date for q in quotes]

    return titles, series, dates