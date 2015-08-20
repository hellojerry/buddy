(function(){
  'use strict';
  
  angular
    .module('buddy.routes')
    .config(config);
    //inject $window here possibly to access localstorage?
  config.$inject = ['$routeProvider'];
  
  function config($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: 'static/app/partials/home.html',
        controller: 'homeController',
    }).when('/profile', {
      templateUrl: '/static/app/partials/profile.html',
      controller: 'profileController'
      }).when('/settings', {
      templateUrl: 'static/app/partials/settings.html',
      controller: 'settingsController'
      }).when('/about', {
      templateUrl: '/static/app/partials/about.html',
      controller: 'aboutController'
      })
  }
  
  
})();