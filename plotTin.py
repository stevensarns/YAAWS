import datetime
import matplotlib.pyplot as plt
import sqlite3

def plot():
        try:
                samples = 2880 #one month at 15 min/sample
                timestamp = []
                tin = []
                rows = []
                plottime = []
                
                conn = sqlite3.connect("/media/pi/ExternalPrograms/wsdata.db")
                cursor = conn.cursor()
                cursor.execute("SELECT timestamp,tin FROM weather ORDER BY timestamp DESC LIMIT "+str(samples))
                rows = cursor.fetchall()
                conn.close()
                
                for row in rows:
                    timestamp.append(row[0])
                    tin.append(row[1])
                
                plottime = [datetime.datetime.fromtimestamp(timestamp[i]) for i in range(len(tin))]
                fig, ax = plt.subplots()
                ax.set(ylabel='Temperature', title='Inside Temperature - degrees F')
                ax.grid()
                ax.plot(plottime,tin, linewidth=1)
                plt.pause(.01)
                plt.gcf().autofmt_xdate()
                plt.pause(.01)
                plt.close("tin.png")
                fig.savefig("tin.png")
        except:
                print("plot() in plotTin() fail")

