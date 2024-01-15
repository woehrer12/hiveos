import helper.hiveosAPI
# import helper.mysql
import helper.telegramsend
import helper.config
import helper.iobroker
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

    kühlung = False

    started_1 = False
    started_2 = False

    booted_1 = False
    booted_2 = False

    shutdown_1 = False
    shutdown_2 = False

    print()

    while True:

        # try:

            grid = helper.iobroker.get_p_grid()
            pv = helper.iobroker.get_p_pv()

            worker_2_online = helper.hiveosAPI.worker(farm_id, worker_id_1)['stats']['online']

            # Wasserkühlung einschalten
            if pv > 500 and kühlung == False:
                kühlung = True
                helper.iobroker.set_miner_1("true")
                helper.telegramsend.send("Kühlung eingeschalten")
                time.sleep(60)
                
            # Miner 1 Hochfahren
            if pv > 600 and grid < -100 and kühlung and not booted_1:
                booted_1 = True
                helper.iobroker.set_miner_2("true")
                helper.telegramsend.send("Miner 1 booted")
                time.sleep(90)

            worker_1_online = helper.hiveosAPI.worker(farm_id, worker_id_1)['stats']['online']

            # Miner 1 Starten
            if pv > 800 and grid < -400 and kühlung and booted_1 and not started_1 and worker_1_online:
                print(helper.hiveosAPI.worker(farm_id, worker_id_1))

                # Payload für RVN
                payload = {
                    'fs_id': '16959780',
                    }
                if helper.hiveosAPI.changefs(payload, farm_id, worker_id_1):
                    started_1 = True
                    helper.telegramsend.send("Start Mining 1")
                    print("Start Mining 1")
                    time.sleep(60)

            # Miner 1 Stoppen
            if (grid > 100 or pv < 500) and started_1:

                # Payload 0
                payload = {
                    'fs_id': None,
                    }
                if helper.hiveosAPI.changefs(payload, farm_id, worker_id_1):
                    started_1 = False
                    helper.telegramsend.send("Stop Mining 1")
                    print("Stop Mining 1")
                    time.sleep(60)

            # Miner 1 Shutdown
            if (grid > 200 or pv < 300) and not started_1 and booted_1:
                payload = {
                'command': "shutdown",
                "data": {}
                }
                if helper.hiveosAPI.command(payload, farm_id, worker_id_1):
                    helper.telegramsend.send("Shutdown Mining 1")
                    print("Shutdown Mining 1")
                    time.sleep(120)
                    shutdown_1 = True

            # Miner 1 Ausschalten
            if (pv < 100 or pv > 800) and not started_1 and shutdown_1 and not worker_1_online:
                time.sleep(60)
                shutdown_1 = False
                helper.iobroker.set_miner_2("false")
                helper.telegramsend.send("Miner 1 Ausgeschaltet")
                print("Miner 1 Ausgeschaltet")
                booted_1 = False
                time.sleep(60)


           # Miner 2 Hochfahren
            if pv > 1200 and grid < -100 and kühlung and not booted_2 and started_1:
                booted_2 = True
                helper.iobroker.set_miner_3("true")
                helper.telegramsend.send("Miner 2 booted")
                time.sleep(90)

            worker_2_online = helper.hiveosAPI.worker(farm_id, worker_id_2)['stats']['online']

            # Miner 2 Starten
            if pv > 1500 and grid < -400 and kühlung and booted_2 and not started_2 and worker_2_online:
                print(helper.hiveosAPI.worker(farm_id, worker_id_2))

                # Payload für RVN
                payload = {
                    'fs_id': '16734657',
                    }
                if helper.hiveosAPI.changefs(payload, farm_id, worker_id_2):
                    started_1 = True
                    helper.telegramsend.send("Start Mining 2")
                    print("Start Mining 2")
                    time.sleep(60)

            # Miner 2 Stoppen
            if (grid > 100 or pv < 1200) and started_2:

                # Payload 0
                payload = {
                    'fs_id': None,
                    }
                if helper.hiveosAPI.changefs(payload, farm_id, worker_id_2):
                    started_2 = False
                    helper.telegramsend.send("Stop Mining 2")
                    print("Stop Mining 2")
                    time.sleep(60)

            # Miner 2 Shutdown
            if (grid > 200 or pv < 1000) and not started_2 and booted_2:
                payload = {
                'command': "shutdown",
                "data": {}
                }
                if helper.hiveosAPI.command(payload, farm_id, worker_id_2):
                    helper.telegramsend.send("Shutdown Mining 2")
                    print("Shutdown Mining 2")
                    time.sleep(120)
                    shutdown_2 = True

            # Miner 2 Ausschalten
            if (pv < 500 or pv > 1500) and not started_2 and shutdown_2 and not worker_2_online:
                time.sleep(60)
                shutdown_1 = False
                helper.iobroker.set_miner_3("false")
                helper.telegramsend.send("Miner 2 Ausgeschaltet")
                print("Miner 2 Ausgeschaltet")
                booted_2 = False
                time.sleep(60)



            time.sleep(600)
        # except Exception as e:
        #     logging.error("Error while loop : " + str(e))
        #     print("Error while loop : " + str(e))


if __name__ == "__main__":
    loop()

