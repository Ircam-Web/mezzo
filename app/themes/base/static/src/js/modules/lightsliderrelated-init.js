var LightSliderRelatedInit = function() {

    this.slider = null;

    //
    // Init
    //
    this.init();

};

LightSliderRelatedInit.prototype.init = function() {

    var that = this;

    that.slider = $('[data-slider-related]').lightSlider({
        item: 1,
        slideMargin: 0,
        pager: false,
        loop: true,
        auto: false,
        pauseOnHover: true,
        responsive: [
            {
                breakpoint: 752,
                settings: {
                    item: 1
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

module.exports = LightSliderRelatedInit;
