var app = angular.module('common_filters',[])

app.filter("integer", function($http) {
  return function(number) {
    if(!number) number = 0;
    number = Math.abs(number);
    return number     
  };
})


app.filter('capitalize', function() {
    return function(input){
      return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
    }
})
