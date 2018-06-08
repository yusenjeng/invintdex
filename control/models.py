from django.db import models


class Company(models.Model):
    ticker = models.CharField(max_length=32, primary_key=True)
    ticker_yahoo = models.CharField(max_length=32)
    ticker_goog = models.CharField(max_length=32)
    ticker_quandl = models.CharField(max_length=32)
    sector = models.TextField(max_length=200, default='')
    industry = models.TextField(max_length=200, default='')
    name = models.TextField(max_length=200, default='')
    ipoyear = models.TextField(max_length=200, default='')
    summary = models.TextField(max_length=200, default='')
    exchange = models.TextField(max_length=200, default='')
    comment = models.TextField(max_length=200, default='')
    caps = models.FloatField(blank=True, null=True, default=0)
    yields = models.FloatField(blank=True, null=True, default=0)
    is_etf = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_filled = models.BooleanField(default=False)

    class Meta:
        db_table = "company"
        ordering = ('created', )

    def __str__(self):
        return self.ticker


class ETF(models.Model):
    ticker = models.CharField(max_length=32, primary_key=True)
    name = models.TextField(max_length=200, default='')
    tag = models.TextField(max_length=200, default='')
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "etf"
        ordering = ('ticker', )

    def __str__(self):
        return self.ticker


class Quote(models.Model):
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    adjclose = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    change = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=False, null=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker

    class Meta:
        db_table = "quote"
        unique_together = (("ticker", "date"))


class ETFQuote(models.Model):
    ticker = models.ForeignKey(ETF, on_delete=models.CASCADE)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    adjclose = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    change = models.DecimalField(
        blank=True, null=True, max_digits=5, decimal_places=2)
    date = models.DateField(blank=False, null=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker

    class Meta:
        db_table = "etf_quote"
        unique_together = (("ticker", "date"))


class SP500(models.Model):
    ticker = models.OneToOneField(
        Company, primary_key=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "sp500"

    def __str__(self):
        return self.ticker


class IS(models.Model):
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE)
    revenue = models.FloatField(blank=True, null=True)
    cogs = models.FloatField(blank=True, null=True)
    rd = models.FloatField(blank=True, null=True)
    sgna = models.FloatField(blank=True, null=True)
    op_expenses = models.FloatField(blank=True, null=True)
    op_income = models.FloatField(blank=True, null=True)
    interest_expense = models.FloatField(blank=True, null=True)
    ebit = models.FloatField(blank=True, null=True)
    net_income = models.FloatField(blank=True, null=True)
    eps = models.FloatField(blank=True, null=True)
    eps_diluted = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=False, null=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker.ticker + ' IS ' + str(self.date)

    class Meta:
        db_table = "is"
        unique_together = (("ticker", "date"))


class BS(models.Model):
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE)
    cash = models.FloatField(blank=True, null=True)
    inventories = models.FloatField(blank=True, null=True)
    receivables = models.FloatField(blank=True, null=True)
    payables = models.FloatField(blank=True, null=True)
    ppne = models.FloatField(blank=True, null=True)
    goodwill = models.FloatField(blank=True, null=True)
    total_assets = models.FloatField(blank=True, null=True)
    long_term_debt = models.FloatField(blank=True, null=True)
    short_term_debt = models.FloatField(blank=True, null=True)
    total_liabilities = models.FloatField(blank=True, null=True)
    total_equity = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=False, null=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker.ticker + ' BS ' + str(self.date)

    class Meta:
        db_table = "bs"
        unique_together = (("ticker", "date"))


class CF(models.Model):
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE)
    net_income = models.FloatField(blank=True, null=True)
    depreciation_amortization = models.FloatField(blank=True, null=True)
    operating_cf = models.FloatField(blank=True, null=True)
    investing_cf = models.FloatField(blank=True, null=True)
    financing_cf = models.FloatField(blank=True, null=True)
    fcf = models.FloatField(blank=True, null=True)
    capex = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=False, null=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker.ticker + ' CF ' + str(self.date)

    class Meta:
        db_table = "cf"
        unique_together = (("ticker", "date"))