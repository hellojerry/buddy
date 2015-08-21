(function(){
'use strict';

  angular
    .module('buddy.static.directives')
    .directive('numberOnly', numberOnly);
    
  function numberOnly(){
    return {
      restrict: 'A',
      require: 'ngModel',
      link: function($scope, element, attrs, modelCtrl){
        modelCtrl.$parsers.push(function(inputValue){
        if (inputValue == undefined){
          return ''
        }
        var transformedInput = inputValue.replace(/[^0-9]/g, '');
        if (transformedInput != inputValue){
          modelCtrl.$setViewValue(transformedInput);
          modelCtrl.$render();
        }
        return transformedInput;
        });
      }
    }
  }
})();