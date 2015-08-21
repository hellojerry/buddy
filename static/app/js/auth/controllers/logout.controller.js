(function(){
  'use strict';
  
  angular
    .module('buddy.auth.controllers')
    .controller('LogoutController', LogoutController);
    
    
    
    LogoutController.$inject = ['Auth'];
  
  function LogoutController(Auth){
    var vm = this;
    
    vm.user = {};
    vm.logout = logout;
    
    function logout(){
      //event.preventDefault();
      Auth.logout()
      
    }
    
  }
})();