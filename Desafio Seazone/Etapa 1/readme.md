# Instruções de uso

## Requerimentos

Este script utiliza o módulo *scrapy* (pip install Scrapy), recomendo que seja criado um ambiente virtual dedicado antes de instalá-lo pois pode haver conflitos com outros módulos do sistema.

## Primeiros passos

Com o módulo instalado, agora é necessário checar se as configurações estão corretas, optei por deixar as configurações em um arquivo em separado para que não houvesse risco de mexer no programa a cada reconfiguração.

### config.cfg

**api_key** representa a chave de acesso ao api da airbnb. O programa foi feito dependante dela pois as informações são muito mais acessíveis com seu uso, e, felizmente, ela não muda com muita frequência. Para pegá-la é necessário usar um *network debugger* como o das ferramentas de desenvolvedor do Google Chrome (*ctrl+shift+j*). Enquanto se navega pelo site (em especial quando se navega pelo mapa na tela de pesquisa) o site chamará a página 'https://www.airbnb.com.br/api/v2/explore_tabs' para pedir informações de busca no mapa. Na URL da página um dos argumentos chamado *key* é a chave do api, basta copiá-lo para este campo das configurações.
**local** representa o local que será feita a busca, a cidade, ou vizinhança conforme definido no sistema de buscas da AirBNB. Basta copiar o nome da pasta da cidade como aparece na URL. Exemplo: em https://www.airbnb.com.br/s/New-York/homes o nome da cidade é *New-York*, em https://www.airbnb.com.br/s/Jurerê--Florianópolis-~-SC/homes é *Jurerê--Florianópolis-~-SC*.
**hospedes** indica a locação mínima de pessoas que o local suporta, para fins de exclusão da busca.
**quartos** indica a quantidade mínima de quartos que o local possui, para fins de exclusão da busca.
**busca** indica o número de locais que serão buscados, em múltiplos de 50.
**previsao_receita** representa quantos meses será calculada a receita dos quartos que não estão mais acessíveis. Representa *meses duros*, não mede 180 dias.

Uma vez configurado, o script opera de maneira bem simples: basta executá-lo diretamente (*python airbnb.py*) enquanto estiver no diretório principal do script. O script cria um arquivo *csv* dentro da pasta leituras, no formato 'airbnb YYYY-mm-dd'. O script roda silenciosamente no background e pode demorar alguns segundos para ser concluído.

### Como ler os dados

A tabela gerada na pasta leituras possui as informações que foram requisitadas *(ID-RECEITA-MEDIA JAN-MEDIA FEV-MEDIA MAR)* mas seria possível buscar muitas outras mais informações sobre os locais para aluguel (como a nota do quarto, as acomodações, reviews, etc), optei pelo formato CSV pois acredito que seria o mais genérico para leitura de dados.

## Observações

Meu primeiro script de scraping, confesso que ainda tenho muito a ler na biblioteca e tendo mais tempo o script ficaria muito melhor.