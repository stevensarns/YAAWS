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
