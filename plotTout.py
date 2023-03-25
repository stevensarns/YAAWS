import datetime
import matplotlib.pyplot as plt
import sqlite3

def plot():
        try:
                samples = 2880 #one month at 15 min/sample
                timestamp = []
                tout = []
                rows = []      
                plottime = []
                
                conn = sqlite3.connect("/media/pi/ExternalPrograms/wsdata.db")
                cursor = conn.cursor()
                cursor.execute("SELECT timestamp,tout FROM weather ORDER BY timestamp DESC LIMIT "+str(samples))
                rows = cursor.fetchall()
                conn.close()
                
                for row in rows:
                    timestamp.append(row[0])
                    tout.append(row[1])
                
                plottime = [datetime.datetime.fromtimestamp(timestamp[i]) for i in range(len(tout))]
                fig, ax = plt.subplots()
                ax.set(ylabel='Temperature', title='Outside Temperature - degrees F')
                ax.grid()
                ax.plot(plottime,tout, linewidth=1)
                plt.pause(.01)
                plt.gcf().autofmt_xdate()
                plt.pause(.01)
                plt.close("tout.png")
                fig.savefig("tout.png")
        except:
                print("plot() in plotTout() fail")


        
