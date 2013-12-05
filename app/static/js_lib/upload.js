$(function(){
        
        var dropbox = $('#dropbox'),
                message = $('.message', dropbox);
        
        StartProject = {}

        StartProject.filesData = {"items":[]};

        dropbox.filedrop({
                paramname: 'file',
                maxfiles: 10,
            maxfilesize: 5,
                url: '/upload_file',
                uploadFinished:function(i,file,response){
                        $.data(file).addClass('done');

                        
   /*                     input = jQuery('<input name="fileField" type="hidden" value="'+file.name+'">');
                        jQuery('#addBook').append(input);
*/
                        StartProject.filesData.items.push(
                            { file: file.name, cover: 0}
                        );

                        var filesDataJson = JSON.stringify(StartProject.filesData);
                        console.log(filesDataJson);

                        $('input[name="fileField"]').val(filesDataJson);

                        $("#coverImage").append('<div class="radio"><label><input type="radio"\
                            name="coverImageRadios" value="'+file.name+'"></label>'+file.name+'</div>');

                },
                
            error: function(err, file) {
                        switch(err) {
                                case 'BrowserNotSupported':
                                        showMessage('Your browser does not support HTML5 file uploads!');
                                        break;
                                case 'TooManyFiles':
                                        alert('Too many files! Please select ' + this.maxfiles + ' at most!');
                                        break;
                                case 'FileTooLarge':
                                        alert(file.name + ' is too large! The size is limited to ' + this.maxfilesize + 'MB.');
                                        break;
                                default:
                                        break;
                        }
                },
                
                beforeEach: function(file){
                        if(!file.type.match(/^image\//)){
                                alert('Only images are allowed!');
                                return false;
                        }
                },
                
                uploadStarted:function(i, file, len){
                        createImage(file);
                },
                
                progressUpdated: function(i, file, progress) {
                        $.data(file).find('.progress').width(progress);
                }
             
        });
        
        var template = '<div class="preview">'+
                                                '<span class="imageHolder">'+
                                                        '<img />'+
                                                        '<span class="uploaded"></span>'+
                                                '</span>'+
                                                '<div class="progressHolder">'+
                                                        '<div class="progress"></div>'+
                                                '</div>'+
                                        '</div>'; 
        
        
        function createImage(file){

                var preview = $(template), 
                        image = $('img', preview);
                        
                var reader = new FileReader();
                
        image.width = 100;
                image.height = 100;

                reader.onload = function(e){
                        image.attr('src',e.target.result);
                };
                
                reader.readAsDataURL(file);
                
                message.hide();
                preview.appendTo(dropbox);
                
                $.data(file,preview);
        }

        function showMessage(msg){
                message.html(msg);
        }

});