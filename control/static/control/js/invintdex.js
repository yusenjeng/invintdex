
(function($){
    var modalProcessing = $('.modal.processing');

    function Validator(){
        this.isDate = function(s){
            return moment(s, "YYYY-MM-DD", true).isValid();
        };
        this.isTicker = function(s){
            return !(s.length === 0 || !s.trim() || !s || /^\s*$/.test(s));
        };
    }

    function Dashboard(){
        /*
        * APIs requests
        */
        function api_upd_sp500_list(){
            var statusOK = $('#upd_sp500_list .status.badge-success');
            var statusFail = $('#upd_sp500_list .status.badge-danger');

            var promise = new Promise(function(resolve, reject){
                statusOK.hide();
                statusFail.hide();

                modalProcessing.modal({
                    keyboard: false,
                    backdrop: false
                });

                $.ajax({
                    url: '/control/upd_sp500_list/',
                    success: function(ret){
                        modalProcessing.modal('hide');
                        statusOK.fadeIn();
                        resolve(ret);
                    },
                    error: function(err){
                        $.fn.hideModal();
                        statusOK.hide();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    fail: function(err){
                        modalProcessing.modal('hide');
                        statusFail.fadeIn();
                        reject(err);
                    },
                    timeout: 20*1000 //in milliseconds
                 });

            });
            return promise;
        }

        function api_upd_nasdaq_nyse_list(){
            var statusOK = $('#upd_nasdaq_nyse_list .status.badge-success');
            var statusFail = $('#upd_nasdaq_nyse_list .status.badge-danger');

            var promise = new Promise(function(resolve, reject){
                statusOK.hide();
                statusFail.hide();

                modalProcessing.modal({
                    keyboard: false,
                    backdrop: false
                });

                $.ajax({
                    url: '/control/upd_nasdaq_nyse_list/',
                    success: function(ret){
                        modalProcessing.modal('hide');
                        statusOK.fadeIn();
                        resolve(ret);
                    },
                    error: function(err){
                        $.fn.hideModal();
                        statusOK.hide();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    fail: function(err){
                        modalProcessing.modal('hide');
                        statusFail.fadeIn();
                        reject(err);
                    },
                    timeout: 60*1000 //in milliseconds
                 });

            });
            return promise;
        }

        function api_import_etf(){
            var statusOK = $('#import_etf .status.badge-success');
            var statusFail = $('#import_etf .status.badge-danger');

            var promise = new Promise(function(resolve, reject){
                statusOK.hide();
                statusFail.hide();

                modalProcessing.modal({
                    keyboard: false,
                    backdrop: false
                });

                $.ajax({
                    url: '/control/import_etf/',
                    success: function(ret){
                        modalProcessing.modal('hide');
                        statusOK.fadeIn();
                        resolve(ret);
                    },
                    error: function(err){
                        $.fn.hideModal();
                        statusOK.hide();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    fail: function(err){
                        modalProcessing.modal('hide');
                        statusFail.fadeIn();
                        reject(err);
                    },
                    timeout: 60*1000 //in milliseconds
                 });

            });
            return promise;
        }

        function api_upd_ticker_price(ticker, f, t){
            var statusOK = $('#upd_ticker_price .status.badge-success');
            var statusFail = $('#upd_ticker_price .status.badge-danger');

            var promise = new Promise(function(resolve, reject){
                statusOK.hide();
                statusFail.hide();

                modalProcessing.modal({
                    keyboard: false,
                    backdrop: false
                });

                if (!validator.isTicker(ticker))
                    return reject('Invalid ticker');
                if (!validator.isDate(f))
                    return reject('Date From is not valid');
                if (!validator.isDate(t))
                    return reject('Date To is not valid');

                $.ajax({
                    url: '/control/upd_ticker_price/',
                    data: {
                        ticker: ticker,
                        f:f,
                        t:t
                    },
                    success: function(ret){
                        setTimeout(function(){
                            modalProcessing.modal('hide');
                        }, 1000)
                        statusOK.fadeIn();
                        resolve(ret);
                    },
                    error: function(err){
                        $.fn.hideModal();
                        statusOK.hide();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    fail: function(err){
                        modalProcessing.modal('hide');
                        statusFail.fadeIn();
                        reject(err);
                    },
                    timeout: 10000 //in milliseconds
                 });

            });
            return promise;
        }

        function api_upd_etf_tickers(f, t){
            var statusOK = $('#upd_etf_tickers .status.badge-success');
            var statusFail = $('#upd_etf_tickers .status.badge-danger');

            var promise = new Promise(function(resolve, reject){
                statusOK.hide();
                statusFail.hide();

                modalProcessing.modal({
                    keyboard: false,
                    backdrop: false
                });

                if (!validator.isDate(f))
                    return reject('Date From is not valid');
                if (!validator.isDate(t))
                    return reject('Date To is not valid');

                $.ajax({
                    url: '/control/upd_etf_tickers/',
                    data: {
                        f:f,
                        t:t
                    },
                    success: function(ret){
                        setTimeout(function(){
                            modalProcessing.modal('hide');
                        }, 1000)
                        statusOK.fadeIn();
                        resolve(ret);
                    },
                    error: function(err){
                        $.fn.hideModal();
                        statusOK.hide();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    fail: function(err){
                        modalProcessing.modal('hide');
                        statusFail.fadeIn();
                        reject(err);
                    },
                    timeout: 10000 //in milliseconds
                 });

            });
            return promise;
        }

        function api_upd_all_tickers(f, t, tickerFrom){
            var statusOK = $('#upd_all_tickers .status.badge-success');
            var statusFail = $('#upd_all_tickers .status.badge-danger');

            var promise = new Promise(function(resolve, reject){
                statusOK.hide();
                statusFail.hide();

                modalProcessing.modal({
                    keyboard: false,
                    backdrop: false
                });

                if (!validator.isDate(f))
                    return reject('Date From is not valid');
                if (!validator.isDate(t))
                    return reject('Date To is not valid');

                $.ajax({
                    url: '/control/upd_all_tickers/',
                    data: {
                        f:f,
                        t:t,
                        tickerFrom:tickerFrom
                    },
                    success: function(ret){
                        setTimeout(function(){
                            modalProcessing.modal('hide');
                        }, 1000)
                        statusOK.fadeIn();
                        resolve(ret);
                    },
                    error: function(err){
                        $.fn.hideModal();
                        statusOK.hide();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    fail: function(err){
                        modalProcessing.modal('hide');
                        statusFail.fadeIn();
                        reject(err);
                    },
                    timeout: 10000 //in milliseconds
                 });

            });
            return promise;
        }

        function api_upd_ticker_financials(ticker){
            var statusOK = $('#upd_ticker_financials .status.badge-success');
            var statusFail = $('#upd_ticker_financials .status.badge-danger');
            var promise = new Promise(function(resolve, reject){
                statusOK.hide();
                statusFail.hide();
                $.ajax({
                    url: '/control/upd_ticker_financials/',
                    data: { ticker:ticker },
                    success: function(ret){
                        $.fn.hideModal();
                        statusOK.fadeIn();
                        resolve(ret);
                    },
                    error: function(err){
                        $.fn.hideModal();
                        statusOK.hide();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    fail: function(err){
                        $.fn.hideModal();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    timeout: 10000 //in milliseconds
                 });
            });
            return promise;
        }
        function api_upd_all_financials(tickerFrom){
            var statusOK = $('#upd_all_financials .status.badge-success');
            var statusFail = $('#upd_all_financials .status.badge-danger');
            var promise = new Promise(function(resolve, reject){
                statusOK.hide();
                statusFail.hide();
                $.ajax({
                    url: '/control/upd_all_financials/',
                    data: { tickerFrom:tickerFrom },
                    success: function(ret){
                        $.fn.hideModal();
                        statusOK.fadeIn();
                        resolve(ret);
                    },
                    error: function(err){
                        $.fn.hideModal();
                        statusOK.hide();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    fail: function(err){
                        $.fn.hideModal();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    timeout: 10000 //in milliseconds
                 });            });
            return promise;
        }

        function api_gen_ticker_list(){
            var statusOK = $('#gen_ticker_list .status.badge-success');
            var statusFail = $('#gen_ticker_list .status.badge-danger');
            var promise = new Promise(function(resolve, reject){
                statusOK.hide();
                statusFail.hide();
                $.ajax({
                    url: '/control/gen_ticker_list/',
                    data: { },
                    success: function(ret){
                        $.fn.hideModal();
                        statusOK.fadeIn();
                        resolve(ret);
                    },
                    error: function(err){
                        $.fn.hideModal();
                        statusOK.hide();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    fail: function(err){
                        $.fn.hideModal();
                        statusFail.fadeIn();
                        reject(err);
                    },
                    timeout: 10000 //in milliseconds
                 });            });
            return promise;
        }

        /*
        * Mount UI events
        */
        function mount_upd_sp500_list(){
            $('#upd_sp500_list .btn.run').click(function(){
                api_upd_sp500_list()
                .then(function(ret){
                    console.log('great job', ret)
                })
                .catch(function(err){
                    console.log(err)
                });
            });
        }

        function mount_upd_nasdaq_nyse_list(){
            $('#upd_nasdaq_nyse_list .btn.run').click(function(){
                api_upd_nasdaq_nyse_list()
                .then(function(ret){
                    console.log('great job', ret)
                })
                .catch(function(err){
                    console.log(err)
                });
            });
        }

        function mount_import_etf(){
            $('#import_etf .btn.run').click(function(){
                api_import_etf()
                .then(function(ret){
                    console.log('great job', ret)
                })
                .catch(function(err){
                    console.log(err)
                });
            });
        }

        function mount_upd_ticker_price(){
            var btn = $('#upd_ticker_price .btn.run');
            var txtTicker = $('#upd_ticker_price .ticker');
            var txtDateFrom = $('#upd_ticker_price .date_from');
            var txtDateTo = $('#upd_ticker_price .date_to');

            btn.click(function(){
                var ticker = txtTicker.val();
                var f = txtDateFrom.val();
                var t = txtDateTo.val();

                api_upd_ticker_price(ticker, f, t)
                .then(function(ret){
                    console.log('great job', ret)
                })
                .catch(function(err){
                    console.log(err)
                });
            });
        }

        function mount_upd_etf_tickers(){
            var btn = $('#upd_etf_tickers .btn.run');
            var txtDateFrom = $('#upd_etf_tickers .date_from');
            var txtDateTo = $('#upd_etf_tickers .date_to');

            btn.click(function(){
                var f = txtDateFrom.val();
                var t = txtDateTo.val();

                api_upd_etf_tickers(f, t)
                .then(function(ret){
                    console.log('great job', ret)
                })
                .catch(function(err){
                    console.log(err)
                });
            });
        }

        function mount_upd_all_tickers(){
            var btn = $('#upd_all_tickers .btn.run');
            var txtDateFrom = $('#upd_all_tickers .date_from');
            var txtDateTo = $('#upd_all_tickers .date_to');
            var txtTicker = $('#upd_all_tickers .ticker');

            btn.click(function(){
                var ticker = txtTicker.val();
                var f = txtDateFrom.val();
                var t = txtDateTo.val();

                api_upd_all_tickers(f, t, ticker)
                .then(function(ret){
                    console.log('great job', ret)
                })
                .catch(function(err){
                    console.log(err)
                });
            });
        }

        function mount_upd_ticker_financials(){
            var btn = $('#upd_ticker_financials .btn.run');
            var txtTicker = $('#upd_ticker_financials .ticker');

            btn.click(function(){
                var ticker = txtTicker.val();
                api_upd_ticker_financials(ticker)
                .then(function(ret){
                    console.log('great job', ret)
                })
                .catch(function(err){
                    console.log(err)
                });
            });
        }

        function mount_upd_all_financials(){
            var btn = $('#upd_all_financials .btn.run');
            var txtTicker = $('#upd_all_financials .ticker');

            btn.click(function(){
                var ticker = txtTicker.val();
                api_upd_all_financials(ticker)
                .then(function(ret){
                    console.log('great job', ret)
                })
                .catch(function(err){
                    console.log(err)
                });
            });
        }

        function mount_gen_ticker_list(){
            var btn = $('#gen_ticker_list .btn.run');

            btn.click(function(){
                api_gen_ticker_list()
                .then(function(ret){
                    console.log('great job', ret)
                })
                .catch(function(err){
                    console.log(err)
                });
            });
        }
        function mountCrawler(){
            mount_upd_sp500_list();
            mount_upd_nasdaq_nyse_list();
            mount_import_etf();
            mount_upd_ticker_price();
            mount_upd_etf_tickers();
            mount_upd_all_tickers();
            mount_upd_ticker_financials();
            mount_upd_all_financials();
            mount_gen_ticker_list();
        }

        this.init = function(){
            console.log('[initDashboard]');
            $('.status').hide();
            mountCrawler();
        };
    }


    $.fn.initBase = function(){
    };

    var validator = null;
    var dashboard = null;
    $.fn.initDashboard = function(){
        if (dashboard==null)
            dashboard = new Dashboard();
        dashboard.init();

        if (validator==null)
            validator = new Validator();
    };
    $.fn.hideModal = function(){
        setTimeout(function(){
            modalProcessing.modal('hide');
        }, 1000)
    };

})(jQuery);