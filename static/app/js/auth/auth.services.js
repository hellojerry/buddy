(function(){
 'use strict';

  angular
    .module('buddy.auth.services')
    .factory('Auth', Auth);
    
    
  Auth.$inject = ['$http', '$window'];
  
  function Auth($http, $window){
    
    var Auth = {
      deleteToken: deleteToken,
      getToken: getToken,
      login: login,
      logout: logout,
      register: register,
      setToken: setToken,
      isAuth: isAuth,
      setTimezone: setTimezone
      
      };
    
    return Auth;
  
    function isAuth(){
      console.log('auth confirmed');
      if(Auth.getToken()){
        return true;
      } else {
        return false;
      }
    }
    
    function deleteToken(){
      $window.localStorage.removeItem('token');
      $window.localStorage.removeItem('user_id');
      $window.localStorage.removeItem('username');
    }
    
    function getToken(){
      $window.localStorage.getItem('token');
      }
    
    function login(login_email, login_password){
      return $http.post('/api/auth/login/', {
        email: login_email,
        password: login_password
        }).then(loginSuccessFn, loginErrorFn);
      
      function loginSuccessFn(data, status, headers, config){
        if(data.data.token){
          Auth.setToken(data.data.token, data.data.user_id, data.data.username);
          }
          $window.location = '/';
          return 'success'
        };
      
      function loginErrorFn(data, status, headers, config){
        console.error(data);
        return 'failure'
        
        };
      }
    function logout(){
      Auth.deleteToken();
      $window.location = '/';
    }
    
    function register(register_email, register_password, confirm_password){
      return $http.post('/api/users/', {
        email: register_email,
        password: register_password
        }).then(registerSuccessFn, registerErrorFn);
    
      function registerSuccessFn(data, status, headers, config){
        Auth.login(register_email, register_password);
      }
      
      function registerErrorFn(data, status, headers, config){
        //stick some sort of message here, or in the controller.
        console.error(data);
      }
    }
    
    function setToken(token, user_id, username){
      $window.localStorage.setItem('token', token);
      $window.localStorage.setItem('user_id', user_id);
      $window.localStorage.setItem('username', username)
      
    }
    
    function setTimezone(){
      var tz = jstz.determine()
      
      var userId = $window.localStorage.getItem('user_id')
      $http.patch('/api/users/'+ userId + '/', {
        'time_zone' : tz.name()
      }).success(function(data, status, headers, config){
        console.log('tz set')
      }).error(function(data, status, headers, config){
        console.log(data)
        console.log(status);
        console.log(headers);
        console.log(config);
        });
      
    }

    
  }

 
})();