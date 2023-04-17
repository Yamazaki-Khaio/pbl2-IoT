from posto import PostoEnergia

# Criando um objeto para a região 1
regiao1 = PostoEnergia("Região 1", 1883)

# Criando um objeto para a região 2
regiao2 = PostoEnergia("Região 2", 1884)

# Publicando mensagens de região 1
for i in range(10):
    regiao1.publicar_mensagem(f"Região 1 - counter: {i}", "URA001/teste_regiao1")

# Publicando mensagens de região 2
for i in range(10):
    regiao2.publicar_mensagem(f"Região 2 - counter: {i}", "URA001/teste_regiao2")
