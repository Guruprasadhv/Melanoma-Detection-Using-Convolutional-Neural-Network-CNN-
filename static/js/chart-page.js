document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('pieChart');
    if (!canvas) return;

    var ctx = canvas.getContext('2d');

    // Read data attributes
    var benignData = parseFloat(canvas.getAttribute('data-benign'));
    var malignantData = parseFloat(canvas.getAttribute('data-malignant'));

    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Benign', 'Malignant'],
            datasets: [{
                data: [benignData, malignantData],
                backgroundColor: [
                    '#4285f4', // Blue for Benign
                    'red'      // Red for Malignant
                ],
                borderColor: [
                    '#ffffff',
                    '#ffffff'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: 'white',
                        font: {
                            size: 14
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Prediction Probability',
                    color: 'white',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
});
