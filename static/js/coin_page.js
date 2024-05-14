document.addEventListener('DOMContentLoaded', function () {
    const progressBar = document.getElementById('progressBar');
    const currentPrice = parseFloat(progressBar.getAttribute('data-current-price'));
    const inputCoinFrom = document.getElementById('coin__converter-from');
    const inputCoinTo = document.getElementById('coin__converter-to');
    const initialCoinPrice = parseFloat(inputCoinTo.value.replace(',', '.').replace(' ', ''));
    const todayLowPriceElement = document.getElementById('todayLowPrice');
    const todayHighPriceElement = document.getElementById('todayHighPrice');
    inputCoinTo.value = formatNumber(initialCoinPrice);
    inputCoinFrom.addEventListener('input', function () {
        updateConversion();
    });

    function updateConversion() {
        const coinPrice = parseFloat(inputCoinFrom.getAttribute('data-coin-price-usd').replace(',', '.').replace(' ', ''));
        const numCoinsValue = inputCoinFrom.value.replace(',', '.');
        const numCoins = numCoinsValue ? parseFloat(numCoinsValue) : 0;
        const conversionResult = numCoins * coinPrice;
        inputCoinTo.value = formatNumber(conversionResult);
    }

    function formatNumber(num) {
        if (typeof num === 'string') {
            num = parseFloat(num);
        }

        if (num === 0) {
            return '0';
        }
        const magnitude = Math.abs(num);
        let decimalPlaces = 2;
        if (magnitude !== 0 && magnitude < 1) {
            decimalPlaces = -Math.floor(Math.log10(magnitude)) + 2;
        }

        const formattedNumber = num.toLocaleString('en-US', {
            minimumFractionDigits: decimalPlaces,
            maximumFractionDigits: decimalPlaces
        });
        return formattedNumber.replace(/(\.\d*[1-9])0+$|\.0*$/, '$1');
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
                    const prices = data.map(item => item.price);
                    const labels = data.map(item => {
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
                                        }
                                    },
                                    grid: {
                                        display: false
                                    }
                                }
                            }
                        },
                    });
                    if (period === '24h') {
                        minPrice = Math.min(...prices);
                        maxPrice = Math.max(...prices);
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
                const prices = data.map(item => item.price);
                const labels = data.map(item => new Date(item.timestamp * 1000).getFullYear());
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
            }
        });
});
