import datetime
import matplotlib.pyplot as plt
import sqlite3

def plot():
        try:
                samples = 2880 #one month at 15 min/sample
                timestamp = []
                pin = []
                rows = []
                plottime = []
                
                conn = sqlite3.connect("/media/pi/ExternalPrograms/wsdata.db")
                cursor = conn.cursor()
                cursor.execute("SELECT timestamp,pin FROM weather ORDER BY timestamp DESC LIMIT "+str(samples))
                rows = cursor.fetchall()
                conn.close()
                
                for row in rows:
                    timestamp.append(row[0])
                    pin.append(row[1])
                
                plottime = [datetime.datetime.fromtimestamp(timestamp[i]) for i in range(len(pin))]
                fig, ax = plt.subplots()
                ax.set(ylabel='Pa', title='Atmospheric Pressure, Inside - Pa')
                ax.grid()
                ax.plot(plottime,pin, linewidth=1)
                plt.pause(.01)
                plt.gcf().autofmt_xdate()
                plt.pause(.01)
                plt.close("pin.png")
                fig.savefig("pin.png")
        except:
                print("plot() in plotPin() fail")
