/**
 * testing widgets
 */
(function( $, undefined ) {

$('.top-open-requests').barchartGoogleTopOpenRequests();
$('.map-google-example').mapGoogleExample({dataSource: 'data/ServiceRequests_Complete.json'});
$('.sparkline').sparklineExample();
$('.open-vs-closed').pieRaphaelOpenClosed();
$('#search').searchType();


//$('.gauge').gaugeGoogleActualEstResponseTime({dataSource: 'data/ClosedServiceRequests_By_SingleServiceType_Slice'});

// $('.map').map();


// Example loading events (Doesnt work)
/*
$('#dashboard div').bind('loading', function() {
  alert('loading...');
});
$('#dashboard div').bind('loaded', function() {
  alert('loaded');
});
*/

})( jQuery );
