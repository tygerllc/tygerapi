define([
  'jquery',
  'underscore', 
  'backbone',
  'views/canvasView',
  'views/homeView',
  'models/solutions'
  ], function($, _, Backbone, CanvasView, HomeView, Solutions){

  var App = Backbone.Router.extend({
    routes:{
      '': 'home',
      ':slug': 'solution'
    },

    initialize: function(){
      _.bindAll(this);

      this.solutions = new Solutions();
      this.homeView = new HomeView({solutions:this.solutions});
      this.canvasView = false;
    },

    home: function(){
      _this = this;
      this.loadSolutions(function(){
        if(_this.canvasView){_this.canvasView.unrender();}
        $("#appView").html(_this.homeView.render().el);
      });
    },

    solution: function(slug){
      _this = this;
      if(this.solutions.length == 0){
        this.loadSolutions(function(){
          solution = _this.validateSlug(slug);
          if(solution){
            _this.showCanvas(solution);
          }
        });
      }
      else{
        solution = this.validateSlug(slug);
        if(solution){
          this.showCanvas(solution);
        }
      }
    },

    loadSolutions:function(callback){
      this.solutions.fetch({success:callback}); 
    },

    showCanvas: function(solution){
      this.canvasView = new CanvasView({model:solution});
      $("#appView").fadeOut(function(){
        $(this).html(_this.canvasView.render().el);
        $(this).show();
      });
    },

    validateSlug: function(slug){
      solution = this.solutions.getBySlug(slug);
      if(!solution){ //If not found, redirect to Bench Home.
        this.navigate('',true);
        return false;
      }      
      return solution;
    }

  });
  return App;
});