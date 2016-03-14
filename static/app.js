var recipe = angular.module('recipe', []);

String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

String.prototype.toTitleCase = function() {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

recipe.controller('homeController', function ($scope,$http) {
    $scope.parsed = false;
    $scope.transformed = false;
    $scope.loading = false;
    
    $scope.capitalizeFirst = function(str) {
        str[0] = str[0].toUpperCase();
        return str;
    }
    
    $scope.getRecipe = function() {
        $scope.loading = true;
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
            $scope.chinese = response['chinese'];
            $scope.italian = response['italian'];
            $scope.title = response['title'];
            $scope.imageUrl = response['imageUrl'];
            $scope.parsed = true;
            $scope.transformed = false;
            $scope.loading = false;
        });
  }
  
  $scope.getAttributes = function() {
      var vegetarianAttr = $scope.vegetarian ? "vegetarian" : "non-vegetarian";
      var veganAttr = $scope.vegan ? "vegan" : "non-vegan";
      var lowCarbAttr = $scope.low_carb ? "low-carb" : "non low-carb";
      var lowSodiumAttr = $scope.low_sodium ? "low-sodium" : "non low-sodium";
      
      return [vegetarianAttr,veganAttr,lowCarbAttr,lowSodiumAttr].join(", ")
  }
  
  $scope.transform = function() {
      $scope.loading = true;
      var params = $scope.transformation.split('_');
      var to_or_from = params[0];
      var category = params[1];
      var path = '/_transform/' + encodeURIComponent($scope.url) + '/' + to_or_from + '/' + category;
      
      $http({
        url:$SCRIPT_ROOT + path,
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
          $scope.title = response['title'];
          $scope.imageUrl = response['imageUrl'];
          $scope.parsed = true;
          $scope.transformed = true;
          $scope.loading = false;
      });
      
  }
  
  
});