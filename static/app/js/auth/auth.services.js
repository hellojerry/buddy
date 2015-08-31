(function () {
  'use strict';
  
  angular
    .module('buddy.auth.services')
    .factory('Auth', Auth);
    
    
  Auth.$inject = ['$http', '$window'];
  
  function Auth($http, $window) {
    
    var Auth = {
      deleteToken: deleteToken,
      getToken:getToken,
      login: login,
      logout: logout,
      register: register,
      setToken: setToken,
      isAuth: isAuth,
      setTimezone: setTimezone,
      
    };
    
    return Auth;
    
    function isAuth(){

      if (Auth.getToken()){
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
      return $window.localStorage.getItem('token');
    }
    
    function login(login_email, login_password) {
      return $http.post('/api/auth/login/', {
        email: login_email,
        password: login_password,
        //call the success or error afterward
      }).then(loginSuccessFn, loginErrorFn);
      
      // modify this and setToken to store the user
      // id information inside of the window.
      // the reason for this is to supply user profile information
      // visually.
      
      function loginSuccessFn(data, status, headers, config) {
        console.log(data.data.user_id);
        if (data.data.token){
          Auth.setToken(data.data.token, data.data.user_id, data.data.username);
          console.log('login success');
          Auth.setTimezone();
        }
        $window.location = '/';
        return 'success'
    }
    
    // we need to figure out a way to display the login error on the page.
    function loginErrorFn(data, status, headers, config) {
      console.error(data);
      return 'failure'
    }
  }
    //modify setToken and deleteToken to hold the user id
    function logout(){
      Auth.deleteToken();
      //event.preventDefault();
      console.log('logout successful');
      $window.location = '/';
    }
    
    
    function register(register_email, register_password, confirm_password) {
      console.log('register service fired');
      return $http.post('/api/users/', {
        email: register_email,
        password: register_password,
        //confirm_password: confirm_password
      }).then(registerSuccessFn, registerErrorFn);
    
      function registerSuccessFn(data, status, headers, config){

        Auth.login(register_email, register_password);
      }
      function registerErrorFn(data, status, headers, config){
        console.error(data);
      }
    
    }
    
    function setToken(token, user_id, username){
      $window.localStorage.setItem('token', token);
      $window.localStorage.setItem('user_id', user_id);
      $window.localStorage.setItem('username', username);
      //for user id
      //$window.localStorage.setItem('userId', 
    }
    
    function setTimezone(){
        var tz = jstz.determine()


        var userId = $window.localStorage.getItem('user_id')
        $http.patch('/api/users/' + userId + '/',{
            'time_zone': tz.name(),
            }).success(function(data, status, headers, config){
            console.log('service success')
            console.log(data, status, headers, config)})
        .error(function(resp, status, headers, config){
            console.log('error at service')
            console.log(resp)
            console.log(status);
            console.log(headers);
            console.log(config.data)});
        
        
    }
    
    
  
  
  }})();