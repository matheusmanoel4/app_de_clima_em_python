import requests
import datetime
import json
import pytz
import pycountry_convert as pc



chave = '52841bddfe21e607f65a5551de9b7cb0'

apy_link = "http://api.openweathermap.org/data/2.5/forecast?id=524901&appid="
cidade = 'São Paulo'
apy_link = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(cidade, chave)    


## chamada 
response = requests.get(apy_link)

## convertendo em json
data = json.loads(response.text)

print(data)



### obejendo zona. pais e horas

pais_codigo = data['sys']['country']


zonas = pytz.country_timezones(pais_codigo)

pais = pytz.country_names[pais_codigo]

data_hora = pytz.timezone(zonas[0])
hora = datetime.datetime.now(data_hora)



#print('Hora:', hora.strftime(' %d/%m/%Y %H:%M:%S'))

tempo = data['main']['temp']
pressao = data['main']['pressure']
humidade = data['main']['humidity']
velocidade_vento = data['wind']['speed']
descriçao = data['weather'][0]['description']
print(tempo, pressao, humidade, velocidade_vento, descriçao)


# mudando informaçoes de pais para continente

def get_continent(pais):
    country_code = pc.country_name_to_country_alpha2(pais, cn_name_format="default")
    continent_name = pc.country_alpha2_to_continent_code(country_code)
    pais_continente_name = pc.convert_continent_code_to_continent_name(continent_name)
    return pais_continente_name

continente = get_continent(pais)

country_code = pc.country_name_to_country_alpha2(pais, cn_name_format="default")
print(country_code)
continent_name = pc.country_alpha2_to_continent_code(country_code)

