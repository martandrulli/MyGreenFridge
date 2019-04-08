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
        '''Returns IP and port of the broker'''

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        # self.threadLock.release()

        return dict['broker_IP'], dict['broker_port']


    def get_users(self):
        '''Returns ID_user and nickname of each user'''

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        # self.threadLock.release()
        return json.dumps(dict['users'])

    def get_user(self, ID_user):
        '''Returns information about a
        specific user with given ID_user'''
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()
        # self.threadLock.release()

        for user in dict['users']:
            if user['ID_user'] == ID_user:
                user_dict = {'nickname': user['nickname'], 'ID_user' : user['ID_user']}
                return json.dumps(user_dict)
        return 'User not found'

    def get_fridges(self):
        '''Returns information about the fridges
        in the system'''

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        # self.threadLock.release()
        return json.dumps(dict['fridges'])

    def get_fridge(self, ID_fridge):
        '''Returns information about a fridge
        with given ID_fridge'''
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()
        
        fridge_list = []
        # return all the information about the fridge, except for the password and the ID_user
        for fridge in dict['fridges']:
            fridge_dict = {'ID_fridge': fridge['ID_fridge'], 'devices' : fridge['devices'], 'products_list' : fridge['products_list']}
            fridge_list.append(fridge_dict)

        # self.threadLock.release()
        return json.dumps(fridge_list)


    def associate(self, ID_user, ID_fridge, password):
        '''Associates a specific fridge with ID_fridge
        to a specific user with ID_user,
        by using a password'''

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        # find the user
        user_found = 0
        for user in dict['users']:
            if user['ID_user'] == ID_user:
                user_found = 1
        
        if user_found == 0: # the user has not been found
            # self.threadLock.release()
            return "User not found"
        else: # the user has been found
            # find the fridge
            fridge_found = 0
            for fridge in dict['fridges']:
                if fridge['ID_fridge'] == ID_fridge:
                    fridge_found = 1 # the fridge has been found
                    if fridge['password'] != password: # the password is incorrect
                        return 'Password incorrect'
                    else: # the password is correct
                        fridge['ID_user'] = ID_user # associate the user to the fridge
                        file = open(self.filename, 'w')
                        file.write(json.dumps(dict))
                        file.close()
                        # self.threadLock.release()
                        return 'Association successful'
            
            if fridge_found == 0: # the fridge has not been found
                return 'Fridge not found'

    def add_fridge(self, fridge_data):
        
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()
        
        

    def add_device(self, device_data_data):

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()

        for fridge in dict['fridges']:
            if fridge['ID'] == fridge_data['ID']:
                fridge['IP'] = fridge_data['IP']
                fridge['port'] = fridge_data['port']
                fridge['GET'] = fridge_data['GET']
                fridge['POST'] = fridge_data['POST']
                fridge['sub_topics'] = fridge_data['sub_topics']
                fridge['pub_topics'] = fridge_data['pub_topics']
                fridge['resources'] = fridge_data['resources']
                fridge['pws'] = fridge_data['psw']
                fridge['insert-timestamp'] = time.time()
                file = open(self.filename, 'w')
                file.write(json.dumps(dict))
                file.close()
                # self.threadLock.release()
                return "Dear user, the fridge time update has been successful."

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
