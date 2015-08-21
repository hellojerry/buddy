(function (){
  'use strict';
  
  
  angular
    .module('buddy.static.directives')
    .directive('tab', tab);
    
  function tab(Auth){
    return {
      restrict: 'E',
      transclude: true,
      template: '<div role="tabpanel" ng-show="active" ng-transclude></div>',
      require: '^tabset',
      scope: {
        heading: '@',
      },
      link: function(scope, elem, attr, tabsetCtrl){
        scope.active = false;
        //tabsetCtrl is nested within the tabset directive.
        tabsetCtrl.addTab(scope);
      }
    }
    
    
  }
})();