var app = app || {};

app.Book = Backbone.Model.extend({
    defaults: {
        coverImage: 'static/img/placeholder.png',
        fileField: false,
        name: 'No title',
        desc: 'Unknown',
        releaseDate: 'Unknown',
    },
    parse: function(response){
        console.log(response);
        return response;
    } 
});
