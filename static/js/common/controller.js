var app = angular.module("common_controller",[]).controller('CommonCtrl', function($scope,$http,$uibModal,$uibModalStack,$templateCache,SweetAlert,toastr,Notification){
	var me = this;
	me.current_dialogs = []
	me.page_loader = {"main" : false,"dialog" : false};
	me.resizeMode = "BasicResizer";
	me.uibdates = {}

	me.open_date = function(key){
		if(!key){key='date';}
		me.uibdates[key] = true;
	}

	me.sort_default = function(){
		default_sort_key = {
			"accounts" : "code",
		}

		key = "id"
		if(default_sort_key[$scope.module_code] !== undefined){
			key = default_sort_key[$scope.module_code];
		}
		return key
	}
	
	me.post_generic = function(url,params,loader_key,notify,assign_response,close_dialog){
		if(loader_key){me.page_loader[loader_key] = true}
		if(!params){params = {};}
		return $http.post(url, params)
		.success(function(response){
			if(loader_key){me.page_loader[loader_key] = false}
			if(notify){Notification.success(response)}
			if(assign_response){me[assign_response] = response; console.log(me.columns)} //not working
			if(close_dialog){me.close_dialog()}

		})
		.error(function(response,status){
			if(loader_key){me.page_loader[loader_key] = false}
			if(status == 404){
				if(notify){Notification.error("Connection error. Please contact administrator.")}
				return;
			}
			if(notify){Notification.error(response)}
		})
	}

	me.common_filter_dialog = function(){
		me.open_dialog("/common/filter_dialog2/","dialog_height_100 dialog_width_50");
	}

	me.open_dialog = function(url,dialog_class,key){
		if(!key){key = "main";}
		me.page_loader[key] = true;
		$templateCache.remove(url);
		var dialog = $uibModal.open({
	        templateUrl: url,
	        windowClass : dialog_class,
	        backdrop : 'static',
	        keyboard : false,
	        scope : $scope,
	    })

	    dialog.opened.then(function(){
			me.page_loader[key] = false;
	    	me.current_dialogs.push(dialog)
	    })

	    return dialog
	}

	me.columns_dialog = function(scope){
		if(!scope.current_module){return;}
		me.open_dialog("/common/columns_dialog/"+scope.current_module,"dialog_height_60 dialog_width_30");
	}
 
	me.close_dialog = function(dialog_instance,last){
		if(dialog_instance){
			me.current_dialogs[dialog_instance].close()
		}else if(last){
			var modal_len = me.current_dialogs.length;
			last_instance = me.current_dialogs[modal_len - 1];
			last_instance.close();
		}else{
			$uibModalStack.dismissAll();
		}
	}

	me.generate_pagination = function(scope,response){
		scope.starting = response.starting;
		scope.ending = response.data.length;
		scope.pagination.limit_options = angular.copy(scope.pagination.limit_options_orig);
		scope.pagination.limit_options.push(response.total_records)
		scope.pagination["total_records"] = response.total_records;
		scope.pagination["total_pages"] = response.total_pages;
	}
	
	me.select_all = function(value,lists,key){
		if(!key){key = "value"}

		for(var i in lists){
			if(lists[i]["uneditable"] !== undefined){continue;}
			lists[i][key] = value;
		}
	}

	/*Mostly called from directives that's unable to load the Notification service*/
	me.notify = function(msg,type){
		if(type == "success"){
			Notification.success(msg)
		}else if(type == "error"){
			Notification.error(msg)
		}
	}

	me.loader = function(remove,key){		
		if(!key){
			key = "main";
		}
		me.page_loader[key] = !remove;
	}

	me.list_format_date = function(lists,fields,from_backend){
		for(i = 0;i < lists.length; i++){
			lists[i] = me.format_date(lists[i],fields,from_backend)
		}
        return lists
    }

	me.format_date = function(obj,fields,from_backend){
		if(!fields){fields = ["date_from","date_to","date"]}
        for(var i in fields){
            var field = fields[i];
            if(obj[field]){
            	if(from_backend){
                	obj[field] = new Date(obj[field]);
            	}else{
                	obj[field] = moment(obj[field]).format('YYYY-MM-DD h:i:s');
            	}
            }
        }
        return obj
    }

    me.go = function(url,newtab){
    	window.location.href = url;
    }

    me.reset_date = function(obj,include_from){
    	var current_year = moment().year()
    	var current_month = moment().month() + 1
    	var date_from = moment([current_year, current_month - 1]);
    	var date_to = moment(date_from).endOf('month');
    	if(include_from){
    		obj["date_from"] = new Date(date_from);
    	}
    	obj["date_to"] = new Date(moment());
    }

    me.key_in_list = function(item_to_search,arr){
    	var status = false;	
    	for(index in arr){
    		item = arr[index]
    		if(item_to_search == item){
    			status = true;
    		}
    	}
    	return status
    }

    function sortByAttribute(array, ...attrs) {
      // generate an array of predicate-objects contains
      // property getter, and descending indicator
      let predicates = attrs.map(pred => {
        let descending = pred.charAt(0) === '-' ? -1 : 1;
        pred = pred.replace(/^-/, '');
        return {
          getter: o => o[pred],
          descend: descending
        };
      });
      // schwartzian transform idiom implementation. aka: "decorate-sort-undecorate"
      return array.map(item => {
        return {
          src: item,
          compareValues: predicates.map(predicate => predicate.getter(item))
        };
      })
      .sort((o1, o2) => {
        let i = -1, result = 0;
        while (++i < predicates.length) {
          if (o1.compareValues[i] < o2.compareValues[i]) result = -1;
          if (o1.compareValues[i] > o2.compareValues[i]) result = 1;
          if (result *= predicates[i].descend) break;
        }
        return result;
      })
      .map(item => item.src);
    }

    /*Place some of the defaults if can be change or depends on some functions.*/
    me.pagination = {"limit" : 10,"current_page" : 1,"total_records" : 0,"total_pages" : 0,"limit_options_orig" : [20,50,100,150],"limit_options" : []}
    me.filters = {}
    me.sort = {"sort_by": me.sort_default(),"reverse": false};
});