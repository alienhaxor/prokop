$(function () {
    $(window).bind('resize load', function () {
        if ($(this).width() < 991) {
            $('.collapse').removeClass('in');
            $('.collapse').addClass('out');
        }
        else {
            $('.collapse').removeClass('out');
            $('.collapse').addClass('in');
        }
    });
    $('#description_tooltip').tooltip();
});