from mqtt import Conectar_mqtt
import uuid
import time 
import random
from threading import Thread


class PostoEnergia:
 
    def __init__(self):

        self.tipo = 'posto'
        self.regiao = random.randint(0,0)
        self.client_id =  f"{self.tipo}--{str(uuid.uuid4())}"
        conectar = Conectar_mqtt
        self.client = conectar.connect_mqtt(self, self.regiao, self.client_id)
        self.fila = random.randint(0,20)
        self.enviar_filas_mqtt()

    def atualizar_filas(self, filas):

        self.filas = filas

    def enviar_filas_mqtt(self):

        topic = "enviar/fila"
        result = self.client.publish(topic, f"{self.client_id}{self.fila}")
        status = result[0]
        if status == 0:
                print(f"Fila de carros enviada ao servidor com sucesso!")
                print(f"Número de carros na fila é {self.fila}")
        else:
            print(f"Fila de carros NÃO enviada ao servidor! topico:{topic}")
        

    def publish(self):

        msg_count = 0
        while True:
            time.sleep(1)
            msg = f"{self.regiao} - counter: {msg_count}"
            result = self.client.publish(self.topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"{self.regiao} - Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"{self.regiao} - Failed to send message to topic {self.topic}")
            msg_count += 1

def criar_postos_energia():

    # Criar e iniciar cinco threads simulando cinco postos de energia em diferentes localidades
    threads = []
    for i in range(5):
        regiao = f"Região {i+1}"
        porta = random.randint(1000, 9999)
        topic = f"URA001/teste{i+1}"
        t = Thread(target=PostoEnergia, args=(regiao, porta, topic))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == '__main__':
    p1 = PostoEnergia()

