var LazyLoadInit = function() {

    //
    // Init
    //
    this.init();

};

LazyLoadInit.prototype.init = function() {

    var that = this;

    $("img.lazyload").lazyload({
        effect : "fadeIn",
        container: $("main")
    });

};

module.exports = LazyLoadInit;
