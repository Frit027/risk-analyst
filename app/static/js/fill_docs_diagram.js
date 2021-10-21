let pieChart = new Chart($("#statusChart"), {
    type: 'pie',
    options: { responsive: false }
});

if (typeof docs !== 'undefined') {
    fill_docs(JSON.parse(docs));
}
if (typeof statistics !== 'undefined') {
    show_diagram(statistics);
}

$( "#searchButton" ).click(function() {
    let cat_ids = $('#select-category').val();
    let req_ids = $('#select-req').val();
    let cond_ids = $('#select-cond').val();
    let sol_ids = $('#select-solution').val();

    $.post( "/docs_statistics", { cat_ids: cat_ids, req_ids: req_ids, cond_ids: cond_ids, sol_ids: sol_ids }, function(data) {
        fill_docs(data.docs);
        show_diagram(data.statistics);
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

function fill_docs(docs) {
    let list_docs = $("#list_docs");
    list_docs.empty();

    $.each(docs, function() {
        $.each(this, function() {
            let li = $('<li/>');
            li.append(`<li class='list-group-item'>
                            <div class="d-flex w-100 justify-content-between">
                                <h5 class="mb-1">
                                    <a href="/document/${this.id.replace('/', '_')}">
                                        ${ this.id.replace('.txt', '') }
                                    </a>
                                </h5>
                            </div>
                            <p class="mb-1">${ this.req_detail }</p>
                            <p class="mb-1">${ this.cond_detail }</p>
                        </li>`)
            list_docs.append(li);
        });
    });
}