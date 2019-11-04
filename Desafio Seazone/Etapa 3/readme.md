# Análise de dados

## Objetivos

Utilizar os dados colhidos nas duas primeiras etapas para escolher três opções de apartamentos que sejam bons investimentos, explicar o porque da escolha.

## Considerações

Esta é uma análise bastante superficial dado os objetivos deste trabalho. Para uma análise mais aprofundada seria interessante colher o máximo de informações possíveis
de ambos os portais, especialmente o AirBNB que disponibiliza reviews e opiniões de usuários além dos bookings completos de cada dia. Notei alguns erros e padrões indicativos de erros nos dados vindos da AirBNB, seria interessante no futuro melhorar a coleta de dados do preco medio e previsao da receita, a fim de identificar cadastros errados e até mesmo desconsiderar comportamentos estranhos nos dados.

Dito isso, vamos aos resultados!

## Análise 1

Carreguei os dados em csv da AirBNB e os plotei no pandas. A primeira coisa que me chamou a atenção foi o desvio padrão dos preços
e que cerca de 90% dos apartamentos estão com preço abaixo da média.

Com o foco em obter o apartamento que seja o melhor investimento decidi imediatamente nesta primeira análise em ir para uma abordagem financeira:
com foco nos três meses de análise *(jan-fev-mar)* minha intuição disse que os apartamentos com melhor custo benefício seriam os mais procurados, e focando
apenas nos dados que coletamos, decidi dividir a receita dos próximos 6 meses pela média de preços.
Esta nova coluna revelou que alguns apartamentos estavam com valores desproporcionalmente superiores nesta relação receita/preco medio,
isso me chamou a atenção, no sentido que poderia haver algum problema com a previsão da receita. Investigando descobri que alguns apartamentos
estavam com preços errados vindos da AirBNB (como alugueis diários de 100 mil reais), possivelmente algum erro cadastral do locador.
Também descobri que certas pessoas não alugam com regularidade os apartamentos, que possuiam discrepâncias muito grandes entre o valor *padrão* (não praticado) e o valor real nos dias em que a pessoa disponibilizava o apartamento. Filtrei as discrepâncias e refiz a análise, desta vez filtrando também pelo preço médio para o mês.

Eu gostaria de pegar apartamentos com preço máximo de 300 reais, sendo assim e usando a relação como 'nota'.

Com os dados em questão, cheguei a conclusão que um investimento bom para o mes de março é o de id **28600926**, enquanto outro bom para o mês de fevereiro é o **30169499**.
Existiam outros melhores mas nenhum com vagas, aprimorando o scrapy seria possível prever tudo isto.

## Análise 2

Desta vez decidi estudar os dados da VivaReal e começar utilizando uma abordagem diferente, como colhi dados diversos decidi brincar com eles e fazer uma regresão linear para ver se tipo de local, andar, quartos, e a area util poderiam ser utilizadas como previsoras do valor dos apartamentos. Após limpar os dados, retirando apartamentos com dados faltantes e com valores claramente errados, fiz uma regressão linear para prever o preco e criei 2 colunas na tabela: uma dividindo a previsao pelo preco diario (demonstrando quanto cada real do preco cobrado vale de acordo com a previsao), e outra diminuindo a previsao pelo preco diario (demonstrando o lucro total ao alugar aquele apartamento).

Utilizei a primeira coluna para análise pois quero ver a oferta mais vantajosa, o id **85005128** em jurere nacional era a oferta de melhor valor segundo a regressão, R$ 240.00 por um apto de 2 quartos e 78 m2. Considerando apenas jurere internacional, os apartamentos **2433096197** e **2456757054** aparecem empatados em primeiro lugar, ambos com preco de R$ 500.00, 3 quartos e area util similares (isso acontece porque a quantidade de quartos são fatores importantes para o regressor). Se precisasse de um apartamento grande em jurere internacional, pelo VivaReal, um deles seria a escolha.
Os preços no AirBNB são mais atrativos mas variam mais diariamente do que os da VivaReal, na prática o melhor investimento precisa ser definido conforme a data da viagem para
ter os valores exatos.
Também, AirBNB possui muito mais quantidade de apartamentos, uma análise de apenas 300 é pequena.