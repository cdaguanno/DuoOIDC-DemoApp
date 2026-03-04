import http.client
import json

def PowerControl(action, instance_id, region):
    conn = http.client.HTTPSConnection("s337y0obzh.execute-api.us-east-2.amazonaws.com")
    
    payload = json.dumps({
        "action": action,        # "start" or "stop"
        "instance_id": instance_id,
        "region": region
    })
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'xfWnTdehiH9MhTrv5ddaQ2TNeiL5NnI1aViRtEMc'
    }
    
    conn.request("POST", "/Prod/", payload, headers)
    res = conn.getresponse()
    return res.read().decode("utf-8")
