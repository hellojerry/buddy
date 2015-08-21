(function(){
  'use strict';
  
  angular
    .module('buddy.static.directives')
    .directive('authOnly', authOnly);
  
  authOnly.$inject = ['$window', 'Auth']
  
  function authOnly($window, Auth){

    return {
      restrict: 'A',
      link: function (scope, elem, attrs, $window){

        if (localStorage.getItem('token')){
          //elem.fadeIn(); this works but its ugly
          elem.removeClass('hidden');
          //console.log('removing hidden')
        } else {
          elem.addClass('hidden');
        }
        if (Auth.isAuth() === true){
          //console.log(Auth.isAuth())
          //console.log('abcdefgh')
        } else {
          //console.log('ADSAFAFEQAGE')
          //console.log(Auth.isAuth())
        }
        
        
      }
    }
    
  };
})();