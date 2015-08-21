
(function(){
'use strict';


angular
  .module('buddy.static.controllers')
  .controller('HomeSizeController', HomeSizeController)
  
  function HomeSizeController($scope){
    angular.element(document).ready(function(){
    var home = document.getElementById('home')
    var ctr = document.getElementById('ctr');
    if(ctr.clientHeight < home.clientHeight){
          var res1 = 2*home.clientHeight

          home.style.height = res1 + 'px'

          
        }
    
      
      
      })
    
    
  }
  })();