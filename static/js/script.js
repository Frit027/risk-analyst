let statusCanvas = document.getElementById("statusChart");
let pieChart = new Chart(statusCanvas, {
    type: 'pie',
    data: {},
    options: { responsive: false }
});

$( "#my_button" ).click(function() {
    let val = parseInt($('select').val())

    $.post( "/data", { category: val }, function(data) {

    pieChart.data = {
        labels: [
            "Удовлетворено",
            "Удовлетворено частично",
            "Отказано"
        ],
        datasets: [
            {
                data: [
                    data.satisfied_percent,
                    data.partially_satisfied_percent,
                    data.denied_percent
                ],
                backgroundColor: [
                    "#FF6384",
                    "#63FF84",
                    "#6384FF"
                ]
            }]
    };
    pieChart.update();

    }, "json");
});
