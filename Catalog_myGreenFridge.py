# import threading
import time
import json

# CATALOG. It implements a catalog with the following entries:
# broker_IP, broker_port, terraria, temperature controls (temp_controls), light_controls, users
# the catalog is initalized by reading the first version of the catalog json file
# each access to the json file is protected against multi-threading by a Lock
# a thread is automatically activated to delete devices (terraria and controls) which are not updated for more than 30 minutes,
# to prevent requests to wrong IP
# terraria are identified by: ID, password, IP, port, GET, POST, sub_topics, pub_topics, resources, user (ID of the associated user, None if not already associated), insert-timestamp
# temperature controls are identified by: ID, IP, port, GET, POST, sub_topics, pub_topics, temp, terrarium (ID of the associated terrarium), insert-timestamp
# light controls are identified by: ID, IP, port, GET, POST, sub_topics, pub_topics, dawn, dusk, terrarium (ID of the associated terrarium), insert-timestamp
# users are identified by a nickname (the one on Telegram) and by the chat_id to send messages on Telegram.

class Catalog:

    def __init__(self, filename):

        self.filename = filename

        # self.threadLock = threading.Lock()
        #
        # self.deletingThread = DeleteDevice(self)
        # self.deletingThread.start()

    def get_broker(self):
        """Returns IP and port of the broker"""

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        # self.threadLock.release()

        return dict['broker_IP'], dict['broker_port']


    def get_users(self):
        """Returns ID and nickname of each user"""

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        user_list = []

        for user in dict['users']:
            user_dict = {"nickname": user['nickname'], "ID" : user['ID']}
            user_list.append(user_dict)

        # self.threadLock.release()
        return json.dumps(user_list)

    def get_user(self, ID):
        """Returns information about a
        specific user with given ID"""
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()
        # self.threadLock.release()

        for user in dict['users']:
            if user['ID'] == ID:
                fridges_list = []
                for fridge in user['fridges']:
                    fridge_dict = {"fridge_ID": fridge['fridge_ID']}
                    fridges_list.append(fridge_dict)
                user_dict = {"nickname": user['nickname'], "ID" : user['ID'], "fridges": fridges_list}
                return json.dumps(user_dict)
        return "User not found"

    def get_user_fridges(self, ID):
        """Returns information about the fridges
        of a user with given ID"""

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        for user in dict['users']:
            if user['ID'] == ID:
                return json.dumps(user['fridges'])

        # self.threadLock.release()
        return "User not found"

    def get_fridge(self, ID_fridge):
        """Returns information about a fridge
        with given ID_fridge"""
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        # self.threadLock.release()

        for user in dict['users']:
            for fridge in user['fridges']:
                if fridge["ID_fridge"] == ID_fridge:
                    return json.dumps(fridge)
        return "Fridge not found"


    def associate(self, IDUser, IDFridge, password):
        # Associates a specific fridge to a user, by means of the relative IDs and a password.

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        # Search for the user
        flag = 0
        for user in dict['users']:
            if user['ID'] == IDUser:
                flag = 1

        if flag == 0:
            # self.threadLock.release()
            return "User not found"


        for fridge in dict['fridges']:
            if fridge['ID'] == IDFridge:
                if fridge['pws'] != password:
                    return "Sorry. The password you have entered is not correct."
                fridge['user'] = IDUser
                file = open(self.filename, 'w')
                file.write(json.dumps(dict))
                file.close()
                # self.threadLock.release()
                return "The association has been successful."

        # ??????

        # if the fridge is not found

        # self.threadLock.release()
        return "Sorry. The fridge you have looked for is not registred."

    # def changetemp(self, IDFridge, temp):
    #
    #     self.threadLock.acquire()
    #
    #     file = open(self.filename, 'r')
    #     json_file = file.read()
    #     dict = json.loads(json_file)
    #     file.close()
    #
    #     for ctrl in dict['temp_controls']:
    #
    #         if ctrl['terrarium'] == IDTerr:
    #             ctrl['temp'] = temp
    #
    #             file = open(self.filename, 'w')
    #             file.write(json.dumps(dict))
    #             file.close()
    #             self.threadLock.release()
    #             return ctrl['IP'], ctrl['port']
    #
    #     # if the control for that terrarium is not found
    #     self.threadLock.release()
    #     return "Error", "Error"

    # def changelightcycle(self, IDTerr, dawn, dusk):
    #
    #     self.threadLock.acquire()
    #
    #     file = open(self.filename, 'r')
    #     json_file = file.read()
    #     dict = json.loads(json_file)
    #     file.close()
    #
    #     for ctrl in dict['light_controls']:
    #
    #         if ctrl['terrarium'] == IDTerr:
    #
    #             ctrl['dawn'] = dawn
    #             ctrl['dusk'] = dusk
    #
    #             file = open(self.filename, 'w')
    #             file.write(json.dumps(dict))
    #             file.close()
    #             self.threadLock.release()
    #
    #             return ctrl['IP'], ctrl['port']
    #
    #     # if the control for that terrarium is not found
    #     self.threadLock.release()
    #     return "Error", "Error"


    def addFridge(self, data):

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        for fridge in dict['fridges']:
            try:
                if fridge['ID'] == data['ID']:
                    fridge['IP'] = data['IP']
                    fridge['port'] = data['port']
                    fridge['GET'] = data['GET']
                    fridge['POST'] = data['POST']
                    fridge['sub_topics'] = data['sub_topics']
                    fridge['pub_topics'] = data['pub_topics']
                    fridge['resources'] = data['resources']
                    fridge['pws'] = data['psw']
                    fridge['insert-timestamp'] = time.time()
                    file = open(self.filename, 'w')
                    file.write(json.dumps(dict))
                    file.close()
                    # self.threadLock.release()
                    return "Dear user, the fridge time update has been successful."
            except:
                # self.threadLock.release()
                return "Sorry, there was an error during the time update of the fridge."

        try:
            dict['fridges'].append({'ID': data['ID'],
                                'IP': data['IP'],
                                'port': data['port'],
                                'GET': data['GET'],
                                'POST': data['POST'],
                                'sub_topics': data['sub_topics'],
                                'pub_topics': data['pub_topics'],
                                'resources': data['resources'],
                                'pws': data['psw'],
                                'user': None,
                                'insert-timestamp': time.time()})

            file = open(self.filename, 'w')
            file.write(json.dumps(dict))
            file.close()
            # self.threadLock.release()
            return "Dear user, the fridge registration has been successful."
        except:
            # self.threadLock.release()
            return "Sorry. There was an error in registrating the fridge."

    # def addtempcontrol(self, data):
    #
    #     self.threadLock.acquire()
    #
    #     file = open(self.filename, 'r')
    #     json_file = file.read()
    #     dict = json.loads(json_file)
    #     file.close()
    #
    #     for device in dict['temp_controls']:
    #         if device['ID'] == data['ID']:
    #             try:
    #                 device['IP'] = data['IP']
    #                 device['port'] = data['port']
    #                 device['GET'] = data['GET']
    #                 device['POST'] = data['POST']
    #                 device['sub_topics'] = data['sub_topics']
    #                 device['pub_topics'] = data['pub_topics']
    #                 device['temp'] = data['temp']
    #                 device['terrarium'] = data['terrarium']
    #                 device['insert-timestamp'] = time.time()
    #
    #                 file = open(self.filename, 'w')
    #                 file.write(json.dumps(dict))
    #                 file.close()
    #                 self.threadLock.release()
    #                 return "Update done"
    #             except:
    #                 self.threadLock.release()
    #                 return "Error"
    #
    #     try:
    #         dict['temp_controls'].append({'ID': data['ID'],
    #                             'IP': data['IP'],
    #                             'port': data['port'],
    #                             'GET': data['GET'],
    #                             'POST': data['POST'],
    #                             'sub_topics': data['sub_topics'],
    #                             'pub_topics': data['pub_topics'],
    #                             'temp': data['temp'],
    #                             'terrarium': data['terrarium'],
    #                             'insert-timestamp': time.time()})
    #
    #         file = open(self.filename, 'w')
    #         file.write(json.dumps(dict))
    #         file.close()
    #         self.threadLock.release()
    #         return "Registration done"
    #     except:
    #         self.threadLock.release()
    #         return "Error"

    # def addlightcontrol(self, data):
    #
    #     self.threadLock.acquire()
    #
    #     file = open(self.filename, 'r')
    #     json_file = file.read()
    #     dict = json.loads(json_file)
    #     file.close()
    #
    #     for device in dict['light_controls']:
    #         try:
    #             if device['ID'] == data['ID']:
    #                 device['IP'] = data['IP']
    #                 device['port'] = data['port']
    #                 device['GET'] = data['GET']
    #                 device['POST'] = data['POST']
    #                 device['sub_topics'] = data['sub_topics']
    #                 device['pub_topics'] = data['pub_topics']
    #                 device['dawn'] = data['dawn']
    #                 device['dusk'] = data['dusk']
    #                 device['terrarium'] = data['terrarium']
    #                 device['insert-timestamp'] = time.time()
    #
    #                 file = open(self.filename, 'w')
    #                 file.write(json.dumps(dict))
    #                 file.close()
    #                 self.threadLock.release()
    #                 return "Update done"
    #         except:
    #             self.threadLock.release()
    #             return "Error"
    #
    #     try:
    #         dict['light_controls'].append({'ID': data['ID'],
    #                             'IP': data['IP'],
    #                             'port': data['port'],
    #                             'GET': data['GET'],
    #                             'POST': data['POST'],
    #                             'sub_topics': data['sub_topics'],
    #                             'pub_topics': data['pub_topics'],
    #                             'dawn': data['dawn'],
    #                             'dusk': data['dusk'],
    #                             'terrarium': data['terrarium'],
    #                             'insert-timestamp': time.time()})
    #
    #         file = open(self.filename, 'w')
    #         file.write(json.dumps(dict))
    #         file.close()
    #         self.threadLock.release()
    #         return "Registration done"
    #     except:
    #         self.threadLock.release()
    #         return "Error"

    def adduser(self, data):

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        for user in dict['users']:
            try:
                if user['ID'] == str(data['ID']):
                    user['nickname'] = data['nickname']
                    file = open(self.filename, 'w')
                    file.write(json.dumps(dict))
                    file.close()
                    # self.threadLock.release()
                    return "Dear user, the nickname has been updated."
            except:
                # self.threadLock.release()
                return "Sorry. There was an error in the nickname update of the user."

        try:
            dict['users'].append({'ID': str(data['ID']),
                                'nickname': data['nickname']})
            file = open(self.filename, 'w')
            file.write(json.dumps(dict))
            file.close()
            # self.threadLock.release()
            return "The user registration has been successful"
        except:
            # self.threadLock.release()
            return "Sorry. There was an error in the user registration."

    def deleteFridge(self, ID):

        # self.threadLock.acquire()

        print "Deleting fridge"
        file = open(self.filename, 'r')
        dict = json.loads(file.read())
        file.close()

        for fridge in dict['fridges']:
            if fridge['ID'] == ID:
                dict['fridges'].remove(fridge)
                file = open(self.filename, 'w')
                file.write(json.dumps(dict))
                file.close()

        # self.threadLock.release()

    # def deletetempcontrol(self, ID):
    #
    #     self.threadLock.acquire()
    #
    #     file = open(self.filename, 'r')
    #     dict = json.loads(file.read())
    #     file.close()
    #
    #     for device in dict['temp_controls']:
    #         if device['ID'] == ID:
    #             dict['temp_controls'].remove(device)
    #             file = open(self.filename, 'w')
    #             file.write(json.dumps(dict))
    #             file.close()
    #             break
    #
    #     self.threadLock.release()


    # def deletelightcontrol(self, ID):
    #
    #     self.threadLock.acquire()
    #
    #     file = open(self.filename, 'r')
    #     dict = json.loads(file.read())
    #     file.close()
    #
    #     for device in dict['light_controls']:
    #         if device['ID'] == ID:
    #             dict['light_controls'].remove(device)
    #             file = open(self.filename, 'w')
    #             file.write(json.dumps(dict))
    #             file.close()
    #             break
    #
    #     self.threadLock.release()


    def deleteUser(self, ID):

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        dict = json.loads(file.read())
        file.close()

        for fridge in dict['fridges']:
            if fridge['user'] == ID:
                fridge['user'] = None

        for user in dict['users']:
            if user['ID'] == ID:
                dict['users'].remove(user)

        file = open(self.filename, 'w')
        file.write(json.dumps(dict))
        file.close()

        # self.threadLock.release()

# RIVEDERE POI, QUANDO CAPIREMO COME E SE INSERIRE I THREAD.
# Letizia sostiene che questa cosa sia abbastanza obbligatoria da fare
# In effetti l'unica soluzione per fare questa cosa -se obbligatoria- sono i thread.


# ## Thread to delete devices older than half an hour
# class DeleteDevice(threading.Thread):
#
#     def __init__(self, catalog):
#         threading.Thread.__init__(self)
#         self.catalog = catalog
#
#     def run(self):
#         while True:
#
#             self.catalog.threadLock.acquire()
#             file = open(self.catalog.filename, 'r')
#             dict = json.loads(file.read())
#             file.close()
#             self.catalog.threadLock.release()
#
#             for device in dict['terraria']:
#                 if time.time() - device['insert-timestamp'] > 30*60:
#                     self.catalog.deleteterrarium(device['ID'])
#
#             # for device in dict['temp_controls']:
#             #     if time.time() - device['insert-timestamp'] > 30*60:
#             #         self.catalog.deletetempcontrol(device['ID'])
#             #
#             # for device in dict['light_controls']:
#             #     if time.time() - device['insert-timestamp'] > 30*60:
#             #         self.catalog.deletelightcontrol(device['ID'])
#
#             time.sleep(10)
