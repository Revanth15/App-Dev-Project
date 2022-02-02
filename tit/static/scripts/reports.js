// Simple-DataTables
// https://github.com/fiduswriter/Simple-DataTables/wiki
window.addEventListener('DOMContentLoaded', event => {

    const inventoryTable = document.getElementById('inventory-table');
    if (inventoryTable) {
        new simpleDatatables.DataTable(inventoryTable);
    }

    const salesTable = document.getElementById('sales-table');
    if (salesTable) {
        new simpleDatatables.DataTable(salesTable);
    }

    const trafficTable = document.getElementById('traffic-table');
    if (trafficTable) {
        new simpleDatatables.DataTable(trafficTable);
    }

    const sessionTable = document.getElementById('session-table');
    if (sessionTable) {
        new simpleDatatables.DataTable(sessionTable);
    }

});



//Chart.js
const restockctx = document.getElementById('restockChart').getContext('2d');
const restockChart = new Chart(restockctx, {
    type: 'bar',
    data: {
        labels: data.x,
        datasets: [{
            label: '# Orders',
            data: data.y,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        aspect_ratio: 1,
        animation: {
            onComplete: done
        },
        plugins: {
            title: {
                display: true,
                align: 'start',
                text: 'Number of times restocked',
                font: {
                    family: "'Roboto', sans-serif",
                    size: 24,
                },
                color: [
                    'rgba(0, 0, 0, 1)'
                ],
                padding: {
                    top: 20
                }
            }
        },
        scales: {
            yAxis: {
                min: 0,
                suggestedMax: 10
            }
        }
    }
});

const outofstockctx = document.getElementById('outofstockChart').getContext('2d');
const outofstockChart = new Chart(outofstockctx, {
    type: 'bar',
    data: {
        labels: data.x,
        datasets: [{
            label: '# Orders',
            data: data.y,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                align: 'start',
                text: 'Number of times out of stock',
                font: {
                    family: "'Roboto', sans-serif",
                    size: 24,
                },
                color: [
                    'rgba(0, 0, 0, 1)'
                ],
                padding: {
                    top: 20
                }
            }
        },
        scales: {
            yAxis: {
                min: 0,
                suggestedMax: 20
            }
        }
    }
});
const revenuectx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(revenuectx, {
    type: 'bar',
    data: {
        labels: data.x,
        datasets: [{
            label: '# Orders',
            data: data.y,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                align: 'start',
                text: 'Number of times restocked',
                font: {
                    family: "'Roboto', sans-serif",
                    size: 24,
                },
                color: [
                    'rgba(0, 0, 0, 1)'
                ],
                padding: {
                    top: 20
                }
            }
        },
        scales: {
            yAxis: {
                min: 0,
                suggestedMax: 10
            }
        }
    }
});

const salesctx = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(salesctx, {
    type: 'bar',
    data: {
        labels: data.x,
        datasets: [{
            label: '# Orders',
            data: data.y,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                align: 'start',
                text: 'Number of times out of stock',
                font: {
                    family: "'Roboto', sans-serif",
                    size: 24,
                },
                color: [
                    'rgba(0, 0, 0, 1)'
                ],
                padding: {
                    top: 20
                }
            }
        },
        scales: {
            yAxis: {
                min: 0,
                suggestedMax: 20
            }
        }
    }
});
const visitorctx = document.getElementById('visitorChart').getContext('2d');
const visitorChart = new Chart(visitorctx, {
    type: 'bar',
    data: {
        labels: data.x,
        datasets: [{
            label: '# Orders',
            data: data.y,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                align: 'start',
                text: 'Number of times restocked',
                font: {
                    family: "'Roboto', sans-serif",
                    size: 24,
                },
                color: [
                    'rgba(0, 0, 0, 1)'
                ],
                padding: {
                    top: 20
                }
            }
        },
        scales: {
            yAxis: {
                min: 0,
                suggestedMax: 10
            }
        }
    }
});

const purchasectx = document.getElementById('purchaseChart').getContext('2d');
const purchaseChart = new Chart(purchasectx, {
    type: 'bar',
    data: {
        labels: data.x,
        datasets: [{
            label: '# Orders',
            data: data.y,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                align: 'start',
                text: 'Number of times out of stock',
                font: {
                    family: "'Roboto', sans-serif",
                    size: 24,
                },
                color: [
                    'rgba(0, 0, 0, 1)'
                ],
                padding: {
                    top: 20
                }
            }
        },
        scales: {
            yAxis: {
                min: 0,
                suggestedMax: 20
            }
        }
    }
});
