
function switchVideo(id, url) {
    var video = $('#'+id);
    video.attr("src", url);
}


function failed(e) {
   // video playback failed - show a message saying why
   switch (e.target.error.code) {
     case e.target.error.MEDIA_ERR_ABORTED:
       alert('You aborted the video playback.');
       break;
     case e.target.error.MEDIA_ERR_NETWORK:
       alert('A network error caused the video download to fail part-way.');
       break;
     case e.target.error.MEDIA_ERR_DECODE:
       alert('The video playback was aborted due to a corruption problem or because the video used features your browser did not support.');
       break;
     case e.target.error.MEDIA_ERR_SRC_NOT_SUPPORTED:
       alert('The video could not be loaded, either because the server or network failed or because the format is not supported.');
       break;
     default:
       alert('An unknown error occurred.');
       break;
   }
}


function cleanCounter() {
    $('#countdown-title').html('<br /><br />');
    $('#countdown').html('<br />');
}

function CountDownTimer(json_event, curr_event_index, id, video_id/*, video_url*/)
    {
        if (Object.keys(json_event).length <= curr_event_index) {
            return ;
        }

        var curr_event;
        var begin;
        var end;

        var _second = 1000;
        var _minute = _second * 60;
        var _hour = _minute * 60;
        var _day = _hour * 24;
        var timer;
        var distance_out = 1;
        var distance_in = 1;

        function init() {
            if (curr_event_index < Object.keys(json_event).length ) {
                curr_event = json_event[curr_event_index];
                begin = moment(new Date(curr_event.begin));
                end = moment(new Date(curr_event.end)).add(0, 'm');
                clearInterval(timer);
            }
        }

        function showRemaining() {
            var now = moment(new Date());
            var distance_out = begin.diff(now);
            if (distance_out < 0) {
                //clearInterval(timer);
                // $('#countdown-title').html('<br /><br />');
                // $('#'+id).html('<br />');
                // $('#live').html('- Live !');
                //switchVideo(video_id, video_url);
                $('.countdown-overlay').hide()
                distance_in = 1;
                hideRemaining()
                //return;
            }

            updateDisplay(distance_out);
        }

        function hideRemaining() {
            var now = moment(new Date());
            var distance_in = end.diff(now);
            if (distance_in < 0) {
                nextEvent();
                distance_out = begin.diff(now);
                updateDisplay(distance_out);
                $('.countdown-overlay').show()
            }
        }

        function nextEvent() {
            curr_event_index++;
            init();
        }

        function updateDisplay(time_remaining) {

            $('#countdown-title').html('Prochain évènement :<br><br/><strong>'+ curr_event.title+'</strong><br/><br/> Retransmission dans :');

            var days = Math.floor(time_remaining / _day);
            var hours = Math.floor((time_remaining % _day) / _hour);
            var minutes = Math.floor((time_remaining % _hour) / _minute);
            var seconds = Math.floor((time_remaining % _minute) / _second);

            document.getElementById(id).innerHTML = days + 'jours ';
            document.getElementById(id).innerHTML += hours + 'hrs ';
            document.getElementById(id).innerHTML += minutes + 'mins ';
            document.getElementById(id).innerHTML +=  seconds + 'secs';
        }

        // initialize
        init();

        // out of event
        if (distance_out > 0) {
            timer = setInterval(showRemaining, 1000);
        }

        // meanwhile an event
        if (distance_in > 0) {
            timer = setInterval(hideRemaining, 1000);
        }
    }


jQuery.fn.center = function () {
    this.css("position","absolute");
    this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) +
                                                $(window).scrollTop()) + "px");
    this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) +
                                                $(window).scrollLeft()) + "px");
    return this;
}
