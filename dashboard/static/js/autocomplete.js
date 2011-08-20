$(function() {
  var search = $('input[type="text"]'),
      geocoder = new google.maps.Geocoder();

  search.autocomplete({
    source: function(request, response){
      // Grab the source objects from Google Maps.
      geocoder.geocode({'address': request.term}, function(results, status){
        response($.map(results, function(item){
          return {
            label: item.formatted_address,
            value: item.formatted_address
          }
        }));
      });
    }
  });
});
