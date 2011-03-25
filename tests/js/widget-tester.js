/**
 * testing widgets
 */
(function( $, undefined ) {

$('.widget.bargraph-type').bargraphType({dataSource: 'data/open_requests_by_type.json'});
$('.widget.sparkline').sparkline();
$('.widget.sparkline').pieType();
$('.widget.map').map();

})( jQuery );
