/**
 * testing widgets
 */
(function( $, undefined ) {

$('.widget.bargraph-type').bargraphType({dataSource: 'data/open_requests_by_type.json'});
$('.widget.sparkline').sparkline();
$('.widget.pie-type').pieType();
$('.widget.top-open-requests').topOpenRequests();

})( jQuery );