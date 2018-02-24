var app = angular.module("settings",['common_module','ui.router']);

app.controller('settingsCtrl', function($scope,$http,$controller,$state,CommonFunc,CommonRead,CommonFac){
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var me = this;
    var btnstandby = "btn btn-default btn-w-m";
    var btnactive = "btn btn-success btn-w-m";

    me.reset_tab = function(){
        me.btnclass = {
            "credentials": btnstandby,
        }
    }

    me.change_tab = function(tab){
        me.reset_tab();
        me.btnclass[tab] = btnactive;
    }

    me.create_dialog = function(record){
        me.record = {}
        if(record){
            me.record = angular.copy(record);
        }
        me.open_dialog("/credentials/create_dialog/","");
    }

    me.create = function(){
        var post = me.post_generic("/credentials/create/",me.record,"main",true,false,true)
        post.success(function(response){
            CommonRead.read_credentials(me);
        })
    }

    me.load_to_edit = function(record){
        me.create_dialog(record);
        /*var post = me.post_generic("/credentials/load_to_edit/"+record.id,{},"main")
        post.success(function(response){
            me.create_dialog(response);
        })*/
    }

    me.delete = function(record){
        var confirmation = CommonFunc.confirmation("Continue delete?");
        confirmation.then(function(){
            var post = me.post_generic("/credentials/delete/"+record.id,{},"main",true)
            post.success(function(response){
                CommonRead.read_credentials(me);
            })
        })
    }

    me.change_tab('credentials');
    CommonRead.read_companies(me);
    CommonRead.read_credentials(me);
});
