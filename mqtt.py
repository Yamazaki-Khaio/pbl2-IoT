
broker = 'localhost'
servidores = [1883,1884,1885,1887]
from paho.mqtt import client as mqtt_client
class Conectar_mqtt:

    def connect_mqtt(self, regiao, client_id):
        try:
            client = mqtt_client.Client(client_id)
            client.connect(broker,servidores[regiao])
            print("Conectado ao Broker!")
            return client
        except:
            print("Erro na conexão")
    
    def on_message(client, userdata, msg):
    
        v = unpack(">H",msg.payload)[0]
        print (msg.topic + "/" + str(v))
    
    def on_connect(client, userdata, flags, rc):
        if(rc==0):
            print("conectado")
        else:
            print("não concetado")
