import helper.hiveosAPI
import helper.mysql
import helper.telegramsend
import helper.config
import time
import helper.functions
import logging

logger = helper.functions.initlogger("hiveos.log")

conf = helper.config.initconfig()


farm_id = conf['hiveosfarmid']
worker_id_1 = conf['hiveosworkerid_1']
worker_id_2 = conf['hiveosworkerid_2']


print("Start HiveOS")
logging.info("Start hiveos.py")

def loop():
    started_1 = False
    started_2 = False

    while True:
        # Request Solar Power
        result = helper.mysql.requestsolarpower()

        x = 0.0
        for i in result:
            if None in i:
                logging.error("None in Result")
                break
            x += float(i[0])

        avg = x / len(result)

        print(avg)

        # Start 1

        if avg < float(conf['hiveospower_1']) and not started_1:

            # Payload für RVN
            payload = {
                'fs_id': '16959780',
                }
            if helper.hiveosAPI.changefs(payload, farm_id, worker_id_1):
                helper.telegramsend.send("Start Mining 1")
                print("Start Mining 1")
                started_1 = True
                time.sleep(600)
                continue

        # Start 2

        if avg < float(conf['hiveospower_2']) and started_1 and not started_2:

            # Payload für RVN
            payload = {
                'fs_id': '16734657',
                }
            if helper.hiveosAPI.changefs(payload, farm_id, worker_id_2):
                helper.telegramsend.send("Start Mining 2")
                print("Start Mining 2")
                started_2 = True
                time.sleep(600)
                continue

        # Stop 2
        if avg > float(conf['hiveosminpower']) and started_2:
            
            # Payload 0
            payload = {
                'fs_id': None,
                }
            if helper.hiveosAPI.changefs(payload, farm_id, worker_id_2):
                helper.telegramsend.send("Stop Mining 2")
                print("Stop Mining 2")
                started_2 = False
                time.sleep(600)
                continue
        
        # Stop 1
        if avg > float(conf['hiveosminpower']) and started_1 and not started_2:
            
            # Payload 0
            payload = {
                'fs_id': None,
                }
            if helper.hiveosAPI.changefs(payload, farm_id, worker_id_1):
                helper.telegramsend.send("Stop Mining 1")
                print("Stop Mining 1")
                started_1 = False
                time.sleep(600)
                continue
            
        time.sleep(600)

def benchmarking():
    # Payload für ETC
    payload = {
        'fs_id': '16733974',
    }

    # Payload für RVN
    payload = {
        'fs_id': '16734657',
    }

    helper.hiveosAPI.changefs(payload)

if __name__ == "__main__":
    loop()