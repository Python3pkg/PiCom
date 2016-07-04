import requests
import json
import socket

api_id = None
api_key = None
deviceId = None
ip = None

tokenData = None


#Get the credentials from a JSON file
tokenFile = open("/usr/local/lib/python2.7/dist-packages/PiCom/token.json", 'r')
tokenData = tokenFile.read()
tokenFile.close()
tokenData = json.loads(tokenData)

api_id = tokenData['idA']
api_key = tokenData['key']
deviceId = tokenData['deviceId']
ip = tokenData['ip']


def getCredentials():
    return tokenData

def storeAPIID(idA):
    d = {
        'idA': idA,
        'key': api_key,
        'ip': ip,
        'deviceId': deviceId
    }
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(d))
    tokenFile.close()
    api_id = idA

def storeAPIKey(key):
    d = {
        'idA': api_id,
        'key': key,
        'ip': ip,
        'deviceId': deviceId
    }
    print(d)
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(d))
    tokenFile.close()
    api_key = key

def storeCredentials(APIId, APIKey):
    global api_id
    global api_key
    d = {
        'idA': APIId,
        'key': APIKey,
        'ip': ip,
        'deviceId': deviceId
    }
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(d))
    tokenFile.close()
    api_key = APIKey
    api_id = APIId

def storeID(idD):
    d = {
        'idA': api_id,
        'key': api_key,
        'ip': ip,
        'deviceId': idD
    }
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(d))
    tokenFile.close()
    deviceId = idD

def storeIP(ipD):
    d = {
        'idA': idA,
        'key': api_key,
        'ip': ipD,
        'deviceId': deviceId
    }
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(d))
    tokenFile.close()
    ip = ipD

def storeAll(idG, key, ipD, dID):
    d = {
        'idA': idG,
        'key': key,
        'ip': ipD,
        'deviceId': dID
    }
    tokenFile = open('token.json', 'w')
    tokenFile.write(json.dumps(d))
    tokenFile.close()
    api_id = idG
    api_key = key
    ip = ipD
    deviceId = dID

def renewCredentials():
    headers = {'Device-Id': api_id, 'Device-Key': api_key}
    r = requests.post("http://" + ip + "/api/v1/device/gen_token/" + str(deviceId), headers=headers)
    res = r.json()
    print(res)
    storeCredentials(res['token_id'], res['token_key'])

def testConnection():
    headers = {'Device-Id': api_id, 'Device-Key': api_key}
    print(ip)
    r = requests.get("http://" + str(ip) + "/api/v1/ping", headers=headers)
    if "Pong" in r.text:
        return True
    else:
        return r.text

def getApifree():
    headers = {'Device-Id': api_id, 'Device-Key': api_key}
    r = requests.get("http://" + ip + "/api/v1/apifrees", headers=headers)
    return r.json()

def updateGarageState(garageId, state):
    headers = {'Device-Id': api_id, 'Device-Key': api_key}
    payload = { "state": state}
    r = requests.post("http://" + ip + "/api/v1/garage/" + str(garageId), data=payload, headers=headers)
    return r.status_code

def sendAlarmSignal():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 5402))
    s.send((api_id + "*" + api_key + "*alarm/").encode())

