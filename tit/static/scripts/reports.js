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

$('#fileselect').change(function() {
    $('.chartselect').hide()
    console.log($('#fileselect').val())
    if ($('#fileselect').val() == 1) {
        $('.chartselect').show()
    }
})


var config = {
    aspect_ratio: 1,
    plugins: {
        title: {
            display: true,
            align: 'start',
            text: 'Out of Stocks',
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
config.animation = false;
var configIMG = {
    aspect_ratio: 1,
    plugins: {
        title: {
            display: true,
            align: 'start',
            text: 'Restocks by SKU',
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
    },
    animation: {
        onComplete: doneOnce
    }
}


const restockctx = document.getElementById('restockChart').getContext('2d');
const restockChart = new Chart(restockctx, {
    type: 'bar',
    data: {
        labels: data[0].x,
        datasets: [{
            label: '#',
            data: data[0].y,
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
    options: configIMG
});


const outofstockctx = document.getElementById('outofstockChart').getContext('2d');
const outofstockChart = new Chart(outofstockctx, {
    type: 'bar',
    data: {
        labels: data[2].x,
        datasets: [{
            label: 'Stocks',
            data: data[2].y,
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
    options: config
});

config.plugins.title.text = 'Inventory Health';
const productQtyctx = document.getElementById('productQtyChart').getContext('2d');
const productQtyChart = new Chart(productQtyctx, {
    type: 'bar',
    data: {
        labels: data[3].x,
        datasets: [{
            label: 'Stocks',
            data: data[3].y,
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
    options: config
});

config.plugins.title.text = 'Revenue this month';
const revenuectx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(revenuectx, {
    type: 'bar',
    data: {
        labels: data[3].x,
        datasets: [{
            label: '$',
            data: data[3].y,
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
        plugins: {
            title: {
                display: true,
                align: 'start',
                text: 'Revenue over time',
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


config.plugins.title.text = 'Sales this month';
const salesctx = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(salesctx, {
    type: 'bar',
    data: {
        labels: data[5].x,
        datasets: [{
            label: '#',
            data: data[5].y,
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
        plugins: {
            title: {
                display: true,
                align: 'start',
                text: 'Sales over time',
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


const visitorctx = document.getElementById('visitorChart').getContext('2d');
const visitorChart = new Chart(visitorctx, {
    type: 'bar',
    data: {
        labels: data[6].x,
        datasets: [{
            label: 'Visitors',
            data: data[6].y,
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
        plugins: {
            title: {
                display: true,
                align: 'start',
                text: 'Visitors Today',
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



config.plugins.title.text = 'Cart Status';
const piectx = document.getElementById('pieChart').getContext('2d');
const pieChart = new Chart(piectx, {
    type: 'pie',
    data: {
        labels: data[7].x,
        datasets: [{
            label: '# Orders',
            data: data[7].y,
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
    options: config
});
