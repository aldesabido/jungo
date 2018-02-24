/**
 * icheck - Directive for custom checkbox icheck
 */
function icheck($timeout) {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function($scope, element, $attrs, ngModel) {
            return $timeout(function() {
                var value;
                value = $attrs['value'];

                $scope.$watch($attrs['ngModel'], function(newValue){
                    $(element).iCheck('update');
                })

                return $(element).iCheck({
                    checkboxClass: 'icheckbox_square-green',
                    radioClass: 'iradio_square-green'

                }).on('ifChanged', function(event) {
                        if ($(element).attr('type') === 'checkbox' && $attrs['ngModel']) {
                            $scope.$apply(function() {
                                return ngModel.$setViewValue(event.target.checked);
                            });
                        }
                        if ($(element).attr('type') === 'radio' && $attrs['ngModel']) {
                            return $scope.$apply(function() {
                                return ngModel.$setViewValue(value);
                            });
                        }
                    });
            });
        }
    };
}

function dropzone($cookies) {
    return {
        restrict: 'C',
        link: function(scope, element, attrs) {
            scopemain = scope.$parent.main;
            scopemain.upload_type = attrs.uploadType;
            var config = {
                paramName: "file",
                maxFileSize : 10,
                parallelUploads : 100,
                uploadMultiple: true,
                autoProcessQueue : false,
                addRemoveLinks : true,
                
                headers: { "X-CSRFToken": $cookies.get("csrftoken")},
                init: function() {
                    var submitButton = document.querySelector("#upload_now")
                    submitButton.addEventListener("click", function() {
                        scope.processDropzone();
                    });
                },
            };

            var eventHandlers = {
                'addedfile': function(file) {
                    scope.file = file;
                    console.log(scope.file)
                    scope.$apply(function() {
                        scopemain.file_added = true;
                    });
                },
                'success': function (file, response) { //add 'complete' event here.
                    if(scopemain.upload_type == "order_photos"){
                        scopemain.photos_read();
                        scopemain.read_pagination();
                    }
                    if(scopemain.upload_type == "order_docs"){
                        scopemain.docs_read();
                        scopemain.read_pagination();
                    }
                    this.removeFile(file);
                },
                'error': function (file, response) {
                    scopemain.notify(response,"error")
                    this.removeFile(file);
                }
            };


            if(scopemain.upload_type == "order_photos"){
                config["acceptedFiles"] = 'image/*';
                config["url"] = "/orders/upload/"+scopemain.selected_record.id+"/";
            }
            if(scopemain.upload_type == "order_docs"){
                config["url"] = "/orders/docs_upload/"+scopemain.selected_record.id+"/";
            }

            

            dropzone = new Dropzone(element[0],config);

            angular.forEach(eventHandlers, function(handler, event) {
                dropzone.on(event, handler);
            });
            
            scope.processDropzone = function() {
                dropzone.processQueue();
            };
        }
    }
}

angular.module('lib_directives', ["ngCookies"])
    .directive('dropzone', ['$cookies', dropzone])
    .directive("icheck", icheck)