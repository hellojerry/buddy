(function(){
'use strict';

  angular
    .module('buddy.profiles.controllers')
    .controller('InfoController', InfoController);
    
    

  
  
  function InfoController($scope, $http, $window){
    var userId = $window.localStorage.getItem('user_id')
    $scope.newTemp = function(data){
        if (data !== null){
            console.log('data')
        }
        console.log('fired')
        return $http.post('api/users/' + userId + '/createtemp/', {
            email: $scope.new_email,
            phone: $scope.new_phone,
            twitter: $scope.new_twitter,
            user_id: userId}).success(function(data){
            console.log('success')
            $scope.formSuccess = true;
            }).error(function(data, status, headers, config){
            console.log(status)
            console.log(config)
            console.log(headers)
            console.log(data)
            $scope.showError = true;});
    }
    
    return $http.get('api/users/' + userId + '/').
    success(function(data){
            console.log(data)
            $scope.phone = data.phone,
            $scope.twitter = data.twitter_handle,
            $scope.email = data.email });
    

    
    $scope.showForm = false;


    
  }
  //api/users/(?P<pk>\d+)/createtemp/





})();