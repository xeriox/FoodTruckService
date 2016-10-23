'use strict'

angular.module 'FoodTruckService.App', [
  'ngMap'
]

.controller 'FoodTruckServiceAppController', ($scope, $http, NgMap) ->
  _this = @

  # Just choosed a place in San Fransisco where i know there is food trucks around, there is none in Denmark

  $scope.latitude_search = "37.786904919457"
  $scope.longitude_search = "-122.390920262962"
  $scope.distance_search = "5000"
  $scope.foodtype_search = ""
  $scope.map_center =  $scope.latitude_search + "," + $scope.longitude_search
  $scope.foodtrucks = []

  $scope.center_icon = {
        "scaledSize": [32, 32],
        "url": "./static/images/center_icon.png"
  }

  $scope.selected_foodtruck = {}

  $scope.showFoodTruckDetail = (e, foodtruck) ->
    $scope.selected_foodtruck = foodtruck
    _this.map.showInfoWindow('foodtruck-infowindow', foodtruck.id)
    return

  $scope.hideFoodTruckDetail = () ->
    _this.map.hideInfoWindow('foodtruck-infowindow')
    return

  $scope.mapInitialized = (map) ->
    _this.map = map

    location = _this.map.getCenter()

    $scope.map_center = location.lat() + "," + location.lng()

    $scope.search()

    return

  $scope.centerChanged = (event) ->

    location = _this.map.getCenter()

    $scope.latitude_search = location.lat()
    $scope.longitude_search = location.lng()

    $scope.map_center = location.lat() + "," + location.lng()

    return

  $scope.search = () ->

    filter = []

    if $scope.latitude_search != "" and  $scope.longitude_search != ""
      gps_location_criteria = {
        'property' : 'location',
        'comparator' : 'nearby:' + $scope.distance_search,
        'value' : $scope.latitude_search + "," + $scope.longitude_search
      }

      filter.push gps_location_criteria

      _this.map.setCenter(new google.maps.LatLng($scope.latitude_search,$scope.longitude_search))


    if $scope.foodtype_search != ""
      foodtype_criteria = {
        'property' : 'food_items',
        'comparator' : 'contain',
        'value' : $scope.foodtype_search
      }

      filter.push foodtype_criteria

    $http.get("api/foodtrucks", {
      params: {
        filter: [filter]
      }
    }).then (response) ->
      $scope.foodtrucks = response.data
      return
    return
  return