/**
 * testing widgets
 */
(function( $, undefined ) {

$('#search').searchType();
$('.bargraph-type').bargraphType({dataSource: 'data/open_requests_by_type.json'});
$('.sparkline').sparkline();
$('.pie-type').pieType();
$('.map').map();
$('.top-open-requests').topOpenRequests();
$('.map-google').mapGoogle({dataSource: 'data/ServiceRequests_Complete.json'});
$('.open-vs-closed').openVsClosed();

})( jQuery );
