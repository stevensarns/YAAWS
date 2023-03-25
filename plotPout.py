import datetime
import matplotlib.pyplot as plt
import sqlite3

def plot():
        try:
                samples = 2880 #one month at 15 min/sample
                timestamp = []
                pout = []
                rows = []
                plottime = []
                
                conn = sqlite3.connect("/media/pi/ExternalPrograms/wsdata.db")
                cursor = conn.cursor()
                cursor.execute("SELECT timestamp,pout FROM weather ORDER BY timestamp DESC LIMIT "+str(samples))
                rows = cursor.fetchall()
                conn.close()
                
                for row in rows:
                    timestamp.append(row[0])
                    pout.append(row[1])

                plottime = [datetime.datetime.fromtimestamp(timestamp[i]) for i in range(len(pout))]
                fig, ax = plt.subplots()
                ax.set(ylabel='Pa', title='Outside Atmospheric Pressure - Pa')
                ax.grid()
                ax.plot(plottime,pout, linewidth=1)
                plt.pause(.01)
                plt.gcf().autofmt_xdate()
                plt.pause(.01)
                plt.close("pout.png")
                fig.savefig("pout.png")
        except:
                print("plot() in plotPout() fail")
