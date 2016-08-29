// MODULE
var Game = angular.module('Game', []);

// CONTROLLERS
Game.controller('gameController', ['$scope', function ($scope) {
    $scope.text = "Choose a class above.";
    $scope.cards = '';
        $scope.testThis = "something";
    $scope.search = "";
    $scope.showGame = function() {
      //start tooltip
      $('[data-toggle="instructions"]').popover({
        html: true,
        trigger: 'focus hover'
      });

      $scope.points = [];
      $scope.plot = $.plot("#placeholder",[{
          data: $scope.points,
          points: {
            show : true,
            fill: true,
            fillColor: '#DAA831'
          },
          color: '#FFCD72'
        }], {
          xaxis: {
              ticks:10,
              min:0,
              max:100
          },
          yaxis: {
              ticks:10,
              min:0,
              max:100
          },
          grid: {
            clickable: true
          }
      });

      $scope.locatorState = new LocatorState(document.getElementById("locator"),
                                            "#points", false, "#nearness", "#location");

      $scope.locatorState.setGoal();
      $scope.locatorState.reset();

      $("#placeholder").bind("plotclick", function(event, pos, item) {
        $scope.points.pop();
        $scope.points.push([pos.x, pos.y]);
        console.log($scope.maxpoints);
        $scope.plot.setData([{
          data: $scope.points,
          clickable: false,
          points: {
            show: true,
            fill: true,
            fillColor: '#DAA831',
            radius: 10
          },
          color: '#FFCD72'
        }]);
        $scope.plot.draw();
        $scope.locatorState.update(pos);
        $scope.locatorState.draw();
      });

      $timeout.cancel($scope.mytimeout);
      $scope.time = $scope.timelimit;
      $scope.mytimeout = $timeout($scope.onTimeout,1000);
    };


}]);
