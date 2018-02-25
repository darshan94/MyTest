
function getWeatherData(lat, long){
      var apiKey = "e2496ee0f518adf13d64f4c530155fc3";      
      var exclude = "?exclude=minutely,hourly,daily,alerts,flags";
      var unit = "?units=si";              
      var url = "https://api.darksky.net/forecast/" + apiKey + "/" + lat + "," + long + exclude + unit;           

//get darksky api data     
$.ajax({       
   url: url,       
   dataType: "jsonp",       
   success: function (weatherData) {          
      //icon information (explained after)         
      var icon = weatherData.currently.icon;         
      //weather description         
      var description = weatherData.currently.summary;
      //temperature
      var temperature = weatherData.currently.temperature;
   }     
 });  
}

/*https://darkskyapp.github.io/skycons/*/
$(document).ready(function() {
  
  var a_lat = "5.355934";
  var a_long = "100.302518";
  var skycons = new Skycons({"color": "#247BA0"});
  
  var listImages = {
        "clear-day": "https://image.ibb.co/m8yzQF/clear_day.jpg",
        "clear-night": "https://image.ibb.co/g9RxCv/clear_night.jpg",
        "partly-cloudy-day": "https://image.ibb.co/kqBKQF/partly_cloudy_day.jpg",
        "partly-cloudy-night": "https://image.ibb.co/jscR5F/partly_cloudy_night.jpg",
        "rain": "https://image.ibb.co/hyCtkF/rain_mobile.jpg",   
        "foggy": "https://image.ibb.co/mQ6m5F/foggy.jpg",
        "sleet": "https://image.ibb.co/eQj0Xv/sleet.jpg",
        "wind": "https://image.ibb.co/nLCnCv/wind.jpg",
        "snow": "https://image.ibb.co/k207Cv/snow.jpg",
        "cloudy": "https://image.ibb.co/mWBVXv/cloudy.jpg",
    };
  
  if (!navigator.geolocation){
    alert("Geolocation is not supported by this browser!");
    return;
  }
  navigator.geolocation.getCurrentPosition(showPosition, error);

  //HELPER FUNCTIONS

  function error() {
    alert("Unable to retrieve your location! Allow the browser to track your location!");
  }
  
function showPosition(position) {
    a_lat =  position.coords.latitude;
    a_long =  position.coords.longitude;
    getCityName(a_lat, a_long);
    getWeatherData(a_lat, a_long);
}

  function getWeatherData(lat, long){
     var apiKey = "ccb03959faa5ad7be9ab026a91147c1b";
     var exclude = "?exclude=minutely,hourly,daily,alerts,flags";
     var unit = "?units=si";
     var url = "https://api.darksky.net/forecast/" + apiKey + "/" + lat + "," + long + exclude + unit;
     
    //get darksky api data
    $.ajax({
      url: url,
      dataType: "jsonp",
      success: function (weatherData) { 
        //icon
        console.log(weatherData.currently.icon);
        skycons.add(document.getElementById("icon1"), weatherData.currently.icon);
        skycons.play();
        //description
        $('#weather-description').text(weatherData.currently.summary);
        //change background image
        setBackgroundImg(weatherData.currently.icon);
        //temperature
        var celsius = toCelsius(weatherData.currently.temperature);
        $('#weather-value').html(celsius + '<a  id="convert" href="#" class="btn btn-primary btn_temp">°C</a>');
        $('#weather-value').val(celsius);
      }
    });
  }
  
  function setBackgroundImg(description){
    $('body').fadeTo('slow', 0.3, function(){
        $('html').css('background-image',"url("+listImages[description]+")");
        $('.containerBlock').css('visibility',"visible");
    }).delay( 500 ).fadeTo('slow', 1); 
  }
  
  /*function checkPosition(url) {
      if (window.matchMedia('(max-width: 767px)').matches) {
          $('body').css('backgroundimage',"url(https://image.ibb.co/gB3AXv/partly_cloudy_day_mobile.jpg)");
        console.log("BBB");
      } else {
       $('body').css('backgroundimage',"url("+url+")");
        console.log("AAA");
      }
  }*/
 
  function getCityName(lat, long){
    var cityName;
    var countryCode;
    var countryName;
    
    var url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+ lat + "," + long;
    $.getJSON(url, function(data) {
          var arr_address_comp = data.results[0].address_components;
          arr_address_comp.forEach(function(val) {
              if(val.types[0] === "locality" ){
                 cityName = val.long_name;
              }
              if(val.types[0] === "country" ){
                   countryCode = val.short_name;
                   countryName = val.long_name;
              }
        });
        $('#weather-location').text(cityName + ", " + countryName);   
    });
  }
  
  function toCelsius(f) {
    return Math.round((5/9) * (f-32));
  }
  
  function toFahrenheit(c){
    return Math.round(c * 9 / 5 + 32);
  }
  //click event to convert temperature
  $(document).on('click', '#convert', function(){
        
         if($("#convert").text() == "°C"){
             var temp = $("#weather-value").val();
             var far = toFahrenheit($("#weather-value").val());
             $('#weather-value').html(far + '<a  id="convert" href="#" class="btn btn-primary btn_temp">°F</a>');
             $("#weather-value").val(far);    
         }else{
             var cel = toCelsius($("#weather-value").val());
             $('#weather-value').html(cel + '<a  id="convert" href="#" class="btn btn-primary btn_temp">°C</a>');
             $("#weather-value").val(cel);
         }
      });
}); 

/*function showError(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED: 
      x.innerHTML = "User denied the request for Geolocation."
      break;
    case error.POSITION_UNAVAILABLE:
      x.innerHTML = "Location information is unavailable."
      break;
    case error.TIMEOUT:
      x.innerHTML = "The request to get user location timed out."
      break;
    case error.UNKNOWN_ERROR:
      x.innerHTML = "An unknown error occurred."
      break;
  }
}*/
