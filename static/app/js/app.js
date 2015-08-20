(function(){
    'use strict';
    //list all module dependencies
    angular.module('buddy', [
        'buddy.config',
        'buddy.routes',
        //'buddy.auth',
        'buddy.static',
        //'buddy.plans',
        //'buddy.stats',
        'ui.bootstrap',
        'ngAnimate',
    ]);
    
    angular.module('buddy.config', []);
    
    angular.module('buddy.routes', ['ngRoute', 'ngAnimate']);
    
    //angular.module('buddy.plans', ['xeditable']);
    
    angular
        .module('buddy')
        .run(run);
    
    run.$inject = ['$http'];
    
    function run($http){
        //$http.defaults.headers.common['My-Custom-Header'] = 'My-Custom-Header';
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }
    
    
})();