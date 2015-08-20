(function(){
    'use strict';
    
    //name the module
    angular
        .module('buddy.config')
        .config(config);
        
    config.$inject = ['$httpProvider', '$locationProvider', '$interpolateProvider'];
    
    
    function config($httpProvider, $locationProvider, $interpolateProvider){
        //$httpProvider.interceptors.push('AuthInterceptor');
        //get rid of hash routing.
        $locationProvider.html5Mode(true).hashPrefix('!');
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

    }
    
})();



//<script>
//  var customInterpolationApp = angular.module('customInterpolationApp', []);
//
//  customInterpolationApp.config(function($interpolateProvider) {
//    $interpolateProvider.startSymbol('//');
//    $interpolateProvider.endSymbol('//');
//  });
//
//
//  customInterpolationApp.controller('DemoController', function() {
//      this.label = "This binding is brought you by // interpolation symbols.";
//  });
//</script>
//<div ng-app="App" ng-controller="DemoController as demo">
//    //demo.label//
//</div>