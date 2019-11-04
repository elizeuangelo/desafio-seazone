"""
Este processo único fará o scraping do site da AirBNB

Ele começa buscando pelos quartos e a cada quarto encontrado já começa inserindo suas informações na tabela .csv,
a ideia é otimizar o tempo, uma vez que as requests não chegam ordenadamente

Observei que o Scrapy tem um exportador de CSV, não o utilizei porque não conhecia, pode ser bastante útil
no futuro
"""

from scrapy.crawler import CrawlerProcess
import scrapy, json, csv
import datetime
import configparser

# A leitura das configurações
config = configparser.ConfigParser()
config.read('config.cfg')
chave_api=config['DEFAULT']['api_key']
local = config['DEFAULT']['local']
quartos=int(config['DEFAULT']['quartos'])
hospedes=int(config['DEFAULT']['hospedes'])
busca=int(config['DEFAULT']['busca'])
prever_receita = int(config['DEFAULT']['previsao_receita'])

# Uma variável global, a data de hoje
hoje = datetime.date.today()

class AirBNB(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com.br']
    start_urls = ['http://www.airbnb.com.br']
    def start_requests(self):
        '''
        Optei por inserir os cookies da sessão diretamente na URL para poupar tempo e porque não havia necessidade
        de alterá-los. Não tenho certeza como a AirBNB processa vários destes cookies, mas acredito que não
        seja problema deixá-los como estão.
        '''
        global filewriter
        filewriter.writerow(['ID','RECEITA PREVISTA','PRECO MEDIO JAN','PRECO MEDIO FEV','PRECO MEDIO MAR','DISPO JAN','DISPO FEV','DISPO MAR'])
        url = ('https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true'
            '&client_session_id=1d2d36b5-50a2-4042-8ec1-dc66d8325018&currency=BRL'
            '&current_tab_id=home_tab&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true'
            '&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true'
            '&items_per_grid=50'
            f'&key={chave_api}&query={local}&adults={hospedes}&min_bedrooms={quartos}'
            '&locale=en&metadata_only=false&ne_lat=-27.42678520822947&ne_lng=-48.48762208061339'
            '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes'
            '&satori_version=1.1.9&screen_height=970&screen_size=large&screen_width=1588&search_by_map=true&search_type=unknown'
            '&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true'
            '&sw_lat=-27.454893278053465&sw_lng=-48.51461583213927&timezone_offset=-180&version=1.6.5&zoom=15')
        # O sistema requisita 50 itens por vez a cada request para obter ids de locais para aluguel,
        # Foi feito assim pois as respostas chegam em tempos diferentes e depois que foi alterado para este jeito não ouveram
        # problemas neste sentido.
        items_offset = 0
        while items_offset < busca:
            url2 = url+f'&items_offset={items_offset}'
            # Aqui são os primeiros requests para obtenção dos dados de página
            # Utilizamos a página https://www.airbnb.com.br/api/v2/ pois ela já vêm em json e sendo muito mais rápido o carregamento
            yield scrapy.Request(url=url2, callback=self.parse, cb_kwargs={'offset':items_offset})
            items_offset += 50

    def parse(self, response, offset):
        '''
        A resposta do request pelos locais de aluguel é processada aqui, primeiro lendo o json e depois criando novas
        requests, uma para cada local pesquisado
        '''
        data = json.loads(response.body)
        size = min(len(data.get('explore_tabs')[0].get('sections')[0].get('listings')),busca-offset)
        print(f'Lendo os items: {offset+1} - {offset+size}')
        rooms = [data.get('explore_tabs')[0].get('sections')[0].get('listings')[n].get('listing')['id'] for n in range(0,size)]
        url = f'https://www.airbnb.com.br/api/v2/homes_pdp_availability_calendar?currency=BRL&key={chave_api}&locale=pt&month={hoje.month}&year={hoje.year}&count={prever_receita}'
        for n in rooms:
            url2 = url+f'&listing_id={n}'
            yield scrapy.Request(url=url2, callback=self.parse_rooms, cb_kwargs={'room':n})
        
    def parse_rooms(self, response, room):
        '''
        A resposta da request dos locais individuais fica aqui
        Checamos as informações de preço e disponibilidade diretamente
        da página https://www.airbnb.com.br/api/v2/homes_pdp_availability_calendar
        pois as informações já vêm em json e prontas para o uso necessário.

        Utilizei listas ao invés de numpy porque o programa já é rápido e não são tantas
        informações para processar.
        '''
        global filewriter
        data = json.loads(response.body)
        dias = []
        disponibilidade = []
        preco = []
        for n in data.get('calendar_months'):
            for j in n.get('days'):
                a = datetime.datetime.strptime(j['date'],'%Y-%m-%d').date()
                if a > hoje:
                    dias += [a]
                    disponibilidade += [j['available']]
                    preco += [float(j.get('price')['local_price_formatted'][2:])]
        precos_booked = [(not disponibilidade[x])*preco[x] for x in range(len(dias))]
        receita = sum(precos_booked)
        janeiro = [(x>datetime.date(2019,12,31) and x<datetime.date(2020,2,1)) for x in dias]
        fevereiro = [(x>datetime.date(2020,1,31) and x<datetime.date(2020,3,1)) for x in dias]
        marco = [(x>datetime.date(2020,2,29) and x<datetime.date(2020,4,1)) for x in dias]
        preco_medio_jan = round(sum([janeiro[x]*preco[x]/sum(janeiro) for x in range(len(dias))]),2)
        preco_medio_fev = round(sum([fevereiro[x]*preco[x]/sum(fevereiro) for x in range(len(dias))]),2)
        preco_medio_mar = round(sum([marco[x]*preco[x]/sum(marco) for x in range(len(dias))]),2)
        dispon_jan = sum([disponibilidade[x]*janeiro[x] for x in range(len(dias))])
        dispon_fev = sum([disponibilidade[x]*fevereiro[x] for x in range(len(dias))])
        dispon_mar = sum([disponibilidade[x]*marco[x] for x in range(len(dias))])
        filewriter.writerow([room,receita,preco_medio_jan,preco_medio_fev,preco_medio_mar,dispon_jan,dispon_fev,dispon_mar])

c = CrawlerProcess({
    '''
    Aqui é o processo principal do Scrapy e onde as configurações do programa podem ser alteradas, basta adicionar a configuração desejada neste dicionário
    '''
    'USER_AGENT': 'Mozilla/5.0', 
    'LOG_ENABLED': False  
})
csv_file = open(f'leituras/airbnb {hoje.isoformat()}.csv','w',newline='',encoding='utf-8')
filewriter = csv.writer(csv_file,delimiter='\t',quotechar='|',quoting=csv.QUOTE_MINIMAL)
c.crawl(AirBNB)
print('Programa iniciado..\nLocal:',local)
c.start()
csv_file.close()
with open(f'leituras/airbnb {hoje.isoformat()}.csv',"r",encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file,delimiter = "\t")
    data = list(reader)
    row_count = len(data)-1
    print(f'Programa finalizado, arquivo "{csv_file.name}" criado. {row_count} locais da AirBNB processados.')