# The Catalog is accessible through REST web services.
# The broker is identified with broker_IP and broker_port. It is set as written in the Catalog.txt file.
# Users are stored as: chat_id, nickname.
# Devices can be terraria or control strategies.
# - GET: - /broker/ -> Retrieve information about IP address and port of the message broker in the platform
#        - /terraria/ -> Retrieve list of registered terraria
#        - /terrarium?ID=<id> -> Retrieve information about a terrarium with a specific id
#        - /users/ -> Retrieve list of registered users
#        - /user?ID=<id> -> Retrieve information about a user with a specific id
#        - associate?IDTerr=<IDTerrarium>&IDUs=<IDUser> -> Associate a terrarium to a user
#        - changetemp?IDTerr=<IDTerrarium>&temp=<temp>
#        - changelightcycle?IDTerr=<IDTerrarium>&dawn=<hour_begin>&dawn=<hour_stop>

#
# - POST: - /add_device/terrarium     ->  Registration or update of a terrarium
#         - /add_device/tempcontrol   ->  Registration or update of a control
#         - /add_device/lightcontrol  ->  Registration or update of a control
#         - /add_user/                -> Registration or update of a user
#
# -DELETE: - /device/terrarium    -> delete a device (done automatically for devices older than 30 minutes)
#          - /device/tempcontrol  -> delete a device (done automatically for devices older than 30 minutes)
#          - /device/lightcontrol -> delete a device (done automatically for devices older than 30 minutes)
#          - /user/               -> delete a user

import cherrypy
import json
import time
import requests
from Catalog import *

## REST Web Service
class RESTCatalog:

    exposed = True

    def __init__(self):
        self.catalog = Catalog("Catalog.txt")

    ## WEB SERVICE
    def GET(self, *uri, **params):

        if len(uri) == 0:
            raise cherrypy.HTTPError(400)

        # /broker/ -> Retrieve information about IP address and port of the message broker in the platform
        if uri[0] == 'broker':
            ip, port = self.catalog.broker()
            return json.dumps({'broker_IP': ip, 'broker_port': port})

        # /terraria/ -> Retrieve list of registered devices
    elif uri[0] == 'fridges':
            return json.dumps({'fridges': self.catalog.fridges()})

        # /terrarium?ID=<id> -> Retrieve information about a device with a specific id
    elif uri[0] == 'myGreenFridge':
            if not 'ID' in params.keys():
                raise cherrypy.HTTPError(400, 'No ID given')

            out = self.catalog.myGreenFridge(params['ID'])

            if out == "Fridge not found":
                raise cherrypy.HTTPError(404, out)
            else:
                return json.dumps({'myGreenFridge': out})

        # /users/ -> Retrieve list of registered users
        elif uri[0] == 'users':
            return json.dumps({'users': self.catalog.users()})

        # /user?ID=<id> -> Retrieve information about a user with a specific id
        elif uri[0] == 'user':
            if not 'ID' in params.keys():
                raise cherrypy.HTTPError(400, 'No ID given')

            out = self.catalog.user(params['ID'])

            if out == "User not found":
                raise cherrypy.HTTPError(404, out)
            else:
                return json.dumps({'user': out})

        # /associate?IDTerr=<IDTerrarium>&IDUs=<IDUser> -> Associate a terrarium to a user
        elif uri[0] == 'associate':
            try:
                IDUser = params['IDUs']
                IDFridge = params['IDFridge']
                password = params['pws']
            except:
                raise cherrypy.HTTPError(400)

            out = self.catalog.associate(IDUser, IDFridge, password)

            if out == "Sorry. The fridge you have looked for is not registred.": #DA SISTEMARE. FORSE CONVENIVA SEMPLICEMENTE "ERROR"
                raise cherrypy.HTTPError(404)
            if out == "Sorry. The password you have entered is not correct.":
                raise cherrypy.HTTPError(401)

        # elif uri[0] == 'changetemp':
        #     try:
        #         IDTerr = params['IDTerr']
        #         temp = params['temp']
        #     except:
        #         raise cherrypy.HTTPError(400)
        #
        #     if temp == 'null':
        #         temp_cat = None
        #
        #     else:
        #         temp_cat = temp
        #
        #     ip, port = self.catalog.changetemp(IDTerr, temp_cat)
        #
        #     if ip == "Error":
        #         raise cherrypy.HTTPError(404)
        #     else:
        #         try:
        #             r = requests.get('http://' + ip + ':' + str(port) + '/temperature', params = {'temp': temp})
        #             r.raise_for_status()
        #         except requests.HTTPError as err:
        #             raise cherrypy.HTTPError(500)
        #             self.catalog.changetemp(IDTerr, None)
        #
        # elif uri[0] == 'changelightcycle':
        #     try:
        #         IDTerr = params['IDTerr']
        #         dawn = params['dawn']
        #         dusk = params['dusk']
        #     except:
        #         raise cherrypy.HTTPError(400, 'Incorrect request format')
        #
        #     if dawn == 'null':
        #         dawn_cat = None
        #         dusk_cat = None
        #
        #     else:
        #         dawn_cat = dawn
        #         dusk_cat = dusk
        #
        #     ip, port = self.catalog.changelightcycle(IDTerr, dawn_cat, dusk_cat)
        #
        #     if ip == "Error":
        #         raise cherrypy.HTTPError(404)
        #     else:
        #         try:
        #             r = requests.get('http://' + ip + ':' + str(port) + '/light/', params = {'dawn': dawn, 'dusk': dusk})
        #             r.raise_for_status()
        #         except requests.HTTPError as err:
        #             raise cherrypy.HTTPError(500)
        #             self.catalog.changelightcycle(IDTerr, None, None)

        elif uri[0] == "delete_user":
            try:
                self.catalog.deleteuser(params['UserID'])
            except:
                raise cherrypy.HTTPError(400, 'Incorrect request format')

        else:
            raise cherrypy.HTTPError(400, 'Incorrect request format')

    def POST(self, *uri):

        if len(uri) == 0:
            raise cherrypy.HTTPError(400)

        mybody = cherrypy.request.body.read()

        try:
            data = json.loads(mybody)
        except:
            raise cherrypy.HTTPError(400)

        # /add_device/ ->  Registration or update of a device
        if uri[0] == 'add_device':

            if uri[1] == 'myGreenFridge':
                out = self.catalog.addFridge(data)
                if out == "Sorry, there was an error during the time update of the fridge." or out == "Sorry. There was an error in registrating the fridge.":
                    raise cherrypy.HTTPError(400)

            # elif uri[1] == 'tempcontrol':
            #     out = self.catalog.addtempcontrol(data)
            #     if out == "Error":
            #         raise cherrypy.HTTPError(400)
            #
            # elif uri[1] == 'lightcontrol':
            #     out = self.catalog.addlightcontrol(data)
            #     if out == "Error":
            #         raise cherrypy.HTTPError(400)

            else:
                raise cherrypy.HTTPError(400)

        # /add_user/ -> Registration or update of a user
        elif uri[0] == 'add_user':
            out = self.catalog.adduser(data)
            if out == "Error":
                raise cherrypy.HTTPError(400)

        else:
            raise cherrypy.HTTPError(400)

    def DELETE(self, *uri, **params):

        try:
            ID = params['ID']
        except:
            raise cherrypy.HTTPError(400)

        if uri[0] == 'device':

            if uri[1] == 'fridge':
                self.catalog.deleteFridge(ID)

            # elif uri[1] == 'tempcontrol':
            #     self.catalog.deletetempcontrol(ID)
            #
            # elif uri[1] == 'lightcontrol':
            #     self.catalog.deletelightcontrol(ID)

            else:
                raise cherrypy.HTTPError(400)

        # /user/ -> delete a user
        elif uri[0] == 'user':
            self.catalog.deleteUser(ID)

        else:
            raise cherrypy.HTTPError(400)


if __name__ == '__main__':
	conf = {
		'/': {
		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		'tools.sessions.on': True,
	}
}

cherrypy.tree.mount (RESTCatalog(), '/', conf)
cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.config.update({'server.socket_port': 8080})
cherrypy.engine.start()
cherrypy.engine.block()
