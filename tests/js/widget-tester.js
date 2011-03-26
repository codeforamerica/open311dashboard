/**
 * testing widgets
 */
(function( $, undefined ) {


$('.gauge').gauge();
$('#search').searchType();
$('.bargraph-type').bargraphType({dataSource: 'data/open_requests_by_type.json'});
$('.sparkline').sparkline();
$('.pie-type').pieType();
// $('.map').map();
$('.top-open-requests').topOpenRequests();
$('.map-google-example').mapGoogleExample({dataSource: 'data/ServiceRequests_Complete.json'});
$('.open-vs-closed').openVsClosed();


})( jQuery );
