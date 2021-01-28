$(".lang_selection").click(function () {
    $("#language_input").val($(this).data('lang'));
    $("#language_next").val($(this).data('url'));
    $("#language_form").submit();
});
