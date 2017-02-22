var Video = function(context) {

    this.player = null;
    this.context = context || $('body');

    //
    // Init
    //
    if($('#video-js-playlist', this.context).length > 0) {
        this.init();
    }

};

Video.prototype.init = function() {

    var that = this;

    if(that.player) {
        that.player.dispose();
    }

    that.player = videojs('video-js-playlist', {
        aspectRatio:"905:520"
    });

    var playlist = [];
    $('.video-playlist li a').each(function(idx) {

        var elem = $(this);

        var srcs = elem.attr('data-src').split(',');
        var mimes = elem.attr('data-mime').split(',');
        var obj = {
            sources: [],
            poster: elem.attr('data-poster')
        };

        for(var i=0; i<srcs.length; i++) {
            obj.sources.push({
                src: srcs[i],
                type: mimes[i]
            });
        }

        playlist.push(obj);

        elem.click(function(e) {
            e.preventDefault();

            $('.video-playlist li').removeClass('playing');
            $(this).parent().addClass('playing');
            that.player.playlist.currentItem($(this).parent().index());
            that.player.play();

            return false;
        });

    });

    that.player.playlist(playlist);
    return that.player;

};

Video.prototype.play = function(e) {

    this.player.play();

}

Video.prototype.open = function(e) {



}

module.exports = Video;
