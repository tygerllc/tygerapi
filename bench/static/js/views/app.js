define([
  'jquery',
  'underscore', 
  'backbone',
  'views/canvas',
  'views/tool'
  ], function($, _, Backbone, CanvasView, ToolPanelView){

  var AppView = Backbone.View.extend({
  	el: $("#appView"),

  	initialize: function(){
  		_.bindAll(this, 'render');
  		this.canvas = new CanvasView;
      this.toolPanel = new ToolPanelView({el:$("#toolPanel", this.el)});
  		this.render();
  	},

  	render: function(){
  		
  	}

  });
  return AppView;
});