import json
import pybase64
import time
import Adafruit_DHT
import cherrypy
import socket
from picamera import PiCamera
from time import sleep
from PIL import Image


class SensorsControl(object):

    def __init__(self,ip):
        # IP
        self.ip = ip

        # DHT22 (T & H sensor)
        self.pin_dht=23
        self.dht_sensor=Adafruit_DHT.DHT22


    def temperature (self):
        # Retrieves Temperature value from sensor DHT22 and gives back a SenMl as output
        humidity, temperature = Adafruit_DHT.read_retry(self.dht_sensor, self.pin_dht)

        if temperature is not None:
            temp_senml = {"bn": "http://" + self.ip + "/Tsensor/", "e": [{ "n": "temperature", "u": "Celsius","t": time.time(), "v": temperature}]}
        else:
            temp_senml = {"bn": "http://" + self.ip + "/Tsensor/", "e": [{ "n": "temperature", "u": "Celsius","t": time.time(), "v": "Error in reading"}]}

        #print T_senml
        print "Temperature is: " + str(((temp_senml['e'])[0])['v'] ) + " Celsius"
        return temp_senml

    def humidity (self):
        # Retrieves Humidity value from sensor DHT22 and gives back a SenMl as output
        humidity, temperature = Adafruit_DHT.read_retry(self.dht_sensor, self.pin_dht)

        if humidity is not None:
            hum_senml= {"bn": "http://" + self.ip + "/Hsensor/", "e": [{ "n": "humidity", "u": "%","t": time.time(), "v": humidity}]}
        else:
            hum_senml= {"bn": "http://" + self.ip + "/Hsensor/", "e": [{ "n": "humidity", "u": "%","t": time.time(), "v": "Error in reading"}]}

        #print H_senml
        print "Humidity is: " + str(((hum_senml['e'])[0])['v'] )+ " %"
        return hum_senml
    
    def camera1 (self):
        # Retrieves an image from the camera and returns it as output

        image_base64 = None
        
        camera = PiCamera()
        camera.capture('/home/pi/picamera_image.jpg') # save image in current folder
        # WHAT ABOUT GIVING THE DIRECTORY AS AN INPUT PARAMETER OF THE CLASS?
        
        #img = Image.open('/home/pi/picamera_image.jpg')
        with open("picamera_image.jpg", "rb") as image_file: 
            image_base64 = pybase64.b64encode(image_file.read())
        
        if image_base64 is not None:
            cam_senml= {"bn": "http://" + self.ip + "/Camera1/", "e": [{ "n": "camera1", "u": "%","t": time.time(), "v": image_base64}]}
        else:
            cam_senml= {"bn": "http://" + self.ip + "/Camera1/", "e": [{ "n": "camera1", "u": "%","t": time.time(), "v": "Error in reading"}]}

        #print cam_senml
        print "Image from camera is: " + str(((cam_senml['e'])[0])['v'] )+ " %"
        return cam_senml


class SensorsWebService(object):

    exposed = True

    def __init__(self, deviceconnector):
        self.deviceconnector = deviceconnector

    def GET (self, *uri):

        if (uri[0] == 'temperature'):
            senml = self.deviceconnector.temperature()
            if senml is None:
                raise cherrypy.HTTPError(500, "Invalid Senml")
            value = ((senml['e'])[0])['v']

            if isinstance(value, basestring):
                raise cherrypy.HTTPError(500, "Error in reading data from sensor")
            else:
                out = json.dumps(senml)


        elif (uri [0] == 'humidity'):
            senml = self.deviceconnector.humidity()
            if senml is None:
                raise cherrypy.HTTPError(500, "Invalid Senml")
            value = ((senml['e'])[0])['v']

            if isinstance(value, basestring):
                raise cherrypy.HTTPError(500, "Error in reading data from sensor")
            else:
                out = json.dumps(senml)

        elif (uri [0] == 'camera1'):            
            senml = self.deviceconnector.camera1()
            
            if senml is None:
                raise cherrypy.HTTPError(500, "Invalid Senml")
            value = ((senml['e'])[0])['v']

            out = json.dumps(senml)


            # if isinstance(value, basestring):
            #     raise cherrypy.HTTPError(500, "Error in reading data from camera")
            # else:
            #     out = json.dumps(senml)
        
        return out


    def POST (self, *uri, **params):
        pass
        return

    def PUT (self, *uri, **params):
        pass
        return

    def DELETE(self):
        pass
        return

if __name__ == '__main__':

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    deviceconnector = SensorsControl(ip)

    cherrypy.tree.mount(SensorsWebService(deviceconnector), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
