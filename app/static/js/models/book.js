var app = app || {};

app.Book = Backbone.Model.extend({
    defaults: {
        coverImage: 'img/placeholder.png',
        name: 'No title',
        info: 'Unknown',
        releaseDate: 'Unknown',
    },
    parse: function(response){
        console.log(response);
        return response;
    } 
});
