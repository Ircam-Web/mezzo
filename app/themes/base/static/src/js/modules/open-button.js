var CloseButton = function() {

    //
    // Init
    //
    this.init();

};

CloseButton.prototype.init = function() {

    var that = this;

    $('[data-open-button]').click(that.close);

};

CloseButton.prototype.close = function(e) {

    e.preventDefault();

    var target = $(this).attr('data-open-button'),
        $target = $('[data-open-button-target="'+target+'"]');

    if($target.length > 0) {

        $target.addClass('open');

    }

    return false;

}

module.exports = CloseButton;
