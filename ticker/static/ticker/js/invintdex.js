(function ($) {
    var modalProcessing = $('.modal.processing');

    function Validator() {
        this.isDate = function (s) {
            return moment(s, "YYYY-MM-DD", true).isValid();
        };
        this.isTicker = function (s) {
            return !(s.length === 0 || !s.trim() || !s || /^\s*$/.test(s));
        };
    }

    function TickerViewer() {
        var CARD_W = 0;
        var CARD_H = 0;

        function financial(x) {
            return Number.parseFloat(x).toFixed(2);
        }

        function ui_chart(ret) {
            $('main .price').html(financial(ret.last_close));
            $('main .change').html(financial(ret.last_change) + '%');
            // $('main .date').html(ret.last_date);
            if (ret.last_change > 0) {
                $('main .change').addClass('green');
            } else {
                $('main .change').addClass('red');
            }

            Highcharts.stockChart('chart', {
                rangeSelector: {
                    selected: 2,
                    buttons: [{
                        type: 'month',
                        count: 1,
                        text: '1m'
                    }, {
                        type: 'month',
                        count: 6,
                        text: '6m'
                    }, {
                        type: 'year',
                        count: 1,
                        text: '1y'
                    }, {
                        type: 'year',
                        count: 3,
                        text: '3y'
                    }, {
                        type: 'year',
                        count: 5,
                        text: '5y'
                    }]
                },
                title: {
                    text: name
                },
                series: [{
                    type: 'candlestick',
                    name: ret.ticker,
                    data: ret.data,
                    dataGrouping: {
                        units: [
                            [
                                'day', // unit name
                                [1, 2, 3, 4] // allowed multiples
                            ],
                            [
                                'week', [5]
                            ]
                        ]
                    }
                }]
            });
        }

        function ui_financials_revenue(data) {
            var series1 = [],
                series2 = [];
            for (var i = 0; i < data.date.length; ++i) {
                var dtm = moment(data.date[i]).valueOf();
                series1.push([dtm, data.revenue[i]]);
                series2.push([dtm, data.eps_diluted[i]]);
            }
            Highcharts.chart('revenue', {
                chart: {
                    width: CARD_W,
                    height: CARD_H
                },
                title: {
                    text: ''
                },
                subtitle: {
                    text: 'Revenue & EPS'
                },
                xAxis: [{
                    type: 'datetime',
                }],
                yAxis: [{ // Primary yAxis
                    labels: {
                        format: '${value}',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    },
                    title: {
                        text: 'Revenue',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    }
                }, { // Secondary yAxis
                    title: {
                        text: 'EPS',
                        style: {
                            color: Highcharts.getOptions().colors[1]
                        }
                    },
                    labels: {
                        format: '${value}',
                        style: {
                            color: Highcharts.getOptions().colors[1]
                        }
                    },
                    opposite: true
                }],
                tooltip: {
                    shared: true,
                },
                legend: {
                    enabled: false
                },
                series: [{
                    name: 'Revenue',
                    type: 'column',
                    yAxis: 0,
                    data: series1,
                    tooltip: {
                        valueSuffix: ''
                    }
                }, {
                    name: 'EPS',
                    type: 'spline',
                    yAxis: 1,
                    data: series2,
                    tooltip: {
                        valuePreffix: '$'
                    },
                    color: Highcharts.getOptions().colors[1]
                }]
            });
        }

        function ui_financials_debt(data) {
            var series1 = [],
                series2 = [],
                series3 = [];
            for (var i = 0; i < data.date.length; ++i) {
                var dtm = moment(data.date[i]).valueOf();
                ratio = 100 * (data.short_term_debt[i] + data.long_term_debt[i]) / data.total_assets[i];
                ratio = Number(ratio.toFixed(1));
                series1.push([dtm, data.long_term_debt[i]]);
                series2.push([dtm, data.short_term_debt[i]]);
                series3.push([dtm, ratio]);
            }
            var label3 = 'Debt to Assets Ratio'
            Highcharts.chart('debt', {
                chart: {
                    width: CARD_W,
                    height: CARD_H
                },
                title: {
                    text: ''
                },
                subtitle: {
                    text: 'Debt'
                },
                xAxis: [{
                    type: 'datetime',
                }],
                yAxis: [{ // Primary yAxis
                    labels: {
                        format: '${value}',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    },
                    title: {
                        text: 'Debt',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    }
                }, { // Secondary yAxis
                    title: {
                        text: label3,
                        style: {
                            color: Highcharts.getOptions().colors[1]
                        }
                    },
                    labels: {
                        format: '{value}%',
                        style: {
                            color: Highcharts.getOptions().colors[1]
                        }
                    },
                    opposite: true
                }],
                tooltip: {
                    shared: true,
                },
                legend: {
                    enabled: false
                },
                series: [{
                    name: 'LT Debt',
                    type: 'column',
                    yAxis: 0,
                    data: series1,
                    tooltip: {
                        valuePreffix: '$'
                    }
                }, {
                    name: 'ST Debt',
                    type: 'column',
                    yAxis: 0,
                    data: series2,
                    tooltip: {
                        valuePreffix: '$'
                    },
                    color: Highcharts.getOptions().colors[3]
                }, {
                    name: label3,
                    type: 'spline',
                    yAxis: 1,
                    data: series3,
                    tooltip: {
                        valueSuffix: '%'
                    },
                    color: Highcharts.getOptions().colors[1]
                }]
            });
        }

        function ui_financials_cashflow(data) {
            var series1 = [],
                series2 = [],
                series3 = [];
            for (var i = 0; i < data.date.length; ++i) {
                var dtm = moment(data.date[i]).valueOf();
                ratio = 100 * (data.operating_cf[i] / data.revenue[i]);
                ratio = Number(ratio.toFixed(1));
                series1.push([dtm, data.operating_cf[i]]);
                series2.push([dtm, data.fcf[i]]);
                series3.push([dtm, ratio]);
            }
            var label3 = 'OCF to Revenue Ratio'
            Highcharts.chart('cashflow', {
                chart: {
                    width: CARD_W,
                    height: CARD_H
                },
                title: {
                    text: ''
                },
                subtitle: {
                    text: 'Operating Cash Flow'
                },
                xAxis: [{
                    type: 'datetime',
                }],
                yAxis: [{ // Primary yAxis
                    labels: {
                        format: '${value}',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    },
                    title: {
                        text: 'Cashflow',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    }
                }, { // Secondary yAxis
                    title: {
                        text: label3,
                        style: {
                            color: Highcharts.getOptions().colors[1]
                        }
                    },
                    labels: {
                        format: '{value}%',
                        style: {
                            color: Highcharts.getOptions().colors[1]
                        }
                    },
                    opposite: true
                }],
                tooltip: {
                    shared: true,
                },
                legend: {
                    enabled: false
                },
                series: [{
                    name: 'OCF',
                    type: 'column',
                    yAxis: 0,
                    data: series1,
                    tooltip: {
                        valuePreffix: '$'
                    }

                }, {
                    name: 'FCF',
                    type: 'column',
                    yAxis: 0,
                    data: series2,
                    tooltip: {
                        valuePreffix: '$'
                    },
                    color: Highcharts.getOptions().colors[3]
                }, {
                    name: label3,
                    type: 'spline',
                    yAxis: 1,
                    data: series3,
                    tooltip: {
                        valueSuffix: '%'
                    },
                    color: Highcharts.getOptions().colors[1]
                }]
            });
        }

        function ui_financials_margin(data) {
            var series1 = [],
                series2 = [],
                series3 = [];
            for (var i = 0; i < data.date.length; ++i) {
                var dtm = moment(data.date[i]).valueOf();
                series1.push([dtm, data.gm[i]]);
                series2.push([dtm, data.om[i]]);
                series3.push([dtm, data.pm[i]]);
            }
            Highcharts.chart('margin', {
                chart: {
                    width: CARD_W,
                    height: CARD_H
                },
                title: {
                    text: ''
                },
                subtitle: {
                    text: 'GM, OM, PM'
                },
                xAxis: [{
                    type: 'datetime',
                }],
                yAxis: [{ // Primary yAxis
                    labels: {
                        format: '{value}%',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    },
                    title: {
                        text: 'Margin',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    }
                }],
                tooltip: {
                    shared: true,
                },
                legend: {
                    enabled: false
                },
                series: [{
                    name: 'Gross Margin',
                    type: 'spline',
                    yAxis: 0,
                    data: series1,
                    tooltip: {
                        valueSuffix: '%'
                    }

                }, {
                    name: 'Operating Margin',
                    type: 'spline',
                    yAxis: 0,
                    data: series2,
                    tooltip: {
                        valueSuffix: '%'
                    },
                    color: Highcharts.getOptions().colors[3]
                }, {
                    name: 'Profit Margin',
                    type: 'spline',
                    yAxis: 0,
                    data: series3,
                    tooltip: {
                        valueSuffix: '%'
                    },
                    color: Highcharts.getOptions().colors[1]
                }]
            });
        }

        function ui_financials_cycle(data) {
            var series1 = [],
                series2 = [],
                series3 = [],
                series4 = [];
            for (var i = 0; i < data.date.length; ++i) {
                var dtm = moment(data.date[i]).valueOf();
                series1.push([dtm, data.days_receivable[i]]);
                series2.push([dtm, data.days_inventory[i]]);
                series3.push([dtm, data.days_payable[i]]);
                series4.push([dtm, data.days_cycle[i]]);
            }
            Highcharts.chart('cycle', {
                chart: {
                    width: CARD_W,
                    height: CARD_H
                },
                title: {
                    text: ''
                },
                subtitle: {
                    text: 'Operating Cycle'
                },
                xAxis: [{
                    type: 'datetime',
                }],
                yAxis: [{ // Primary yAxis
                    labels: {
                        format: '{value}',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    },
                    title: {
                        text: 'Days',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    }
                }],
                tooltip: {
                    shared: true,
                },
                legend: {
                    enabled: false
                },
                series: [{
                    name: 'Days Receivable',
                    type: 'spline',
                    yAxis: 0,
                    data: series1,
                    tooltip: {
                        valueSuffix: ''
                    }
                }, {
                    name: 'Days Inventory',
                    type: 'spline',
                    yAxis: 0,
                    data: series2,
                    tooltip: {
                        valueSuffix: ''
                    },
                    color: Highcharts.getOptions().colors[3]
                }, {
                    name: 'Days Payable',
                    type: 'spline',
                    yAxis: 0,
                    data: series3,
                    tooltip: {
                        valueSuffix: ''
                    },
                    color: Highcharts.getOptions().colors[1]
                }, {
                    name: 'Net Trade Cycle',
                    type: 'spline',
                    yAxis: 0,
                    data: series4,
                    tooltip: {
                        valueSuffix: ''
                    },
                    color: Highcharts.getOptions().colors[2]
                }]
            });
        }

        function mountChart(ticker, name) {
            modalProcessing.modal('show');
            $.getJSON('/ticker/' + ticker + '/get_quote', function (ret) {
                $.fn.hideModal();
                ui_chart(ret)
            });
        }

        function mountRss(ticker) {
            $("#rss").rss("https://feeds.finance.yahoo.com/rss/2.0/headline?s=" + ticker, {
                entryTemplate: '<li><div class="rssdate">{date}</div><div class="rsslink"><a href="{url}" target="_blank">{title}</a></div><br/></li>',
                dateFormat: 'D MMM hA',
                limit: 17,
                dateLocale: 'en',
                effect: 'show',
                ssl: true
            });
        }

        function preprocess(data) {
            data.gm = [];
            data.om = [];
            data.pm = [];
            data.days_receivable = [];
            data.days_inventory = [];
            data.days_payable = [];
            data.days_cycle = [];
            for (var i = 0; i < data.revenue.length; ++i) {
                var gm = 100 * (data.revenue[i] - data.cogs[i]) / data.revenue[i];
                var om = 100 * data.op_income[i] / data.revenue[i];
                var pm = 100 * data.net_income[i] / data.revenue[i];
                data.gm.push(Number(gm.toFixed(1)));
                data.om.push(Number(om.toFixed(1)));
                data.pm.push(Number(pm.toFixed(1)));

                var days_receivable = 90 * data.receivables[i] / data.revenue[i];
                var days_inventory = 90 * data.inventories[i] / data.cogs[i];
                var days_payable = 90 * data.payables[i] / data.cogs[i];
                var days_cycle = days_receivable + days_inventory - days_payable;
                data.days_receivable.push(parseInt(days_receivable));
                data.days_inventory.push(parseInt(days_inventory));
                data.days_payable.push(parseInt(days_payable));
                data.days_cycle.push(parseInt(days_cycle));

            }
        }

        function mountFinancials(ticker) {
            $.getJSON('/ticker/' + ticker + '/get_financials', function (data) {
                preprocess(data);
                console.log(data);
                ui_financials_revenue(data);
                ui_financials_debt(data);
                ui_financials_cashflow(data);
                ui_financials_margin(data);
                ui_financials_cycle(data);
            });
        }

        this.init = function (ticker, name) {
            console.log('[initTickerPage]');

            CARD_W = $('.card-chart').width() - 10;
            CARD_H = CARD_W * 0.75;

            Highcharts.setOptions({
                lang: {
                    thousandsSep: ','
                }
            });
            mountChart(ticker, name);
            mountFinancials(ticker);
            mountRss(ticker);
        };
    }

    function EntranceViewer() {
        function mountRss(keyword) {
            $("#rss").rss("https://feeds.finance.yahoo.com/rss/2.0/headline?s=" + keyword, {
                entryTemplate: '<li><div class="rssdate">{date}</div><div class="rsslink"><a href="{url}" target="_blank">{title}</a></div><br/></li>',
                dateFormat: 'D MMM hA',
                limit: 20,
                dateLocale: 'en',
                effect: 'show',
                ssl: true
            });
        }

        this.init = function () {
            console.log('[initEntrance]');
            mountRss('s&p500');
        };
    }


    function BaseViewer() {
        function gotoTicker(){
            var ticker = $("#searchTicker").getSelectedItemData().ticker;
            setTimeout(function () {
                window.location.href = '/ticker/' + ticker;
            }, 300);
        }

        function mountSearchBox() {
            var options = {
                url: "/static/ticker/ticker_list.json",
                getValue: "name",
                template: {
                    type: "description",
                    fields: {
                        description: "comment"
                    }
                },
                list: {
                    match: {
                        enabled: true
                    },
                    onClickEvent: gotoTicker,
                    onKeyEnterEvent: gotoTicker
                },
                theme: "plate-dark"
            };
            $("#searchTicker").easyAutocomplete(options);
            $("#searchTicker").keypress(function(e){
                if ( e.which == 13 ) {
                    e.preventDefault();
                    var ticker = $(this).val();
                    if (ticker != ''){
                        window.location.href = '/ticker/' + ticker;
                    }
                }
            });
        }

        this.init = function (mark) {
            console.log('[initBase]');
            $('.status').hide();
            mountSearchBox();
            if (mark)
                $('nav a.'+mark).addClass('highlight')
        };
    }


    function EntranceViewer() {
        function mountRss(keyword) {
            $("#rss").rss("https://feeds.finance.yahoo.com/rss/2.0/headline?s=" + keyword, {
                entryTemplate: '<li><div class="rssdate">{date}</div><div class="rsslink"><a href="{url}" target="_blank">{title}</a></div><br/></li>',
                dateFormat: 'D MMM hA',
                limit: 20,
                dateLocale: 'en',
                effect: 'show',
                ssl: true
            });
        }

        this.init = function () {
            console.log('[initEntrance]');
            mountRss('s&p500');
        };
    }

    function MarketsViewer() {
        this.colors = [
            '#333333', '#4BA7B3', '#1E6583', '#F25F5C', '#898E8C', '#FFE066',
            '#DA413D', '#672E3B', '#F3D6E4', '#C48F65', '#005960', '#9C9A40',
            '#4F84C4', '#D2691E'
        ];
        this.colors2 = ['#333333'];
        this.colors3 = ['#1E6583'];

        this.axes = {
            y:{
                drawGrid: true,
                independentTicks: false
            },
            y2:{
                drawGrid: true,
                independentTicks: true
            }
        };
        var w = $(document).width();
        if (w > 420)
            w = 480;
        else if (w > 380)
            w = 440;
        else
            w = 380;
        this.w = w;

        this.init = function () {
            console.log('[MarketsViewer]', 'init');
        };
    }

    $.m = {};
    var validator = null;
    var baseViewer = null;
    var tickerViewer = null;
    var entranceViewer = null;
    var marketsViewer = null;

    $.fn.initBase = function (nav_mark) {
        if (baseViewer == null){
            baseViewer = new BaseViewer();
        }
        baseViewer.init(nav_mark);
    };
    $.fn.initTickerViewer = function (name) {
        if (tickerViewer == null)
            tickerViewer = new TickerViewer();
        if (validator == null)
            validator = new Validator();
        tickerViewer.init(name);
    };
    $.fn.initEntranceViewer = function () {
        if (entranceViewer == null){
            entranceViewer = new EntranceViewer();
        }
        entranceViewer.init();
    };
    $.fn.initMarketsViewer = function () {
        if (marketsViewer == null){
            marketsViewer = new MarketsViewer();
        }
        marketsViewer.init();
        $.m.marketsViewer = marketsViewer;
    };
    $.fn.hideModal = function () {
        setTimeout(function () {
            modalProcessing.modal('hide');
        }, 1000)
    };


})(jQuery);