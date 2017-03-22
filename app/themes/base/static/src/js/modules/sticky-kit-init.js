var StickyKitInit = function() {

    this.elements = [];
    this.pageContentTop = -1;
    this.pageContentBottom = -1;

    //
    // Init
    //
    this.init();

};

StickyKitInit.prototype.init = function() {

    var that = this,
        options = {},
        data, element, $element;

    var sliders = $('.page__slider');
    if(sliders.length > 0) {
        that.pageContentTop = $(sliders[0]).offset().top - 72;
        that.pageContentBottom = that.pageContentTop + (sliders.length * 724) + 72;
    }

    $('[data-sticky]').each(function(i) {

        $element = $(this);
        $element.on('sticky_kit:bottom', function(e) {
            var $self = $(this);
            $(this).parent().parent().css('position', 'static');
            $(this).parent().css('position', 'static');
            $(this).addClass('to-bottom');
        })
        .on('sticky_kit:unbottom', function(e) {
            $(this).parent().parent().css('position', 'relative');
            $(this).parent().css('position', 'relative');
            $(this).removeClass('to-bottom');
        });

        data = $(this).data();

        if(data.stickyOffset) {
            options.offset_top = data.stickyOffset;
        }
        if(data.stickyParent) {
            options.parent = '.' + data.stickyParent;
        }

        element = {
            $element: $(this),
            options: options,
            data: $(this).data(),
            attached: false
        };
        that.elements.push(element);
        that.attach(element);

    });

    $(window).resize( $.throttle(1000, that.windowResize.bind(that)) );
    $(window).scroll( that.windowScroll.bind(that) );
    that.windowScroll();

};

StickyKitInit.prototype.windowScroll = function(e) {

    var that = this;

    if(that.pageContentTop >= 0 && that.pageContentBottom >= 0) {
        for(var i=0; i<that.elements.length; i++) {

            if(that.elements[i].attached) {

                var height = that.elements[i].$element.height();
                var top = $(window).scrollTop();
                if(top >= (that.pageContentTop - height) && top < (that.pageContentBottom)) {
                    that.elements[i].$element.addClass('faded');
                } else {
                    console.log('remove');
                    that.elements[i].$element.removeClass('faded');
                }

            }

        }
    }

};

StickyKitInit.prototype.windowResize = function(e) {

    var that = this,
        windowWidth = $(window).width();

    for(var i=0; i<that.elements.length; i++) {

        if(that.elements[i].data.stickyDetachAt) {

            if(windowWidth > that.elements[i].data.stickyDetachAt && !that.elements[i].attached) {
                that.attach(that.elements[i]);
            }

            if(windowWidth <= that.elements[i].data.stickyDetachAt && that.elements[i].attached) {
                that.detach(that.elements[i]);
            }

        }

    }

};

StickyKitInit.prototype.attach = function(element) {

    var that = this;

    if(element.data.stickyDetachAt) {

        var $window = $(window);

        //
        // Attach if window width is larger
        //
        if($window.width() > element.data.stickyDetachAt) {

            element.$element.stick_in_parent(element.options);
            element.attached = true;

        }

    } else {

        element.$element.stick_in_parent(element.options);
        element.attached = true;

    }

};

StickyKitInit.prototype.detach = function(element) {

    element.$element.trigger("sticky_kit:detach");
    element.attached = false;

};

module.exports = StickyKitInit;
