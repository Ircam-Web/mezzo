var OpenButton = function() {

    //
    // Init
    //
    this.init();

};

OpenButton.prototype.init = function() {

    var that = this;

    $('[data-close-button]').click(that.open);

};

OpenButton.prototype.open = function(e) {

    e.preventDefault();

    var target = $(this).attr('data-close-button'),
        $target = $('[data-close-button-target="'+target+'"]');

    if($target.length > 0) {

        $target.removeClass('open');

    }

    return false;

}

module.exports = OpenButton;
