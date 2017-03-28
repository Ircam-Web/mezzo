var HomeMenu = function() {

    //
    // Init
    //
    this.init();

    this.$menu = $('.home__menu-item');

};

HomeMenu.prototype.init = function() {

    var that = this,
        $elements = $('.home__menu-item a');

    $('.home__menu-item').hover(function() {

        $elements.removeClass('active');
        $(this).find('>a').addClass('active');
        $('.home__shutter').removeClass('active');
        $(this).find('.home__shutter').addClass('active');

    }, function() {

        $('.home__shutter').removeClass('active');
        $elements.removeClass('active');
        $($elements.get(0)).addClass('active');

    });

    /*$('.home__menu').bind('mouseleave', function() {

        $('.home__shutter').removeClass('active');
        $elements.removeClass('active');
        $($elements.get(0)).addClass('active');

    });*/

};

module.exports = HomeMenu;
