//Coordinates of NYC
var lat = 40.730610, lng= -73.935242;
var map;
var viewModel;
var infowindow;
var fourSquareClientID =  'ER04ZOC0MLWDLIX5QWUNOBB5SHFUU11CENIEYS12XTBKKTR2';
var fourSquareClientSecret =  'PPHUYGEYGSSCTPKO1A5RKU1QY2KNPIZNR2OS4L5W0KQUF2XI';   
var fourSquareURL = 'https://api.foursquare.com/v2/venues/search?client_id=' +
 fourSquareClientID + 
 '&client_secret=' + 
 fourSquareClientSecret + 
 '&v=20130815' +'&ll=' + 
 lat + ',' + lng + 
 '&query=' + 
 'library' + 
 '&limit=' + 15 + 
 '&intent=browse&radius=2000';


// Venue constructor
var Venue = function(data) {
  //Copy the data locally
  this.name = data.name;
  this.lat = data.location.lat;
  this.lng = data.location.lng;
  this.url = data.url;
  this.formattedAddress = data.location.formattedAddress;
  this.marker =  new google.maps.Marker({
                        map: map,
                        position: {lat: this.lat, lng: this.lng},
                        title: data.name,
                        animation: google.maps.Animation.DROP
                    });

    var contentHTML =  '<h3>' + data.name + '</h3>' +
                      '<p>Address: ' + this.formattedAddress + '</p>';
    if(data.url){
      contentHTML = contentHTML + '<a href="' + data.url + '" target="_blank">' + data.url + '</a>';
    }
    this.marker.contentString = contentHTML;
    this.marker.addListener('click', markerClickHandler);
};

// ViewModel
var ViewModel = function() {
    var self = this;
    self.searchString = ko.observable('');
    self.venues = ko.observableArray([]);

    self.getVenues = ko.computed(function() {
      $.get(fourSquareURL, function (result) {
            for (var venue in result.response.venues){
              self.venues.push(new Venue(result.response.venues[venue]));
            }
          });
      });

    self.filteredVenues = ko.computed(function() {
      var filter = self.searchString().toLowerCase();
      if (!filter) {
        self.venues().forEach(function(venue){ venue.marker.setVisible(true); });
        return self.venues();
      } else {
          return ko.utils.arrayFilter(self.venues(), function(venue) {
            var isIncluded = venue.name.toLowerCase().indexOf(filter) !== -1;
            venue.marker.setVisible(isIncluded);
            return isIncluded;
          });
        }
    });

    // Triggers the same event as a click on a marker
    self.markerClickHandler = function(venue){
      google.maps.event.trigger(venue.marker, 'click');
    };
};

//Is called once the google maps api is loaded
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14,
    mapTypeControl: false,
    center: {lat:lat,lng:lng}
  });
  infowindow = new google.maps.InfoWindow();
  viewModel = new ViewModel(); 
  ko.applyBindings(viewModel);  
}


function markerClickHandler(){
  var marker = this;
  viewModel.venues().forEach(function(Venue){
    Venue.marker.setAnimation(null);
  });
  marker.setAnimation(google.maps.Animation.BOUNCE);
  setTimeout(function(){
    marker.setAnimation(null);
  },750);
  infowindow.setContent(this.contentString);
  infowindow.open(map, this);
}

