let pieChart = new Chart($("#pieChart"), {
    type: 'pie',
    options: { responsive: false }
});

let barChart = new Chart($("#barChart"), {
    type: 'bar',
    options: {
        responsive: false,
        plugins: {
            title: {
                display: true,
                text: 'Конечная инстанция рассмотрения дела'
            },
            legend: {
                display: false
            }
        }
    }
});

if (typeof percents !== 'undefined') {
    show_pie_diagram(percents);
}
if (typeof counts !== 'undefined') {
    show_bar_diagram(counts);
}

$( "#show_statistics_button" ).click(function() {
    let cat_ids = $('#select-category').val();
    let req_ids = $('#select-req').val();
    let cond_ids = $('#select-cond').val();

    $.post( "/data", { cat_ids: cat_ids, req_ids: req_ids, cond_ids: cond_ids }, function(data) {
        console.log(data);
        show_pie_diagram(data.percents_by_sol);
        show_bar_diagram(data.count_by_inst);
    }, "json");
});

function show_pie_diagram(data) {
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

function show_bar_diagram(data) {
    barChart.data = {
        labels: [
            "Первая инстанция",
            "Апелляция",
            "Кассация",
            "Вторая кассация/Надзор"
        ],
        datasets: [
            {
                data: [
                    data.count_1,
                    data.count_2,
                    data.count_3,
                    data.count_4
                ],
                backgroundColor: [
                    "#78DBE2",
                    "#9966CC",
                    "#4E5754",
                    "#A8E4A0"
                ]
            }]
    };
    barChart.update();
}