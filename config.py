__author__ = 'jmh081701'
#coding:utf8
import os
import json
from crypto.hash import  hashkey
def find_config():
    config_path = 'config.json'
    if os.path.exists(config_path):
        return config_path
    config_path = os.path.join(os.path.dirname(__file__), '../', 'config.json')
    if os.path.exists(config_path):
        return config_path
    return None

def get_config(config_path=None):
    if config_path==None:
        config_path=find_config()
    with open(config_path,"r") as fp:
        _config=json.load(fp)
    config={}
    try:
        config["type"]=_config["type"]
        config["hello"]="uestchello"
        if _config["type"]=="client":
            config["local_port"]=_config["local_port"]
            config["server_port"]=_config["server_port"]
            config["server_ip"]=_config["server_ip"]
            config["password"]=hashkey(_config["password"])
        elif _config["type"]=="server":
            config["server_port"]=_config["server_port"]
            config["server_ip"]=_config["server_ip"]
            config["password"]=hashkey(_config["password"])
        else:
            print(-1/0)
    except:
        print("config file error.")
        print('''config.json should like this:
{
"type":"client",
"local_port":9090,
"server_ip":"123.200.148.94",
"server_port":9091,
"password":"12345678"
}
or
{
"type":"server",
"server_ip":"123.200.148.94",
"server_port":9091,
"password":"12345678"
}
            ''')
        exit(-1)
    return  config
get_config()
