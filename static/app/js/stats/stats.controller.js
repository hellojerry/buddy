var statsControllers = angular.module('buddy.stats.controllers')

statsControllers.controller('StatsController', function($scope, $http, $window){
    var userId = $window.localStorage.getItem('user_id');
    $http.get('/api/users/streaks/' + userId + '/').success(function(data, status, headers, config){
        console.log(data)
        $scope.current_streak = data.current_streak,
        
        $scope.longest_streak = data.longest_streak,
        $scope.points = data.points,
        
        $scope.next_badge = data.next_badge,
                
        $scope.join_date = data.created_at.slice(0,10)
        
        
        var t = new Date(1970,0,1)
        t.setSeconds(1439078400)
        console.log(t)
        console.log(data)
        console.log(status)
        console.log(headers)
        console.log(config)
        
        }).error(function(data){
        console.log(data)
        });
    
});
    