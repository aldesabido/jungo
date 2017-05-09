var app = angular.module("app",['common_module','ui.router']);

app.config(['$httpProvider', '$interpolateProvider','$stateProvider', '$urlRouterProvider', function($httpProvider, $interpolateProvider, $stateProvider, $urlRouterProvider) {

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$interpolateProvider.startSymbol('{$').endSymbol('$}');

    $stateProvider
        .state('orders', { 
            url: '/orders',
            templateUrl: '/orders',
            controller: 'ordersCtrl as main',
            cache: false,
            resolve: {
                load: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'orders',
                            files: [ '/static/js/orders/orders.js',]
                        },
                    ]);
                }
            }
        })

        .state('settings', { 
            url: '/settings',
            templateUrl: '/settings',
            controller: 'settingsCtrl as main',
            cache: false,
            resolve: {
                load: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'settings',
                            files: [ '/static/js/settings.js',]
                        },
                    ]);
                }
            }
        })

        .state('users', { 
            url: '/users',
            templateUrl: '/users',
            controller: 'usersCtrl as main',
            cache: false,
            resolve: {
                load: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'users',
                            files: [ '/static/js/users.js',]
                        },
                    ]);
                }
            }
        })

        .state('reports', { 
            url: '/reports',
            templateUrl: '/reports',
            controller: 'reportsCtrl as main',
            cache: false,
            resolve: {
                load: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'reports',
                            files: [ '/static/js/reports.js',]
                        },
                    ]);
                }
            }
        })


    $urlRouterProvider.otherwise('orders');
}])

app.controller('wrapperCtrl', function($scope,$http,$controller,$state,CommonFunc,CommonRead,CommonFac){
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var me = this;
    var titles = {
        "home": "Home",
        "orders": "Orders",
        "settings": "Settings",
        "users": "Users",
        "reports": "Reports",
    }

    $scope.$on('$stateChangeStart',function(){me.page_loader["main"] = true;})
    $scope.$on('$stateChangeSuccess',function(){
        me.page_loader["main"] = false;
        CommonFac.set_title(titles[$state.current.name]);
        me.title = CommonFac.get_title();
        me.current_page = $state.current.name;
    })
});

app.controller('dashboardCtrl', function($scope,$http,$controller,$state,CommonFunc,CommonRead,CommonFac){
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var me = this;
});

