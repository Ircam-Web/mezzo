var VideoOverlay = function() {

    this.$overlay = $('#overlay');
    this.$overlayContent = $('#overlayContent');

    //
    // Init
    //
    this.init();

};

VideoOverlay.prototype.init = function() {

    var that = this;

    $('[data-video-overlay]').click(function(e) {
        e.preventDefault();

        that.openOverlay(this.href);

        return false;
    });

};

VideoOverlay.prototype.openOverlay = function(url) {

    var that = this;

    that.$overlay.addClass('open');

    that.$overlayContent.load(url, function() {

        window['Video'].init();
        setTimeout(function() {
            that.$overlayContent.addClass('loaded');
        }, 2000);

    });

};

module.exports = VideoOverlay;
