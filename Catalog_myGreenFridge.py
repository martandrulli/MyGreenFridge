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
                        try:
                            fridge['ID_user'] = ID_user # associate the user to the fridge
                            file = open(self.filename, 'w')
                            file.write(json.dumps(dict))
                            file.close()
                            # self.threadLock.release()
                            return 'Association successful'
                        except:
                            # self.threadLock.release()
                            return 'Error in association'
            
            if fridge_found == 0: # the fridge has not been found
                return 'Fridge not found'

    def add_fridge(self, fridge_data):
        '''Adds a fridge to the system. The input parameter "fridge_data" is a json containing
        the fields "ID_fridge", "ID_user" and "password" '''
        
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()
        
        fridge_found = 0
        for fridge in dict['fridges']:
            if fridge['ID_fridge'] == fridge_data['ID_fridge']: # already existing fridge
                # update the information about the existing fridge
                fridge_found = 1
                try:
                    fridge['ID_user'] = fridge_data['ID_user']
                    fridge['password'] = fridge_data['password']
                    fridge['timestamp'] = time.time()
                    # self.threadLock.release()
                    return 'Fridge data updated successfully'
                except:
                    # self.threadLock.release()
                    return 'Error in updating fridge data'
        
        if fridge_found == 0: # the fridge does not already exist
            try:
                dict['fridges'].append({'ID_fridge': fridge_data['ID_fridge'],
                                    'ID_user': fridge_data['ID_user'],
                                    'password': fridge_data['password'],
                                    'timestamp': time.time()})
                file = open(self.filename, 'w')
                file.write(json.dumps(dict))
                file.close()
                # self.threadLock.release()
                return 'Fridge registered successfully'
            except:
                # self.threadLock.release()
                return 'Error in fridge registration'
    
        
    def add_device(self, device_data):
        '''Adds a device to a specific fridge with "ID_fridge". The input parameter
        "device_data" is a json containing the fields "ID_fridge", "ID_device",
        "endpoints", "protocol"and "resources" '''
        
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()
        
        fridge_found = 0
        for fridge in dict['fridges']:
            if fridge['ID_fridge'] == device_data['ID_fridge']:
                fridge_found = 1
                
                device_found = 0
                for device in fridge['devices']:
                    if device['ID_device'] == device_data['ID_device']: # already existing device
                        # update the information about the existing device
                        device_found = 1
                        try:
                            device['endpoints'] = device_data['endpoints']
                            device['protocol'] = device_data['protocol']
                            device['resources'] = device_data['resources']
                            device['timestamp'] = time.time()
                            # self.threadLock.release()
                            return 'Device data updated successfully'
                        except:
                            # self.threadLock.release()
                            return 'Error in updating device data'
                            

                if device_found == 0: # the device does not already exist
                    try:
                        fridge['devices'].append({'ID_device': device_data['ID_device'],
                                            'endpoints': device_data['endpoints'],
                                            'protocol': device_data['protocol'],
                                            'resources': device_data['resources'],
                                            'timestamp': time.time()})
                        file = open(self.filename, 'w')
                        file.write(json.dumps(dict))
                        file.close()
                        # self.threadLock.release()
                        return 'Device registered successfully'
                    except:
                        # self.threadLock.release()
                        return 'Error in device registration'
        
        if fridge_found == 0:
            return 'Fridge not found'
        

    def add_user(self, user_data):
        '''Adds a user to the system. The input parameter "user_data"
        is a json containing the fields "ID_user" and "nickname" '''
        
        
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        json_file = file.read()
        dict = json.loads(json_file)
        file.close()
        
        for user in dict['users']:
            if user['ID_user'] == str(data['ID_user']): # CHECK THIS: USE str(data) ??? also elsewhere???
                try:
                    user['nickname'] = data['nickname']
                    file = open(self.filename, 'w')
                    file.write(json.dumps(dict))
                    file.close()
                    # self.threadLock.release()
                    return 'User data updated successfully'
                except:
                    # self.threadLock.release()
                    return 'Error in updating user data'

        try:
            dict['users'].append({'ID_user': str(data['ID_user']),
                                'nickname': data['nickname']})
            file = open(self.filename, 'w')
            file.write(json.dumps(dict))
            file.close()
            # self.threadLock.release()
            return 'User registered successfully'
        except:
            # self.threadLock.release()
            return 'Error in user registration'

    def delete_fridge(self, ID_fridge):
        '''Removes a fridge from the system'''
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        dict = json.loads(file.read())
        file.close()

        fridge_found = 0
        for fridge in dict['fridges']:
            if fridge['ID_fridge'] == ID_fridge:
                fridge_found = 1
                try:
                    dict['fridges'].remove(fridge)
                    file = open(self.filename, 'w')
                    file.write(json.dumps(dict))
                    file.close()
                    # self.threadLock.release()
                    return 'Fridge removed successfully'
                except:
                    # self.threadLock.release()
                    return 'Error in fridge removal'
        if fridge_found == 0:
            # self.threadLock.release()
            return 'Fridge not found'
    
    def delete_device(self, device_data):
        '''Removes a device from the system. The input parameter "device_data"
        is a json containing the fields "ID_fridge" and "ID_device" '''
        
        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        dict = json.loads(file.read())
        file.close()

        fridge_found = 0
        for fridge in dict['fridges']:
            if fridge['ID_fridge'] == device_data['ID_fridge']:
                fridge_found = 1
                
                device_found = 0
                for device in fridge['devices']:
                    if device['ID_device'] == device_data['ID_device']:
                        device_found = 1
                        try:
                            fridge['devices'].remove(device)
                            file = open(self.filename, 'w')
                            file.write(json.dumps(dict))
                            file.close()
                            # self.threadLock.release()
                            return 'Device removed successfully'
                        except:
                            # self.threadLock.release()
                            return 'Error in device removal'
                
                if device_found == 0:
                    # self.threadLock.release()
                    return 'Device not found'
        
        if fridge_found == 0:
            # self.threadLock.release()
            return 'Fridge not found'

   
    def delete_user(self, ID_user):

        # self.threadLock.acquire()

        file = open(self.filename, 'r')
        dict = json.loads(file.read())
        file.close()

        user_found = 0
        for user in dict['users']:
            if user['ID'] == ID:
                user_found = 1
                try:
                    dict['users'].remove(user)

                    # remove the association between the user and his/her fridges
                    for fridge in dict['fridges']:
                        if fridge['ID_user'] == ID_user:
                            fridge['ID_user'] = None

                    file = open(self.filename, 'w')
                    file.write(json.dumps(dict))
                    file.close()

                    # self.threadLock.release()
                    return 'User removed successfully'
                except:
                    # self.threadLock.release()
                    return 'Error in user removal'
        
        if user_found == 0:
            # self.threadLock.release()
            return 'User not found'

# SOLO PER PROVA
if __name__ == '__main__':
    catalog = Catalog("test_file.txt")




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
