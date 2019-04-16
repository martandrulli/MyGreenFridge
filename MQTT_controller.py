import paho.mqtt.client as PahoMQTT
import json
import time
import cherrypy

class MQTTControl():																# MQTT CLASS

	def __init__(self, deviceID, brokerip, brokerport, fridgeID, controller):

		self.broker = brokerip
		self.port = brokerport
		self.deviceID = deviceID
		self.fridgeID = fridgeID
		self.controller = controller

		# create an instance of paho.mqtt.client
		self._paho_mqtt = PahoMQTT.Client(deviceID, False)

		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect
		self._paho_mqtt.on_message = self.myOnMessage

	def myOnConnect(self, paho_mqtt, userdata, flags, rc):

		print ("Connected to %s with result code: %d" % (self.messageBroker, rc))

	def myOnMessage(self, paho_mqtt, userdata, msg):

		message = json.loads(msg.payload.decode('string-escape').strip('"'))
		
		if msg.topic == '/FRIDGE/' + self.fridgeID + '/temperature':
			temp = ((message["e"])[0])["v"]
			ctrl = self.controller.temp_control(temp)
            self.mypublish('/FRIDGE' + self.fridgeID + '/Tcontrol'+ '/TEMPERATURE', temp)
			if ctrl != None: 
                # siamo nel caso in cui è stata settata una temperatura di riferimento
				pub_mess = json.dumps({"v":ctrl})
				self.mypublish('/FRIDGE/' + self.fridgeID + '/Tcontrol', pub_mess)
			else:
            # siamo nel caso in cui non è stata settata una temperatura di riferimento

				print "no reference value"
				pub_mess = json.dumps({"v":0})
				self.mypublish('/SPYthon/' + self.fridgeID + '/Tcontrol', pub_mess)
				
		elif msg.topic == '/SPYthon/' + self.terrariumID + '/light_status':
			light = ((message['e'])[0])['v']
			self.controller.setCurrentLight(light)

		elif msg.topic == '/SPYthon/' + self.terrariumID + '/humidity':
			hum = ((message["e"])[0])["v"]
			ctrl = self.controller.hum_alert(hum)
			pub_mess = json.dumps({"v":ctrl})
			self.mypublish('/SPYthon/' + self.terrariumID + '/Halert', pub_mess)


	def start(self):

		self._paho_mqtt.connect(self.broker, self.port)
		self._paho_mqtt.loop_start()

	def stop(self):

		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def mysubscribe(self, topic):

		self._paho_mqtt.subscribe(topic, 2)

	def mypublish(self, topic, message):
		print "Publishing on ", topic, "with message ", message
		self._paho_mqtt.publish(topic, message, 2)


class TempRegistration(threading.Thread):											# REGISTRATION TO THE CATALOG

	def __init__(self, deviceID, terrariumID, catalogurl):

		threading.Thread.__init__(self)
		self.deviceID = str(deviceID)
		self.terrariumID = terrariumID
		self.catalogurl = catalogurl

 	def run(self):

		while True:

			url = self.catalogurl + "add_device/tempcontrol"
			
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8",80))
			controllerip = s.getsockname()[0]
			main_topic = "/SPYthon/" + self.terrariumID
			tempGET = ["temperature?temp=<temp>"]
			tempsub = [main_topic + "/temperature", main_topic + "/humidity", main_topic + "/light_status"]
			temppub = [main_topic + "/Tcontrol", main_topic + "/Halert"]

			data = {"ID": self.deviceID, "IP": controllerip, "port": 8080, "GET": tempGET, "POST": [],
					"sub_topics": tempsub, "temp": None, "pub_topics": temppub, "terrarium": self.terrariumID}

			try:
				r = requests.post(url, data = json.dumps(data))
				r.raise_for_status()

			except requests.HTTPError as err:
				print "Error in posting, aborting"
				return

			time.sleep(15*60)

			
if __name__ == '__main__':															# MAIN

	file = open("configControl.txt","r")
	data = json.loads(file.read())

	catalogip = data["catalogip"]
	catalogport = data["catalogport"]
	deviceID = "TempControl"
	terrariumID = data["terrariumID"]
	hum_ref = data["hum_ref"]

	file.close()
	catalogurl = "http://" + catalogip + catalogport

	try:
		r = requests.get(catalogurl + "broker")
		r.raise_for_status()
		broker = r.json()
		brokerip = broker["broker_IP"]
		brokerport = broker["broker_port"]
		print "broker ok " + str(brokerip) + " " + str(brokerport)
	except requests.HTTPError as err:
		print "Error retrieving the broker"
		sys.exit()

	Charmender = TempControl(hum_ref)

	TempActor = MQTTControl(deviceID, brokerip, brokerport, terrariumID, Charmender)

	temp_registration = TempRegistration(deviceID, terrariumID, catalogurl)

	TempActor.start()
	TempActor.mysubscribe("/SPYthon/" + terrariumID + "/#")

	temp_registration.start()


	conf = {'/':{'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True}}

	cherrypy.tree.mount(WebTemp(Charmender), '/', conf)
	cherrypy.config.update({'server.socket_host': '0.0.0.0'})
	cherrypy.config.update({'server.socket_port': 8080})
	cherrypy.engine.start()
	cherrypy.engine.block()
