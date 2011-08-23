(function(window, $) {

  window._results = {};

  var search = $('input[type="text"]'),
      geocoder = new google.maps.Geocoder();

  search.autocomplete({
    select: function(event, ui) {
        var url = '/search/?',
            value = ui.item.value,
            parameters = window._results[value];
        parameters['q'] = value;
        console.log(parameters);
        window.location = url + $.param(parameters);
    },
    source: function(request, response) {
      // Grab the source objects from Google Maps.
      var southwest = new google.maps.LatLng(37.68, -122.57),
          northeast = new google.maps.LatLng(37.84, -122.35),
          bounds = new google.maps.LatLngBounds(southwest, northeast);

      geocoder.geocode({
          'address': request.term,
          'bounds': bounds
      }, function(results, status){
           response($.map(results, function(item){
               var location = item.geometry.location,
                   coordinates = {
                    'lat': location.lat(),
                    'lng': location.lng()
                   };
             window._results[item.formatted_address] = coordinates;
             return {
               label: item.formatted_address,
               value: item.formatted_address
             }
           }));
        });
    }
  });
})(window, jQuery);
