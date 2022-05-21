function renderSimpleChart(chartTitle, dataTitle, labelsValues, dataValues, canvasId, xTitle, yTitle) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labelsValues,
            datasets: [{
                label: dataTitle,
                data: dataValues,
                backgroundColor: [
                    'rgba(68, 139, 148, 1)',
                ],
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        text: xTitle,
                        display: true,
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        text: yTitle,
                        display: true,
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: chartTitle
                },
            },
            responsive: false
        }
    });
}

function renderDoubleChart(chartTitle, dataLabel1, dataLabel2, chartLabels, dataValues1, dataValues2, canvasId, xTitle, yTitle) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartLabels,
            datasets: [
                {
                    label: dataLabel1,
                    data: dataValues1,
                    backgroundColor: [
                        'rgba(149, 209, 204, 1)',
                    ],
                },
                {
                    label: dataLabel2,
                    data: dataValues2,
                    backgroundColor: [
                        'rgba(85, 132, 172, 1)',
                    ],
                },
            ]
        },
        options: {
            scales: {
                x: {
                    title: {
                        text: xTitle,
                        display: true,
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        text: yTitle,
                        display: true,
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: chartTitle
                },
            },
            responsive: false
        }
    });
}

function renderPieChart(chartTitle, chartLabels, dataValues, canvasId) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: chartTitle,
                data: dataValues,
                backgroundColor: [
                    'rgba(149, 209, 204, 1)',
                    'rgba(85, 132, 172, 1)',
                ],
                hoverOffset: 5
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: chartTitle
                },
            },
            responsive: false
        }
    });
}

function renderScatterChart(canvasId, lineBorderCoords, trainCoords, testCoords) {
    let trainCoordsObject = [];
    for(let i = 0; i < trainCoords.length; i++) {
        trainCoordsObject.push({
            x: trainCoords[i][0],
            y: trainCoords[i][1],
        });
    }

    let testCoordsObject = [];
    for(let i = 0; i < testCoords.length; i++) {
        testCoordsObject.push({
            x: testCoords[i][0],
            y: testCoords[i][1],
        });
    }

    const ctx = document.getElementById(canvasId).getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Treino',
                    data: trainCoordsObject,
                    backgroundColor: [
                        'rgba(68, 139, 148, 1)',
                    ],
                    elements: {
                        point: {
                            radius: 4,
                        }
                    },       
                },
                {
                    label: 'Teste',
                    data: testCoordsObject,
                    backgroundColor: [
                        'rgba(255, 0, 20, 1)',
                    ],
                    elements: {
                        point: {
                            radius: 4,
                        }
                    },
                },
                {
                    label: 'Previsão',
                    data: [
                        {
                            x: lineBorderCoords[0],
                            y: lineBorderCoords[1]
                        },
                        {
                            x: lineBorderCoords[2],
                            y: lineBorderCoords[3]
                        },
                    ],
                    showLine: true,
                    backgroundColor: [
                        'rgba(102, 3, 252, 1)',
                    ],
                    borderColor: 'rgba(102, 3, 252, 1)',
                    elements: {
                        point: {
                            radius: 0,
                        }
                    },
                }
            ]
        },
        options: {
            scales: {
                x: {
                    title: {
                        text: 'Mês',
                        display: true,
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        text: 'Vendas (R$)',
                        display: true,
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Vendas de Roupas (Previsão)'
                },
            },
            responsive: false
        }
    });
}