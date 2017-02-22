var Audio = function(context) {

    this.context = context || $('body');

    this.audios = [];
    this.playlists = [];

    //
    // Init
    //
    this.init();

};

Audio.prototype.init = function() {

    var that = this,
        as, i, playlist;

    audiojs.events.ready(function() {

        as = audiojs.createAll();

        for(i = 0; i<as.length; i++) {

            playlist = $(as[i].element).parent().next('.audio-playlist');

            as[i].title = $('<div class="title"></div>');
            $(as[i].wrapper).append(as[i].title);

            as[i].element.onplay = function (e) {
                that.pauseAllExcept(this);
            };

            //
            // Future refs
            //
            that.audios.push(as[i]);
            that.playlists.push(playlist[0]);

            //
            // Set the trackEnded function
            //
            as[i].settings.trackEnded = function() {

                var idx, next, playlist;

                idx = that.audios.indexOf(this);
                playlist = that.playlists[idx];

                var next = playlist.find('li.playing').next();
                if (!next.length) next = playlist.find('li').first();
                next.addClass('playing').siblings().removeClass('playing');
                this.load($('a', next).attr('data-src'));
                this.play();

            };

            //
            // Load the first audio
            //
            var first = playlist.find('li a').attr('data-src');
            playlist.find('li').first().addClass('playing');
            that.setTitle(as[i], playlist.find('li:first-child a span').text(), playlist.find('li:first-child a small').text());
            as[i].load(first);

            playlist.find('li').bind('click', function(e) {

                var idx = that.playlists.indexOf($(this).parent().get(0));

                e.preventDefault();
                $(this).addClass('playing').siblings().removeClass('playing');
                that.audios[idx].load($('a', this).attr('data-src'));
                that.audios[idx].play();
                that.setTitle(that.audios[idx], $('a span', this).text(), $('a small', this).text());

            });

        }

    });

};

Audio.prototype.pauseAllExcept = function(audio) {

    var that = this,
        i = 0;

    for(i=0; i<that.audios.length; i++) {

        if(that.audios[i].element != audio) {
            that.audios[i].element.pause();
        }

    }

};

Audio.prototype.setTitle = function(audio, title, subtitle) {

    var split = title.split(",");
    var html = '';

    /*if(split[0]) {
        html += split[0];
    }
    if(split[1]) {
        html += '<br/><span>'+split[1]+'</span>'
    }*/

    html += title;

    if(subtitle) {
        html += '<br/><span>'+subtitle+'</span>';
    }

    audio.title.html(html);

};

Audio.prototype.play = function(e) {

    this.audios[0].play();

}

module.exports = Audio;
