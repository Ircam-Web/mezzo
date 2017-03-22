var Instagram = function() {

    this.feed = null;

    //
    // Init
    //
    this.init();

};

Instagram.prototype.init = function() {

    var that = this;

    $('.instagram').lightSlider({
        item: 3,
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

module.exports = Instagram;
