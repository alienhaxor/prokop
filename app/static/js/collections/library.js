var app = app || {};

app.Library = Backbone.Collection.extend({
    model: app.Book,
    url: '/api/v1.0/projects',
    parse: function(response){
        console.log(response.Projects);
        return response.Projects;
    } 
});