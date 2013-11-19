var app = app || {};

app.LibraryView = Backbone.View.extend({
        el: $( '#books' ),

        initialize: function() {
                this.collection = new app.Library();
                this.collection.fetch();
                this.render();

                this.listenTo( this.collection, 'add', this.renderBook );
                this.listenTo( this.collection, 'reset', this.render );
        },

        events: {
                'click #add': 'addBook',
        },

        addBook: function( e ) {
                e.preventDefault();

                var formData = {};

                var image = new FormData($('form input[id=coverImage]'));
                console.log($('form input[id=coverImage]').val());

                //can perform client side field required checking for "fileToUpload" field
                $.ajaxFileUpload({
                    url:'doajaxfileupload.php',
                    secureuri:false,
                    fileElementId:'fileToUpload',
                    dataType: 'json',
                    success: function (data, status) {
                        if(typeof(data.error) != 'undefined') {
                            if(data.error != '') {
                                alert(data.error);
                            } else {
                                alert(msg); // returns location of uploaded file
                            }   
                        }
                    },
                    error: function (data, status, e) {
                        alert(e);
                    }
                })

                $( '#addBook div' ).children( 'input' ).each( function( i, el ) {
                    formData[ el.id ] = $( el ).val() || null;
                });

                this.collection.create( formData );
        },

        // render library by rendering each book in its collection
        render: function() {
                this.collection.each(function( item ) {
                        this.renderBook( item );
                }, this );
        },

        // render a book by creating a BookView and appending the
        // element it renders to the library's element
        renderBook: function( item ) {
                var bookView = new app.BookView({
                        model: item
                });
                this.$el.append( bookView.render().el );
        }
});