/**
 * testing widgets
 */
(function( $, undefined ) {

$('.top-open-requests').barchartGoogleTopOpenRequests();
$('.map-google-example').mapGoogleExample({dataSource: 'data/ServiceRequests_Complete.json'});
$('.sparkline').sparklineExample();
$('.open-vs-closed').pieRaphaelOpenClosed();
$('#search').searchType();

$('.gauge').gaugeGoogleActualEstResponseTime();
// $('.map').map();


})( jQuery );
