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


var config = {
    aspect_ratio: 1,
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
config.animation = false;
var configIMG = {
    aspect_ratio: 1,
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
    },
    animation: {
        onComplete: doneOnce
    }
}


//Chart.js
const restockctx = document.getElementById('restockChart').getContext('2d');
const restockChart = new Chart(restockctx, {
    type: 'bar',
    data: {
        labels: data[0].x,
        datasets: [{
            label: '# Orders',
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

config.plugins.title.text = 'Number of times low stock by product'
const outofstockctx = document.getElementById('outofstockChart').getContext('2d');
const outofstockChart = new Chart(outofstockctx, {
    type: 'bar',
    data: {
        labels: data[1].x,
        datasets: [{
            label: '# Orders',
            data: data[1].y,
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

config.plugins.title.text = 'Inventory Health'
const productQtyctx = document.getElementById('productQtyChart').getContext('2d');
const productQtyChart = new Chart(productQtyctx, {
    type: 'bar',
    data: {
        labels: data[3].x,
        datasets: [{
            label: '# Orders',
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

config.plugins.title.text = 'Revenue this year'
const revenuectx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(revenuectx, {
    type: 'line',
    data: {
        labels: data[4].x,
        datasets: [{
            label: '# Orders',
            data: data[4].y,
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
config.plugins.title.text = 'Sales this month'
const salesctx = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(salesctx, {
    type: 'line',
    data: {
        labels: data[5].x,
        datasets: [{
            label: '# Orders',
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
    options: config
});

config.plugins.title.text = 'Visitors Today'
const visitorctx = document.getElementById('visitorChart').getContext('2d');
const visitorChart = new Chart(visitorctx, {
    type: 'line',
    data: {
        labels: data[6].x,
        datasets: [{
            label: '# Orders',
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
    options: config
});

const purchasectx = document.getElementById('purchaseChart').getContext('2d');
const purchaseChart = new Chart(purchasectx, {
    type: 'bar',
    data: {
        labels: data[1].x,
        datasets: [{
            label: '# Orders',
            data: data[1].y,
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
