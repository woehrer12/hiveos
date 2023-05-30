from datetime import datetime
import logging
import time

import helper.config
import mysql.connector

conf = helper.config.initconfig()

# Request
def requestsolarpower():
    try:
        mydb = mysql.connector.connect(
        host = conf['MYSQL_HOST'],
        user = conf['MYSQL_USER'],
        password = conf['MYSQL_PASS'],
        database = 'iobrokerwinzerhausen'
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT val FROM ts_number WHERE id = 10 ORDER BY ts DESC LIMIT 10")
        myresult = mycursor.fetchall()
        mycursor.close()

        return myresult
    except Exception as e:
        logging.error("Fehler beim lesen von solarpower Daten aus SQL: " + str(e))
        print("Fehler beim lesen von solarpower Daten aus SQL: " + str(e))