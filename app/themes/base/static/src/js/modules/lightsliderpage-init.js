var LightSliderPageInit = function() {

    this.elements = [];

    //
    // Init
    //
    this.init();

};

LightSliderPageInit.prototype.init = function() {

    var that = this,
        element,
        elements = $('[data-slider-page]');

    elements.each(function(idx) {

        element = {
            $element: $(this),
            attached: 1,
            slider: null,
            options: {
                autoWidth: true,
                item: 4,
                pager: false,
                responsive: [
                    {
                        breakpoint: 752,
                        settings: {
                            autoWidth: false,
                            adaptiveHeight: true,
                            item: 1
                        }
                    }
                ],
                onBeforeSlide: function(el) {
                    $(el).find('video').each(function(i) {
                        this.pause();
                    });
                },
                onSliderLoad: function (el) {

                    var maxHeight = 0,
                    container = $(el),
                    children = container.children();

                    el.lightGallery({
                        selector: '.slider-page .lslide',
                        download: false
                    });

                    children.each(function () {
                        var childHeight = $(this).height();
                        if (childHeight > maxHeight) {
                            maxHeight = childHeight;
                        }
                    });
                    container.height(maxHeight);
                }
            }
        };

        that.elements.push(element);

    });

    elements.imagesLoaded( function() {

        that.windowResize();
        $(window).resize( $.throttle(1000, that.windowResize.bind(that)) );

    });

};

LightSliderPageInit.prototype.windowResize = function(e) {

    var that = this,
        windowWidth = $(window).width(),
        totalWidth, element;

    for(var i=0; i<that.elements.length; i++) {

        element = that.elements[i];
        totalWidth = 0;

        element.$element.find('li.slider-page__slide').each(function() {

            var img =  $(this).find('img').get(0);

            if(img) {
                totalWidth += img.naturalWidth;
            } else {
                totalWidth += 905;
            }

        });

        if(totalWidth > windowWidth) {

            that.attach(that.elements[i]);

        } else {

            that.detach(that.elements[i]);

        }

    }

};

LightSliderPageInit.prototype.attach = function(element) {

    var that = this,
        windowWidth = $(window).width(),
        totalWidth = 0;

    element.$element.find('li').each(function() {
        totalWidth += $(this).find('img').width();
    });

    if(element.attached !== true) {
        element.slider = element.$element.lightSlider(element.options);
        element.$element.removeClass('flexbox');
        element.attached = true;
    }

};

LightSliderPageInit.prototype.detach = function(element) {

    var that = this;

    if(element.attached !== false) {
        if(element.slider) {
            element.slider.destroy();
            element.$element.lightSlider = $.fn.lightSlider;
        }
        element.slider = null;
        element.$element.addClass('flexbox');
        element.attached = false;
    }

};

module.exports = LightSliderPageInit;
