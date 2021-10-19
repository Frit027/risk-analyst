let pieChart = new Chart($("#statusChart"), {
    type: 'pie',
    options: { responsive: false }
});

if (typeof data !== 'undefined') {
    show_diagram(data)
    console.log(data);
} else {
    console.log(123);
}

$( "#show_statistics_button" ).click(function() {
    let cat_id = $('#select-category').val().map(Number)
    let req_id = $('#select-req').val().map(Number)
    let cond_id = $('#select-cond').val().map(Number)

    $.post( "/data", { cat_ids: cat_id, req_ids: req_id, cond_ids:cond_id }, function(data) {
        show_diagram(data)
    }, "json");
});

function show_diagram(data) {
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
}