var LightSliderPersonsInit = function() {

    this.feed = null;

    //
    // Init
    //
    this.init();

};

LightSliderPersonsInit.prototype.init = function() {

    var that = this;

    $('[data-slider-persons]').lightSlider({
        item: 2,
        slideMargin: 0,
        pager: false,
        loop: true,
        auto: true,
        pauseOnHover: true,
        responsive: [
            {
                breakpoint: 752,
                settings: {
                    item: 2
                }
            },
            {
                breakpoint: 480,
                settings: {
                    item: 1
                }
            }
        ]
    });

};

module.exports = LightSliderPersonsInit;
