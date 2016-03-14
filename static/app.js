var recipe = angular.module('recipe', []);

String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

recipe.controller('homeController', function ($scope,$http) {
    $scope.parsed = false;
    
    $scope.capitalizeFirst = function(str) {
        str[0] = str[0].toUpperCase();
        return str;
    }
    
    $scope.getRecipe = function() {
        var parsed_url = encodeURIComponent($scope.url);
        $http({
          url:$SCRIPT_ROOT + '/_recipe_scraper/' +parsed_url,
          method: "GET"
        }).success(function(response){
            $scope.steps = response.steps;
            $scope.recipe = response.results;
            $scope.ingredients = response['results']['ingredients'];
            $scope.primary_method = response['results']['primary cooking method'];
            $scope.methods = response['results']['cooking methods'];
            $scope.tools = response['results']['cooking tools'];
            $scope.vegetarian = response['vegetarian'];
            $scope.vegan = response['vegan'];
            $scope.low_carb = response['low-carb'];
            $scope.low_sodium = response['low-sodium'];

            $scope.parsed = true;
 
    });
  }
  // $scope.change_year = function (year) {
  //   $scope.category = false;
  //   $scope.working = true;
  //   $http({
  //     url: $SCRIPT_ROOT + '/_get_year/' + year,
  //     method: "GET"
  //   }).success(function(response){
  //     $scope.working = false;
  //     $scope.category = response.result;
  //   });
  // }

  // $scope.change_options = function (option) {
  //   preprocess();
  //   $http({
  //     url: $SCRIPT_ROOT + '/_run_category',
  //     method: "GET",
  //     params: {
  //       year: $scope.year,
  //       category: option
  //     }
  //   }).success(function(response){
  //     $scope.working = false;
  //     switch (option) {
  //       case "hosts":
  //         $scope.name = $scope.year + " Golden Globe Hosts";
  //         $scope.list_result = response.result;
  //         break;
  //       case "awards":
  //         $scope.name = $scope.year + " Golden Globe Awards";
  //         $scope.list_result = response.result;
  //         break;
  //       case "nominees":
  //         $scope.name = $scope.year + " Golden Globe Nominees";
  //         $scope.nom_keys = Object.keys(response.result);
  //         $scope.nom_results = response.result;
  //         break;
  //       case "presenters":
  //         $scope.name = $scope.year + " Golden Globe Presenters";
  //         $scope.presenters = response.result;
  //       case "winner":
  //         $scope.name = $scope.year + " Golden Globe Winners";
  //         $scope.winners = response.result;
  //     }
  //   });
  // }
});