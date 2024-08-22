import tkinter
from tkinter import ttk, Frame, Entry, Button, Label, NW
import requests
import json
import pytz
import datetime
import pycountry_convert as pc
from PIL import Image, ImageTk

######### cores ###############
co0 = "#444466" # preta
co1 = "#feffff" # branca 
co2 = "#6f9bd1" # azul

fundo_dia = "#6cc4cc"
fundo_noite = "#484f60"
fundo_tarde = "#bfb86d"
fundo = fundo_dia

janela = tkinter.Tk()
janela.title("")
janela.geometry("320x350")
janela.configure(bg=fundo)

ttk.Separator(janela, orient="horizontal").grid(row=0, columnspan=1, ipadx=157)

def informacoess():
    chave = '52841bddfe21e607f65a5551de9b7cb0'
    cidade = e_local.get()
    apy_link = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(cidade, chave)    

    ## chamada 
    response = requests.get(apy_link)

    ## verificando se a resposta foi bem-sucedida
    if response.status_code == 200:
        ## convertendo em json
        data = json.loads(response.text)

        print(data)

        ### obtendo zona, país e horas
        pais_codigo = data['sys']['country']
        zonas = pytz.country_timezones(pais_codigo)
        pais = pytz.country_names[pais_codigo]
        data_hora = pytz.timezone(zonas[0])
        hora = datetime.datetime.now(data_hora)

        tempo = data['main']['temp']
        pressao = data['main']['pressure']
        humidade = data['main']['humidity']
        velocidade_vento = data['wind']['speed']
        descriçao = data['weather'][0]['description']
        print(tempo, pressao, humidade, velocidade_vento, descriçao)

        # mudando informações de país para continente
        def get_continent(pais):
            country_code = pc.country_name_to_country_alpha2(pais, cn_name_format="default")
            continent_name = pc.country_alpha2_to_continent_code(country_code)
            pais_continente_name = pc.convert_continent_code_to_continent_name(continent_name)
            return pais_continente_name
        
        ### passando informações para a tela
        l_cidade['text'] = cidade + '-' + pais + ' / ' + get_continent(pais)
        l_data['text'] = hora.strftime(' %d/%m/%Y %H:%M:%S')
        l_humidade['text'] = str(humidade) + '%' + '\n' + 'Temperatura: ' + str(tempo) + '°C'
        l_velocidade_vento['text'] = str(velocidade_vento) + ' m/s'
        l_pressao['text'] = 'Pressão : '+ str(pressao)
    else:
        print("Erro na chamada da API:", response.status_code, response.text)

# criando frames
frame_top = Frame(janela, width=320, height=50, bg=co1, pady=0, padx=0)
frame_top.grid(row=1, column=0)

frame_corpo = Frame(janela, width=320, height=300, bg=fundo, pady=12, padx=0)
frame_corpo.grid(row=2, column=0, sticky=NW)

ESTILO = ttk.Style(janela)
ESTILO.theme_use('clam')

# configuração frame_top
e_local = Entry(frame_top, width=20, justify="left", font=("Arial", 14), highlightthickness=1, relief="solid")
e_local.place(x=15, y=10)
b_local = Button(frame_top, command=informacoess, text="Ver clima", bg=co1, fg=co2, font=("Arial 9 bold"), highlightthickness=1, relief="solid")
b_local.place(x=250, y=10)

# frame corpo 
l_cidade = Label(frame_corpo, text="", bg=fundo, anchor='center', fg=co1, font=("Arial 12"))
l_cidade.place(x=10, y=4)

l_data = Label(frame_corpo, text="", bg=fundo, anchor='center', fg=co1, font=("Arial 10"))
l_data.place(x=10, y=54)

l_humidade = Label(frame_corpo, text="", bg=fundo, anchor='center', fg=co1, font=("Arial 45"))
l_humidade.place(x=10, y=100)

l_velocidade_vento = Label(frame_corpo, text="", bg=fundo, anchor='center', fg=co1, font=("Arial 14"))
l_velocidade_vento.place(x=15, y=212)

l_pressao = Label(frame_corpo, text="", bg=fundo, anchor='center', fg=co1, font=("Arial 10"))
l_pressao.place(x=10, y=184)

l_descricao = Label(frame_corpo, text="Nublado", bg=fundo, anchor='center', fg=co1, font=("Arial 10"))
l_descricao.place(x=10, y=212)

# Carregar e exibir a imagem
imagem = Image.open("imagens/sol2.png")
imagem = imagem.resize((130, 130))
imagem = ImageTk.PhotoImage(imagem)
label_imagem = Label(frame_corpo, image=imagem, bg=fundo)
label_imagem.image = imagem
label_imagem.place(x=160, y=50)


informacoess()

janela.mainloop()