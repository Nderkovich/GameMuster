$('#sidebar').css({
    maxHeight: $(document).height() + 'px'
});

$('#collapseMenu').on('show.bs.collapse', function () {
    $('#sidebar').attr('class', 'col-2 bg-danger');
});

$('#collapseMenu').on('hide.bs.collapse', function () {
    $('#sidebar').attr('class', 'col-2');
})

var $range = $(".js-range-slider"),
    $inputFrom = $(".js-input-from"),
    $inputTo = $(".js-input-to"),
    instance,
    min = 0,
    max = 10,
    from = 0,
    to = 10;

$range.ionRangeSlider({
    skin: "round",
    type: "double",
    min: min,
    max: max,
    from: 0,
    to: 10,
    step: 0.1,
    onStart: updateInputs,
    onChange: updateInputs
});
instance = $range.data("ionRangeSlider");

function updateInputs(data) {
    from = data.from;
    to = data.to;

    $inputFrom.prop("value", from);
    $inputTo.prop("value", to);
}

$inputFrom.on("input", function () {
    var val = $(this).prop("value");

    // validate
    if (val < min) {
        val = min;
    } else if (val > to) {
        val = to;
    }

    instance.update({
        from: val
    });
});

$inputTo.on("input", function () {
    var val = $(this).prop("value");

    // validate
    if (val < from) {
        val = from;
    } else if (val > max) {
        val = max;
    }

    instance.update({
        to: val
    });
});