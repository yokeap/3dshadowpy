const chart_histH = new Chart(document.getElementById('histH'), {
    type: "line",
    data: {
        labels: _360num(),
        datasets: [{
            backgroundColor: [
                'rgba(153, 102, 255, 0.2)',
            ],
            borderColor: [
                'rgba(153, 102, 255, 1)',
            ],
            data: [],
            fill: 'origin'
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
            }
        },
        scales: {
            y: {
                ticks: {
                    color: 'rgba(255, 159, 64, 0.4)',
                },
                beginAtZero: true
            },
            x: {
                type: 'linear',
                min: 0,
                max: 255,
                ticks: {
                    color: 'rgba(255, 159, 64, 0.4)',
                    stepSize: 50,
                },
                beginAtZero: true
            }
        }

    }
});

const chart_histS = new Chart(document.getElementById('histS'), {
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
            fill: 'origin'
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
                ticks: {
                    color: 'rgba(255, 159, 64, 0.4)',
                },
                beginAtZero: true
            },
            x: {
                type: 'linear',
                min: 0,
                max: 255,
                ticks: {
                    color: 'rgba(255, 159, 64, 0.4)',
                    stepSize: 50,
                },
                beginAtZero: true
            }
        }

    }
});

const chart_histV = new Chart(document.getElementById('histV'), {
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
            fill: 'origin'
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
                ticks: {
                    color: 'rgba(255, 159, 64, 0.4)',
                },
                beginAtZero: true
            },
            x: {
                type: 'linear',
                min: 0,
                max: 255,
                ticks: {
                    color: 'rgba(255, 159, 64, 0.4)',
                    stepSize: 50,
                },
                beginAtZero: true
            }
        }

    }
});

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