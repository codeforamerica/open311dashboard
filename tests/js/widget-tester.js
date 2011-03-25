/**
 * testing widgets
 */
(function( $, undefined ) {

$('.bargraph-type').bargraphType({dataSource: 'data/open_requests_by_type.json'});
$('.sparkline').sparkline();
$('.pie-type').pieType();
$('.top-open-requests').topOpenRequests();

})( jQuery );