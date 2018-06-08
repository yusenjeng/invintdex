import csv
import pandas
import pandas_datareader
import pandas_datareader.data as web

from control.models import Company, ETF, SP500, Quote, ETFQuote, IS, BS, CF


def loadETF():
    print('[listETF]', 'loading ETF')
    with open('data/TICKER_ETF.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] == 'Symbol':
                continue
            doc, created = ETF.objects.get_or_create(ticker=row[0])
            doc.name = row[1]
            doc.tag = row[2]
            doc.save()
            print(doc)


def loadNASDAQ_NYSE():
    print('[listNASDAQ_NYSE]', 'loading NASDAQ')
    with open('data/TICKER_NASDAQ.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] == 'Symbol':
                continue
            doc, created = Company.objects.get_or_create(ticker=row[0])
            doc.name = row[1]
            doc.sector = row[6]
            doc.industry = row[7]
            doc.ipoyear = row[5]
            doc.exchange = 'NASDAQ'
            doc.summary = row[8]
            doc.save()

    print('[listNASDAQ_NYSE]', 'loading NYSE')
    with open('data/TICKER_NYSE.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] == 'Symbol':
                continue
            doc, created = Company.objects.get_or_create(ticker=row[0])
            doc.name = row[1]
            doc.sector = row[5]
            doc.industry = row[6]
            doc.ipoyear = row[4]
            doc.exchange = 'NYSE'
            doc.summary = row[7]
            doc.save()
    pass


def loadSP500():
    df = pandas.read_excel('data/SPY_All_Holdings.xls')
    print(df.columns)

    for i in df.index:
        ticker = df['Identifier'][i]
        name = df['Name'][i]
        sector = df['Sector'][i]
        if str(ticker) != 'nan':
            print(ticker, sector, name)
            doc, created = Company.objects.get_or_create(ticker=ticker)
            doc.name = name
            doc.sector = sector
            doc.save()

            doc, created = SP500.objects.get_or_create(ticker_id=ticker)
            doc.save()
    pass