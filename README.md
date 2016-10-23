# FoodTruckService

##Purpose
The purpose of this service is to able to find food trucks nearby a specific location. The initial requirement was to build a service that could find food trucks in San Francisco, but I’ve focused on making the service a world wide solution, only limited by amount of food truck data available.

I’ve created the solution so it’s possible to search for food trucks within a distance of a certain geo location. It’s also possible to filter by the food you wish to eat.

The solution consists of a very lightweight and simple front-end and a more complex backend rest service

##Architecture
I’ve chosen to build a classic web-tier solution with a single page frontend, build on top of a rest service. I’ve been mostly focusing on the query part, as if this solution was part of a CQRS architecture, therefor there hasn’t been a lot of focus on the fetching part, which is limited to a single fetching script.

The rest service architecture follows a general layered design with a clear separation between service layer and business-/data access-layer. I’ve chosen to use the architectural pattern, repository pattern, as seperation. 

###Stack
There was no requirement to the stack, so it has been chosen based on best architectural fit, known languages and stack used by Uber.

I’ve chosen to use elasticsearch as database because it’s highly optimized for searching and has a natural fit for searching by geo location and It’s very scalable. And since we don't have any data transaction model, I found it as a perfect fit for this kind of service.

I’ve chosen python as language because I’ve had previous experience with that and I know that Uber is using that a lot.

The web framework is tornado because it seems like a decent fast lightweight web framework, based on python and I know that Uber is using that.

For the frontend I’ve chosen AngularJS v1, and using the scripting language Coffescript. I’ve chosen AngularJS because I find the framework very nice, and has a very fine separation of concerns. The reason for choosing Coffescript instead of just vanilla javascript is because I like the abstraction. Coffescript make the code very clean but still create a nice readably javascript afterwards.

###Scaling
Since the solution is based on rest service, and therefore stateless, it allows us to scale horizontal, adding more resources as the load increase. I’ve chosen to deploy the solution with docker, this allow us to easily managing scaling by using the right toolset, like AWS ECS, docker swarm etc. 

Currently the demo version of this service is hosted in AWS, and using AWS ECS. It consists of two nano EC2 instances with a load balancer in front of it, should this ever be a world wide service, it would be easy to add more resources.

Elastic search is also highly scaleable and they claims to be able to scale horizontal, the demo service is using a managed cluster, hosted by AWS.

Given the known data set for food trucks in San Francisco, it would have been worth discussing the need of a central database at all, since it could easily be cached or handled client side. But given that the purpose of this service was to support a world wide solution, I’ve chosen to stick with a database. It of cause always make sense to look into caching strategies for further scalability.
###Security

When building a web solution you should always be aware of the OWASP top 10 suggestion. But since this service is reduced to a query only service, with no input and no login functionality, and given the time frame, I haven’t spent much time focusing on this.

## Production-readiness
There is no logging and monitoring, but preferably you would log all activities and request, with a correlation id from the client or services to be able to follow the request stack trace. Especially if the system should use several different services, micro-/nano-service architecture.

It would also make sense to monitor response time, min, max and avg. and provide that information to the load balancer or even better some kind of auto scale functionality.

Before deployment monitoring should also be able to do proper load test of the service, and testing that changes hasn't caused any performance drop. 

## Known limitation

I've would loved to spent more time on building the correct UI and UX for this service, but given the time frame, (and a lot of time wasted to make the Google Map Directive behave), i chosed to keep it simple.

The test coverage should also be higher but given the time frame again, i choosed to do a few so you have someting for the review

##Experience
I haven’t been developing much in almost 1,5 year, because I’ve been in a management position, where there unfortunately wasn't much time for hands on coding, I however, have been involved with the architectural discussion and decisions.

I have previously been developing a lot in python, but that’s about 4 years ago, so if my code it not as pythonic as it should be, this might be the reason.

I didn’t have any experience with Tornado before building this project

I've been using elasticsearch before but mostly for logging, so this is actually my first project where I use it as primary database.

## Links

Live WebApp: http://ec2contai-ecselast-1039w1ldqm2e2-1302854665.eu-west-1.elb.amazonaws.com/

Live Api: http://ec2contai-ecselast-1039w1ldqm2e2-1302854665.eu-west-1.elb.amazonaws.com/api

** Remember to append endpoint, otherwise you will get a not found error, see API doc below **

Linkedin profile: https://www.linkedin.com/in/andersarnfast

# API Doc

### Request Query Language
All LIST request can include different query parameters to make the result more specific  
Queries are applied as `GET-parameters`  

#### Pagination
Pagination can be applied directly through limit and offset parameters

| Field      | Type        | Details  |
| :--------- | :---------- | :------- |
| limit      | Integer     | Default limit is 1000 |
| offset     | Integer     | Default offset is 0 |

#### Conditions

The value should be a JSON array of filter objects, following the form specified below

| Field      | Required |   Type   | Details |
| -----      | :------: | :------: | ------  |
| property   |   YES    | `string` | This is the property you want to filter on|
| value      |   YES    | `string` | This is the value to search for |
| comparator |   YES    | `string` | The comparator of your condition. |

*Filter objects types*

**GPSPoint Filter**

| comparator        | Value                 | Details |
| -----             | :------:              |------|
| nearby:{distance} | latitude,longitude    | This is used for finding items within a distance of a specific location, distance parameter define the search radius in meters |

***EXAMPLE***
```
/foodtrucks?filter=[
    {"property":"location","comparator":"nearby:1000","value":"37.7891192076677,-122.395881039335"}
  ]
```

Finding all items within a radius of 1000 meter for specific location.

**String Filter**

| Comparator        | Value     | Details              |
| -----             | :------:  |  ------                             |
| contain           | String    | Search for string or string array which contain specific the value|

***EXAMPLE***
```
/foodtrucks?
  filter=[
    {"property":"food_items", "comparator":"contain", "value":"sandwich" }
  ]
```


***EXAMPLE***
```
/foodtrucks?
  filter=[
    {"property":"location","comparator":"nearby:1000","value":"37.7891192076677,-122.395881039335"},
    {"property":"food_items", "comparator":"contain", "value":"sandwich" }
  ]
```

### Endpoints

GET /foodtrucks

*Filter properties*

| Property      | Required  |   Type            | Details |
| -----         | :------:  | :------:          | ------  |
| location      |   NO      | GPSPoint Filter   |         |
| food_items    |   NO      | String Filter     |         |

*Model*

| Property                      |   Type            | Details |
| -----                         |:------:           | ------  |
| id                            | String            |         |
| opening_hours                 | String            |         |
| location_description          | String            |         |
| name                          | String            |         |
| location                      | GPS Point Object  | ex.     "location": { "latitude": 37.792109338609,"longitude": -122.395803865502 }         |
| food_items                    | String            |         |