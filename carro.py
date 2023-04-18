from mqtt import Conectar_mqtt
import uuid
import time 
import random

class Carro:

    def __init__(self):
            
            self.tipo = 'carro'
            self.bateria = 100
            self.regiao = random.randint(0,0)
            self.client_id =  f"{self.tipo}--{str(uuid.uuid4())}"
            conectar = Conectar_mqtt
            self.client = conectar.connect_mqtt(self, self.regiao, self.client_id)
            self.descarga_bateria()
    
    def menor_fila(self):
    
            topic = "solicitar/menor_fila"
            result = self.client.publish(topic, f"{self.client_id}")
            status = result[0]
            
            if status == 0:
                print(f"Solicitação de posto com menor fila ao servidor enviada com sucesso!")
                   
            else:
                print(f"Solicitação de menor fila ao servidor falhou! topico:{topic}")
    
    def descarga_bateria(self):

        taxa = random.randint(1,2)
        
        while self.bateria >= 11:
             
            time.sleep(taxa)
            self.bateria -= 1
            print(f"Bateria:{self.bateria}%")
        
        self.menor_fila()

if __name__ == '__main__':
    c1 = Carro()
