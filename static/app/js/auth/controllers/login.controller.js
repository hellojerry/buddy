(function () {
  'use strict';
  
  angular
    .module('buddy.auth.controllers')
    .controller('LoginController', LoginController);
    
    
  LoginController.$inject = ['Auth'];
  
  //this is to give us access to the login function at the
  //template level.
  function LoginController(Auth) {

    var vm = this;
    
    vm.login = login;
    vm.user = {};
    vm.loginError = false;
    
    //modify the user model so the username field is 'email'.
    function login() {
      Auth.login(vm.login_email, vm.login_password).then(
        function(val){
          var item = val;

          if (item === 'failure'){
            vm.loginError = true;
          } else {

            Auth.setTimezone();
          }

          });
      
      //console.log(Auth.login(vm.login_email, vm.login_password));
    }

  }

})();