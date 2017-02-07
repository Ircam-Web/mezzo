var LangSelector = function() {

    this.$element = null;
    this.$elementMobile = null;

    //
    // Init
    //
    this.init();

};

LangSelector.prototype.init = function() {

    var that = this;

    that.$element = $('#langSelector');
    that.$element.find('li:first-child a').click(function(e) {

        e.preventDefault();
        that.$element.toggleClass('open');

        if(that.$element.hasClass('open')) {

            that.$element.one('mouseleave', function() {
                that.$element.removeClass('open');
            })

        }

        return false;

    });

    that.$element.find('li:not(:first-child) a').click(function(e) {

        e.preventDefault();
        that.changeLanguage($(this).attr('data-lang'));
        return false;

    });

    that.$elementMobile = $('#langSelectorMobile');
    that.$elementMobile.find('a').click(function(e) {

        e.preventDefault();
        that.changeLanguage($(this).attr('data-lang'));
        return false;

    });

    $('[data-lang]').click(function() {

        that.changeLanguage($(this).attr('data-lang'));

    });

};

LangSelector.prototype.changeLanguage = function(lang) {

    $('#language_selector_select').val(lang);
    $('#language_selector_form').submit();

}

module.exports = LangSelector;
