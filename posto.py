from paho.mqtt import client as mqtt_client
import uuid
import time 
import random
from threading import Thread

broker = 'localhost'

class PostoEnergia:
 
    def __init__(self, regiao, porta, topic):
        self.regiao = regiao
        self.lista = {regiao: porta}
        self.topic = topic
        self.client = self.connect_mqtt()
        self.publish()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"{self.regiao} - conectado ao MQTT!")
            else:
                print(f"{self.regiao} - Falha ao conectar, return code {rc}\n")

        def on_publish(client, userdata, mid):
            print(f"{self.regiao} - Mensagem publicada com sucesso (id={mid})")

        client = mqtt_client.Client(str(uuid.uuid4()))
        client.on_connect = on_connect
        client.on_publish = on_publish  # adiciona listener para eventos de publicação de mensagens
        client.connect(broker)
        return client

    def atualizar_filas(self, filas):
        self.filas = filas

    def enviar_filas_mqtt(self, mensagem):
        port = self.lista[self.regiao]
        topic = "enviar/fila"

    def simular(self, latitude_carro, longitude_carro):
        # simular o funcionamento do posto de energia
        pass

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
    criar_postos_energia()
    print("Execução concluída!")
