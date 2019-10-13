#!/usr/bin/python3

import requests
import os
import code
import sys
import json

config_dict = {}

session = None

config_example = {
    "login_token": "",
    "domain": "",
    "subdomain": ""
}

def get_records_list(config=None):
    global session
    if not session:
        session = requests.Session()
    if not config:
        config = config_dict
    data = {
        "login_token": config["login_token"],
        "format": "json",
        "domain": config["domain"],
        "record_type": "A"
    }
    raw_list = json.loads(session.post("https://dnsapi.cn/Record.List", data=data).text)
    return raw_list["records"]

def get_record_info(config=None):
    if not config:
        config = config_dict
    records_list = get_records_list(config)
    for record in records_list:
        if record["name"] == config["subdomain"]:
            return record
    return None

def get_new_ip():
    return input()

def update(new_ip, config=None):
    global session
    if not session:
        session = requests.Session()
    if not config:
        config = config_dict
    record = get_record_info(config)
    if not record:
        return {"record": {}, "status": {"code": "-1", "message": "Record not found."}}
    if (new_ip == record["value"]):
        return {"record": {}, "status": {"code": "-1", "message": "IP is already the latest."}}
    else:
        data = {
            "login_token": config["login_token"],
            "format": "json",
            "domain": config["domain"],
            "record_id": record["id"],
            "sub_domain": record["name"],
            "value": str(new_ip),
            "record_type": "A",
            "record_line_id": record["line_id"]
        }
        return json.loads(session.post("https://dnsapi.cn/Record.Modify", data=data).text)

def load_config(path="./"):
    global config_dict
    if not path.startswith("/") or not path.startswith("~"):
        path = os.getcwd() + "/" + path
    if not path.endswith("/"):
        path += "/"
    if os.path.isfile(path + "config.json"):
        with open("config.json", "r") as config_file:
            config_dict = json.load(config_file)
            return True
    else:
        with open(path + "config_template.json", "w") as template_file:
            json.dump(config_example, template_file)
            print("config.json not found. template file created at: " + path + "config_template.json")
            return False

def help():
    print("Command arguments:")
    print("-h: Show this message and quit, ignoring other arguments")
    print("-c: Specify the **PATH** of file config.json. Default: current working directory")
    print("-I: Specify the new IP. Default: standard input (syntax unchecked)")
    print("-i: Enter Python interactive mode after execution")

if __name__ == "__main__":
    if "-h" in sys.argv:
        help()
        exit()
    config_flag = True
    if "-c" in sys.argv:
        try:
            config_flag = load_config(sys.argv[sys.argv.index("-c")+1])
        except:
            print("Config file path expected!")
            config_flag = False
    else:
        config_flag = load_config()
    if not config_flag:
        exit(-1)
    new_ip = ""
    if "-I" in sys.argv:
        try:
            new_ip = sys.argv[sys.argv.index("-I")+1]
        except:
            print("New IP expected in argument!")
            exit(-1)
    else:
        print("Enter new IP: ", end="")
        new_ip = get_new_ip()
    session = requests.Session()
    print(update(new_ip))
    if "-i" in sys.argv:
        code.interact(local=locals())