var CloseEscape = function() {

    this.$elements = $('[data-close-escape]');

    //
    // Init
    //
    this.init();

};

CloseEscape.prototype.init = function() {

    var that = this;

    $(document).keyup(function(e) {

        if(e.keyCode === 27) {

            that.$elements.removeClass('open');

        }

    });

};

module.exports = CloseEscape;
