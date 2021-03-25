/*
    Copyright 2020 XEBIALABS
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
// var dataForGraph = {};
// dataForGraph['test'] = 132;
console.log("javascript")
angular
		.module('tutor', [])
		.config(
				function($httpProvider) {

					// The following code retrieves credentials from the main XL Deploy application
					// and tells AngularJS to append them to every request.
					var flexApp = parent.document
							.getElementById("flexApplication");
					if (flexApp)
						$httpProvider.defaults.headers.common.Authorization = flexApp
								.getBasicAuth();

				})
		.controller(
				'TutorController',
				function($http, $scope) {
					$scope.message = "Hello World";
					$scope.myFunction = function() {
						$http.get('/api/extension/counter').
							  success(function(data) {
									$scope.response = data.entity;
                  $scope.TotalScore = data.entity.TotalScore;
                  $scope.Infrastructure = data.entity.InfrastructureComplexScore;
                  $scope.Applications = data.entity.ApplicationsComplexScore;
									$scope.names = [];
									$scope.apps = [];
									$scope.counts = [];
									response = [
									{value: $scope.Applications, name: 'Applications'},
									{value: $scope.Infrastructure, name: 'Infrastructure' }];
									// response['Infrastructure'] = $scope.Infrastructure;
									// response['Applications'] = $scope.Applications;
									var bigResponse = [];
									//bigResponse[0] = {value: $scope.Applications, name: 'Applications'}
									var apps = data.entity.appSum;
									infraStart =0;
									angular.forEach(apps, function (value, key) {
											bigResponse[key] = {value: value.count, name: value.name };
											var context = value;//value.name + " has a complexity score of " + value.count.toString()
											$scope.apps.push(context);
											infraStart++;
									});
									var values = data.entity.infraSum
									angular.forEach(values, function (value, key) {
											bigResponse[infraStart+key] = {value: value.count, name: value.name};
										  var context = value;//value.name + " has a complexity score of " + value.count.toString()
                			$scope.names.push(context);
            			});
									contributionsSummary(response, bigResponse, "chart");
							  }).
							  error(function(data) {
									$scope.response = data.entity;
							  });
					};
				});
