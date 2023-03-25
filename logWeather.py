import sqlite3
import time
import config


def log():
    try:
        timeStart = time.time()    # time
        timestamp = int(timeStart) # timestamp
        con = sqlite3.connect('/media/pi/ExternalPrograms/wsdata.db')
        cur = con.cursor()
        cur.execute("INSERT INTO weather(timestamp,tin,pin,tout,pout,vout) VALUES (?,?,?,?,?,?)", (timestamp,config.tin,config.pin,config.tout,config.pout,config.vout))
        con.commit()
        con.close()
    except:
        print("log() fail")
