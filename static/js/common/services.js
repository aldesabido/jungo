var app = angular.module('common_services', [])


app.factory("CommonFac", function($state,$http) {
    var title = "Home";
    return {
        set_title: function(title){
            this.title = title;
        },

        get_title: function(){
            return this.title
        }
    }
})


app.factory("Notification", function(toastr) {
    return {
        success: function(title, body, timeout) {
            if (!title) {
                title = "Success"
            }

            if (!timeout) {
                timeout = 5000;
            }

            var config = {
                timeOut: timeout
            }

            return toastr.success(body, title, config);
        },
        error: function(title, body, timeout) {

            if (!title) {
                title = "Error"
            }

            if (!timeout) {
                timeout = 15000;
            }

            var config = {
                timeOut: timeout
            }

            return toastr.error(body, title, config);
        },
        warning: function(title, body, timeout) {

            if (!title) {
                title = "Warning"
            }

            if (!timeout) {
                timeout = 15000;
            }

            var config = {
                timeOut: timeout
            }

            return toastr.warning(body, title, config);
        },
    }

});



app.factory("CommonFunc", function($http, Notification, SweetAlert) {
    return {
        arr2str: function(arr) {
            str = null;
            console.log(arr)
            for (var i in arr) {
                var item = arr[i];
                console.log(item)
                if (!str) {
                    str = String(item)
                } else {
                    str += ", " + String(item)
                }
            }
            return str;
        },

        confirmation: function(title, text, type) {
            if (!title) {
                title = "Continue?"
            }
            if (!type) {
                type = "warning"
            }

            var sweetalert = SweetAlert.swal({
                title: title,
                text: text,
                type: type,
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Delete",
                cancelButtonText: "Cancel",
                closeOnConfirm: true
            });
            return sweetalert;
        },

        /*get the likely percentage of two string*/
        similar(a,b) {
            var lengthA = a.length;
            var lengthB = b.length;
            var equivalency = 0;
            var minLength = (a.length > b.length) ? b.length : a.length;    
            var maxLength = (a.length < b.length) ? b.length : a.length;    
            for(var i = 0; i < minLength; i++) {
                if(a[i] == b[i]) {
                    equivalency++;
                }
            }


            var weight = equivalency / maxLength;
            return (weight * 100)
        },

        first_day_of_date(date){
            date = moment([date.year(), date.month()]);
            return new Date(date)
        },
        last_day_of_date(date){
            date = new Date(moment(date).endOf('month'));
            return new Date(date)
        }

    }
});

app.factory("CommonRequests", function($http, Notification) {
    return {
        read_common_records: function(scope, key, url, params, no_success) {
            if (!params) { params = {}; }
            return $http.post(url, params)
                .success(function(response) {
                    if (!no_success) {
                        scope[key] = response;
                    }
                })
        },
    }
});

app.factory("CommonRead", function($http, CommonRequests) {
    return {
        read_companies: function(scope){
            return CommonRequests.read_common_records(scope, "companies", "/common_requests/read_companies/");
        },

        read_credentials: function(scope,params){
            return CommonRequests.read_common_records(scope, "credentials", "/common_requests/read_credentials/",params);
        },

        read_order_types: function(scope){
            return CommonRequests.read_common_records(scope, "order_types", "/common_requests/read_order_types/");
        },

        read_clients: function(scope){
            return CommonRequests.read_common_records(scope, "clients", "/common_requests/read_clients/");
        },

        read_cdas: function(scope){
            return CommonRequests.read_common_records(scope, "cdas", "/common_requests/read_cdas/");
        }
    }
})
