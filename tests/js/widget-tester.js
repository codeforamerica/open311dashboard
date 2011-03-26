/**
 * testing widgets
 */
(function( $, undefined ) {

$('.top-open-requests').barchartGoogleTopOpenRequests();
$('.map-google-example').mapGoogleExample({dataSource: 'data/ServiceRequests_Complete.json'});
$('.sparkline').sparklineExample();

$('.gauge').gauge();
$('#search').searchType();
// $('.map').map();
$('.open-vs-closed').openVsClosed();


})( jQuery );
