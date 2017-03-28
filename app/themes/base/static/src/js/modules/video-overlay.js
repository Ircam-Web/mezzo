var Audio = require('./audio');
var Video = require('./video');

var VideoOverlay = function() {

    this.$overlay = $('#overlay');
    this.$overlayContent = $('#overlayContent');
    this.$overlayClose = $('#overlayClose');
    this.$overlayLoader = $('#overlayLoader');

    this.player = null;
    this.type = null;

    //
    // Init
    //
    this.init();

};

VideoOverlay.prototype.init = function() {

    var that = this;

    $(document).keyup(function(e) {

        if(e.keyCode === 27) {

            that.closeOverlay();

        }

    });

    that.$overlayClose.bind('click', function(e) {

        e.preventDefault();

        that.closeOverlay();

        return false;

    });

    $('[data-video-overlay]').click(function(e) {
        e.preventDefault();

        that.$overlayLoader.show();
        that.openOverlay(this.href);

        return false;
    });

};

VideoOverlay.prototype.openOverlay = function(url) {

    var that = this;

    that.$overlay.addClass('open');

    that.$overlayContent.load(url, function() {

        if($('video', that.$overlay).length > 0) {
            that.player = new Video(that.$overlay);
            that.type = 'video';
        } else {
            that.player = new Audio(that.$overlay);
            that.type = 'audio';
        }

        setTimeout(function() {
            that.player.play();
            that.$overlayLoader.hide();
            that.$overlayContent.addClass('loaded');
        }, 2000);

    });

};

VideoOverlay.prototype.closeOverlay = function(url) {

    var that = this;

    that.$overlayContent.removeClass('loaded');
    setTimeout(function() {
        if(that.type == 'video') {
            that.player.player.dispose();
        } else {

        }
        that.$overlayContent.html('');
        that.$overlay.removeClass('open');
    }, 1000);

};

module.exports = VideoOverlay;
