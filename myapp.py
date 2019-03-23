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



class getData():
    def getAPIData():
        tfl_api_url = 'https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml'
        response = requests.get(tfl_api_url)
        root = ET.fromstring(response.content)

        id_list = [int(root[i][0].text) for i in range(0, len(root))]
        name_list = [root[i][1].text for i in range(0, len(root))]
        locked_list = [root[i][6].text for i in range(0, len(root))]
        capacity_list = [int(root[i][11].text) for i in range(0, len(root))]
        total_dock_list = [int(root[i][12].text) for i in range(0, len(root))]

        all_list = pd.DataFrame(list(zip(id_list,name_list,locked_list,
                                 capacity_list, total_dock_list)), columns = ["Station ID","Station Name","Closed","Capacity","TotalDock"])
        all_list['Bikeleft'] = all_list['TotalDock']-all_list['Capacity']
        all_list = all_list.drop('Capacity',1)

        print(all_list)
        return(all_list)


class SecurityCheck():
    def check():
        #api_key = '0ba38fh'
        #app_id = 'Bgt56yhN'

        user_app_id = request.args.get('app_id')
        user_api_key = request.args.get('api_key')
        bIsPass = DbUtil.AuthCheck(user_app_id,user_api_key)

        #if (user_app_id == app_id and user_api_key == api_key):
        #    bIsPass = True
        #else:
        #    bIsPass = False

        return(bIsPass)

class DbUtil():
    def AuthCheck(user_app_id,user_api_key):
        cluster = Cluster(['35.246.43.76'])
        session = cluster.connect('tflbike')
        rows = session.execute("""SELECT COUNT(*) AS CNT FROM user WHERE app_id='{}' and api_key='{}' ALLOW FILTERING""".format(user_app_id,user_api_key))
        for user_row in rows:
            if(user_row.cnt>0):
                return True
            else:
                return False



@app.route('/tflbikes/allList', methods=['GET'])

def getAllList():
    bSecurityCheck = SecurityCheck.check()

    if(bSecurityCheck==True):
        data = getData.getAPIData()
        #return(data.to_html(justify='center',index=False))
        return jsonify(data.to_json(orient='records')),200
    else:
        return jsonify({'status':'error','message':'SecurityCheck Error!'}),404





@app.route('/tflbikes/stationstat/<id>', methods=['GET'])

def get_station_by_id(id):

    bSecurityCheck = SecurityCheck.check()

    if(bSecurityCheck==True):
        data = getData.getAPIData()
        filterStationId = data['Station ID']==int(id)
        result = data[filterStationId]
    #return(result.to_html(justify='center',index=False))
        return jsonify({'status':'success','message':'success','data':result.to_json(orient='records')}),200
    else:
        return jsonify({'status':'error','message':'SecurityCheck Error!'}),404

@app.route('/tflbikes/route/<Start_ID>/<End_ID>', methods=['GET'])

def get_route_station_status(Start_ID,End_ID):
    bSecurityCheck = SecurityCheck.check()

    if(bSecurityCheck==True):
        data = getData.getAPIData()
        filterRoute = (data['Station ID']==int(Start_ID)) | (data['Station ID']==int(End_ID))
        result = data[filterRoute]
        #return(result.to_html(justify='center',index=False))
        return jsonify({'status':'success','message':'success','data':result.to_json(orient='records')}),200
    else:
        return jsonify({'status':'error','message':'SecurityCheck Error!'}),404

@app.route('/tflbikes/aval/<Bikeleft>', methods=['GET'])

def get_aval_station(Bikeleft):

    bSecurityCheck = SecurityCheck.check()

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
