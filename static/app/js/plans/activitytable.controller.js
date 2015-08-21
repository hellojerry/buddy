
'use strict';



var planControllers = angular.module('buddy.plans.controllers',
                                     ['xeditable']);

planControllers.$inject = ['Activity', 'Auth', '$location', '$anchorScroll'];

planControllers.run(function(editableOptions){
  editableOptions.theme = 'bs3'
}); 

planControllers.controller('ActivityTableController',
                           function($scope, $filter, Activity,
                                    $http, $window, Auth, $location,
                                    $anchorScroll) {
    

    if (Auth.isAuth() === true){
    var user_id = $window.localStorage.getItem('user_id')
    $http({method:'GET', url: '/api/activities/' + user_id + '/'})
      .success(function(data){
        var acts = [];
        for(var i=0, l=data.length; i<l; i++){
          
          var date = data[i].local_time.slice(0,10)
          //console.log(data[i])
          
          var activity = {
            'id': data[i].id,
            'local_id': data[i].id,
            'name': data[i].name,
            'day': data[i].day_of_week,
            'date': date,
            'time': data[i].local_time.slice(11,16),
            'call_time': data[i].call_time,
            'editable':data[i].editable,

            
          }

          acts.push(activity)
          
          
        }

        $scope.activities = acts;
      })
      .error(function(data){
        console.log('no auth')})}
      else {
        console.log('none')};
    
    
    
    $scope.days = [
      {text: 'Sunday'},
      {text: 'Monday'},
      {text: 'Tuesday'},
      {text: 'Wednesday'},
      {text: 'Thursday'},
      {text: 'Friday'},
      {text: 'Saturday'}
    ];
    
    


    function times(){
      var avail = [];
      var cur_hr = '00';
      var cur_min = '00';
      for (var i=0, l=48; i<l; i++){
        avail.push({text: cur_hr + ':' + cur_min})
        if(i % 2 == 0 || i == 0){
          cur_min = '30';
          
        }else {
          var int_cur_hr = parseInt(cur_hr);
          int_cur_hr += 1;
          cur_hr = ('0' + int_cur_hr).slice(-2).toString();
          cur_min = '00';
        }
      }

      return avail;
    }

    times();
    $scope.time_options = times();

    $scope.showEditable = function(index){

      var item = $scope.activities[index]
      if (item.editable === true){
        return true;
      }
    }
    
    $scope.showDay = function(activity){
      var selected = [];
      if (activity.day) {
        selected = $filter('filter')($scope.days, {value: activity.day});
        }
      return selected.length ? selected[0].text : 'Not set';
      };
      
    $scope.showTime = function(activity){
      var selected = [];
      if (activity.time){
        selected = $filter('filter')($scope.time_options, {value: activity.time});
      }
      return selected.length ? selected[0].text : 'Not Set';
    }
    
    $scope.addActivity = function(){
      $scope.inserted = {
        local_id: $scope.activities.length+1,
        id: null,
        name: null,
        time: null,
        calltime: null,
        day: null,
        date: null,
        editable: true,
        
      };
      $scope.activities.push($scope.inserted);
      
      var result = document.getElementById('home')
      var resultHeight = document.getElementById('home').clientHeight;
      var ctr = document.getElementById('ctr');
      var ctrHeight = ctr.clientHeight;

      if ($window.localStorage.getItem('orig') === null){
        $window.localStorage.setItem('orig', parentHeight)
      }
      
      if (resultHeight < ctrHeight*1.2){
        result.style.height = 1.25*resultHeight + 'px';
        
      }      
      
    };
    
    $scope.removeActivity = function(index){

      var item = $scope.activities[index]         
      $scope.activities.splice(index, 1);
      var user_id = $window.localStorage.getItem('user_id')
      var user = $window.localStorage.getItem('username');
      if (item.id != null){
        return $http.delete('/api/activities/' + user_id +'/' + item.id +'/')
        .success(function(data){
            console.log('delete success')
            var resultHeight = document.getElementById('home').clientHeight;
            var parent = document.getElementById('page-contain');
            var parentHeight = parent.clientHeight
            if (resultHeight >= parentHeight*.8){
              parent.style.height = .99*parentHeight + 'px'
      }        
            
            })
        .error(function(data){
            console.log('error')});
      }
    }
    
    
    
    $scope.saveActivity = function(data, local_id){
      var user_id = $window.localStorage.getItem('user_id')
      var user = $window.localStorage.getItem('username');
      
      
      if(data.id == null){
      return $http.post('/api/activities/' + user_id + '/', {
        day_of_week: data.day,
        provided_time: data.time,
        user: user_id,
        name: data.name
        // set the element attribute id 
        }).success(function(response){

        for (var i=0, l=$scope.activities.length; i<l; i++){
          if($scope.activities[i].local_id == local_id){

            $scope.activities[i].id = response.id,
            $scope.activities[i].date = response.local_time.slice(0,10)

          }
        }        
        })
        .error(function(data, errors){
          console.log(data)
          })
      } else {
        return $http.put('/api/activities/' + user_id +'/' + data.id + '/',{
        day_of_week: data.day,
        provided_time: data.time,
        user: user_id,
        name: data.name
        
        }).success(function(response){
          for (var i=0, l=$scope.activities.length; i<l; i++){
            if($scope.activities[i].local_id == local_id){
              $scope.activities[i].date = response.local_time.slice(0,10);
            }
          }
        //console.log(data)
        })
        .error(function(data, errors){
          console.log(data)
          })
        }}
        
    $scope.checkEmpty = function(data){
      if (data == null){
        return 'Field required.'
      }
    }
    
    $scope.gotoBottom = function(event){
        console.log('fired')
        //console.log(id)
        var old = $location.hash();
        $location.hash('bottom');
        $anchorScroll();
        $location.hash(old)
        
    }

  
  });
//r'^api/users/checkin/(?P<pk>\d+)/$
planControllers.controller('CheckInController', function($scope, $http, $window){
    var userId = $window.localStorage.getItem('user_id');
    


    
    $scope.checkIn = function (){
        return $http.get('api/users/checkin/' + userId +'/', {}).success(function(data){
            console.log(data)
            console.log(data.completed)
            if (data.completed === false){
                $scope.checkInMsg = "Looks like there's nothing to check in right now. Try again later!"
            } else {
                $scope.checkInMsg = "You've successfully checked in!"
            }
            console.log('success')
            $scope.checkInSuccess = true;}).error(function(data){
            console.log(data)});
    }
    
    });