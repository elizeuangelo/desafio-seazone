# Análise de dados

## Objetivos

Utilizar os dados colhidos nas duas primeiras etapas para escolher três opções de apartamentos que sejam bons investimentos, explicar o porque da escolha.

## Considerações

Esta é uma análise bastante superficial dado os objetivos deste trabalho. Para uma análise mais aprofundada seria interessante colher o máximo de informações possíveis
de ambos os portais, especialmente o AirBNB que disponibiliza reviews e opiniões de usuários além dos bookings completos de cada dia. Notei alguns erros e padrões indicativos de erros nos dados vindos da AirBNB, seria interessante no futuro melhorar a coleta de dados do preco medio e previsao da receita, a fim de identificar cadastros errados e até mesmo desconsiderar comportamentos estranhos nos dados.

Dito isso, vamos aos resultados!

## Análise 1 - AirBNB

Carreguei os dados em csv da AirBNB e os plotei no pandas. A primeira coisa que me chamou a atenção foi o desvio padrão dos preços
e que cerca de 90% dos apartamentos estão com preço abaixo da média.

Com o foco em obter o apartamento que seja o melhor investimento decidi imediatamente nesta primeira análise em ir para uma abordagem financeira:
com foco nos três meses de análise *(jan-fev-mar)* minha intuição disse que os apartamentos com melhor custo benefício seriam os mais procurados, e focando apenas nos dados que coletamos, decidi dividir a receita dos próximos 6 meses pela média de preços de cada um destes meses.
Esta nova coluna revelou que alguns apartamentos estavam com valores desproporcionalmente superiores nesta relação receita/preco medio,
isso me chamou a atenção, no sentido que poderia haver algum problema com a previsão da receita. Investigando descobri que alguns apartamentos estavam com preços errados vindos da AirBNB (como alugueis diários de 100 mil reais), possivelmente algum erro cadastral do locador.
Também descobri que certas pessoas não alugam com regularidade os apartamentos, que possuiam discrepâncias muito grandes entre o valor *padrão* (não praticado) e o valor real nos dias em que a pessoa disponibilizava o apartamento, como a previsão foi dos 6 próximos meses, apartamentos *fechados* possuíam receitas altas. Notando que a previsão da receita não é um atributo muito confiável, parti para uma análise de preços médios mês a mês, usando a relação apenas como um comentário de 'nota'.

### Resultados

Pegando os 10 apartamentos com preços médios mais baratos para janeiro, notei que eles variam entre *R$ 220.00* e *R$ 350.00*. Avaliando a disponibilidade do mês de janeiro, escolhi entre aqueles apartamentos com disponibilidade maior que zero.

Com os dados em questão, cheguei a conclusão que um investimento bom para o mes de janeiro é o de id **28600926**, outro bom é o **21538493**.
Repetindo a mesma análise para fevereiro, dentre os com disponibilidade temos que dois bons apartamentos são **28600926** e **30169499**.
Repetindo para março: **28600926** e **22629043**, ambos com preços extremamente discrepantes com relação aos anteriores, mas parecem orgânicos e possuem disponibilidade.

## Análise 2 - VivaReal

Desta vez decidi estudar os dados da VivaReal e começar utilizando uma abordagem diferente, como colhi dados diversos decidi brincar com eles e fazer uma regresão linear para ver se tipo de local, andar, quartos, e a area util poderiam ser utilizadas como previsoras do valor dos apartamentos. Após limpar os dados, retirando apartamentos com dados faltantes e com valores claramente errados, fiz uma regressão linear para prever o preco e criei 2 colunas na tabela: uma dividindo a previsao pelo preco diario (demonstrando quanto cada real do preco cobrado vale de acordo com a previsao), e outra diminuindo a previsao pelo preco diario (demonstrando o lucro total ao alugar aquele apartamento).

Analisando o gráfico de resíduos logo vejo que o modelo de regressão linear não é perfeito para tarefa em questão, mas parece uma boa estimativa.

### Resultados

O id [**2450369092**](https://www.vivareal.com.br/imovel/apartamento-3-quartos-jurere-internacional-bairros-florianopolis-com-garagem-110m2-aluguel-RS300-id-2450369092/) em jurere internacional aparece como as oferta de melhor valor segundo a regressão, com 3 quartos por *R$ 300,00*. Os apartamentos [**2433096197**](https://www.vivareal.com.br/imovel/apartamento-3-quartos-jurere-internacional-bairros-florianopolis-com-garagem-94m2-venda-RS905000-id-2433096197/) e [**2456757054**](https://www.vivareal.com.br/imovel/apartamento-3-quartos-jurere-internacional-bairros-florianopolis-com-garagem-110m2-aluguel-RS300-id-2450369092/) aparecem empatados em seguida, ambos com preco de R$ 500.00, 3 quartos e area util similares (isso acontece porque a quantidade de quartos demonstraram serem fatores importantes para o regressor).
 
 Para dois quartos o apartamento [**85005128**](https://www.vivareal.com.br/imovel/apartamento-2-quartos-jurere-bairros-florianopolis-com-garagem-78m2-aluguel-RS240-id-85005128/) de jurere nacional aparece em primeiro lugar, um apto de 78 m2 por *R$ 240.00*.
