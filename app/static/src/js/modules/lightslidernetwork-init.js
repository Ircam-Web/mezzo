var LightSliderNetworkInit = function() {

    this.slider = null;
    this.map = null;
    this.markers = [];
    this.currentLine = null;
    this.animationInterval = null;

    //
    // Init
    //
    this.init();

};

LightSliderNetworkInit.prototype.init = function() {

    var that = this;

    //
    // Slider init
    //
    /*that.slider = $('[data-slider-network]').lightSlider({
        item: 4,
        slideMargin: 10,
        pager: false,
        controls: false,
        loop: false,
        adaptiveHeight: true,
        onSliderLoad: function(elem) {
            elem.parents('.slider-network').find('.lSPrev').click(function(e) {
                elem.goToPrevSlide();
            });
            elem.parents('.slider-network').find('.lSNext').click(function(e) {
                elem.goToNextSlide();
            });
        },
        onBeforeSlide: function(elem) {
            if (that.currentLine) {
                that.currentLine.setMap(null);
            }
        }
    });*/

    //
    // Init map
    //
    if($('#network-map').length > 0) {

        that.map = new google.maps.Map(document.getElementById('network-map'), {
            zoom: 10,
            center: {lat: 48.85982, lng: 2.351402},
            //styles: [ { "featureType": "all", "elementType": "labels", "stylers": [ { "visibility": "off" } ] }, { "featureType": "administrative", "elementType": "labels.text", "stylers": [ { "visibility": "off" } ] }, { "featureType": "landscape", "elementType": "all", "stylers": [ { "color": "#6c8080" }, { "visibility": "simplified" } ] }, { "featureType": "landscape.man_made", "elementType": "geometry.fill", "stylers": [ { "lightness": "0" }, { "color": "#000f24" } ] }, { "featureType": "landscape.natural", "elementType": "geometry.fill", "stylers": [ { "lightness": "0" }, { "color": "#000f24" } ] }, { "featureType": "landscape.natural.landcover", "elementType": "geometry.fill", "stylers": [ { "saturation": "0" }, { "lightness": "0" }, { "color": "#000f24" } ] }, { "featureType": "landscape.natural.terrain", "elementType": "geometry.fill", "stylers": [ { "color": "#000f24" } ] }, { "featureType": "landscape.natural.terrain", "elementType": "geometry.stroke", "stylers": [ { "saturation": "0" }, { "lightness": "0" } ] }, { "featureType": "poi", "elementType": "all", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road", "elementType": "all", "stylers": [ { "visibility": "simplified" } ] }, { "featureType": "road", "elementType": "labels.icon", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway", "elementType": "all", "stylers": [ { "color": "#d98080" }, { "hue": "#eeff00" }, { "lightness": 100 }, { "weight": 1.5 } ] }, { "featureType": "road.highway", "elementType": "labels", "stylers": [ { "visibility": "off" } ] }, { "featureType": "transit", "elementType": "labels", "stylers": [ { "visibility": "off" } ] } ]
            styles: [{"featureType":"all","elementType":"geometry","stylers":[{"color":"#ffffff"}]},{"featureType":"all","elementType":"labels.text.fill","stylers":[{"gamma":0.01},{"lightness":20}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"saturation":-31},{"lightness":-33},{"weight":2},{"gamma":0.8}]},{"featureType":"all","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"administrative.locality","elementType":"labels.text.fill","stylers":[{"color":"#050505"}]},{"featureType":"administrative.locality","elementType":"labels.text.stroke","stylers":[{"color":"#fef3f3"},{"weight":"3.01"}]},{"featureType":"administrative.neighborhood","elementType":"labels.text.fill","stylers":[{"color":"#0a0a0a"},{"visibility":"off"}]},{"featureType":"administrative.neighborhood","elementType":"labels.text.stroke","stylers":[{"color":"#fffbfb"},{"weight":"3.01"},{"visibility":"off"}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"lightness":30},{"saturation":30}]},{"featureType":"poi","elementType":"geometry","stylers":[{"saturation":20}]},{"featureType":"poi.attraction","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"lightness":20},{"saturation":-20}]},{"featureType":"road","elementType":"geometry","stylers":[{"lightness":10},{"saturation":-30}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"saturation":25},{"lightness":25}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#a1a1a1"}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#292929"}]},{"featureType":"road.highway","elementType":"labels.text.fill","stylers":[{"visibility":"on"},{"color":"#202020"}]},{"featureType":"road.highway","elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"}]},{"featureType":"road.highway","elementType":"labels.icon","stylers":[{"visibility":"simplified"},{"hue":"#0006ff"},{"saturation":"-100"},{"lightness":"13"},{"gamma":"0.00"}]},{"featureType":"road.arterial","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#686868"}]},{"featureType":"road.arterial","elementType":"geometry.stroke","stylers":[{"visibility":"off"},{"color":"#8d8d8d"}]},{"featureType":"road.arterial","elementType":"labels.text.fill","stylers":[{"visibility":"on"},{"color":"#353535"},{"lightness":"6"}]},{"featureType":"road.arterial","elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"weight":"3.45"}]},{"featureType":"road.local","elementType":"geometry.fill","stylers":[{"color":"#d0d0d0"}]},{"featureType":"road.local","elementType":"geometry.stroke","stylers":[{"lightness":"2"},{"visibility":"on"},{"color":"#999898"}]},{"featureType":"road.local","elementType":"labels.text.fill","stylers":[{"color":"#383838"}]},{"featureType":"road.local","elementType":"labels.text.stroke","stylers":[{"color":"#faf8f8"}]},{"featureType":"water","elementType":"all","stylers":[{"lightness":-20}]}]
        });

        google.maps.event.addListenerOnce(that.map, 'projection_changed', function() {
            that.initMarkers();
        });

        google.maps.event.addListener(that.map, 'zoom_changed', function() {
            if (that.map.getZoom() < 3) that.map.setZoom(3);
        });

    }

};

LightSliderNetworkInit.prototype.initMarkers = function() {

    var that = this;

    $('[data-marker-idx]').each(function(idx) {

        var obj = {
            'lat': parseFloat($(this).attr('data-marker-lat').replace(',', '.')),
            'lng': parseFloat($(this).attr('data-marker-lng').replace(',', '.')),
            'elem': $(this),
            'marker': new google.maps.Marker({
                position: {lat: parseFloat($(this).attr('data-marker-lat').replace(',', '.')), lng: parseFloat($(this).attr('data-marker-lng').replace(',', '.'))},
                map: that.map,
                icon: "/static/img/map-marker-" + $(this).attr('data-marker-color') + ".png"
            })
        };

        var info = new google.maps.InfoWindow({
            content: '<div class="map-infowindow"><div class="map-infowindow__image"><a href="' + $(this).attr('data-marker-url') + '" target="_blank"><img src="' + $(this).attr('data-marker-image') + '" /></a></div><div class="map-infowindow__content"><div class="map-infowindow__title">' + $(this).find('[data-marker-title]').text() + '</div><div class="map-infowindow__subtitle">' + $(this).find('[data-marker-subtitle]').text() + '</div><p>' + $(this).find('[data-marker-description]').text() + '</p></div></div>'
        });

        obj.info = info;

        obj.marker.addListener('click', function() {
            that.markers.forEach(function(m, i) {
                m.info.close();
            });
            info.open(that.map, obj.marker);
        });

        that.markers.push(obj);

    });

};

module.exports = LightSliderNetworkInit;
