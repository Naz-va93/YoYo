document.addEventListener('DOMContentLoaded', function () {
    const progressBar = document.getElementById('progressBar');
    const todayLowPriceElement = document.getElementById('todayLowPrice');
    const todayHighPriceElement = document.getElementById('todayHighPrice');

    const currentPrice = parseFloat(progressBar.getAttribute('data-current-price').replace(',', '.'));
    const inputCoinFrom = document.getElementById('coin__converter-from');
    const inputCoinTo = document.getElementById('coin__converter-to');
    inputCoinTo.value = formatNumber(parseFloat(inputCoinFrom.getAttribute('data-coin-price-usd').replace(',', '.')))

    inputCoinFrom.addEventListener('input', function () {
        updateConversionFrom();
    });

    inputCoinTo.addEventListener('input', function () {
        updateConversionTo();
    });

    function updateConversionFrom() {
        const coinPriceUsd = parseFloat(inputCoinFrom.getAttribute('data-coin-price-usd').replace(',', '.'));
        const coinPriceCurrencyToUsd = parseFloat(inputCoinFrom.getAttribute('data-coin-price-currency-to-usd').replace(',', '.'));
        const numCoinsValue = parseInputValue(inputCoinFrom.value);

        const currentCurrencySymbol = document.getElementById('current-currency').innerText.toLowerCase();
        const converterCryptoSymbol = document.getElementById('converter-crypto-symbol').innerText.toLowerCase();
        console.log(currentCurrencySymbol, converterCryptoSymbol);
        if (currentCurrencySymbol === converterCryptoSymbol) {
            inputCoinTo.value = formatNumber(numCoinsValue);
            return;
        }
        const numCoins = numCoinsValue ? numCoinsValue : 0;
        const conversionResult = numCoins * coinPriceUsd * coinPriceCurrencyToUsd;
        inputCoinTo.value = formatNumber(conversionResult);
    }

    function updateConversionTo() {
        const coinPriceUsd = parseFloat(inputCoinFrom.getAttribute('data-coin-price-usd').replace(',', '.'));
        const coinPriceCurrencyToUsd = parseFloat(inputCoinFrom.getAttribute('data-coin-price-currency-to-usd').replace(',', '.'));
        const numCurrenciesValue = parseInputValue(inputCoinTo.value);

        const currentCurrencySymbol = document.getElementById('current-currency').innerText.toLowerCase();
        const converterCryptoSymbol = document.getElementById('converter-crypto-symbol').innerText.toLowerCase();
        if (currentCurrencySymbol === converterCryptoSymbol) {
            inputCoinFrom.value = formatNumber(numCurrenciesValue);
            return;
        }

        const numCurrencies = numCurrenciesValue ? numCurrenciesValue : 0;
        const conversionResult = (numCurrencies / coinPriceCurrencyToUsd) / coinPriceUsd;
        inputCoinFrom.value = formatNumber(conversionResult);
    }

    function parseInputValue(value) {
        const numberPattern = /^[0-9\s,.]+$/;

        if (numberPattern.test(value)) {
            value = value.replace(/\s+/g, '');
            value = value.replace(/,/g, '.');

            let parsedValue = parseFloat(value);

            if (isNaN(parsedValue)) {
                return 0;
            }

            return parsedValue;
        } else {
            return 0;
        }
    }

    function formatNumber(num) {
        if (typeof num === 'string') {
            num = parseFloat(num);
        }

        if (isNaN(num) || num === 0) {
            return '0';
        }

        const magnitude = Math.abs(num);
        let decimalPlaces = 2;
        if (magnitude !== 0 && magnitude < 1) {
            decimalPlaces = -Math.floor(Math.log10(magnitude)) + 2;
        }

        const formattedNumber = num.toLocaleString('en-US', {
            minimumFractionDigits: decimalPlaces,
            maximumFractionDigits: decimalPlaces,
            useGrouping: true
        }).replace(/,/g, ' ').replace(/\./g, ',');

        return formattedNumber.replace(/(\,\d*[1-9])0+$|\,0*$/, '$1').replace(/,/g, '.');
    }

    const coinTradingCoinInfo = document.querySelector('.coin__trading--coin__info');
    const coinChart = document.querySelector('.coin__chart');
    const marketPriceTabs = document.querySelectorAll('.coin__tab.market_price');
    const coinTabContainerHistoryPrice = document.getElementById('coin__tab-container-history_price');
    marketPriceTabs.forEach(tab => {
        tab.addEventListener('click', function (e) {
            switchTabMarketPrice(marketPriceTabs, parseInt(tab.getAttribute('data-index')), e);
        });
    });

    function switchTabMarketPrice(tabs, index, e) {
        if (index === 1) {
            coinChart.classList.add('visually-hidden');
            coinTabContainerHistoryPrice.classList.add('visually-hidden');
            coinTradingCoinInfo.classList.remove('visually-hidden');
        }
        if (index === 0) {
            coinTradingCoinInfo.classList.add('visually-hidden');
            coinChart.classList.remove('visually-hidden');
            coinTabContainerHistoryPrice.classList.remove('visually-hidden');
        }
        tabs.forEach(tab => {
            tab.classList.remove('active');
        });
        e.target.classList.add('active');
        const sliderWidth = e.target.offsetWidth;
        document.querySelector('.coin__slider').style.transform = `translateX(${index * sliderWidth}px)`;
    }

    const historyPriceTabs = document.querySelectorAll('.coin__tab.history_price');
    let chart = null;

    historyPriceTabs.forEach(tab => {
        tab.addEventListener('click', function (e) {
            switchTabPriceHistory(e, historyPriceTabs, tab.getAttribute('data-period'), tab.getAttribute('data-coin-api-id'), tab.getAttribute('data-coin-api-type'))
        });
    });

    document.querySelector('.coin__tab.history_price[data-period="24h"]').click();

    function switchTabPriceHistory(e, tabs, period, coinApiId, coinApiType) {
        tabs.forEach(tab => {
            tab.classList.remove('active');
        });
        e.target.classList.add('active');

        const chartWrapper = document.querySelector('.coin__chart-wrapper.period');
        let canvas = chartWrapper.querySelector('canvas');
        if (canvas) {
            if (chart) {
                chart.destroy();
            }
            chartWrapper.removeChild(canvas);
        }

        canvas = document.createElement('canvas');
        canvas.id = 'coinChartHistoryPrice';
        chartWrapper.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(30, 116, 254, 0.4)');
        gradient.addColorStop(0.78966, 'rgba(30, 116, 254, 0)');

        fetch(`https://coinyoyo.io/coin-price-history?coinId=${coinApiId}&type=${coinApiType}&period=${period}`)
            .then(response => response.json())
            .then(response => {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                if (response.status === "success") {
                    const data = response.data.history;
                    data.sort((a, b) => a.timestamp - b.timestamp);

                    const filteredData = data.filter(item => item.price !== null);
                    const prices = filteredData.map(item => item.price);
                    const labels = filteredData.map(item => {
                        const date = new Date(item.timestamp * 1000);
                        if (period === '24h') {
                            return date.toLocaleTimeString('en-GB', {
                                hour: '2-digit',
                                minute: '2-digit',
                                hour12: false
                            });
                        } else {
                            return date.toLocaleDateString('en-GB');
                        }
                    });

                    chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                data: prices,
                                borderColor: '#3c86fe',
                                borderWidth: 2,
                                fill: true,
                                pointRadius: 0,
                                pointHoverRadius: 0,
                                lineTension: 0.1,
                                backgroundColor: gradient,
                            }]
                        },
                        options: {
                            responsive: false,
                            animation: {
                                duration: 0
                            },
                            interaction: {
                                mode: 'nearest',
                                axis: 'x',
                                intersect: false
                            },
                            plugins: {
                                legend: {
                                    display: false
                                },
                                tooltip: {
                                    enabled: true,
                                    mode: 'index',
                                    intersect: false,
                                    displayColors: false,
                                    callbacks: {
                                        label: function (context) {
                                            return formatNumber(context.raw);
                                        }
                                    }
                                },
                                crosshair: {
                                    line: {
                                        color: '#282b31',
                                        width: 1
                                    },
                                    zoom: {
                                        enabled: false
                                    }
                                }
                            },
                            scales: {
                                y: {
                                    ticks: {
                                        color: 'rgb(148, 149, 152)',
                                        font: {
                                            family: 'Commissioner',
                                            size: 12
                                        },
                                        callback: function (value) {
                                            if (value !== undefined) {
                                                return formatNumber(value);
                                            }
                                            return '';
                                        }
                                    },
                                    beginAtZero: false,
                                    position: 'right',
                                    border: {
                                        display: false
                                    },
                                    grid: {
                                        color: '#949598',
                                        lineWidth: 0.6
                                    }
                                },
                                x: {
                                    ticks: {
                                        align: 'start',
                                        autoSkip: true,
                                        maxTicksLimit: 6,
                                        color: 'rgb(148, 149, 152)',
                                        font: {
                                            family: 'Commissioner',
                                            size: 12
                                        },
                                        padding: 0,
                                        maxRotation: 0,
                                        minRotation: 0
                                    },
                                    grid: {
                                        display: false
                                    },
                                }
                            }
                        },
                    });

                    function updateChartMaxTicksLimit() {
                        const isSmallScreen = window.innerWidth < 600;
                        const maxTicksLimit = isSmallScreen ? 4 : 6;

                        if (chart && chart.options && chart.options.scales && chart.options.scales.x) {
                            chart.options.scales.x.ticks.maxTicksLimit = maxTicksLimit;
                            chart.update();
                        }
                    }

                    updateChartMaxTicksLimit();

                    window.addEventListener('resize', updateChartMaxTicksLimit);
                    if (period === '24h') {
                        const minPrice = Math.min(...prices);
                        const maxPrice = Math.max(...prices);
                        todayLowPriceElement.textContent = `$${minPrice ? formatNumber(minPrice) : '--'}`;
                        todayHighPriceElement.textContent = `$${maxPrice ? formatNumber(maxPrice) : '--'}`;
                        if (maxPrice - minPrice !== 0) {
                            const percent = ((currentPrice - minPrice) / (maxPrice - minPrice)) * 100;
                            progressBar.style.width = `${percent}%`;
                        } else {
                            progressBar.style.width = '0%';
                        }
                    }

                } else {
                    ctx.fillText('Error loading data', canvas.width / 2 - 50, canvas.height / 2);
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                ctx.fillText('Error loading data', canvas.width / 2 - 50, canvas.height / 2);
            });
    }

    const buttonAllTimePriceHistory = document.querySelector('.coin__tab.history_price.all_time');
    const coinApiId = buttonAllTimePriceHistory.getAttribute('data-coin-api-id');
    const coinApiType = buttonAllTimePriceHistory.getAttribute('data-coin-api-type');
    const allTimeCanvas = document.getElementById('coinChartAllHistoryPrice');
    const allTimeCtx = allTimeCanvas.getContext('2d');
    allTimeCanvas.height = 80;

    fetch(`https://coinyoyo.io/coin-price-history?coinId=${coinApiId}&type=${coinApiType}&period=all`)
        .then(response => response.json())
        .then(response => {
            if (response.status === "success") {
                const data = response.data.history;
                data.sort((a, b) => a.timestamp - b.timestamp);

                const filteredData = data.filter(item => item.price !== null);
                const prices = filteredData.map(item => item.price);
                const years = [...new Set(filteredData.map(item => new Date(item.timestamp * 1000).getFullYear()))];
                const labels = filteredData.map(item => {
                    const date = new Date(item.timestamp * 1000);
                    if (years.length === 1) {
                        return date.toLocaleDateString('en-GB', {month: 'short', year: 'numeric'});
                    } else {
                        return date.getFullYear();
                    }
                });

                allTimeChart = new Chart(allTimeCtx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: prices,
                            borderColor: '#3c86fe',
                            borderWidth: 2,
                            fill: false,
                            pointRadius: 0,
                            pointHoverRadius: 0,
                            lineTension: 0.1
                        }]
                    },
                    options: {
                        animation: {
                            duration: 0
                        },
                        interaction: {
                            mode: 'nearest',
                            axis: 'x',
                            intersect: false
                        },
                        tooltip: {
                            enabled: false,
                        },
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                display: true,
                                position: 'right',
                                grid: {
                                    display: false
                                },
                                ticks: {
                                    color: 'transparent',
                                    font: {
                                        family: 'Commissioner',
                                        size: 12
                                    },
                                },
                                border: {
                                    display: false
                                }

                            },
                            x: {
                                ticks: {
                                    align: 'start',
                                    autoSkip: true,
                                    maxTicksLimit: 6,
                                    color: 'rgb(148, 149, 152)',
                                    font: {
                                        family: 'Commissioner',
                                        size: 12
                                    }
                                },
                                grid: {
                                    color: '#5b5c61',
                                    lineWidth: 0.4,
                                },
                                border: {
                                    color: '#5b5c61',
                                    width: 0.4,
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                display: false
                            },
                            tooltip: {
                                enabled: false
                            },
                            crosshair: false
                        }
                    }
                });

                function updateAllTimeChartTicksLimit() {
                    const isSmallScreen = window.innerWidth < 600;
                    const maxTicksLimit = isSmallScreen ? 4 : 6;

                    if (allTimeChart && allTimeChart.options && allTimeChart.options.scales && allTimeChart.options.scales.x) {
                        allTimeChart.options.scales.x.ticks.maxTicksLimit = maxTicksLimit;
                        allTimeChart.update();
                    }
                }

                updateAllTimeChartTicksLimit();

                window.addEventListener('resize', updateAllTimeChartTicksLimit);
            }
        });

    //===============================<converter script>================================
    const currencyLabel = document.getElementById('currency-label');
    const currencyDropdown = document.getElementById('currency-dropdown');
    const currentCurrency = document.getElementById('current-currency');

    currencyLabel.addEventListener('click', function (event) {
        event.stopPropagation();
        if (currencyDropdown.classList.contains('show')) {
            currencyDropdown.classList.remove('show');
            setTimeout(() => {
                currencyDropdown.style.display = 'none';
            }, 300);
        } else {
            currencyDropdown.style.display = 'block';
            setTimeout(() => {
                currencyDropdown.classList.add('show');
            }, 10);
        }
    });

    document.addEventListener('click', function (event) {
        if (!currencyDropdown.contains(event.target) && event.target !== currencyLabel) {
            if (currencyDropdown.classList.contains('show')) {
                currencyDropdown.classList.remove('show');
                setTimeout(() => {
                    currencyDropdown.style.display = 'none';
                }, 300);
            }
        }
    });

    currencyDropdown.addEventListener('click', function (event) {
        if (event.target.tagName.toLowerCase() === 'li') {
            const currencySymbol = event.target.getAttribute('data-currency-symbol');
            const currencyPriceToUsd = event.target.getAttribute('data-currency-price-to-usd');
            currentCurrency.textContent = currencySymbol;

            inputCoinFrom.setAttribute('data-coin-price-currency-to-usd', currencyPriceToUsd);
            updateConversionFrom();
            const liElements = currencyDropdown.querySelectorAll('li');
            liElements.forEach(li => {
                li.classList.remove('selected');
            });

            event.target.classList.add('selected');

            currencyDropdown.classList.remove('show');
            setTimeout(() => {
                currencyDropdown.style.display = 'none';
            }, 300);
        }
    });
    //===============================</converter script>================================
});
