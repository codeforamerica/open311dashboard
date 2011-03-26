/**
 * testing widgets
 */
(function( $, undefined ) {

$('.top-open-requests').barchartGoogleTopOpenRequests();
$('.map-google-example').mapGoogleExample({dataSource: 'data/ServiceRequests_Complete.json'});

$('.gauge').gauge();
$('#search').searchType();
$('.bargraph-type').bargraphType({dataSource: 'data/open_requests_by_type.json'});
$('.sparkline').sparkline();
$('.pie-type').pieType();
// $('.map').map();
$('.open-vs-closed').openVsClosed();


})( jQuery );
