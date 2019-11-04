# Instruções de uso

## Requerimentos

Este script utiliza o módulo *scrapy* (pip install Scrapy), recomendo que seja criado um ambiente virtual dedicado antes de instalá-lo pois pode haver conflitos com outros módulos do sistema.

## Primeiros passos

Com o módulo instalado, agora é necessário checar se as configurações estão corretas, optei por deixar as configurações em um arquivo em separado para que não houvesse risco de mexer no programa a cada reconfiguração.

### config.cfg

**quartos** indica a quantidade mínima de quartos que o local possui, para fins de exclusão da busca.
**filtros** representa as chaves de um dicionário dentro do script, que direciona a busca para uma vizinhança ou cidade específica. Apenas dois filtros estão disponíveis mas é
bem fácil criar novos. *Filtros: jurere, jurere-internacional*

Uma vez configurado, o script opera de maneira bem simples: basta executá-lo diretamente (*python vivareal.py*) enquanto estiver no diretório principal do script. O script cria um arquivo *csv* dentro da pasta leituras, no formato 'vivareal YYYY-mm-dd'. O script roda silenciosamente no background e pode demorar alguns segundos para ser concluído.

### Como ler os dados

A tabela gerada na pasta leituras possui várias informações genéricas que achei interessante colocar *(ID-TIPO DE LOCAL-BAIRRO/VIZINHANÇA-PRECO DE ALUGUEL AJUSTADO PARA DIARIA (30 DIAS)-O TIPO DE CONTRATO, ANDAR, AREA UTIL, AREA TOTAL)* mas seria possível buscar muitas outras mais informações sobre os locais para aluguel, como antes, optei pelo formato CSV pois acredito que seria o mais genérico para leitura de dados.

## Observações

Estou aprendendo a biblioteca do scrapy e acho que encontrei algumas soluções melhores do que no primeiro script, testei o uso de classes para armazenar os dados e acredito
que foi uma abordagem melhor.
