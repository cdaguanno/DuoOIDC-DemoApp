import http.client
import json

def GetInstanceState(arg1):
    conn = http.client.HTTPSConnection("6yah8uooec.execute-api.us-east-2.amazonaws.com")
    
    #payload = json.dumps({...})
    
    
    headers = {
      'Content-Type': 'application/json',
      'x-api-key': 'xfWnTdehiH9MhTrv5ddaQ2TNeiL5NnI1aViRtEMc'
    }
    conn.request("GET", "/prod/instances?region=" + arg1, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))
    #print(data.decode("utf-8"))
