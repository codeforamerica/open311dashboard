/**
 * testing widgets
 */
(function( $, undefined ) {

$('.widget.gauge').gauge();
$('.widget.bargraph-type').bargraphType({dataSource: 'data/open_requests_by_type.json'});
$('.widget.sparkline').sparkline();
$('.widget.sparkline').pieType();

})( jQuery );