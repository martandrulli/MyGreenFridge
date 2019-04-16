# Temperature control class, responsible for activating the heater and send alert when humidity goes out of range
# object to be used in the Temperature web service 

class TempControl:

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