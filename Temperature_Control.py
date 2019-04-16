# Temperature control class, responsible for activating the heater and send alert when humidity goes out of range
# object to be used in the Temperature web service 

class T_Control:

	def __init__(self, h_ref):#(self , t_ref , h_ref):

		self.t_ref = None #t_ref
		self.h_ref = None #h_ref

# non so se tenere questo metodo, noi abbiamo un TEMPERATURE ALARM web service quindi si potrebbe 
# evitare questa parte e fissare la temperatura di riferimento una tantum oppure
# metterla comunque nel web service e sticazzi (stesso discorso per l'UMIDITA')
# LO STESSO DISCORSO VALE PER L'UMIDITA

	def setReferenceTemperature(self, t_ref):										# SET THE REFERENCE TEMPERATURE in the 
       
		if (t_ref == None):
			self.t_ref = None
		else:
			self.t_ref = float(t_ref)

	def setReferenceHumidity(self, h_ref):										# SET THE REFERENCE HUMIDITY in the 
       
		if (h_ref == None):
			self.h_ref = None
		else:
			self.h_ref = float(h_ref)

	def temp_control(self, temp):													# TEMPERATURE CONTROL

		if (self.t_ref == None): # controllo nell'inserimento del riferimento, vedere commento prima
			return None
        # setto le soglie inf e sup sulla base del riferimento
        delta_t = 2
        t_inf = self.t_ref - delta_t
        t_sup = self.t_ref + delta_t
        if (temp <= t_inf or temp >= t_sup):
            return 1 # ALLARME TEMPERATURA OLTRE SOGLIA 
        else:
            return 0

	def hum_alert(self, hum):														# HUMIDITY ALERT

        if (self.t_ref == None): # controllo nell'inserimento del riferimento, vedere commento prima
			return None
        # setto le soglie inf e sup sulla base del riferimento
        delta_h = 6.0
		h_inf = float(self.h_ref) - delta_h
		h_sup = float(self.h_ref) + delta_h

		if (hum <= h_inf or hum >= h_sup):
			return 1 # ALLARME UMIDITA' OLTRE SOGLIA
		else:
			return 0

import paho.mqtt.client as PahoMQTT
import time


class TempControl():
		def __init__(self, clientID):
			self.clientID = clientID
			# create an instance of paho.mqtt.client
			self._paho_mqtt = PahoMQTT.Client(clientID, False) 

			# register the callback
			self._paho_mqtt.on_connect = self.myOnConnect
			self._paho_mqtt.on_message = self.myOnMessageReceived

			self.topic_received(self) = '/this/is/my/topic'
			self.messageBroker = 'iot.eclipse.org' # va inserito indirizzo del RASPBERRY
			#self.messageBroker = '192.168.1.5'


		def start (self):
			#manage connection to broker
			self._paho_mqtt.connect(self.messageBroker, 1883)
			self._paho_mqtt.loop_start()
			# subscribe for a topic
			self._paho_mqtt.subscribe(self.topic_received(self), 2)

		def stop (self):
			self._paho_mqtt.unsubscribe(self.topic_received(self))
			self._paho_mqtt.loop_stop()
			self._paho_mqtt.disconnect()

		def myOnConnect (self, paho_mqtt, userdata, flags, rc):
			print ("Connected to %s with result code: %d" % (self.messageBroker, rc))

		def myOnMessageReceived (self, paho_mqtt , userdata, msg):
			# A new message is received
			print ("Topic:'" + self.topic_received(msg)+"', QoS: '"+str(msg.qos)+"' Message: '"+str(msg.payload) + "'")

#                def topic_received(self, msg):
#                   return msg.topic 
# modifcabile se vogliamo un topic MUTEVOLE o cangiante
			
			message = json.loads(msg.payload.decode('string-escape').strip('"'))
		
			if msg.topic == '/SPYthon/' + self.terrariumID + '/temperature':
			temp = ((message["e"])[0])["v"]
			ctrl = self.controller.temp_control(temp)
			if ctrl != None:
				pub_mess = json.dumps({"v":ctrl})
				self.mypublish('/SPYthon/' + self.terrariumID + '/Tcontrol', pub_mess)
			else:
				print "Controller disabled"
				pub_mess = json.dumps({"v":0})
				self.mypublish('/SPYthon/' + self.terrariumID + '/Tcontrol', pub_mess)
			control = T_Control(self, t_ref , h_ref)



if __name__ == "__main__":
	test = MySubscriber("MySubscriber 1")
	test.start()

	a = 0
	while (a < 30):
		a += 1
		time.sleep(1)

	test.stop()
