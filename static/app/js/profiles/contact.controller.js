(function(){
'use strict';

  angular
    .module('buddy.profiles.controllers')
    .controller('ContactController', ContactController);
    
    
    
    //ContactController.$inject = ['CONTACTSERVICE'];

  function ContactController($scope, $http, $window){
    var userId = window.localStorage.getItem('user_id');

    $scope.text_binary = 'no';
    $scope.call_binary = 'yes';
    $scope.email_binary = 'no';
    $scope.twitter_binary = 'yes';
    
    $scope.showForm = false;
    
    
    $scope.updateCall = function(data){
        
        console.log('fired')
        if ($scope.call_binary === 'no'){
            var call = false;
            } else {
                var call = true;
            }
        return $http.patch('/api/users/' + userId + '/',{
            'call': call})
        .success(function(data){
            console.log('success')
            console.log(data)
            }).error(function(data){
            console.log(data)
            console.log('error')})
    }
    
    
    
    $scope.updateEmail = function(data){
        
        console.log('fired')
        if ($scope.email_binary === 'no'){
            var email_me = false;
            } else {
                var email_me = true;
            }
        return $http.patch('/api/users/' + userId + '/',{
            'email_me': email_me})
        .success(function(data){
            console.log('success')
            console.log(data)
            }).error(function(data){
            console.log(data)
            console.log('error')})
    }
    
    
    
    $scope.updateText = function(data){
        
        console.log('fired')
        if ($scope.text_binary === 'no'){
            var text = false;
            } else {
                var text = true;
            }
        return $http.patch('/api/users/' + userId + '/',{
            'text': text})
        .success(function(data){
            console.log('success')
            console.log(data)
            }).error(function(data){
            console.log(data)
            console.log('error')})
    }
    
    
    
    
    $scope.updateTweet = function(data){
        
        console.log('fired')
        if ($scope.twitter_binary === 'no'){
            var twitter = false;
            } else {
                var twitter = true;
            }
        return $http.patch('/api/users/' + userId + '/',{
            'tweet': twitter})
        .success(function(data){
            console.log('success')
            console.log(data)
            }).error(function(data){
            console.log(data)
            console.log('error')})
    }
    //for form submission, call the same service with a post request
    // and show a success/fail.
    
  }


})();