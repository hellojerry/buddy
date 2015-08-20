var staticControllers = angular.module('buddy.static.controllers', ['ngRoute', 'ngAnimate']);


staticControllers.controller('homeController', function($scope){
  $scope.pageClass = 'home';

  
  //console.log(angular.element('#test'))
  });

staticControllers.controller('profileController', function($scope){
  $scope.pageClass = 'profile';
  });

staticControllers.controller('settingsController', function($scope){
  $scope.pageClass = 'settings';
  });

staticControllers.controller('aboutController', function($scope){
  $scope.pageClass = 'about';
  });