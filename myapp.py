from flask import Flask, jsonify, json, request
from cassandra.cluster import Cluster
import json
import requests
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import requests_cache
import pandas as pd






requests_cache.install_cache('tfl_api_cache',backend='sqlite',expire_after=12000)

app = Flask(__name__,instance_relative_config=True)


"""
This class is for get TflBikes (Santander Bikes) bikepoint status data
By calling API wich tfl provides
"""
class getData():
    def getAPIData():
            #Get json data
            url = 'https://api.tfl.gov.uk/bikepoint'
            resp = requests.get(url=url)
            data_array = resp.json()

            #Get data this services need
            id_list = [int(data_array[i]['id'].split("_")[1]) for i in range(0, len(data_array))]
            name_list = [data_array[i]['commonName'] for i in range(0, len(data_array))]
            locked_list = [data_array[i]['additionalProperties'][2]['value'] for i in range(0, len(data_array))]
            bike_left_list = [int(data_array[i]['additionalProperties'][6]['value']) for i in range(0, len(data_array))]
            capacity_list = [int(data_array[i]['additionalProperties'][7]['value']) for i in range(0, len(data_array))]
            total_dock_list = [int(data_array[i]['additionalProperties'][8]['value']) for i in range(0, len(data_array))]
            all_list = pd.DataFrame(list(zip(id_list,name_list,locked_list,
                                            capacity_list, total_dock_list,bike_left_list)), columns = ["Station ID","Station Name","Closed","Capacity","TotalDock","Bikeleft"])

            return(all_list)


"""
Class SecurityCheck provides authentication function to make sure user has enter the right api_key and user_app_id while calling the service.
The result will return as a boolean value
"""
class SecurityCheck():
    def check():
        user_app_id = request.args.get('app_id')
        user_api_key = request.args.get('api_key')
        bIsPass = DbUtil.AuthCheck(user_app_id,user_api_key)
        #bIsPass = True
        return(bIsPass)


"""
Class DbUtil provides function to interactive with cassandra
Using api_key and app_id as conditions
"""

class DbUtil():
    def AuthCheck(user_app_id,user_api_key):
        cluster = Cluster(['cassandra'])
        session = cluster.connect('tflbike')
        rows = session.execute("""SELECT COUNT(*) AS CNT FROM user WHERE app_id='{}' and api_key='{}' ALLOW FILTERING""".format(user_app_id,user_api_key))
        for user_row in rows:
            if(user_row.cnt>0): #If query returns rows count>0, authentication success
                return True
            else:
                return False


"""
Pattern '/tflbikes/allList' returns the status data of all Tflbikes bike points
@ param :
@ return: json array
"""
@app.route('/tflbikes/allList', methods=['GET'])
def getAllList():
    bSecurityCheck = SecurityCheck.check()#authentication check

    if(bSecurityCheck==True):
        data = getData.getAPIData()
        #return(data.to_html(justify='center',index=False))
        return jsonify({'status':'success','message':'success','data':data.to_json(orient='records')}),200
    else:
        return jsonify({'status':'error','message':'SecurityCheck Error!'}),404



"""
Pattern '/tflbikes/allList/<id>' returns the status data of specific bikepoint
@ param : station id
@ return: json array
"""

@app.route('/tflbikes/stationstat/<id>', methods=['GET'])

def get_station_by_id(id):

    bSecurityCheck = SecurityCheck.check()#authentication check

    if(bSecurityCheck==True):
        data = getData.getAPIData()
        filterStationId = data['Station ID']==int(id)
        result = data[filterStationId]
    #return(result.to_html(justify='center',index=False))
        return jsonify({'status':'success','message':'success','data':result.to_json(orient='records')}),200
    else:
        return jsonify({'status':'error','message':'SecurityCheck Error!'}),404

"""
Pattern '/tflbikes/route/<Start_ID>/<End_ID>' returns the status data of two specific bikepoints
@ param : Start_ID, End_ID
@ return: json array
"""
@app.route('/tflbikes/route/<Start_ID>/<End_ID>', methods=['GET'])

def get_route_station_status(Start_ID,End_ID):
    bSecurityCheck = SecurityCheck.check()#authentication check

    if(bSecurityCheck==True):
        data = getData.getAPIData()
        filterRoute = (data['Station ID']==int(Start_ID)) | (data['Station ID']==int(End_ID))
        result = data[filterRoute]
        #return(result.to_html(justify='center',index=False))
        return jsonify({'status':'success','message':'success','data':result.to_json(orient='records')}),200
    else:
        return jsonify({'status':'error','message':'SecurityCheck Error!'}),404



"""
Pattern '/tflbikes/aval/<Bikeleft>' returns bikepoints has number of bike more than the quantity which user assign
@ param : Bikeleft
@ return: json array
"""

@app.route('/tflbikes/aval/<Bikeleft>', methods=['GET'])

def get_aval_station(Bikeleft):

    bSecurityCheck = SecurityCheck.check()#authentication check

    if(bSecurityCheck==True):
        data = getData.getAPIData()
        filteravalBikeNum = data['Bikeleft']>=int(Bikeleft)
        result = data[filteravalBikeNum]
        #return(result.to_html(justify='center',index=False))
        return jsonify({'status':'success','message':'success','data':result.to_json(orient='records')}),200
    else:
        return jsonify({'status':'error','message':'SecurityCheck Error!'}),404


if __name__=="__main__":
        app.run(host='0.0.0.0',port=8080,debug=True)
