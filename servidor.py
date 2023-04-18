from mqtt import Conectar_mqtt
from struct import unpack
import uuid
import random
class Servidor:
 
    def __init__(self):
            
            self.tipo = 'servidor'
            self.postos = []
            self.regiao = random.randint(0,0)
            self.client_id =  f"{self.tipo}--{str(uuid.uuid4())}"
            conectar = Conectar_mqtt
            self.client = conectar.connect_mqtt(self, self.regiao, self.client_id)
    
    def on_connect(client, data, rc):
        print("entrou")
        client.subscribe([('solicitar/menor_fila',0)])

    def on_message(client, userdata, msg):

        v = unpack(">H",msg.payload)[0]
        print(msg.topic + "/" + str(v))
    
    def retornar_requisicao():
          pass
    
    def cadastrar_posto():
          pass
    
    def atualizar_fila_posto():
          pass
    
    def aguardando(self):
          self.client.connect_callback

if __name__ == '__main__':
    S1 = Servidor()
