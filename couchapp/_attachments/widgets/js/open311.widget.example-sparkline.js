/*
 * Sparkline example
 *
 * Depends:
 *   jquery.ui.core.js
 *   jquery.ui.widget.js
 */
(function( $, undefined ) {

$.widget('Open311.sparklineExample', $.Open311.sparklineGoogle, {
  options: {
    title: 'Sparkline Example'
	},

	_create: function() {
		this.updateContent('<img src="http://chart.apis.google.com/chart?cht=lc&chs=380x70&chd=t:5,28,15.9,31.7,42.3,21,26.5,42.3,47.6,95.2,18.5,26.5,21.2,37.0,52.9,58.2,47.6,68.8,26.5,31.7,42.3&chco=336699&chls=1,1,0&chm=o,990000,0,20,4&chxt=r,x,y&chxs=0,990000,11,0,_|1,990000,1,0,_|2,990000,1,0,_&chxl=0:|8|1:||2:||&chxp=0,42.3"></img>');
	},
  
  /**
   * Destroy widget
   */
  destroy: function() {
    // Default destroy
    $.Widget.prototype.destroy.apply(this, arguments);
  }

});

})( jQuery );

