# REPOSITORIO DESTINADO AO PROBLEMA 2 DA DISCIPLINA MI - Concorrência e Conectividade - 2023.1

# Resumo 
Este relatório descreve o funcionamento de um sistema de gerenciamento de carga para carros elétricos que utiliza a arquitetura de publish/subscribe em uma arquitetura distribuída, na qual vários dispositivos se comunicam por meio de um broker MQTT centralizado. O sistema implementa uma arquitetura de processamento de borda que utiliza dois tipos de nós, fog nodes e edge nodes, para processar as informações recebidas. Essa arquitetura permite uma distribuição de carga de processamento mais equilibrada e uma melhor utilização dos recursos disponíveis em cada tipo de nó.

O sistema é composto por três "nós": o MQTT Broker, o fog node e o edge node, que simulam os nós da rede. O MQTT Broker é responsável por receber as mensagens dos sensores instalados nos carros elétricos e nos postos de recarga e encaminhá-las para os nós adequados. O fog node é responsável por processar as mensagens dos carros elétricos e o edge node é responsável por processar as mensagens dos postos de recarga.

As mensagens dos carros elétricos contêm informações sobre a carga da bateria e o tipo de descarga (rápida ou lenta). O fog node processa essas informações e calcula o tempo de carregamento necessário para cada carro elétrico, adicionando essa informação à mensagem que é encaminhada para o edge node. Já as mensagens dos postos de recarga contêm informações sobre a capacidade do posto e a fila de espera. O edge node processa essas informações e calcula o tempo de espera necessário para cada carro elétrico, adicionando essa informação à mensagem que é encaminhada de volta para o MQTT Broker.

Para o controle da carga de processamento dos nós, o sistema utiliza variáveis. O fog node possui uma capacidade máxima de processamento definida pela variável fog_capacity, enquanto o edge node possui uma capacidade máxima de processamento definida pela variável edge_capacity. As variáveis fog_load e edge_load contêm a carga atual de processamento dos nós e são atualizadas a cada mensagem processada.

O código principal é um loop que gera mensagens aleatórias dos carros elétricos e dos postos de recarga a cada cinco segundos. Essas mensagens são publicadas no MQTT Broker e encaminhadas para os nós adequados para processamento. O sistema utiliza threads para a recepção de mensagens e para a conexão com o MQTT Broker. A função mqtt_loop é executada em uma thread separada e é responsável por manter a conexão com o MQTT Broker e receber as mensagens. A função on_message é executada em uma thread separada e é responsável por chamar as funções de processamento de dados de acordo com o tópico da mensagem recebida.

# Tecnologias Utilizadas
O código foi desenvolvido em Python e utiliza a biblioteca PAHO MQTT para a comunicação entre os diferentes nós do sistema e a biblioteca FLASK para API REST e DOCKEFILE.

# Arquitetura do Sistema
usando o padrão de arquitetura publish/subscribe em uma arquitetura distribuída, na qual vários dispositivos se comunicam por meio de um broker MQTT centralizado

MQTT Broker: é responsável por receber as mensagens dos sensores instalados nos carros elétricos e nos postos de recarga e encaminhá-las para os "nós" adequados, simulando a nuvem.
Fog node: é um topico responsável por processar as mensagens dos carros elétricos e calcular o tempo de carregamento necessário para cada carro elétrico.
Edge node: é um outro topico responsável por processar as mensagens dos postos de recarga e calcular o tempo de espera necessário para cada carro elétrico.
Processamento de Mensagens
As mensagens dos carros elétricos contêm informações sobre a carga da bateria e o tipo de descarga (rápida ou lenta). O fog node processa essas informações e calcula o tempo de carregamento necessário para cada carro elétrico. Esse tempo é adicionado à mensagem e a mensagem é encaminhada para o edge node.

# Mensagens
As mensagens dos carros elétricos contêm informações sobre a carga da bateria e o tipo de descarga (rápida ou lenta). O fog node processa essas informações e calcula o tempo de carregamento necessário para cada carro elétrico. Esse tempo é adicionado à mensagem e a mensagem é encaminhada para o edge node.

As mensagens dos postos de recarga contêm informações sobre a capacidade do posto e a fila de espera. O edge node processa essas informações e calcula o tempo de espera necessário para cada carro elétrico. Esse tempo é adicionado à mensagem e a mensagem é encaminhada de volta para o MQTT Broker.

# Controle de Carga de Processamento
O sistema utiliza variáveis para controle da carga de processamento dos nós. O fog node possui uma capacidade máxima de processamento definida pela variável fog_capacity. O edge node possui uma capacidade máxima de processamento definida pela variável edge_capacity. As variáveis fog_load e edge_load contêm a carga atual de processamento dos nós e são atualizadas a cada mensagem processada.

# Loop Principal e Threads
O código principal é um loop que gera mensagens aleatórias dos carros elétricos e dos postos de recarga a cada cinco segundos. Essas mensagens são publicadas no MQTT Broker e encaminhadas para os nós adequados para processamento.

O sistema utiliza threads para a recepção de mensagens e para a conexão com o MQTT Broker. A função mqtt_loop é executada em uma thread separada e é responsável por manter a conexão com o MQTT Broker e receber as mensagens. A função on_message é executada em uma thread separada e é responsável por chamar as funções de processamento de dados de acordo com o tópico da mensagem recebida.

# Fluxo de dados
1. Os sensores dos carros elétricos e dos postos de recarga enviam mensagens para o MQTT Broker.
2. O MQTT Broker encaminha as mensagens para os nós adequados.
3. O fog node processa as mensagens dos carros elétricos, calcula o tempo de carregamento necessário e adiciona essa informação à mensagem.
4. O edge node processa as mensagens dos postos de recarga, calcula o tempo de espera necessário e adiciona essa informação à mensagem.
5. A mensagem é encaminhada de volta para o MQTT Broker.
5. Os carros elétricos recebem a informação do tempo de carregamento necessário e os postos de recarga recebem a informação do

# Organização das pastas
A solução está organizada em três arquivos executavéis, com o Diagrama de Sequência básico da arquitetura, executaveis python do servidor_mqtt, publish_mqtt e computador_bordo tambem contém trÊs arquivos dockerfiles para criação da imagem do Servidor_mqtt e Publish_Mqtt e Computador_bordo.

# Funcionamento

Este código é um exemplo de simulação de comunicação entre dispositivos IoT (Internet das Coisas) utilizando o protocolo MQTT (Message Queuing Telemetry Transport).

Inicialmente, as configurações dos brokers, tópicos, nós fog e edge são definidas. As variáveis para controle da carga de processamento dos nós também são inicializadas. Em seguida, são definidas duas funções que processam dados: a primeira processa dados de carros elétricos e publica no tópico do fog node, enquanto a segunda processa dados de postos de recarga e publica no tópico do edge node.

Em seguida, é criado um cliente MQTT, que se conecta ao broker e se inscreve em dois tópicos: "dadoscarros" e "dadospontos". O loop de recebimento de mensagens é iniciado em uma thread separada para que a conexão com o broker seja mantida enquanto a aplicação continua a executar.

Após isso, um loop principal é iniciado para gerar e publicar dados aleatórios de carros elétricos e postos de recarga, respectivamente, utilizando funções específicas. Esses dados são gerados aleatoriamente e incluem informações como ID do carro, marca, modelo, porcentagem de bateria, tipo de descarga, ID do posto de recarga, capacidade do posto, tamanho da fila e localização.

# Conclusão
Após pesquisas sobre computação de ponta e em borda, de uma maneira simples e em um cenario ficticio o a solução foi beneficiada da simulação de "nós" para que utilize o padrão de arquitetura publish/subscribe em uma arquitetura distribuída, na qual vários dispositivos se comunicam por meio de um broker MQTT centralizado. O sistema implementa uma arquitetura de processamento de borda que utiliza dois tipos de nós, fog nodes e edge nodes, para processar as informações recebidas. Essa arquitetura permite uma distribuição de carga de processamento mais equilibrada e uma melhor utilização dos recursos disponíveis em cada tipo de nó, o produto também contem uma comunicação API REST para requerir serviços via protocolo HTTP.


