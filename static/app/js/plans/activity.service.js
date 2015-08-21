(function(){
    
  'use strict';

  angular
    .module('buddy.plans.services')
    .factory('Activity', Activity);
    
    
    
  Activity.$inject = ['$http', '$window', '$q'];
  
  function Activity($http, $window, $q){
      var Activity = {
        getActivities: getActivities,
        getUser: getUser
        
      };
      return Activity;
      
      function getUser(){
        var user_id = $window.localStorage.getItem('user_id');
        console.log(user_id)
        return user_id;
      }

      
      function getActivities(){
        var user_id = getUser()
        //console.log(user_id)
        
        //var d = $q.defer();
        
        return $http.get('/api/activities/' + user_id + '/')

        .success(function(data, status, headers, config){
          console.log('success')
          //console.log(headers)
          //console.log(status)
          var reformed = [];
          for(var i=0, l=data.length; i<l; i++){

            var activity = {
              'id': data[i].id,
              'name': data[i].name,
              'day': data[i].day_of_week,
              'time': data[i].time,
              'call_time': data[i].call_time,
              'editable':data[i].editable
              
            }
            //console.log(typeof(activity))
            reformed.push(activity)
          }
          console.log(reformed)
          console.log(typeof(reformed))
          return reformed;})
        
        .error(function(data, status, headers, config){
          console.error(data)})
      }
    
  
  
  


  }
})();