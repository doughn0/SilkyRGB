import os
import re

from colors import PALETTES, get_palette
from effects.effect_store import MODES

CONFIG = {
    "fps": 30,
    "mode": "shimmer",
    "brightness": 7,
    "brightness.adaptive": False,
    "palette": "Knulli",
    "palette.swap": False,
    "palette.stealth": False,
    "palette.swap.secondary": False,
    "retroachievements": True,
    "battery.low": "notification",
    "battery.low.threshold": 20,
    "battery.charging": "notification",
}

conf_map = {
    "mode": {
        "type": "string"
    },
    "brightness": {
        "type": "int",
        "range": [0,10]
    },
    "brightness.adaptive": {
        "type": "bool"
    },
    "palette": {
        "type": "string"
    },
    "palette.swap": {
        "type": "bool"
    },
    "palette.stealth": {
        "type": "bool"
    },
    "palette.swap.secondary": {
        "type": "bool",
        "reqs": ['has_secondary']
    },
    "retroachievements": {
        "type": "bool"
    },
    "battery.low": {
        "type": "enum",
        "values": ["off", "notification", "continuous"]
    },
    "battery.low.threshold": {
        "type": "int",
        "range": [0,30]
    },
    "battery.charging": {
        "type": "enum",
        "values": ["off", "notification", "continuous"]
    }
}

for k in conf_map:
    conf_map[k]["value"] = CONFIG[k]

def get_param(key):
    ret = os.popen('knulli-settings-get '+"led."+key).read().strip()
    #print('read knulli option:', key, '| val:', ret)
    return ret

def read_config_knulli():
    for k in conf_map:
        set_option(k, get_param(k))

def bounds(val, bounds):
    return bounds[0] <= val <= bounds[1]

def set_option(key:str, val:str):
    try:
        if key == "mode":
            if val in MODES:
                CONFIG["mode"] = val

        if key == "palette":
            if val in PALETTES:
                CONFIG["palette"] = val

        if key == "brightness":
            if val.isnumeric() and bounds(int(val), conf_map['brightness']['range']):
                CONFIG["brightness"] = int(val)

        if key == "brightness.adaptive":
            CONFIG["brightness.adaptive"] = val == '1'

        if key == "palette.swap":
            CONFIG["palette.swap"] = val == '1'

        if key == "palette.stealth":
            CONFIG["palette.stealth"] = val == '1'

        if key == "palette.swap.secondary":
            CONFIG["palette.swap.secondary"] = val == '1'

        if key == "battery.charging":
            if val in conf_map['battery.charging']['values']:
                CONFIG["battery.charging"] = val
        
        if key == "battery.low":
            if val in conf_map['battery.low']['values']:
                CONFIG["battery.low"] = val

        if key == "battery.low.threshold":
            if val.isnumeric() and bounds(int(val), conf_map['battery.low.threshold']['range']):
                CONFIG["battery.low.threshold"] = int(val)

    except:
        pass
