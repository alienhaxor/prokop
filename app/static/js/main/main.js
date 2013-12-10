$(function () {
    //resizing, closing/opening info tabs in project page
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

    //adding tooltips
    $('.tooltip_custom').tooltip();

    //project_manage user handling
    $('#project_members').on('click', '.col-xs-5 .no_padding .col-xs-3 .user_move_button', function () {
        $removeStr = '<div class="col-xs-3"><a href="#" class="user_move_button btn btn-danger btn-block"><span class="glyphicon glyphicon-chevron-left"></span> Remove</a></div>';
        $acceptStr = '<div class="col-xs-3"><a href="#" class="user_move_button btn btn-success">Accept <span class="glyphicon glyphicon-chevron-right"></span></a></div>';
        $userStr = $(this).parent().siblings('.col-xs-9').text();
        $userUrlStr = $(this).parent().siblings('.col-xs-9').find('a').attr('href');
        if (($(this).closest('.col-xs-5').attr('id')) === 'signed_users') {
            //signed user, move this to #accepted_users 
            $('#accepted_users').append('<div class="no_padding">' + $removeStr + '<div class="col-xs-9"><a href="'+ $userUrlStr +'" class="btn btn-default btn-block">' + $userStr + '</a></div></div>');
            $(this).parent().parent().remove();
        } else if (($(this).closest('.col-xs-5').attr('id')) === 'accepted_users') {
            //accepted user, move this to #signed_users
            $('#signed_users').append('<div class="no_padding"><div class="col-xs-9"><a href="'+ $userUrlStr +'" class="btn btn-default btn-block">' + $userStr + '</a></div>'+$acceptStr);
            $(this).parent().parent().remove();
        }
    });

    //disabling the not chosen radiobutton input in project management and new project
    $('#PMediaRadio1').click(function () {
        $('#PMediaRadioTextInput2').attr('disabled', 'disabled');
        $('#PMediaRadioTextInput1').removeAttr('disabled');
    });
    $('#PMediaRadio2').click(function () {
        $('#PMediaRadioTextInput1').attr('disabled', 'disabled');
        $('#PMediaRadioTextInput2').removeAttr('disabled');
    });
    
});