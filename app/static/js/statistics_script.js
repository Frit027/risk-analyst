let pieChart = new Chart($("#statusChart"), {
    type: 'pie',
    options: { responsive: false }
});

$( "#show_statistics_button" ).click(function() {
    let cat_id = $('#select-category').val().map(Number)
    let req_id = parseInt($('#select-req').val())
    let cond_id = parseInt($('#select-cond').val())

    $.post( "/data", { cat_ids: cat_id, req_id: req_id, cond_id:cond_id }, function(data) {
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