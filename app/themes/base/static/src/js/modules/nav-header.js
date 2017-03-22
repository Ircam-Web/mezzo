var NavHeader = function() {

    this.$element = $('#navHeader');
    this.$elements = $('#navHeader .nav-header__item');

    //
    // Init
    //
    this.init();

};

NavHeader.prototype.init = function() {

    var that = this;

    that.$elements.hover(function(e) {

        var $submenu = $(this).find('.nav-header__submenu');

        if($submenu.length > 0) {

            var offsetLeft = $(this).position().left,
                originOffsetLeft = $('#navHeader .nav-header__item:first-child').position().left + 100,
                originWidth = that.$element.width();

            $(this).toggleClass('hover');

            $submenu.css('left', -offsetLeft + originOffsetLeft);
            $submenu.css('width', originWidth - 200);
            $submenu.toggle();

        }

    });

};

module.exports = NavHeader;
