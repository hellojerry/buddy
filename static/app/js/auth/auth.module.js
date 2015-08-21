(function (){
  'use strict';
  
  //this module is registered at the app level.
  //the sub modules here have no outer dependencies.
  
  angular
    .module('buddy.auth', [
        'buddy.auth.controllers',
        'buddy.auth.interceptors',
        'buddy.auth.services'
        ]);
    
  angular
    .module('buddy.auth.controllers', []);
    
  angular
    .module('buddy.auth.interceptors', []);
    
  angular
    .module('buddy.auth.services', []);
  
    
})();