class Carro:
    def __init__(self, id, localizacao, nivel_bateria):
        self.id = id
        self.localizacao = localizacao
        self.nivel_bateria = nivel_bateria

    def atualizar_localizacao(self, nova_localizacao):
        self.localizacao = nova_localizacao

    def atualizar_nivel_bateria(self, novo_nivel_bateria):
        self.nivel_bateria = novo_nivel_bateria
