//Switching between types of maps
$(function(){    
        
  var map_choice = $('select#map_choice').selectmenu({
    select: function(event, options) {
            if(options.value == 1){
                response_time_map.visible(true);
                response_lines.visible(true);
                density_map.visible(false);
                density_lines.visible(false);
                $('#legend').html('<img src="images/response_key-1.png" alt="Legend for Response Time Map" width="300" height="62"/><div id="low">Fast to Slow Response</div>');
            } else {
                response_time_map.visible(false);
                response_lines.visible(false);
                density_map.visible(true);
                density_lines.visible(true);
                $('#legend').html('<img src="images/density_key.png" alt="Legend for Density Map" width="300" height="62"/><div id="low">Low to High Density</div>');
            }
    }
  });
});
