(function(){
  'use strict';
  
  angular
    .module('buddy.static.directives')
    .directive('authHide', authHide);
  
  authHide.$inject = ['$window', 'Auth']
  function authHide(Auth, $window){

    return {
      restrict: 'A',
      link: function (scope, elem, attrs, $window){

        if (localStorage.getItem('token')){
          //elem.fadeIn(); this works but its ugly
          elem.addClass('hidden');

        } else {
          elem.removeClass('hidden');
        }
        
        
      },
      scope: { },
    }
    
  };
})();