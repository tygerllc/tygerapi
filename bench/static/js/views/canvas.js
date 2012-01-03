define([
  'jquery',
  'underscore', 
  'backbone',
  ], function($, _, Backbone){

  var CanvasView = Backbone.View.extend({
  	el: $("#benchCanvas"),

  	initialize: function(){
  		_.bindAll(this, 'render');

      $(window).bind('resize', this.render);

  		this.render();
  	},

    render: function(){
      $(this.el).attr("height", $(window).height());
      $(this.el).attr("width", $(window).width());
    }
  });

  return CanvasView;
});