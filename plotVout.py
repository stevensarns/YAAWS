import datetime
import matplotlib.pyplot as plt
import sqlite3

def plot():
        try:
                samples = 2880 #one month at 15 min/sample
                timestamp = []
                vout = []
                rows = []
                plottime = []
                
                conn = sqlite3.connect("/media/pi/ExternalPrograms/wsdata.db")
                cursor = conn.cursor()
                cursor.execute("SELECT timestamp,vout FROM weather ORDER BY timestamp DESC LIMIT "+str(samples))
                rows = cursor.fetchall()
                conn.close()
                
                for row in rows:
                    timestamp.append(row[0])
                    vout.append(row[1])
                
                plottime = [datetime.datetime.fromtimestamp(timestamp[i]) for i in range(len(vout))]
                fig, ax = plt.subplots()
                ax.set(ylabel='Volts', title='Outside Unit Vcc')
                ax.grid()
                ax.plot(plottime,vout, linewidth=1)
                plt.pause(.01)
                plt.gcf().autofmt_xdate()
                plt.pause(.01)
                plt.close("vout.png")
                fig.savefig("vout.png")
        except:
                print("plot() in plotVout() fail")
