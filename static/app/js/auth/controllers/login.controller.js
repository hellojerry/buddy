(function () {
  'use strict';
  
  angular
    .module('buddy.auth.controllers')
    .controller('LoginController', LoginController);
    
    
  LoginController.$inject = ['Auth'];
  
  //this is to give us access to the login function at the
  //template level.
  function LoginController(Auth) {
    //console.log($rootScope)
    var vm = this;
    
    vm.login = login;
    vm.user = {};
    vm.loginError = false;
    
    //modify the user model so the username field is 'email'.
    function login() {
      Auth.login(vm.login_email, vm.login_password).then(
        function(val, val2){
          var item = val;
          console.log(item);
          console.log(val2)
          if (item === 'failure'){
            vm.loginError = true;
          } else {
            //$rootScope.currentUserLoggedIn = true;
            //console.log($rootScope)
            Auth.setTimezone();
          }

          });
      
      //console.log(Auth.login(vm.login_email, vm.login_password));
    }

  }

})();