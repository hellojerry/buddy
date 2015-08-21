'use strict';

var buddy = angular.module('buddy', [
  'ngRoute',
  'ngAnimate',

  'buddy.auth',
  'buddy.static',
  'buddy.plans',
  'buddy.stats',
  
  'buddy.profiles',
    //'ui.bootstrap',
]);

buddy.config(function($locationProvider, $routeProvider, $httpProvider){
  //$httpProvider.interceptors.push('AuthInterceptor');
  $locationProvider.html5Mode(true).hashPrefix('!');
  
   $routeProvider
        .when('/', {
            templateUrl: 'static/app/partials/home.html',
        })
        .when('/profile', {
            templateUrl: 'static/app/partials/profile.html'
        })
        .when('/settings', {
            templateUrl: 'static/app/partials/settings.html'
        })
        .when('/about', {
            templateUrl: 'static/app/partials/about.html'
        })

  
  
  });

buddy.run(['$rootScope', '$location',
           '$window', '$http', function($rootScope, $location,
                                             $window, $http, $scope){

    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.headers.common.Authorization = 'JWT ' + localStorage.getItem('token');
    

    
    $rootScope.go = function (path, pageAnimationClass) {

        if (typeof(pageAnimationClass) === 'undefined') { // Use a default, your choice
            $rootScope.pageAnimationClass = 'crossFade';
        }
        
        else { // Use the specified animation
            $rootScope.pageAnimationClass = pageAnimationClass;
        }

        if (path === 'back') { // Allow a 'back' keyword to go to previous page
            $window.history.back();
        }
        
        else { // Go to the specified path
            $location.path(path);
        }
        //resize div if 
        if($window.localStorage.getItem('orig') != null){
          console.log($window.localStorage.getItem('orig'))
          var string = $window.localStorage.getItem('orig')
          var origHeight = parseInt(string)
          var pageContain = document.getElementById('page-contain')
          pageContain.style.height = origHeight + 'px'
          }
        

        
    };
    

  
  }]);

  