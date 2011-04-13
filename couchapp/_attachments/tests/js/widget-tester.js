/**
 * testing widgets
 */
(function( $, undefined ) {

$('.top-open-requests').barchartGoogleTopOpenRequests();
$('.map-google-example').mapGoogleExample({dataSource: 'data/ServiceRequests_Complete.json'});
$('.sparkline').sparklineExample();
$('.open-vs-closed').pieRaphaelOpenClosed();
$('.available-data').barchartGoogleAvailableData();
$('.choropleth-example').choroplethMap();
$('.open-vs-closed-bar').barRaphaelOpenClosed();

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

// It is IMPORTANT to load the search widget last because it does a search automatically.
// You'll want the other widgets to be initialized before data is published.
$('#search').searchType();

})( jQuery );
