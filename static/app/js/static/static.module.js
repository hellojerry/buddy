(function (){
  'use strict';
  
  angular
    .module('buddy.static', [
        'buddy.static.directives',
        'buddy.static.animations',
        'buddy.static.controllers',]);
    
  angular
    .module('buddy.static.directives', []);
    
  angular
    .module('buddy.static.animations', ['ngAnimate']);
    
  angular
    .module('buddy.static.controllers', []);
  
  
})();