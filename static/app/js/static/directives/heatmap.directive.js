'use strict';
var heatMap = angular.module('buddy.static.directives', [])
//var d3 = typeof require === "function" ? require("d3") : window.d3;
heatMap.$inject = ['$window'];

heatMap.directive('calHeatmap', function ($window, $http) {
  
    console.log('heatmap directive')
    var userId = $window.localStorage.getItem('user_id');
    
    function link(scope, elem, $http) {

        var config = scope.config || {};
        var element = elem[0];
        var cal = new CalHeatMap();
        var defaults = {
            itemSelector: element,
            previousSelector: '#previousSelector',
            nextSelector: '#nextSelector',
            domain: 'month',
            subDomain: 'day',
            subDomainTextFormat: '%d',
            data: 'http://localhost:8000/api/records/' + userId + '/',
            start: new Date(2015,6,15),
            cellSize: 25,
            range: 3,
            legendCellSize: 25,
            legendHorizontalPosition: 'center',
            //legendOrientation: 'vertical',
            //legendMargin: [0,0,0,30],
            legendColors: {
                min: '#FFCCCC',
                max: '#FF4D4D',
                empty: 'white',
            },
            legendTitleFormat: {
              lower: 'No checkins',
              inner: '{down} {name}',
              upper: 'more than {max} {name}'
            },
            legendTextSide: "left",
            legend_text: "less",
            domainGutter: 10,
            legend: [1, 2, 3, 4, 5],
            itemName: 'checkin',
            colLimit: 5
        };

        console.log(defaults.data)
        var tz = jstz.determine();
        console.log(tz.name());
        angular.extend(defaults, config);
        cal.init(defaults);

    }
    return {
        template: '<div class="cal-heatmap" ng-transclude config="config"></div>',
        transclude: true,
        restrict: 'E',
        link: link,
        scope: {
            config: '='
        }
    };
});
heatMap.directive('nxEqualEx', function() {
    
    return {
        require: 'ngModel',
        link: function (scope, elem, attrs, model) {
            if (!attrs.nxEqualEx) {
                console.error('nxEqualEx expects a model as an argument!');
                return;
            }
            scope.$watch(attrs.nxEqualEx, function (value) {
                // Only compare values if the second ctrl has a value.
                if (model.$viewValue !== undefined && model.$viewValue !== '') {
                    model.$setValidity('nxEqualEx', value === model.$viewValue);
                }
            });
            model.$parsers.push(function (value) {
                // Mute the nxEqual error if the second ctrl is empty.
                if (value === undefined || value === '') {
                    model.$setValidity('nxEqualEx', true);
                    return value;
                }
                var isValid = value === scope.$eval(attrs.nxEqualEx);
                model.$setValidity('nxEqualEx', isValid);
                return isValid ? value : undefined;
            });
        }
    };
});