import requests

import helper.config

conf = helper.config.initconfig()

url = conf['iobrokerurl']

def get_p_grid():
    url = conf['iobrokerurl'] + "/get/fronius.0.site.P_Grid"

    response = requests.get(url)

    return response.json()['val']

def get_p_pv():
    url = conf['iobrokerurl'] + "/get/fronius.0.site.P_PV"

    response = requests.get(url)

    return response.json()['val']

def set_miner_1(value):
    url = conf['iobrokerurl'] + "/set/beckhoff.0.plc.IOBROKER.Miner1?value=" + value

    response = requests.get(url)

def set_miner_2(value):
    url = conf['iobrokerurl'] + "/set/beckhoff.0.plc.IOBROKER.Miner2?value=" + value

    response = requests.get(url)

def set_miner_3(value):
    url = conf['iobrokerurl'] + "/set/beckhoff.0.plc.IOBROKER.Miner3?value=" + value

    response = requests.get(url)

def set_miner_4(value):
    url = conf['iobrokerurl'] + "/set/beckhoff.0.plc.IOBROKER.Miner4?value=" + value

    response = requests.get(url)

def set_miner_5(value):
    url = conf['iobrokerurl'] + "/set/beckhoff.0.plc.IOBROKER.Miner5?value=" + value

    response = requests.get(url)

def set_miner_6(value):
    url = conf['iobrokerurl'] + "/set/beckhoff.0.plc.IOBROKER.Miner6?value=" + value

    response = requests.get(url)
