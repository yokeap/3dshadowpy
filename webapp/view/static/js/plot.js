if (chart_histObjH instanceof Chart) {
    chart_histObjH.destroy();
}

if (chart_histObjS instanceof Chart) {
    chart_histObjS.destroy();
}

if (chart_histObjV instanceof Chart) {
    chart_histObjV.destroy();
}

if (chart_histShadowH instanceof Chart) {
    chart_histShadowH.destroy();
}

if (chart_histShadowS instanceof Chart) {
    chart_histShadowS.destroy();
}

if (chart_histShadowV instanceof Chart) {
    chart_histShadowV.destroy();
}

var chartHConfig = {
    responsive: false,
    maintainAspectRatio: true,
    type: "line",
    data: {
        labels: _360num(),
        datasets: [{
            backgroundColor: [
                'rgba(153, 102, 255, 1)',
            ],
            borderColor: [
                'rgba(153, 102, 255, 1)',
            ],
            data: [],
            fill: false,
            borderWidth: 1,
            pointRadius: 0,
        }]
    },
    options: {
        plugins: {
            filler: {
                propagate: false,
            },
            title: {
                display: true,
                text: "Hue",
                color: 'white'
            },
            legend: {
                display: false,
            },
            layout: {
                padding: 0
            }
        },
        scales: {
            y: {
                grid: {
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                },
                beginAtZero: true
            },
            x: {
                type: 'linear',
                min: 0,
                max: 360,
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                    stepSize: 50,
                },
                beginAtZero: true
            }
        }

    }
}

var chartSConfig =  {
    responsive: false,
    maintainAspectRatio: false,
    type: "line",
    data: {
        labels: _256num(),
        datasets: [{
            backgroundColor: [
                'rgba(153, 102, 255, 0.2)',
            ],
            borderColor: [
                'rgba(153, 102, 255, 1)',
            ],
            data: [],
            fill: false,
            borderWidth: 1,
            pointRadius: 0,
        }]
    },
    options: {
        plugins: {
            filler: {
                propagate: false,
            },
            title: {
                display: true,
                text: "Saturation",
                color: 'white'
            },
            legend: {
                display: false,
            }
        },
        scales: {
            y: {
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                },
                beginAtZero: true
            },
            x: {
                type: 'linear',
                min: 0,
                max: 255,
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                    stepSize: 50,
                },
                beginAtZero: true
            }
        }

    }
}

var chartVConfig = {
    responsive: false,
    maintainAspectRatio: false,
    type: "line",
    data: {
        labels: _256num(),
        datasets: [{
            backgroundColor: [
                'rgba(153, 102, 255, 0.2)',
            ],
            borderColor: [
                'rgba(153, 102, 255, 1)',
            ],
            data: [],
            fill: false,
            borderWidth: 1,
            pointRadius: 0,
        }]
    },
    options: {
        plugins: {
            filler: {
                propagate: false,
            },
            title: {
                display: true,
                text: "Value",
                color: 'white'
            },
            legend: {
                display: false,
            }
        },
        scales: {
            y: {
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                },
                beginAtZero: true
            },
            x: {
                type: 'linear',
                min: 0,
                max: 255,
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                    stepSize: 50,
                },
                beginAtZero: true
            }
        }

    }
}

var chartShadowHConfig = {
    responsive: false,
    maintainAspectRatio: true,
    type: "line",
    data: {
        labels: _360num(),
        datasets: [{
            backgroundColor: [
                'rgba(153, 102, 255, 1)',
            ],
            borderColor: [
                'rgba(153, 102, 255, 1)',
            ],
            data: [],
            fill: false,
            borderWidth: 1,
            pointRadius: 0,
        }]
    },
    options: {
        plugins: {
            filler: {
                propagate: false,
            },
            title: {
                display: true,
                text: "Hue",
                color: 'white'
            },
            legend: {
                display: false,
            },
            layout: {
                padding: 0
            }
        },
        scales: {
            y: {
                grid: {
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                },
                beginAtZero: true
            },
            x: {
                type: 'linear',
                min: 0,
                max: 360,
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                    stepSize: 50,
                },
                beginAtZero: true
            }
        }

    }
}

var chartShadowSConfig =  {
    responsive: false,
    maintainAspectRatio: false,
    type: "line",
    data: {
        labels: _256num(),
        datasets: [{
            backgroundColor: [
                'rgba(153, 102, 255, 0.2)',
            ],
            borderColor: [
                'rgba(153, 102, 255, 1)',
            ],
            data: [],
            fill: false,
            borderWidth: 1,
            pointRadius: 0,
        }]
    },
    options: {
        plugins: {
            filler: {
                propagate: false,
            },
            title: {
                display: true,
                text: "Saturation",
                color: 'white'
            },
            legend: {
                display: false,
            }
        },
        scales: {
            y: {
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                },
                beginAtZero: true
            },
            x: {
                type: 'linear',
                min: 0,
                max: 255,
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                    stepSize: 50,
                },
                beginAtZero: true
            }
        }

    }
}

var chartShadowVConfig = {
    responsive: false,
    maintainAspectRatio: false,
    type: "line",
    data: {
        labels: _256num(),
        datasets: [{
            backgroundColor: [
                'rgba(153, 102, 255, 0.2)',
            ],
            borderColor: [
                'rgba(153, 102, 255, 1)',
            ],
            data: [],
            fill: false,
            borderWidth: 1,
            pointRadius: 0,
        }]
    },
    options: {
        plugins: {
            filler: {
                propagate: false,
            },
            title: {
                display: true,
                text: "Value",
                color: 'white'
            },
            legend: {
                display: false,
            }
        },
        scales: {
            y: {
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                },
                beginAtZero: true
            },
            x: {
                type: 'linear',
                min: 0,
                max: 255,
                grid: { 
                    color: 'rgba(255, 159, 64, 0.1)',
                    drawTicks: false,
                },
                ticks: {
                    color: 'rgba(255, 159, 64, 1)',
                    stepSize: 50,
                },
                beginAtZero: true
            }
        }

    }
}

var chart_histObjH = new Chart(document.getElementById('histObjH'), chartHConfig)
    ,chart_histObjS = new Chart(document.getElementById('histObjS'), chartSConfig)
    ,chart_histObjV = new Chart(document.getElementById('histObjV'), chartVConfig)
    ,chart_histShadowH = new Chart(document.getElementById('histShadowH'), chartShadowHConfig)
    ,chart_histShadowS = new Chart(document.getElementById('histShadowS'), chartShadowSConfig)
    ,chart_histShadowV = new Chart(document.getElementById('histShadowV'), chartShadowVConfig);

function generateData(hist) {
    var xValues = [];
    var yValues = [];
    for (let i = 0; i < hist.shape[0]; i++) {
        xValues.push(i);
        yValues.push(hist[0])
    }
}

function _256num() {
    var xValues = [];
    for (let i = 0; i < 256; i++) {
        xValues.push(i);
    }
    return xValues;
}

function _360num() {
    var xValues = [];
    for (let i = 0; i < 360; i++) {
        xValues.push(i);
    }
    return xValues;
}