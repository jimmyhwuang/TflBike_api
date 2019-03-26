# TflBike API

The service provides set of restful API function to let client to get information about the bikepoint od TflBike (Santander Bike)

## How it works

TflBike API service provides Restful API function and will returns json format data to the client


## Technologies used

Python, json, Flask, pandas, Google Cloud Service (Cassandra, Kubernetes)

## Function List

### All Tflbike points status

```
Function : returns the status data of all Tflbikes bike points
url   : /tflbikes/allList
param :
return: json array
```

```
Function : returns the status data of specific bikepoint
url   : '/tflbikes/allList/<id>' 
param : station id (int)
return: json array
```

```
Function : returns the status data of specific bikepoint
url   : '/tflbikes/stationstat/<id>' 
param : station id (int)
return: json array
```

```
Function : Returns the status data of two specific bikepoints
url   :'/tflbikes/route/<Start_ID>/<End_ID>' 
param : Start_ID (int), End_ID(int)
return: json array
```

```
Function : returns bikepoints has number of bike more than the quantity which user assign
url   : '/tflbikes/aval/<Bikeleft>' 
param : Bikeleft (int)
return: json array
```



