# TflBike_api
The service provides set of restful API function to let client to get information about the bikepoint od TflBike (Santander Bike)

The Services are :

Pattern '/tflbikes/allList' 
description :returns the status data of all Tflbikes bike points
@ param :
@ return: json array


Pattern '/tflbikes/allList/<id>' 
description : returns the status data of specific bikepoint
@ param : station id (int)
@ return: json array
  

Pattern '/tflbikes/route/<Start_ID>/<End_ID>' 
description : returns the status data of two specific bikepoints
@ param : Start_ID (int), End_ID(int)
@ return: json array


Pattern '/tflbikes/aval/<Bikeleft>' 
description : returns bikepoints has number of bike more than the quantity which user assign
@ param : Bikeleft (int)
@ return: json array
