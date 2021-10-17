let statusCanvas = document.getElementById("statusChart");
let pieChart = new Chart(statusCanvas, {
    type: 'pie',
    data: {},
    options: { responsive: false }
});

$( "#my_button" ).click(function() {
    let cat_id = parseInt($('#select-category').val())
    let req_id = parseInt($('#select-req').val())
    let cond_id = parseInt($('#select-cond').val())

    $.post( "/data", { cat_id: cat_id, req_id: req_id, cond_id:cond_id }, function(data) {
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
                        "#32CD32",
                        "#FFA420",
                        "#F80000"
                    ]
                }]
        };
        pieChart.update();
    }, "json");
});
