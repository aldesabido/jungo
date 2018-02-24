var app = angular.module("orders",['common_module','ui.router']);

app.controller('ordersCtrl', function($scope,$http,$controller,$state,CommonFunc,CommonRead,CommonFac,Notes,Photos,Documents){
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var me = this;
    var btnstandby = "btn btn-default btn-w-m";
    var btnactive = "btn btn-success btn-w-m";
    me.current_tab = "active";
    me.status = {
        "active": [{"value": "completed","display": "Complete"},{"value": "hold","display": "Hold"},{"value": "cancelled","display": "Cancel"}],
        "hold": [{"value": "active","display": "Unhold"},{"value": "cancel","display": "Cancel"}],
        "completed": [{"value": "qc","display": "QC"},{"value": "submitted","display": "Submit"},{"value": "active","display": "Active"},{"value": "cancelled","display": "Cancel"}],
        "qc": [{"value": "cancel","display": "Cancel"}],
        "submitted": [{"value": "completed","display": "Unsubmit"}],
        "cancelled": [{"value": "active","display": "Open"}]

        /*"active": [{"value": "hold","display": "Hold"},{"value": "complete","display": "Complete"},{"value": "cancel","display": "Cancel"}],
        "hold": [{"value": "active","display": "Unhold"},{"value": "cancel","display": "Cancel"}],
        "completed": [{"value": "qc","display": "QC"},{"value": "submit","display": "Submit"},{"value": "active","display": "Active"},{"value": "cancel","display": "Cancel"}],
        "hold": [{"value": "cancel","display": "Cancel"}],
        "submitted": [{"value": "complete","display": "Unsubmit"}],
        "cancelled": [{"value": "laststatus","display": "Open"}]*/
    }


    me.reset_tab_status = function(){
        me.btnclass = {
            "active": btnstandby,
            "hold": btnstandby,
            "completed": btnstandby,
            "qc": btnstandby,
            "submitted": btnstandby,
            "cancelled": btnstandby,
        }
    }

    me.change_tab = function(tab){
        me.reset_tab_status();
        me.selected_status = null;
        me.selected_record = null;
        me.btnclass[tab] = btnactive;
        me.current_tab = tab;
        me.read_pagination(true);
    }

    me.create_dialog = function(record){
        var template_url = "/orders/create_dialog/"
        me.reset_data();
        if(record){
            me.record = angular.copy(record);
            template_url += me.record.id;
        }
        me.open_dialog(template_url,"");
    }

    me.create = function(controller_instance){
        var post = me.post_generic("/orders/create/",me.record,"main",true,false,true)
        post.success(function(response){
            me.read_pagination();
        })
    }


    me.load_to_edit = function(record){
        var post = me.post_generic("/orders/load_to_edit/"+record.id,me.record,"main")
        post.success(function(response){
            me.create_dialog(response);
        })
    }

    me.delete = function(record){
        var confirmation = CommonFunc.confirmation("Remove "+record.order_number+"?");
        confirmation.then(function(){
            var post = me.post_generic("/orders/delete/"+record.id,{},"main",true)
            post.success(function(){
                me.main_loader();
            })
        })
    }

    me.read_pagination = function(reset){
        if(reset){me.filters = {};}
        me.filters["sort"] = me.sort;
        me.filters["status"] = me.current_tab;
        var filters = angular.copy(me.filters);
        filters["pagination"] = me.pagination;
        var post = me.post_generic("/orders/read_pagination/",filters,"main")
        post.success(function(response){
            me.records = response.data;
            me.starting = response.starting;
            me.ending = response.data.length;
            me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
            me.pagination.limit_options.push(response.total_records)
            me.pagination["total_records"] = response.total_records;
            me.pagination["total_pages"] = response.total_pages;
            me.success_count = response.success_count;
        });
    };

    me.change_status = function(){
        params = {
            "order": me.selected_record.id,
            "status": me.selected_status.value
        }
        var post = me.post_generic("/orders/update_status/",params,"main",true)
        post.success(function(response){
            me.read_pagination();
        })
    }

    me.order_details_dialog = function(record){
        var post = me.post_generic("/orders/order_details/"+record.id,{},"main")
        post.success(function(response){
            me.status_histories = response.status_histories;
            me.assignment_histories = response.assignment_histories;
            me.open_dialog("/orders/order_details_dialog/");
        })
    }


    me.order_status_history_dialog = function(record){
        var post = me.post_generic("/orders/show_history/"+record.id,{},"main")
        post.success(function(response){
            me.status_histories = response;
            me.open_dialog("/orders/order_status_history_dialog/");
        })
    }

    me.credential_dialog = function(record){
        me.open_dialog("/orders/credential_dialog/");
    }





    /*Notes*/
    me.notes_dialog = function(record){
        Notes.open_dialog(me,record);
    }

    me.create_note = function(note){
        Notes.create(me,note);
    }

    me.delete_note = function(note){
        Notes.delete(me,note);
    }
    /*End Notes*/

    /*Photos*/
    me.photos_dialog = function(record){
        Photos.open_dialog(me,record)
    }
    me.photos_read = function(){
        Photos.read(me)
    }
    me.photos_remove = function(phot){
        Photos.remove(me,phot);
    }
    /*End Photos*/

    /*Photos*/
    me.docs_dialog = function(record){
        Documents.open_dialog(me,record)
    }

    me.docs_read = function(record){
        Documents.read(me,record)
    }

    me.docs_remove = function(record){
        Documents.remove(me,record)
    }
    /*End Photos*/


    /*Order Assignment*/
    me.order_assignment_dialog = function(record){
        me.current_record = record;
        me.current_assignee = undefined;
        me.reset_assignee();


        var post = me.post_generic("/orders/get_assignee/"+me.current_record.id,{},"main")
        post.success(function(response){
            me.reset_assignee(response);
            me.open_dialog("/orders/order_assignment_dialog/");        
        })
        /*Get current assignee here and pass the result to check_assignee*/
    }

    me.reset_assignee = function(cda){
        me.current_assignee = false;
        for(i in me.cdas){
            if(cda){
                if(cda.id == me.cdas[i].id){
                    me.cdas[i].assigned = true;
                    me.current_assignee = angular.copy(me.cdas[i]);
                }
            }else{
                me.cdas[i].assigned = false;
            }
        }
    }

    me.check_assignee = function(cda){
        if(!cda.assigned){
            me.reset_assignee();
        }else{
            me.reset_assignee();
            cda.assigned = true;
            me.current_assignee = angular.copy(cda);
        }
    }

    me.set_assignee = function(){
        var filters = {}

        // if "assignee": me.current_assignee
        if(me.current_assignee){
            filters["assignee"] = me.current_assignee;
        }

        var post = me.post_generic("/orders/set_assignee/"+me.current_record.id,filters,"main",true,false,true)
        post.success(function(response){
            me.read_pagination();
        })
    }

    me.order_assignment_history_dialog = function(record){
        var post = me.post_generic("/orders/read_order_assignment_history/"+record.id,{},"main")
        post.success(function(response){
            me.assignment_histories = response;
            me.open_dialog("/orders/order_assignment_history_dialog/");
        })
    }


    /*End of Order Assignment*/



    /*Admin*/
    me.read_clients = function(user_type){
        me.user_type = user_type;
        if(user_type == "admin"){
            CommonRead.read_clients(me);
        }
    }

    me.read_credentials = function(){
        filters = {"user": me.record.client}
        CommonRead.read_credentials(me,filters);
    }

    /*End of Admin*/



    me.reset_data = function(){
        me.record = {"address": "Test"}
    }


    me.main_loader = function(reset){
        me.read_pagination(reset);    
    }

    me.change_tab('active');
    CommonRead.read_credentials(me);
    CommonRead.read_order_types(me);
    CommonRead.read_cdas(me);
});