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
        $dataUrl = $(this).attr('data-url');
        $removeStr = '<div class="col-xs-3"><button data-url="'+$dataUrl+'" class="remove_user user_move_button btn btn-danger btn-block"><span class="glyphicon glyphicon-chevron-left"></span> Remove</button></div>';
        $acceptStr = '<div class="col-xs-3"><button data-url="'+$dataUrl+'" class="accept_user user_move_button btn btn-success">Accept <span class="glyphicon glyphicon-chevron-right"></span></button></div>';
        $userStr = $(this).parent().siblings('.col-xs-9').text();
        $userUrlStr = $(this).parent().siblings('.col-xs-9').find('a').attr('href');
        
        if (($(this).closest('.col-xs-5').attr('id')) === 'signed_users') {
            //signed user, move this to #accepted_users 

            var role = 'worker_confirmed'
            $.ajax({
                url: $dataUrl+role,
                type: 'POST',
                data: {submit:true}, // An object with the key 'submit' and value 'true;
                success: function (result) {
                  console.log(result);
                }
            });  

            $('#accepted_users').append('<div class="no_padding">' + $removeStr + '<div class="col-xs-9"><a href="'+ $userUrlStr +'" class="btn btn-default btn-block">' + $userStr + '</a></div></div>');
            $(this).parent().parent().remove();
        
        } else if (($(this).closest('.col-xs-5').attr('id')) === 'accepted_users') {
            //accepted user, move this to #signed_users

            var role = 'worker'
            $.ajax({
                url: $dataUrl+role,
                type: 'POST',
                data: {submit:true}, // An object with the key 'submit' and value 'true;
                success: function (result) {
                  console.log(result);
                }
            });

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


    $('#project_apply').click(function() {
        var url = $(this).attr('data-url');
        var message = 'You applied to the project! We will email you to let you know if you got accepted.'
        console.log(url);
            $.ajax({
                url: url,
                type: 'POST',
                //data: {submit:true}, // An object with the key 'submit' and value 'true;
                success: function (result) {
                    $('.project_apply_buttons').replaceWith('<div class="success">'+message+'/div>');

                }
            });  

    });

    
});