import time
import signal
import smbus
import config

bus = smbus.SMBus(1)
time.sleep(1)

def unsigned2signed(x):
    if x>0x7FFF:
        x = x - 0x10000
    return x

config.pin = 0.0
config.tin = 0.0
Tcal = -7.0
Pcal = 0.0
def get():
        try:
                ADDR_H = 0x38
                config = [0x08, 0x00]
                MeasureCmd = [0x33, 0x00]
                
                ADDR_B     = 0x76
                TEMP_XSB   = 0xFC
                TEMP_LSB   = 0xFB
                TEMP_MSB   = 0xFA
                PRES_XSB   = 0xF9
                PRES_LSB   = 0xF8
                PRES_MSB   = 0xF7
                CONFIG     = 0xF5
                CTRL       = 0xF4
                TCOMP      = 0x88
                PCOMP      = 0x8E
                
                DIG_T1_LSB = 0x88
                DIG_T1_MSB = 0x89 
                DIG_T2_LSB = 0x8A
                DIG_T2_MSB = 0x8B
                DIG_T3_LSB = 0x8C
                DIG_T3_MSB = 0x8D
                
                DIG_P1_LSB = 0x8E
                DIG_P1_MSB = 0x8F 
                DIG_P2_LSB = 0x90
                DIG_P2_MSB = 0x91
                DIG_P3_LSB = 0x92
                DIG_P3_MSB = 0x93
                DIG_P4_LSB = 0x94
                DIG_P4_MSB = 0x95 
                DIG_P5_LSB = 0x96
                DIG_P5_MSB = 0x97
                DIG_P6_LSB = 0x98
                DIG_P6_MSB = 0x99
                DIG_P7_LSB = 0x9A
                DIG_P7_MSB = 0x9B 
                DIG_P8_LSB = 0x9C
                DIG_P8_MSB = 0x9D
                DIG_P9_LSB = 0x9E
                DIG_P9_MSB = 0x9F
                
                
                VAL_CONFIG = 0b01001000 # t_sb=010, filter=010, spi_en=0
                VAL_CTRL   = 0b00101011 # T=001, P=010, MODE=11
                
                dig_T1 = (bus.read_byte_data(ADDR_B,DIG_T1_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_T1_LSB)
                dig_T2 = (bus.read_byte_data(ADDR_B,DIG_T2_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_T2_LSB)
                dig_T2 = unsigned2signed(dig_T2)
                dig_T3 = (bus.read_byte_data(ADDR_B,DIG_T3_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_T3_LSB)
                dig_T3 = unsigned2signed(dig_T3)
                
                dig_P1 = (bus.read_byte_data(ADDR_B,DIG_P1_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P1_LSB)
                dig_P2 = (bus.read_byte_data(ADDR_B,DIG_P2_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P2_LSB)
                dig_P2 = unsigned2signed(dig_P2)
                dig_P3 = (bus.read_byte_data(ADDR_B,DIG_P3_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P3_LSB)
                dig_P3 = unsigned2signed(dig_P3)
                dig_P4 = (bus.read_byte_data(ADDR_B,DIG_P4_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P4_LSB)
                dig_P4 = unsigned2signed(dig_P4)
                dig_P5 = (bus.read_byte_data(ADDR_B,DIG_P5_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P5_LSB)
                dig_P5 = unsigned2signed(dig_P5)
                dig_P6 = (bus.read_byte_data(ADDR_B,DIG_P6_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P6_LSB)
                dig_P6 = unsigned2signed(dig_P6)
                dig_P7 = (bus.read_byte_data(ADDR_B,DIG_P7_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P7_LSB)
                dig_P7 = unsigned2signed(dig_P7)
                dig_P8 = (bus.read_byte_data(ADDR_B,DIG_P8_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P8_LSB)
                dig_P8 = unsigned2signed(dig_P8)
                dig_P9 = (bus.read_byte_data(ADDR_B,DIG_P9_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P9_LSB)
                dig_P9 = unsigned2signed(dig_P9)
                
                bus.write_byte_data(ADDR_B,CONFIG,VAL_CONFIG) # initialize BMP280
                bus.write_byte_data(ADDR_B,CTRL,  VAL_CTRL)
                
                tempMSB = bus.read_byte_data(ADDR_B,TEMP_MSB)
                tempLSB = bus.read_byte_data(ADDR_B,TEMP_LSB)
                tempXSB = bus.read_byte_data(ADDR_B,TEMP_XSB)
                adc_T = ((tempMSB<<16) | (tempLSB<<8) | tempXSB)>>4
                
                var1 = (((adc_T>>3) - (dig_T1<<1)) * dig_T2)>>11
                var2 = (((((adc_T>>4) - dig_T1)) * ((adc_T>>4) - ((dig_T1)))>>12) * dig_T3)>>14
                t_fine = var1 + var2
                T = (((t_fine*5)+128)>>8)/100.
                T = (9.*T/5.) + 32.
                tin = T + Tcal
                
                presMSB = bus.read_byte_data(ADDR_B,PRES_MSB)
                presLSB = bus.read_byte_data(ADDR_B,PRES_LSB)
                presXSB = bus.read_byte_data(ADDR_B,PRES_XSB) # i2c takes 4 mS
                adc_P = ((presMSB<<16) | (presLSB<<8) | presXSB)>>4
                
                var1 = t_fine/2. - 64000
                var2 = var1 * var1 * dig_P6/32768.
                var2 = var2 + var1 * dig_P5 *2
                var2 = var2/4 + dig_P4*65536.
                var1 = (dig_P3 * var1 * var1 / 524288. + var1 * dig_P2) / 524288.
                var1 = (1. + var1/32768.) * dig_P1
                p = 1048576. - adc_P
                p = (p - (var2/4096.)) * 6250. / var1
                var1 = dig_P9 * p / 2147483648. * p
                var2 = p * dig_P8 / 32768.
                p = (p + (var1 + var2 + dig_P7)/ 16.)/100.
                pin = p
                return tin, pin
        except:
                print("get() in bmp() fail")

ctrl = 0
vout = 0
tout = 0.0
pout = 0.0
tin  = 0.0
pin  = 0.0
xxx = 0.0

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

import paho.mqtt.client as mqtt
import config

dataComplete = 0
mqtt_topic1 = "ss/ctrl"
mqtt_topic2 = "ss/vout"
mqtt_topic3 = "ss/tout"
mqtt_topic4 = "ss/pout"
#mqtt_broker_ip = "broker.hivemq.com" # useful for debug
mqtt_broker_ip = "192.168.0.40"    # mosquitto running on this pi
mqttClient = mqtt.Client()
def on_connect(mqttClient, userdata, flags, rc):
    try:
        mqttClient.subscribe("ss/ctrl") # subscribe to the topics
        mqttClient.subscribe("ss/vout")
        mqttClient.subscribe("ss/tout")
        mqttClient.subscribe("ss/pout")
    except:
        print("on_connect() in mqtt() fail")
    
def on_message(mqttClient, userdata, msg):
    try:
        global dataComplete             # global to save over calls
        if msg.topic=="ss/ctrl":
            config.ctrl = int(msg.payload)
            dataComplete = dataComplete | 1
        elif msg.topic=="ss/tout":
            config.tout = float(msg.payload)
            dataComplete = dataComplete | 2
        elif msg.topic=="ss/pout":
            config.pout = float(msg.payload)  
            dataComplete = dataComplete | 4
        elif msg.topic=="ss/vout":
            config.vout = float(msg.payload)
            dataComplete = dataComplete | 8
        if dataComplete==15:
            dataComplete = 0
            mqttClient.loop_stop
            mqttClient.disconnect()
    except:
        print("on_message() in mwtt() fail")

mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.connect(mqtt_broker_ip, 1883) # connect to the broker
mqttClient.loop_forever()                #let the client object run itself

def get():
    try:
        mqttClient.on_connect
        mqttClient.on_message
        mqttClient.connect(mqtt_broker_ip, 1883)
        mqttClient.loop_forever() 
        return
        #    return config.ctrl,vout,tout,pout
    except:
        print("get() in mqtt() fail")


import matplotlib.pyplot as plt

def plot():
        try:
                plt.rcParams['figure.figsize'] = [8,2]
                plt.close("all")
        except:
                print("plot.close() fail")
        

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


import ftplib

def send():
        try:
                ftp = ftplib.FTP()
                host = "stevensarns.com"
                port = 21
                ftp.connect(host, port)
                ftp.login("stevensa", "Fe615243!@")
                ftp.cwd('/public_html/wimages')
                filename = 'vout.png'
                ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                filename = 'tin.png'
                ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                filename = 'pout.png'
                ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                filename = 'tout.png'
                ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                # filename = 'pic.jpg'
                # ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                ftp.quit()
        except:
                print("FTP fail")


from picamera import PiCamera, Color
import time
import datetime as dt

def snap():
        try:
                camera = PiCamera()
                #camera.resolution = (1280, 720)
                camera.resolution = (640, 480)
                camera.vflip = True
                camera.contrast = 10
                #camera.image_effect = "watercolor"
                #camera.image_effect = "sketch"
                #camera.image_effect = "hatch"
                camera.annotate_background = Color('black')
                camera.annotate_foreground = Color('white')
                camera.annotate_text_size = 15 # (values 6 to 160, default is 32)
                camera.annotate_text = dt.datetime.now().strftime('%A %I:%M %p')
                time.sleep(2)
                camera.capture("/home/pi/Scripts/pic.jpg")
                time.sleep(2)
                camera.close()
        except:
                print("snap() in snapPic() fail")


import time
import datetime as dt


fswebcam -save, test.jpg -d, "qucik cam pro 9000"

#camera.resolution = (640, 480)
# camera.annotate_background = Color('black')
# camera.annotate_foreground = Color('white')
# camera.annotate_text_size = 15 # (values 6 to 160, default is 32)
# camera.annotate_text = dt.datetime.now().strftime('%A %I:%M %p')
# time.sleep(2)
# camera.capture("/home/steven/Scripts/pic.jpg")
# time.sleep(2)
# camera.close()
                


<style>
table, th,td {border: 1px solid black;}
</style>

<table style="width: 640, height:400 border: 1px blac;">
</table>

<table width="510">
<tr>
<td> 
<div id="ww_4f18b95296739" v='1.3' loc='id' a='{"t":"horizontal","lang":"en","sl_lpl":1,"ids":["wl1809"],"font":"Arial","sl_ics":"one","sl_sot":"fahrenheit","cl_bkg":"image","cl_font":"#FFFFFF","cl_cloud":"#FFFFFF","cl_persp":"#81D4FA","cl_sun":"#FFC107","cl_moon":"#FFC107","cl_thund":"#FF5722"}'>Weather Data Source: <a href="https://wetterlabs.de/wetter_tucson/30_tage/" id="ww_4f18b95296739_u" target="_blank">Tucson wetter 30 tage</a></div><script async src="https://app1.weatherwidget.org/js/?id=ww_4f18b95296739"></script>
</td>
</tr>
</table>


<table width="500">
<tr>
<td>
<img src="https://www.theweather.com/wimages/foto01d7ec83d07a72c2af14b8e7f3d81077.png" width="500" height="200" />
</td>
</tr>
</table>



<table width="500">
<tr>
<td> 
<img src="https://www.wpc.ncep.noaa.gov/basicwx/92fndfd.gif" width="500" height="350" />
</td>
</tr>
</table>


<table width="495">
<tr>
<td> <img src="tout.png" width="246" height="120" /> </td>
<td> <img src="tin.png"  width="246" height="120" /> </td>
</tr>

<tr>
<td> <img src="pout.png" width="246" height="120" /> </td>
<td> <img src="vout.png" width="246" height="120" /> </td>
</tr>
</table>


<body>

<table bgcolor="#4287f5">
   

<tr>   


<td>  
<img src="pic.png" width="200" height="200" /> 
</td>
<td> 
<img src="https://www.theweather.com/wimages/fotodffde5c8492b030a8268898a673a2607.png" width="200" height="200" />
</td>
</tr>

<tr>
<td>
<img src="https://www.theweather.com/wimages/foto01d7ec83d07a72c2af14b8e7f3d81077.png" width="500" height="200" />
</td>
</tr>



<tr>
<td> 
<img src="https://www.wpc.ncep.noaa.gov/basicwx/92fndfd.gif" width="200" height="150" />
</td>
</tr>
   
<tr>
<td> <img src="tout.png" width="320" height="120" /> </td>
<td> <img src="tin.png"  width="320" height="120" /> </td>
</tr>

<tr>
<td> <img src="pout.png" width="320" height="120" /> </td>
<td> <img src="vout.png" width="320" height="120" /> </td>
</tr>

</table>
</body>
</html>


import pyautogui

def update():
	try:
		pyautogui.click(x=150, y=100)
		pyautogui.hotkey('ctrl', 'f5')
		pyautogui.moveTo(0,200)
	except:
		print("!!!!!!!!!!!!!!!!!!!!!!updateBrowser fail")

<img src="https://www.theweather.com/wimages/foto01d7ec83d07a72c2af14b8e7f3d81077.png">

<div id="cont_d52815915dbf86a10e9153b2c00cab99"><script type="text/javascript" async src="https://www.theweather.com/wid_loader/d52815915dbf86a10e9153b2c00cab99"></script></div>

<img src="https://www.theweather.com/wimages/fotodffde5c8492b030a8268898a673a2607.png">


<div id="ww_4f18b95296739" v='1.3' loc='id' a='{"t":"horizontal","lang":"en","sl_lpl":1,"ids":["wl1809"],"font":"Arial","sl_ics":"one","sl_sot":"fahrenheit","cl_bkg":"image","cl_font":"#FFFFFF","cl_cloud":"#FFFFFF","cl_persp":"#81D4FA","cl_sun":"#FFC107","cl_moon":"#FFC107","cl_thund":"#FF5722"}'>Weather Data Source: <a href="https://wetterlabs.de/wetter_tucson/30_tage/" id="ww_4f18b95296739_u" target="_blank">Tucson wetter 30 tage</a></div><script async src="https://app1.weatherwidget.org/js/?id=ww_4f18b95296739"></script>

&nbsp;





import sys
import time
import config
import bmp
import mqtt
import logWeather
import plotVout
import plotTout
import plotTin
import plotPin
import plotPout
import plotClose
import sendFtp
import snapPic
import updateBrowser

lastHour = 0
samples = 0
config.tin, config.pin = bmp.get()
def ET() :
    
    elapsedTime = time.time() - timeStart
    elapsedTime = "{:.3f}".format(elapsedTime)
    elapsedTime = str(elapsedTime)
    return elapsedTime

while True:
    samples += 1                            # count number of times this runs
    timeStart = time.time()                 # time now
    hour = int(int(timeStart)/3600)
    print(time.asctime(time.localtime(timeStart)),     "     Elapsed Time")
    print("This sample count: ",samples,               "        ",ET())
    config.tin, config.pin = bmp.get()      # get indoor data
    print(f'Inside Temperature: {"%.2f" % config.tin}', "     ",  ET())
    print(f'Inside Pressure:    {"%.2f" % config.pin}', "    ",   ET())
    mqtt.get()                              # get outdoor data
    print(f'Outside Temperature:{"%.2f" % config.tout}', "     ", ET())
    print(f'Outside Pressure:   {"%.2f" % config.pout}', "    ",  ET())
    print(f'Outside Vcc:        {"%.2f" % config.vout}', "      ",ET())
    print("Remote msgs sent   ",          config.ctrl,   "      ",ET())
    logWeather.log()                        # log data
    print("Log Weather                    ", ET())
    
    plotTout.plot()                         # plot outdoor temperature
    plotPout.plot()                         # plot outdoor pressure
    print("Weather Graphics               ", ET())
    if hour != lastHour :                   # if hour has rolled...
        lastHour = hour                     # save this hour
        plotPin.plot()                      # plot indoor pressure
        plotTin.plot()                      # plot indoor temperature
        plotVout.plot()                     # plot outdoor Vcc
        sendFtp.send()                      # ftp images to websiteVcc
        print("Send FTP                       ", ET())
    print("Elapsed Time                   ", ET())
    plotClose.plot()                        # close all graphs showing
    updateBrowser.update()
    print("--------------------------")
    time.sleep(60)                          # wait for next time to log data
    
