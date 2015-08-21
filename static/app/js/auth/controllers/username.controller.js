(function (){
'use strict';
  
  angular
    .module('buddy.auth.controllers')
    .controller('UsernameController', UsernameController);
    
    
    UsernameController.$inject = ['$scope'];
    
    function UsernameController($scope) {
      var un = localStorage.getItem('username');
      $scope.username = un;
    };
})();