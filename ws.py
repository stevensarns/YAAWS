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
    
