//
// Require all the modules
//
var LangSelector = require('./modules/lang-selector');
var RoleSelector = require('./modules/role-selector');
var NavHeader = require('./modules/nav-header');
var OpenButton = require('./modules/open-button');
var CloseButton = require('./modules/close-button');
var CloseEscape = require('./modules/close-escape');
var Search = require('./modules/search');
var Summary = require('./modules/summary');
var OverflowInit = require('./modules/overflow-init');
var StickyKitInit = require('./modules/sticky-kit-init');
var LightSliderPageInit = require('./modules/lightsliderpage-init');
var LightSliderHomeInit = require('./modules/lightsliderhome-init');
var LightSliderNetworkInit = require('./modules/lightslidernetwork-init');
var LazyLoadInit = require('./modules/lazyload-init');
var HomeMenu = require('./modules/home-menu');
var Audio = require('./modules/audio');
var Video = require('./modules/video');
var VideoOverlay = require('./modules/video-overlay');
var Instagram = require('./modules/instagram');

//
// Init all the modules
//
window[LangSelector] = new LangSelector();
window[RoleSelector] = new RoleSelector();
window[NavHeader] = new NavHeader();
window[OpenButton] = new OpenButton();
window[CloseButton] = new CloseButton();
window[CloseEscape] = new CloseEscape();
window[Search] = new Search();
window[Summary] = new Summary();
window[OverflowInit] = new OverflowInit();
window[StickyKitInit] = new StickyKitInit();
window[LightSliderPageInit] = new LightSliderPageInit();
window[LightSliderHomeInit] = new LightSliderHomeInit();
window[LightSliderNetworkInit] = new LightSliderNetworkInit();
window[LazyLoadInit] = new LazyLoadInit();
window[HomeMenu] = new HomeMenu();
window[Audio] = new Audio();
window['Video'] = new Video();
window[VideoOverlay] = new VideoOverlay();
window[Instagram] = new Instagram();
