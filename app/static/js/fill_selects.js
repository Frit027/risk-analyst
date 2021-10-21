$( "#select-category" ).click(function() {
    $.post( "/req_cond", { cat_ids: $('#select-category').val().map(Number) }, function(data) {
        fill_selects_req_cond(data.requirements, data.conditions)
    }, "json");
});

$( "#clear_selected_category" ).click(function() {
    $('#select-category').prop('selectedIndex', -1);
    $.post( "/all_req_cond", function(data) {
        fill_selects_req_cond(data.requirements, data.conditions)
    }, "json");
});

$( "#clear_selected_req" ).click(function() {
    $('#select-req').prop('selectedIndex', -1);
    $.post( "/clear_req", function() {});
});

$( "#clear_selected_cond" ).click(function() {
    $('#select-cond').prop('selectedIndex', -1);
    $.post( "/clear_cond", function() {});
});

$( "#clear_selected_sol" ).click(function() {
    $('#select-solution').prop('selectedIndex', -1);
    $.post( "/clear_sol", function() {});
});

function fill_selects_req_cond(requirements, conditions) {
    let select_req = $("#select-req");
    let select_cond = $("#select-cond");

    select_req.empty()
    $.each(requirements, function() {
        select_req.append($("<option />").val(this.id).text(this.name));
    });

    select_cond.empty()
    $.each(conditions, function() {
        select_cond.append($("<option />").val(this.id).text(this.name));
    });
}