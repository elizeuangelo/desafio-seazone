"""
Este processo único fará o scraping do site da Viva Real

Ele começa buscando pelos apartamentos e a cada apartamento encontrado já começa inserindo suas informações na tabela .csv,
a ideia é otimizar o tempo, uma vez que as requests não chegam ordenadamente
"""

from scrapy.crawler import CrawlerProcess
import scrapy, json, csv
import datetime
import configparser

# A leitura das configurações
config = configparser.ConfigParser()
config.read('config.cfg')
filtros_ = config['DEFAULT']['filtros'].split(',')
quartos = int(config['DEFAULT']['quartos'])

# Algumas variáveis globais
hoje = datetime.date.today()
headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
            'Origin':'https://www.vivareal.com.br',
            'Referer':'https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/',
            'Sec-Fetch-Mode':'cors',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.107',
            'x-domain':'www.vivareal.com.br'}

# A leitura dos filtros
filtro_referencia = {
    'jurere' : 'addressCity=Florian%C3%B3polis&addressLocationId=BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EJurere&addressNeighborhood=Jurer%C3%AA&addressState=Santa%20Catarina&addressCountry=BR&addressStreet=&addressZone=Bairros&addressPointLat=-27.453543&addressPointLon=-48.511221',
    'jurere-internacional' : 'addressCity=Florian%C3%B3polis&addressLocationId=BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis%3EBarrios%3EJurere%20Internacional&addressNeighborhood=Jurer%C3%AA%20Internacional&addressState=Santa%20Catarina&addressCountry=BR&addressStreet=&addressZone=Bairros&addressPointLat=-27.598639&addressPointLon=-48.518722'
}
filtros = {}
for n in filtros_:
    filtros[n] = filtro_referencia[n]

class Apartamentos:
    '''
    As informações dos locais encontrados na pesquisa são salvas através desta classe
    Ela armazena nos atributos informações consideradas relevantes
    '''
    def __init__(self,listing):
        self.id = listing.get('id')
        self.tipo = listing.get('unitTypes')[0]
        self.bairro = listing.get('address')['neighborhood']
        self.andar = listing['unitFloor']
        self.quartos = listing.get('bedrooms')[0]
        try:
            self.areautil = listing.get('usableAreas')[0]
            self.area = listing.get('totalAreas')[0]
        except:
            self.areautil = 0
            self.area = 0
        financeiro = listing.get('pricingInfos')
        busca = -1
        for n in range(len(financeiro)):
            if financeiro[n]['businessType'] == 'RENTAL':
                if financeiro[n].get('rentalInfo')['period'] == 'DAILY':
                    busca = n
        if busca == -1:
            self.price = 'nan'
        else:
            financeiro = financeiro[busca]
            self.rent_type = financeiro.get('rentalInfo')['period']
            if self.rent_type == 'DAILY':
                price = float(financeiro['price'])
            elif self.rent_type == 'MONTHLY':
                price = float(financeiro.get('rentalInfo')['monthlyRentalTotalPrice'])/30
            self.price = round(price,2)

class VivaReal(scrapy.Spider):
    name = 'vivareal'
    allowed_domains = ['www.vivareal.com.br','glue-api.vivareal.com']
    start_urls = ['https://www.vivareal.com.br']

    def start_requests(self):
        '''
        Optei por inserir os cookies da sessão diretamente na URL para poupar tempo e porque não havia necessidade
        de alterá-los.
        '''
        global headers
        global filtros
        global quartos
        global fwriter
        fwriter.writerow(['ID','TIPO','BAIRRO','PRECO (diario)','TIPO DE ALUGUEL','ANDAR','QUARTOS','AREA UTIL (m2)','AREA TOTAL (m2)'])
        # Para cada filtro, para cada quantidade de quartos da mínima até 9, processa um novo request
        # Isso ocorre porque ao contrário do que o site indica, o 'mínimo de quartos' é a 'quantidade exata de quartos' da busca.
        for n in filtros:
            for j in range(quartos,9):
                url = f'https://glue-api.vivareal.com/v2/listings?{filtros[n]}&bedrooms={j}&business=RENTAL&facets=amenities&unitTypes=APARTMENT%2CAPARTMENT%2CAPARTMENT%2CAPARTMENT%2CRESIDENTIAL_BUILDING%2CHOME%2CHOME&unitSubTypes=UnitSubType_NONE%2CDUPLEX%2CLOFT%2CSTUDIO%2CTRIPLEX%7CFLAT%7CPENTHOUSE%7CKITNET%7CUnitSubType_NONE%7CUnitSubType_NONE%2CSINGLE_STOREY_HOUSE%2CVILLAGE_HOUSE%2CKITNET%7CCONDOMINIUM&unitTypesV3=APARTMENT%2CFLAT%2CPENTHOUSE%2CKITNET%2CRESIDENTIAL_BUILDING%2CHOME%2CCONDOMINIUM&usageTypes=RESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL&listingType=USED&parentId=null&categoryPage=RESULT&includeFields=page%2Csearch%2Cexpansion%2Cnearby%2CfullUriFragments%2Caccount%2Cfacets&size=100&from=0&q=&developmentsSize=5&__vt='
                yield scrapy.Request(url=url, callback=self.parse, headers=headers, cb_kwargs={'filtro':n,'key':filtros[n],'bedrooms':j})

    def parse(self, response, filtro, key, bedrooms):
        '''
        A resposta do request pelos locais de aluguel é processada aqui, lendo o json de cada request e
        criando uma linha na tabela csv
        '''
        global headers
        global quartos
        data = json.loads(response.body)
        total_count = data.get('page').get('uriPagination')['total']
        a = data.get('search').get('result').get('listings')
        count = len(a)
        if total_count > count:
            total_count = count
        print(f'Lendo as páginas de {filtro} com {bedrooms} quartos: {count} / {total_count}')
        if count < total_count:
            url = f'https://glue-api.vivareal.com/v2/listings?{key}&bedrooms={quartos}&business=RENTAL&facets=amenities&unitTypes=APARTMENT%2CAPARTMENT%2CAPARTMENT%2CAPARTMENT%2CRESIDENTIAL_BUILDING%2CHOME%2CHOME&unitSubTypes=UnitSubType_NONE%2CDUPLEX%2CLOFT%2CSTUDIO%2CTRIPLEX%7CFLAT%7CPENTHOUSE%7CKITNET%7CUnitSubType_NONE%7CUnitSubType_NONE%2CSINGLE_STOREY_HOUSE%2CVILLAGE_HOUSE%2CKITNET%7CCONDOMINIUM&unitTypesV3=APARTMENT%2CFLAT%2CPENTHOUSE%2CKITNET%2CRESIDENTIAL_BUILDING%2CHOME%2CCONDOMINIUM&usageTypes=RESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL&listingType=USED&parentId=null&categoryPage=RESULT&includeFields=page%2Csearch%2Cexpansion%2Cnearby%2CfullUriFragments%2Caccount%2Cfacets&size=100&from={count}&q=&developmentsSize=5&__vt='
            yield scrapy.Request(url=url, callback=self.parse, headers=headers, cb_kwargs={'filtro':filtro,'key':key})
        # Cria uma lista de apartamento com as informações de cada listing
        rooms = [Apartamentos(a[x].get('listing')) for x in range(len(a))]
        global fwriter
        # Se o preco de aluguel existir, escrever a linha na tabela
        # O preço é 'nan' quando não foi encontrado um preço de aluguel
        for n in rooms:
            if n.price != 'nan':
                fwriter.writerow([n.id,n.tipo,n.bairro,n.price,n.rent_type,n.andar,n.quartos,n.areautil,n.area])
        
c = CrawlerProcess({
    '''
    Aqui é o processo principal do Scrapy e onde as configurações do programa podem ser alteradas, basta adicionar a configuração desejada neste dicionário
    '''
    'USER_AGENT': 'Mozilla/5.0', 
    'LOG_ENABLED': False
})
f = open(f'leituras/vivareal {hoje.isoformat()}.csv','w',newline='', encoding='utf-8')
fwriter= csv.writer(f,delimiter='\t',quotechar='|',quoting=csv.QUOTE_MINIMAL)
c.crawl(VivaReal)
print('Programa iniciado..')
c.start()
f.close()
with open(f'leituras/vivareal {hoje.isoformat()}.csv',"r", encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file,delimiter = "\t")
    data = list(reader)
    row_count = len(data)-1
    print(f'Programa finalizado, arquivo "{csv_file.name}" criado. {row_count} locais da VivaReal processados.')