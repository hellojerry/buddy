(function (){
  'use strict';
  
  angular
    .module('buddy.auth.controllers')
    .controller('RegisterController', RegisterController);
    
  RegisterController.$inject = ['Auth'];
  
  
  function RegisterController(Auth){
    var vm = this;
    
    vm.register = register;
    vm.user = {};
    
    function register(){
      console.log('register controller fired');
      Auth.register(vm.register_email, vm.register_password, vm.confirm_password);
    }
  }
})();