/**
 * testing widgets
 */
(function( $, undefined ) {

$('.top-open-requests').barchartGoogleTopOpenRequests();
$('.map-google-example').mapGoogleExample({dataSource: 'data/ServiceRequests_Complete.json'});

$('.gauge').gauge();
$('#search').searchType();
$('.sparkline').sparkline();
// $('.map').map();
$('.open-vs-closed').openVsClosed();


})( jQuery );
