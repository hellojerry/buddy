(function(){
'use strict';

  angular
    .module('buddy.auth.interceptors')
    .service('AuthResponseInterceptor', AuthResponseInterceptor)

    AuthResponseInterceptor.$inject = ['$injector', '$q', '$location', '$window$']
    function AuthResponseInterceptor($injector, $q, $location, $window){

      var AuthResponseInterceptor = {
        response: response,
        responseError: responseError
      }
      return AuthResponseInterceptor;

        function response (response){
          if (response.status === 401){
            console.log('response 401')
            $window.localStorage.removeItem('token')
            $window.localStorage.removeItem('user_id')
            $window.localStorage.removeItem('username')
          }
          return response || $q.when(response);
        }

        function responseError (rejection){
          if (rejection.status === 401){
          console.log('response error 401', rejection)
          $window.localStorage.removeItem('token')
          $window.localStorage.removeItem('user_id')
          $window.localStorage.removeItem('username')
          $location.path('/').search('returnTo', $location.path());
          }
          return $q.reject(rejection)
        }
    }
})();

