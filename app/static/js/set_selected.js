if (typeof ids !== 'undefined') {
    $.each(ids.cat_ids, function() {
        $(`#select-category option[value=${this}]`).attr("selected", "selected");
    });
    $.each(ids.req_ids, function() {
        $(`#select-req option[value=${this}]`).attr("selected", "selected");
    });
    $.each(ids.cond_ids, function() {
        $(`#select-cond option[value=${this}]`).attr("selected", "selected");
    });
    if ($('#select-solution').length) {
        $.each(ids.sol_ids, function () {
            $(`#select-solution option[value=${this}]`).attr("selected", "selected");
        });
    }
}