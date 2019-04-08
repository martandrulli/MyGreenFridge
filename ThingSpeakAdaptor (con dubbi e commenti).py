### this scripts has to receive from MQTT data sensor in SenML format
### and post via HTTP request in my ThingSpeak Channels

#DUBBI DA ILLUSTRARE A LETIZIA O COMUNQUE DA RISOLVERE:

# - Capire bene come funzioni Thingspeak, il file di configurazione, gli URL, etc.etc.
#   in merito a ciò nella mia testa è tutto molto opaco...
# - Capire come fare la stima del FoodWaste. In che modo riceveremo questi dati
#   dal telegram bot? In che formato?
# - Controllare che i nomi dei topic siano giusti wrt il Catalog.

#import thingspeak
import threading
import json
import paho.mqtt.client as PahoMQTT
import datetime
import time
import requests
import sys
import urllib


#this class manages the messages arrived from MQTT, it's a subscriber
class ThingSpeakDataManager :
    def __init__(self, deviceID, broker, port, pCalc):
        self.deviceID = deviceID
        self.broker = broker
        self.port = port
        self.topic = ""
        self._isSubscriber = False
        self._paho_mqtt = PahoMQTT.Client(deviceID, False)
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived
        self.pCalc = pCalc

    def mySubscribe (self, topic):
		# if needed, you can do some computation or error-check before subscribing
        print ("subscribing to %s" % (topic))
		# subscribe for a topic
        self._isSubscriber = True
        self._paho_mqtt.subscribe(topic, 2)
		# just to remember that it works also as a subscribe
        self._topic = topic

    def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived (self, paho_mqtt , userdata, msg):
        # print ("!")

        # if (msg.topic != '/MyGreenFridge/'+ self.deviceID +"/Tcontrol"):
        #     msg_dict = json.loads(msg.payload.decode('string-escape').strip('"'))
        #     value = ((msg_dict["e"])[0])["v"]


                #controllare gli URL, potrebbero essere giusti, ma anche no...
            if (msg.topic == '/MyGreenFridge/'+ self.deviceID +"/temperature") :
                data = urllib.urlopen("https://api.thingspeak.com/update?api_key=AFD10RO5MXMAS7XU&field1="+str(value))
                print ("value updated")
                print value
            elif (msg.topic =='/MyGreenFridge/'+ self.deviceID +"/humidity") :
                data = urllib.urlopen("https://api.thingspeak.com/update?api_key=J4GGNYGH12CM8ZGY&field1="+str(value))
                print ("value updated")
                print value

                #controllare che i nomi di questi topic siano coerenti con quelli
                #scelti nel Catalog
            elif (msg.topic == 'MyGreenFridge/'+self.deviceID+"/cameraIN") :
                data = urllib.urlopen("https://api.thingspeak.com/update?api_key=J4GGNYGH12CM8ZGY&field1="+str(value))
                print ("value updated")
                print value

            elif (msg.topic == 'MyGreenFridge/'+self.deviceID+"/cameraOUT") :
                data = urllib.urlopen("https://api.thingspeak.com/update?api_key=J4GGNYGH12CM8ZGY&field1="+str(value))
                print ("value updated")
                print value

    def start(self):
		#manage connection to broker
		self._paho_mqtt.connect(self.broker , self.port)
		self._paho_mqtt.loop_start()


    def stop (self):
        if self._isSubscriber :
            self._paho_mqtt.unsubscribe(self.topic)
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

# Do we have to do the waste estimate here? zan zan zan
# This is kind of difficult since we still have to wait for the
# Telegram interaction with the user.

class FoodWasteEstimate: #ZAN ZAN ZANNNNNN

# class PowerConsumptioneEstimate:
#     def __init__(self):
#         self.pLight = 0.025 #in kw
#         self.pHeat = 0.025
#         self.eRPi = 0.004 *120./3600
#
#         self.lastTime = time.time()
#         self.deltaTlight = 15./3600 #h
#         self.energyLight = 0
#         self.energyHeat = 0
#         self.energyRPi = 0
#
#     def energyLightCalc(self, statusLight):
#         energyL = self.pLight * statusLight * self.deltaTlight
#         self.energyLight += energyL
#
#     def energyHeatCalc (self, tControlStatus):
#         deltaTins = time.time() - self.lastTime
#         deltaT = deltaTins*0.000278 #(1/3600)
#         self.lastTime = time.time()
#         energyH = self.pHeat * tControlStatus * deltaT
#         self.energyHeat += energyH
#
#     def sumContributes(self):
#         return self.energyLight+self.energyHeat+ self.eRPi

# class EnergyThread(threading.Thread):
# 	def __init__ (self, pEstimate):
# 		threading.Thread.__init__(self)
# 		self.pEstimate = pEstimate
# 		self.now = datetime.datetime.now().month
# 	def run (self):
# 		while True:
# 			actualMonth = datetime.datetime.now().month
# 			if (self.now != actualMonth):
# 				self.pEstimate.energyLight = 0
# 				self.pEstimate.energyHeat = 0
# 				self.pEstimate.energyRPi = 0
# 				payload = {"api_key" : "9N2P4LUVSZOE63MN"}
# 				r = requests.delete("https://api.thingspeak.com/channels/702275/feeds.json", data = payload)
# 				print "data cleared"
# 			value = self.pEstimate.sumContributes()
# 			data = urllib.urlopen("https://api.thingspeak.com/update?api_key=KUSHZ7LZ6SJ96C4X&field1="+str(value))
# 			print "data published: " + str(value)
# 			time.sleep(60)

if __name__ == "__main__":

    conf_file = open("configControl.txt", 'r')
    conf_file_dict = json.loads(conf_file.read())
    conf_file.close()
    deviceID = conf_file_dict['fridgeID'] #prende l'ID del device
    catalogIP = conf_file_dict['catalogip'] #prende l'IP del catalog

    try:
		r2 = requests.get('http://'+ catalogIP + ':8080/broker')
		r2.raise_for_status()

		brokerip = r2.json()['broker_IP']
		print brokerip
		brokerport = r2.json()['broker_port'] #trova il broker
    except requests.HTTPError as err:
            print 'Error in posting, aborting'
            sys.exit()
    # pConsEstimate = PowerConsumptioneEstimate()
    tdsm = ThingSpeakDataManager(deviceID, brokerip, brokerport, pConsEstimate)
    # enThread = EnergyThread(pConsEstimate)
    enThread.start()
    tdsm.start()
    time.sleep(2)
    tdsm.mySubscribe('/MyGreenFridge/#')

    while True:
        time.sleep(1)
