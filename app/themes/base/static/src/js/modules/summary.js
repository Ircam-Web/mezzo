var Summary = function() {

    this.$summary = $('[data-summary]');
    this.$content = $('[data-summary-content]');
    this.$links = [];

    //
    // Init
    //
    this.init();

};

Summary.prototype.init = function() {

    var that = this,
        $template, sectionCount = 0;

    if(that.$summary.length == 1 && that.$content.length > 0) {

        $template = that.$summary.find('li:first-child');
        that.$content.each(function(idx) {

            $(this).find('h2:not(.page-box__title)').each(function(idx) {

                var $element = $(this),
                    $template_clone = $template.clone();

                $template_clone.find('a').text($element.text());
                $template_clone.find('a').attr('href', '#section-' + sectionCount);
                $template_clone.removeClass('hide');

                $template_clone.find('a').bind('click', function(e) {

                    e.preventDefault();
                    var self = $(this);
                    $('html, body').animate({
                		scrollTop:$(self.attr('href')).offset().top
                	}, 'slow');
                    return false;

                });

                that.$links.push($template_clone.find('a'));

                that.$summary.append($template_clone);

                $element.attr('id', "section-" + sectionCount);
                sectionCount++;

                $element.waypoint(function(direction) {
                    that.$links.forEach(function (elem) {
                        elem.removeClass('active');
                    });
                    $('[href="#' + $(this.element).attr('id') + '"]').addClass('active');
                }, {
                    offset: '200'
                });

                $element.waypoint(function(direction) {
                    that.$links.forEach(function (elem) {
                        elem.removeClass('active');
                    });
                    var sectionNumber = parseInt($(this.element).attr('id').substr(8));
                    sectionNumber--;
                    console.log(sectionNumber);
                    $('[href="#section-' + sectionNumber + '"]').addClass('active');
                }, {
                    offset: '50%'
                });

            });

        });

        $template.remove();

        // Scrollspy
        //$(document).on("scroll", that.onScroll.bind(that));

        // Row height
        if($('.page__sidebar .nav-tree--level-0').height() > $('.page__content').height()) {

            $('.page__content').css({
                'margin-bottom': $('.page__sidebar .nav-tree--level-0').height() - $('.page__content').height() + 48
            });

        }

    }

};

Summary.prototype.onScroll = function(e) {

    var scrollPos = $(document).scrollTop(),
        that = this,
        currentTitle, minDiff = 200;

    that.$links.forEach(function (elem) {
        var currLink = elem;
        var refElement = $(elem.attr("href"));
        var diff = refElement.offset().top - scrollPos;
        if(diff < minDiff && diff < 200) {
            minDiff = diff;
            currentTitle = refElement;
        }
        if (refElement.position().top <= scrollPos) {
            that.$links.forEach(function (elem) {
                elem.removeClass('active');
            });
            currLink.addClass("active");
        }
        else{
            currLink.removeClass("active");
        }
    });

    that.$links.forEach(function (elem) {
        elem.removeClass('active');
    });

    if(currentTitle) {
        $('[href="#' + currentTitle.attr('id') + '"]').addClass('active');
    }

};

module.exports = Summary;
