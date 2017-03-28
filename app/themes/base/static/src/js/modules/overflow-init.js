var OverflowInit = function() {

    //
    // Init
    //
    this.init();

};

OverflowInit.prototype.init = function() {

    var that = this;

    Overflow.initialize({
        selector: '[data-overflow]'
    });

    Overflow.initialize({
        selector: 'hr'
    });

};

module.exports = OverflowInit;
