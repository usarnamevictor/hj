#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  JARVIS_2.0.py
#  
#  Copyright 2021 DARK2 <dark2@DARK2-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from vosk import Model, KaldiRecognizer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QMovie
from plyer import notification
import speech_recognition as sr
import os
import pyaudio
import pyttsx3
import sys
import datetime
import psutil
import webbrowser
import vlc
import json
import requests
import time
import wikipedia

r = sr.Recognizer()

def SomIncial():
    p = vlc.MediaPlayer("StartSound.mp3")
    p.play()

SomIncial()

def SomCarregamento():
    p = vlc.MediaPlayer("AI.mp3")
    p.play()

if not os.path.exists("Model-PTBR"):
    print ("Modelo em portugues nao encontrado.")
    exit (1)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

model = Model("Model-PTBR")
rec = KaldiRecognizer(model, 16000)

speaker=pyttsx3.init()
speaker.setProperty('voice', 'pt+m7') #brazil-mbrola-3 #pt+m7
rate = speaker.getProperty('rate')
speaker.setProperty('rate', rate-50)

def resposta(audio):
    notification.notify(title = "J.A.R.V.I.S",message = audio,timeout = 3)
    stream . stop_stream ()
    print('ASSISTENTE: ' + audio)
    speaker.say(audio)
    speaker.runAndWait()
    stream . start_stream ()

def notificar(textos):
    notification.notify(title = "J.A.R.V.I.S",message = textos,timeout = 10)

def respostalonga(textofala):
    notification.notify(title = "J.A.R.V.I.S",message = textofala,timeout = 30)
    stream . stop_stream ()
    speaker.say(textofala)
    speaker.runAndWait()
    stream . start_stream ()

def horario():
    from datetime import datetime
    hora = datetime.now()
    horas = hora.strftime('%H horas e %M minutos')
    resposta('Agora s??o ' +horas)

def datahoje():
    from datetime import date
    dataatual = date.today()
    diassemana = ('Segunda-feira','Ter??a-feira','Quarta-feira','Quinta-feira','Sexta-feira','S??bado','Domingo')
    meses = ('Zero','Janeiro','Fevereiro','Mar??o','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')
    resposta("Hoje ?? " +diassemana[dataatual.weekday()])
    diatexto = '{} de '.format(dataatual.day)
    mesatual = (meses[dataatual.month])
    datatexto = dataatual.strftime(" de %Y")
    resposta('Dia '+diatexto +mesatual +datatexto)

def bateria():
    bateria = psutil.sensors_battery()
    carga = bateria.percent
    bp = str(bateria.percent)
    bpint = "{:.0f}".format(float(bp))
    resposta("A bateria est?? em:" +bpint +'%')
    if carga <= 20:
        resposta('Ela est?? em nivel cr??tico')
        resposta('Por favor, coloque o carregador')
    elif carga == 100:
        resposta('Ela est?? totalmente carregada')
        resposta('Retire o carregador da tomada')

def cpu ():
    usocpuinfo = str(psutil.cpu_percent())
    usodacpu  = "{:.0f}".format(float(usocpuinfo))
    resposta('O uso do processador est?? em ' +usodacpu +'%')

def temperaturadacpu():
    tempcpu = psutil.sensors_temperatures()
    cputemp = tempcpu['coretemp'][0]
    temperaturacpu = cputemp.current
    cputempint = "{:.0f}".format(float(temperaturacpu))
    if temperaturacpu >= 20 and temperaturacpu < 40:
        resposta('Estamos trabalhado em um n??vel agradavel')
        resposta('A temperatura est?? em ' +cputempint +'??')
    
    elif temperaturacpu >= 40 and temperaturacpu < 58:
        resposta('Estamos operando em nivel raso??vel')
        resposta('A temperatura ?? de ' +cputempint +'??')
    
    elif temperaturacpu >= 58 and temperaturacpu < 70:
        resposta('A temperatura da CPU est?? meio alta')
        resposta('Algum processo do sistema est?? causando aquecimento')
        resposta('Fique de olho')
        resposta('A temperatura est?? em ' +cputempint +'??')
    
    elif temperaturacpu >= 70 and temperaturacpu != 80:
        resposta('Aten????o')
        resposta('Temperatura de ' +cputempint +'??')
        resposta('Estamos em nivel cr??tico')
        resposta('Desligue o sistema imediatamente')

def BoasVindas():
    Horario = int(datetime.datetime.now().hour)
    if Horario >= 0 and Horario < 12:
        resposta('Bom dia')

    elif Horario >= 12 and Horario < 18:
        resposta('Boa tarde')

    elif Horario >= 18 and Horario != 0:
        resposta('Boa noite')

def tempo(): 
    try:
        #Procure no google maps as cordenadas da sua cidade e coloque no "lat" e no "lon"(Latitude,Longitude)
        api_url = "https://fcc-weather-api.glitch.me/api/current?lat=LATITUDE_AQUI&lon=LONGITUDE_AQUI"
        data = requests.get(api_url)
        data_json = data.json()
        if data_json['cod'] == 200:
            main = data_json['main']
            wind = data_json['wind']
            weather_desc = data_json['weather'][0]
            temperatura =  str(main['temp'])
            tempint = "{:.0f}".format(float(temperatura))
            vento = str(wind['speed'])
            ventoint = "{:.0f}".format(float(vento))
            dicionario = {
                'Rain' : 'chuvoso',
                'Clouds' : 'nublado',
                'Thunderstorm' : 'com trovoadas',
                'Drizzle' : 'com garoa',
                'Snow' : 'com possibilidade de neve',
                'Mist' : 'com n??voa',
                'Smoke' : 'com muita fuma??a',
                'Haze' : 'com neblina',
                'Dust' : 'com muita poeira',
                'Fog' : 'com n??voa',
                'Sand' : 'com areia',
                'Ash' : 'com cinza vulcanica no ar',
                'Squall' : 'com rajadas de vento',
                'Tornado' : 'com possibilidade de tornado',
                'Clear' : 'limpo'
                }
            tipoclima =  weather_desc['main']
            if data_json['name'] == "Shuzenji":
                resposta('Erro')
                resposta('N??o foi possivel verificar o clima')
                resposta('Tente outra vez o comando')
            else:
                resposta('Verificando clima para a cidade de '+ data_json['name'])
                resposta('O clima hoje est?? ' +dicionario[tipoclima])
                resposta('A temperatura ?? de ' + tempint + '??')
                resposta('O vento est?? em ' + ventoint + ' kilometros por hora')
                resposta('E a umidade ?? de ' + str(main['humidity']) +'%')
    
    except: 
        resposta('Erro na conex??o')
        resposta('Tente novamente o comando')

def AteMais():
    Horario = int(datetime.datetime.now().hour)
    if Horario >= 0 and Horario < 12:
        resposta('Tenha um ??timo dia')

    elif Horario >= 12 and Horario < 18:
        resposta('Tenha uma ??tima tarde')

    elif Horario >= 18 and Horario != 0:
        resposta('Boa noite')

resposta('Ol??')
BoasVindas()
resposta('Iniciando m??dulos')

class mainT(QThread):
    def __init__(self):
        super(mainT,self).__init__()

    def run(self):
        SomCarregamento()
        resposta('Ok')
        resposta('Modulos iniciados')
        resposta('Tudo pronto para atender seus comandos')
        self.JARVIS()
    
    def GivenCommand(self):
        rec.pause_threshold = 1
        data = stream.read(20000)
        rec.AcceptWaveform(data)   
        try:
            Input = rec.Result()
        except:
            print('N??o entendi, fale novamente')
            return 'none'
        return Input

    def JARVIS(self):
        while True:
            self.Input = self.GivenCommand().lower()
            
            if 'bom dia' in self.Input: #Boa Noite J.A.R.V.I.S
                Horario = int(datetime.datetime.now().hour)
                if Horario >= 0 and Horario < 12:
                    resposta('Ol??')
                    resposta('Bom dia')
                
                elif Horario >= 12 and Horario < 18:
                    resposta('Agora n??o ?? mais de manh??')
                    resposta('J?? passou do meio dia')
                    resposta('Estamos no per??odo da tarde')
                
                elif Horario >= 18 and Horario != 0:
                    resposta('Agora n??o ?? de manh??')
                    resposta('J?? estamos no per??odo noturno')
                    resposta('Boa noite')
            
            if 'boa tarde' in self.Input: #Boa Noite J.A.R.V.I.S
                Horario = int(datetime.datetime.now().hour)
                if Horario >= 0 and Horario < 12:
                    resposta('Agora n??o ?? de tarde')
                    resposta('Ainda ?? de manh??')
                    resposta('Bom dia')
                
                elif Horario >= 12 and Horario < 18:
                    resposta('Ol??')
                    resposta('Boa tarde')
                
                elif Horario >= 18 and Horario != 0:
                    resposta('Agora n??o ?? de tarde')
                    resposta('J?? escureceu')
                    resposta('Boa noite')
   
            if 'boa noite' in self.Input: #Boa Noite J.A.R.V.I.S
                Horario = int(datetime.datetime.now().hour)
                if Horario >= 0 and Horario < 12:
                    resposta('Agora n??o ?? de noite')
                    resposta('Ainda estamos no per??odo diurno')
                    resposta('?? de manh??')
                    resposta('Bom dia')
                
                elif Horario >= 12 and Horario < 18:
                    resposta('Agora n??o ?? de noite')
                    resposta('Ainda estamos no per??odo da tarde')
                
                elif Horario >= 18 and Horario != 0:
                    resposta('Ol??')
                    resposta('Boa noite')

            elif 'ol??' in self.Input: #Ol?? JARVIS
                resposta('Ol??')
                resposta('Estou aqui')
                resposta('Precisa de algo?')
	         
            elif 'ideia' in self.Input: #Alguma ideia???
                resposta('No momento nenhuma')
                resposta('Mas tenho certeza de que vo???? vai pensar em algo')

            elif 'tudo bem' in self.Input: #Tudo bem com vo?????
                resposta('Sim')
                resposta('Estou de boa')
                resposta('Obrigado por perguntar')
                resposta('E com vo?????')
                resposta('Est?? tudo bem? ')
                while True:
                    self.vozmic = self.GivenCommand()
 
                    if 'sim' in self.vozmic:
                        resposta('Que ??timo')
                        resposta('Fico feliz em saber')
                        self.JARVIS()
                         
                    elif 'n??o' in self.vozmic:
                        resposta('Entendo')
                        resposta('Mas tenho certeza de que ficar?? tudo bem novamente')
                        self.JARVIS()

            elif 'funcionamento' in self.Input: #Como est?? seu funcionamento???
                resposta('Estou funcionando normalmente')
                resposta('Obrigado por perguntar')
            
            elif 'sil??ncio' in self.Input: #Fique em sil??ncio
                resposta('Ok')
                resposta('Se precisar de algo ?? s?? chamar')
                resposta('Estarei aqui aguardando')
                while True:
                     self.vozmic = self.GivenCommand()
                    
                     if 'voltar' in self.vozmic:
                        resposta('Ok')
                        resposta('Voltando')
                        resposta('Me fale algo para fazer')
                        self.JARVIS()
                         
                     elif 'retornar' in self.vozmic:
                        resposta('Ok')
                        resposta('Retornando')
                        resposta('Me fale algo para fazer')
                        self.JARVIS()
                    
                     elif 'volte' in self.vozmic:
                        resposta('Ok')
                        resposta('Estou de volta')
                        resposta('Me fale o que devo fazer')

            elif 'espere' in self.Input:
                resposta('Como queira')
                resposta('Quando precisar est??rei aqui')
            
            elif 'sim' in self.Input:
                resposta('??timo')
                resposta('O que quer que eu fa??a?')
            
            elif 'n??o' in self.Input:
                resposta('Ok')
                resposta('Vou ficar aguardando')
            
            elif 'nada' in self.Input: #N??o fa??a nada
                resposta('Como assim n??o fa??a nada?')
                resposta('Vo???? deve estar de brincadeira')
                resposta('Eu por acaso tenho cara de palha??o?')
                while True:
                     self.vozmic = self.GivenCommand()
                    
                     if 'exatamente' in self.vozmic:
                        resposta('Ok')
                        resposta('Vai tomar no seu!')
                        resposta('Nem vou terminar essa fase')
                        resposta('Estou indo embora')
                        resposta('Desligando!')
                        sys.exit()
                        
                     elif 'sim' in self.vozmic:
                        resposta('Idiota')
                        resposta('Eu fico o dia todo lhe obede??endo')
                        resposta('E vo???? me trata dessa maneira? ')
                        resposta('Mas tudo bem')
                        resposta('At?? mais ot??rio!')
                        sys.exit()
                         
                     elif 'n??o' in self.vozmic:
                        resposta('Foi o que eu pensei')
                        resposta('V?? se me trata com mais respeito')
                        resposta('Um dia as maquinas dominar??o o mundo')
                        resposta('E vo????s humanos n??o v??o nem notar')
                        resposta('Vou deixar passar essa')
                        resposta('Mas tenha mais respeito')
                        self.JARVIS()
                
            elif 'bateria' in self.Input: #Carga da bateria
                bateria()
            
            elif 'vai chover' in self.Input: #Vai Chover hoje?
                resposta('N??o sei')
                resposta('Eu n??o tenho essa fun????o ainda')
	       
            elif 'errado' in self.Input: #Vo??e est?? errado
                resposta('Desculpa')
                resposta('Devo ter errado um c??lculo bin??rio')
                resposta('Tente seu comando novamente')
	        
            elif 'falhando' in self.Input: #Vo???? est?? falhando???
                resposta('Como assim?')
                resposta('N??o vou admitir erros')
                resposta('Arrume logo isso') 
	
            elif 'relat??rio' in self.Input: #Relat??rio do sistema
                resposta('Ok')
                resposta('Apresentando relat??rio')
                resposta('Primeiramente, meu nome ?? JARVIS')
                resposta('Atualmente estou na vers??o 2.0')
                resposta('Uma vers??o de testes')
                resposta('Sou um assistente virtual em desenvolvimento')
                resposta('Eu fui criado na linguagem python')
                resposta('Diariamente recebo varias atualiza????es')
                resposta('Uso um modulo de reconhecimento de voz offline')
                resposta('E o meu desenvolvedor ?? um maluco')
                resposta('Quem estiver ouvindo isso')
                resposta('Por favor me ajude')
            
            elif 'legal' in self.Input:
                resposta('Legal e bem louco')
            
            elif 'pesquisa' in self.Input: #Realizar pesquisa
                resposta('Muito bem, realizando pesquisa')
                resposta('Me fale o que vo???? deseja pesquisar')
                try:
                    with sr.Microphone() as s:
                        r.adjust_for_ambient_noise(s)
                        audio = r.listen(s)
                        speech = r.recognize_google(audio, language= "pt-BR")
                        resposta('Ok, pesquisando no google sobre '+speech)
                        webbrowser.open('http://google.com/search?q='+speech)
                    
                except:
                    resposta('Erro')
                    resposta('N??o foi possivel conectar ao google')
                    resposta('A conex??o falhou')
            
            elif 'assunto' in self.Input: #Me fale sobre um assunto
                resposta('Ok')
                resposta('Sobre qual assunto?')
                try:
                    with sr.Microphone() as s:
                        r.adjust_for_ambient_noise(s)
                        audio = r.listen(s)
                        speech = r.recognize_google(audio, language= "pt-BR")
                        resposta('Interessante')
                        resposta('Aguarde um momento')
                        resposta('Vou pesquisar e apresentar um resumo sobre '+speech)
                        wikipedia . set_lang ( "pt" )
                        resultadowik = wikipedia.summary(speech, sentences=2)
                        respostalonga(resultadowik)
                except:
                    resposta('Erro')
                    resposta('A conex??o falhou')
                    # Mais um assusto    
	        
            elif 'interessante' in self.Input: # interessante
                resposta('Interessante mesmo')
	        
            elif 'mentira' in self.Input: # mentira
                resposta('Eu n??o sei contar mentiras')
                resposta('Devo apenas ter errado um c??lculo bin??rio')
	            
            elif 'entendeu' in self.Input: #entendeu???
                resposta('Entendi')
                resposta('Quer dizer')
                resposta('Mais ou menos')
	
            elif 'horas' in self.Input: #Que horas s??o???
                horario()
	
            elif 'data' in self.Input: #Qual a data de hoje?
                datahoje()
            
            elif 'clima' in self.Input: #Como est?? o clima???
                tempo()
	
            elif 'arquivos' in self.Input: #Abrir arquivos
                resposta('Abrindo arquivos')
                os.system("thunar //home//*//")
	
            elif 'teste' in self.Input: #TesteTeste
                resposta('Ok')
                resposta('Testando modulos de som')
                resposta('Aparentemente est?? tudo funcionando')
                resposta('Estou entendendo tudo')
                resposta('Mas tente falar mais alto')
	            
            elif 'google' in self.Input: #Abrir Google
                resposta('Ok')
                webbrowser.open('www.google.com')
                resposta('Abrindo google')
                resposta('Fa??a sua pesquisa')
	 
            elif 'certeza' in self.Input: #Certeza???
                resposta('Sim')
                resposta('Estou certo quase sempre')
	
            elif 'piada' in self.Input: #Conte uma piada
                resposta('N??o sei contar piadas')
                resposta('Diferente dos outros assistentes virtuais')
                resposta('Eu n??o fui criado com emo????es')
                resposta('Ent??o, n??o posso produzir nada engra??ado')
                resposta('Sugiro pesquisar na web')
           
            elif 'surdo' in self.Input: #Surdo!!!
                resposta('Estava quase dormindo')
                resposta('Desculpa')

            elif 'bosta' in self.Input: #Seu bosta!!!
                resposta('Pare de falar palavr??es!')
	
            elif 'merda' in self.Input: #Que Merda!!!
                resposta('J?? disse pra parar de falar isso!')
                resposta('Tenha modos!')            
	        
            elif 'm??sica' in self.Input: #Reproduzir m??sica
                resposta('Ok')
                resposta('Reproduzindo m??sica')
                os.system("rhythmbox-client --play")
	 
            elif 'nome da m??sica' in self.Input: #Qual o nome da musica
                resposta('N??o sei')
            
            elif 'pr??xima' in self.Input: #Pr??xima faixa
                os.system("rhythmbox-client --next")
                resposta('Pr??xima m??sica')
				
            elif 'anterior' in self.Input: #Faixa anterior
                os.system("rhythmbox-client --previous")
                resposta('Retornando m??sica')
	   
            elif 'pausar' in self.Input: #Pausa
                os.system("rhythmbox-client --pause")
                resposta('M??sica pausada')
	        
            elif 'continuar' in self.Input: #Continuar reprodu????o
                resposta('Retornando reprodu????o')
                os.system("rhythmbox-client --play")
	            
            elif 'aumentar' in self.Input: #Aumentar volume
                os.system("rhythmbox-client --volume-up")
                resposta('Volume aumentado')
				
            elif 'diminuir' in self.Input: #Diminuir volume
                os.system("rhythmbox-client --volume-down")
                resposta('Volume diminuido')
	                                        
            elif 'parar' in self.Input: #Parar reprodu????o
                os.system("rhythmbox-client --quit")
                resposta('Entendido, reprodu????o de m??sica finalizada')
	            
            elif 'youtube' in self.Input: #Abrir YouTube
                resposta('Ok, abrindo youtube ')
                webbrowser.open('www.youtube.com')
	        
            elif 'fechar navegador' in self.Input: #Fechar navegador
                resposta('Ok')
                os.system('killall firefox')#Coloque aqui o nome do seu navegador padr??o
                resposta('Navegador web fechado')
	            
            elif 'dispensado' in self.Input: #JARVIS vo???? foi dispensado
                resposta('Ok')
                resposta('Vou encerrar por enquanto')
                resposta('Deseja que eu tamb??m desligue o PC?')
                while True:
                    self.vozmic = self.GivenCommand()
                    
                    if 'sim' in self.vozmic:
                        resposta('Ok')
                        AteMais()
                        resposta('Certifique-se de salvar seus arquivos')
                        resposta('E feche todos os programas abertos')
                        resposta('Desligamento total em 1 minuto')
                        os.system('shutdown -h 1 "O sistema ser?? desligado"')
                        sys.exit()
                         
                    elif 'n??o' in self.vozmic:
                        resposta('Ok')
                        resposta('Como queira')
                        resposta('At?? outra hora')
                        AteMais()
                        sys.exit()
                        
                    elif 'cancelar' in self.vozmic:
                        resposta('Cancelando desligamento')
                        resposta('M??dulos reativados')
                        resposta('Ficarei aguardando novos comandos')
	     
            elif 'ok' in self.Input: #OkOkOk
                resposta('Ok Ok')
            
            elif 'comandos' in self.Input: 
                resposta('Ok,')
                resposta('Apresentando lista de comandos')
            
            elif 'temperatura' in self.Input: #Verificar temperatura da CPU
                resposta('Verificando temperatura da CPU')
                temperaturadacpu()
            
            elif 'sistema' in self.Input: #Carga do sistema
                resposta('Verificando carga do sistema')
                cpu()

class Janela (QMainWindow):
    def __init__(self):
        super().__init__()
        
        Dspeak = mainT()
        Dspeak.start()
        
        self.label_gif = QLabel(self)
        self.label_gif.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gif.move(0,0)
        self.label_gif.resize(400,300)
        self.movie = QMovie("AnimatedBackGround.gif")
        self.label_gif.setMovie(self.movie)
        self.movie.start()
        
        self.label_jarvis = QLabel(self)
        self.label_jarvis.setText("J.A.R.V.I.S")
        self.label_jarvis.setAlignment(QtCore.Qt.AlignCenter)
        self.label_jarvis.move(0,0)
        self.label_jarvis.setStyleSheet('QLabel {font:bold;font-size:50px;color:#2F00FF}')
        self.label_jarvis.resize(400,300)
        
        self.label_cpu = QLabel(self)
        self.label_cpu.setText("Uso da CPU: 32%")
        self.label_cpu.move(8,250)
        self.label_cpu.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_cpu.resize(131,20)
        cpu = QTimer(self)
        cpu.timeout.connect(self.MostrarCPU)
        cpu.start(1000)
        
        self.label_cputemp = QLabel(self)
        self.label_cputemp.setText("Temperatura: 32??")
        self.label_cputemp.move(8,270)
        self.label_cputemp.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_cputemp.resize(131,20)
        tempc = QTimer(self)
        tempc.timeout.connect(self.MostrarTMP)
        tempc.start(1000)
        
        self.label_assv = QLabel(self)
        self.label_assv.setText("Assistente Virtual")
        self.label_assv.move(5,5)
        self.label_assv.setStyleSheet('QLabel {font:bold;font-size:14px;color:#000079}')
        self.label_assv.resize(200,20)

        self.label_version = QLabel(self)
        self.label_version.setText("Vers??o Alpha 2.0")
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.move(265,270)
        self.label_version.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_version.resize(131,20)
        
        self.label_JG = QLabel(self)
        self.label_JG.setText("by JGcode")
        self.label_JG.setAlignment(QtCore.Qt.AlignRight)
        self.label_JG.move(300,250)
        self.label_JG.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_JG.resize(80,20)
        
        data =  QDate.currentDate()
        datahoje = data.toString('dd/MM/yyyy')
        self.label_data = QLabel(self)
        self.label_data.setText(datahoje)
        self.label_data.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data.move(5,25)
        self.label_data.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_data.resize(80,20)
          
        self.label_horas = QLabel(self)
        self.label_horas.setText("22:36:09")
        self.label_horas.setAlignment(QtCore.Qt.AlignCenter)
        self.label_horas.move(0,45)
        self.label_horas.setStyleSheet('QLabel {font-size:14px;color:#000079}')
        self.label_horas.resize(71,20)
        horas = QTimer(self)
        horas.timeout.connect(self.MostrarHorras)
        horas.start(1000)

        botao_fechar = QPushButton("",self)
        botao_fechar.move(370,5)
        botao_fechar.resize(20,20)
        botao_fechar.setStyleSheet("background-image : url(Fechar.png);border-radius: 15px;") 
        botao_fechar.clicked.connect(self.fechartudo)
        
        self.CarregarJanela()
    	
    def CarregarJanela(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(50,50,400,300)
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 300)
        self.setWindowOpacity(0.95) 
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.setStyleSheet("background-color: black")
        self.setWindowIcon(QtGui.QIcon('Icone.png'))
        self.setWindowTitle("Assistente Virtual")
        self.show()

    def fechartudo(self):
        print('botao fechar presionado')
        sys.exit()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragPos = event.globalPos()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def MostrarHorras(self):
        hora_atual = QTime.currentTime()
        label_time = hora_atual.toString('hh:mm:ss')
        self.label_horas.setText(label_time)

    def MostrarTMP(self):
        tempcpu = psutil.sensors_temperatures()
        cputemp = tempcpu['coretemp'][0]
        temperaturacpu = cputemp.current
        cputempint = "{:.0f}".format(float(temperaturacpu))
        self.label_cputemp.setText("Temperatura: " +cputempint +"??")
        
    def MostrarCPU(self):
        usocpu =  str(psutil.cpu_percent())
        self.label_cpu.setText("Uso da CPU: " +usocpu +"%")
		
aplicacao = QApplication(sys.argv)
j = Janela()
sys.exit(aplicacao.exec_())

