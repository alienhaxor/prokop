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
                "click input[type=radio]": "onRadioClick"
        },

        addBook: function( e ) {
                e.preventDefault();

                var formData = {};

                $( '#addBook div' ).children( 'input' ).each( function( i, el ) {
                        if( $( el ).val() != "" )
                        {
                                if( el.id === 'keywords' ) {
                                        formData[ el.id ] = [];
                                        _.each( $( el ).val().split( ' ' ), function( keyword ) {
                                                formData[ el.id ].push({ 'keyword': keyword });
                                        });
                                } else {
                                        formData[ el.id ] = $( el ).val();
                                }
                        }
                });

                this.collection.create( formData );
        },

        onRadioClick: function(e) {
            var coverImage = $('input:radio[name=coverImageRadios]:checked').val();
            $.each(StartProject.filesData.items, function() {
                if (this.file == coverImage) {
                    this.cover = 1;
                } else {
                    this.cover = 0;
                }
            });

            var filesDataJson = JSON.stringify(StartProject.filesData);
            console.log(filesDataJson);

            $('input[name="fileField"]').val(filesDataJson);

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