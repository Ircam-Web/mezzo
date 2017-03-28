var RoleSelector = function() {

    this.$element = null;

    //
    // Init
    //
    this.init();

};

RoleSelector.prototype.init = function() {

    var that = this;

    that.$element = $('.role-switcher');

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
        that.changeUrl($(this).attr('data-url'));
        return false;

    });

};

RoleSelector.prototype.changeUrl = function(lang) {

    window.location.href = lang;

}

module.exports = RoleSelector;
