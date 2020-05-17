#!/usr/bin/env python
#!-*- coding: utf-8 -*-


#PLANTAS
#+---------------+-------------+------+-----+-------------------+-----------------------------+
#| Field         | Type        | Null | Key | Default           | Extra                       |
#+---------------+-------------+------+-----+-------------------+-----------------------------+
#| id            | int(11)     | NO   | PRI | NULL              | auto_increment              |
#| temperatura   | smallint(6) | YES  |     | NULL              |                             |
#| umidade       | smallint(6) | YES  |     | NULL              |                             |
#| condensa      | smallint(6) | YES  |     | NULL              |                             |
#| umidadesolo   | smallint(6) | YES  |     | NULL              |                             |
#| luzmaeativa   | smallint(6) | YES  |     | NULL              |                             |
#| luzcloneativa | smallint(6) | YES  |     | NULL              |                             |
#| dia           | timestamp   | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
#+---------------+-------------+------+-----+-------------------+-----------------------------+

#USUARIO
#+----------+-------------+------+-----+---------+---------------------------------------+
#| Field    | Type        | Null | Key | Default | Extra                                 |
#+----------+-------------+------+-----+---------+---------------------------------------+
#| id       | int(11)     | NO   | PRI | NULL              | auto_increment              |
#| name     | varchar(20) | NO   |     | NULL              |                             |
#| password | varchar(20) | NO   |     | NULL              |                             |
#| Data     | timestamp   | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
#+----------+-------------+------+-----+-------------------+-----------------------------+

#PLANTAS
#+--------------------+-------------+------+-----+-------------------+-----------------------------+
#| Field              | Type        | Null | Key | Default           | Extra                       |
#+--------------------+-------------+------+-----+-------------------+-----------------------------+
#| num                | int(11)     | NO   | PRI | NULL              | auto_increment              |
#| ativa              | tinyint(1)  | NO   |     | NULL              |                             |
#| nome_ent           | varchar(30) | NO   |     | NULL              |                             |
#| nom_cien           | varchar(30) | NO   |     | NULL              |                             |
#| tipo_ent           | varchar(30) | NO   |     | NULL              |                             |
#| unidade            | varchar(30) | NO   |     | NULL              |                             |
#| data_colhe_verao   | varchar(30) | NO   |     | NULL              |                             |
#| data_colhe_inverno | varchar(30) | NO   |     | NULL              |                             |
#| distan_linha       | int(11)     | NO   |     | NULL              |                             |
#| distan_plant       | int(11)     | NO   |     | NULL              |                             |
#| mes_1              | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_2              | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_3              | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_4              | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_5              | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_6              | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_7              | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_8              | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_9              | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_10             | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_11             | tinyint(1)  | NO   |     | 0                 |                             |
#| mes_12             | tinyint(1)  | NO   |     | 0                 |                             |
#| consumo_agua       | tinyint(4)  | NO   |     | 0                 |                             |
#| DATA               | timestamp   | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
#+--------------------+-------------+------+-----+-------------------+-----------------------------+





from flask import Flask, render_template, redirect, url_for, request, session, abort , flash
#import RPi.GPIO as GPIO
import datetime
import time
from xbee import XBee
import serial
import sys
import os
from os.path import join
import MySQLdb
import urllib2
import json
import locale

reload(sys)  
sys.setdefaultencoding('utf8')
locale.setlocale(locale.LC_ALL,'pt_BR.utf8')


def gravadb(codigo=0, dados1=0, dados2=0, dados3=0, dados4=0, dados5=0, dados6=0):

  plantas=MySQLdb.connect(host="localhost",user="root",passwd="guto73",db="HORTA")
  plantasdb=plantas.cursor()
  if codigo == 0:
     plantasdb.execute("INSERT INTO ENERGIA (fase1,fase2,neutro,ativado) VALUES(%i,%i,%i,%i)"%(dados1, dados2, dados3, dados4))
  if codigo == 1:
     plantasdb.execute("INSERT INTO RELES (ativado,canteiro,usuario,RELE) VALUES(%i,%i,'%s',%i)"%(dados1, int(dados2+1), dados3, dados4))
  if codigo == 2:
     plantasdb.execute("INSERT INTO SENSOR (tempext,umidadeext,orvalho,umidadesolo) VALUES(%i,%i,%i,%i,%i,%i)"%(dados1, dados2, dados3, dados4,dados5,dados6))
  plantas.commit()  
  plantas.close()








def find_tty_usb(idVendor, idProduct):
    #find_tty_usb('067b', '2302') -> '/dev/ttyUSB0
    # Note: if searching for a lot of pairs, it would be much faster to search
    # for the enitre lot at once instead of going over all the usb devices
    # each time.
    for dnbase in os.listdir('/sys/bus/usb/devices'):
        dn = join('/sys/bus/usb/devices', dnbase)
        if not os.path.exists(join(dn, 'idVendor')):
            continue
        idv = open(join(dn, 'idVendor')).read().strip()
        if idv != idVendor:
            continue
        idp = open(join(dn, 'idProduct')).read().strip()
        if idp != idProduct:
            continue
        for subdir in os.listdir(dn):
            if subdir.startswith(dnbase+':'):
                for subsubdir in os.listdir(join(dn, subdir)):
                    if subsubdir.startswith('ttyUSB'):
                        return join('/dev', subsubdir)
           

    
    


#ser = serial.Serial(find_tty_usb('0403','6001'), 9600,rtscts=1)
#xbee = XBee(ser,escaped=True)
#DEST_ADDR_LONG = "\x00\x13\xa2\x00\x40\x2d\xde\x38"

#GPIO.setmode(GPIO.BCM)
#portas=(18,23,24,25,12,16,20,21)
#GPIO.setup(portas,GPIO.OUT,initial=GPIO.HIGH)
#" GPIO.output(portas,GPIO.LOW)"







app = Flask(__name__)

@app.route("/")			

def mestre():
 
   if not session.get('logged_in'):
      return render_template('login.html')
   else:

      temperatura_maxima = 30
      temperatura_minima = 4
      chuva = 8
      vento = 30
      umidade = 98
      plantas=MySQLdb.connect(host="localhost",user="root",passwd="guto73",db="HORTA")
      plantasdb=plantas.cursor()
      plantasdb.execute("SELECT tempext,umidadeext,orvalho,umidadesolo,DIA FROM SENSOR where DIA = (SELECT MAX(dia) FROM SENSOR)")
      sensordb=plantasdb.fetchall() 

      plantasdb.execute("SELECT RELE,ATIVADO FROM RELES WHERE DIA IN (SELECT MAX(DIA) FROM RELES GROUP BY RELE)")
      releativo=plantasdb.fetchall()
      plantas.close()



      parsed_json = json.loads(json_string)

      for x in range(4):

         data = parsed_json['forecast']['simpleforecast']['forecastday'][x]['date']['epoch']
         temp_max = parsed_json['forecast']['simpleforecast']['forecastday'][x]['high']['celsius']
         temp_min = parsed_json['forecast']['simpleforecast']['forecastday'][x]['low']['celsius']
         condicao = parsed_json['forecast']['simpleforecast']['forecastday'][x]['conditions']
         if condicao=="Mostly Cloudy":
            condicao="Predominantemente nublado"
         if condicao=="Chance of Rain":
            condicao="Chance de chuva"
         if condicao=="Partly Cloudy":
            condicao="Parcialmente nublado"
         if condicao=="Clear":
            condicao="Ceu Limpo"
         chuva_total = parsed_json['forecast']['simpleforecast']['forecastday'][x]['qpf_allday']['mm']
         chuva_dia = parsed_json['forecast']['simpleforecast']['forecastday'][x]['qpf_day']['mm']
         if chuva_dia==None:
            chuva_dia=0
         chuva_noite = parsed_json['forecast']['simpleforecast']['forecastday'][x]['qpf_night']['mm']
         vel_max_vento = parsed_json['forecast']['simpleforecast']['forecastday'][x]['maxwind']['kph']
         vel_media_vento = parsed_json['forecast']['simpleforecast']['forecastday'][x]['avewind']['kph']
         direcao_vento = parsed_json['forecast']['simpleforecast']['forecastday'][x]['avewind']['dir']
         grau_direcao_vento = parsed_json['forecast']['simpleforecast']['forecastday'][x]['avewind']['degrees']
         umidade_media = parsed_json['forecast']['simpleforecast']['forecastday'][x]['avehumidity']
         resultado="%s  -- temperatura maxima %sº , temperatura minima %sº, %s, com chuva total de %s mm (chuva de dia %s mm e chuva de noite %s mm), velocidade maxima de vento %s km/h (velocidade media %s km/h, direcao %s , %sº ) umidade media %s %%" % (datetime.datetime.fromtimestamp(float(data)).strftime('%A, %d %B de %Y'),temp_max, temp_min, condicao,chuva_total,chuva_dia,chuva_noite,vel_max_vento,vel_media_vento,direcao_vento,grau_direcao_vento,umidade_media)

         if x==0:
            cordia1="blue"  
            if int(temp_max) >= temperatura_maxima:
               cordia1 = "red"
            if int(temp_min) <= temperatura_minima:
               cordia1 = "red"
            if int(chuva_total) >= chuva:
               cordia1 = "red"
            if int(vel_max_vento) >= vento:
               cordia1 = "red"
            if int(umidade_media) >= umidade:
               cordia1 = "red"
            dia1 = resultado

         if x==1:
            cordia2="blue"
            if int(temp_max) >= temperatura_maxima:
               cordia2 = "red"
            if int(temp_min) <= temperatura_minima:
               cordia2 = "red"
            if int(chuva_total) >= chuva:
               cordia2 = "red"
            if int(vel_max_vento) >= vento:
               cordia2 = "red"
            if int(umidade_media) >= umidade:
               cordia2 = "red"
            dia2 = resultado

         if x==2:
            cordia3="blue"
            if int(temp_max) >= temperatura_maxima:
               cordia3 = "red"
            if int(temp_min) <= temperatura_minima:
               cordia3 = "red"
            if int(chuva_total) >= chuva:
               cordia3 = "red"
            if int(vel_max_vento) >= vento:
               cordia3 = "red"
            if int(umidade_media) >= umidade:
               cordia3 = "red"
            dia3 = resultado

         if x==3:
            cordia4="blue"
            if int(temp_max) >= temperatura_maxima:
               cordia4 = "red"
            if int(temp_min) <= temperatura_minima:
               cordia4 = "red"
            if int(chuva_total) >= chuva:
               cordia4 = "red"
            if int(vel_max_vento) >= vento:
               cordia4 = "red"
            if int(umidade_media) >= umidade:
               cordia4 = "red"
            dia4 = resultado

      now=datetime.datetime.now()
      timeString= now.strftime("%d/%m/%Y %H:%M")
      for res in releativo:
         exec ('sole%s=res[1]')%res[0]

      sole6 = 0#GPIO.input(portas[6])
      sole7 = 0# GPIO.input(portas[7])
  
      #xbee.remote_at(dest_addr_long=DEST_ADDR_LONG,command='D1',parameter='\x04')
      #time.sleep(5)
      #response = xbee.wait_read_frame()
  
    
      #xbee.remote_at(dest_addr_long=DEST_ADDR_LONG,command='D1',parameter='\x05')
    

      #resposta = response.get(r'rf_data')
      #resfinal = resposta.split(r',')
      #potencia = str(ord(response.get('rssi')))+" db"  
      #tempext = resfinal[1]
      #umidadeext = resfinal[0]
      #orvalhoext = resfinal[2]
      #umidadesolo = resfinal[3]
      potencia =60
      tempext=sensordb[0][0]
      umidadeext=sensordb[0][1]
      orvalhoext=sensordb[0][2]
      umidadesolo=sensordb[0][3]  



      templateData = {'title':'MENU','time':timeString,'sole0':sole0,'sole1':sole1,'sole2':sole2,'sole3':sole3,'sole4':sole4,'sole5':sole5,'sole6':sole6,'sole7':sole7,'potencia':potencia,'tempext':tempext,'umidadeext':umidadeext,'orvalhoext':orvalhoext,'umidadesolo':umidadesolo,'dia1':dia1,'dia2':dia2,'dia3':dia3,'dia4':dia4,'cordia1':cordia1,'cordia2':cordia2,'cordia3':cordia3,'cordia4':cordia4}
   

      return render_template('main.html',**templateData)

@app.route('/login', methods=['POST'])
def do_admin_login():
    global nome
    global json_string
    nome=request.form['username']
    senha=request.form['password']
    plantas=MySQLdb.connect(host="localhost",user="root",passwd="guto73",db="HORTA")
    plantasdb=plantas.cursor()
    plantasdb.execute("""SELECT * FROM USUARIO WHERE NAME="%s" AND PASSWORD="%s" """%(nome,senha))
    if plantasdb.rowcount:
        session['logged_in'] = True
        f = urllib2.urlopen('http://api.wunderground.com/api/e471ff28477f95b1/forecast/q/BRAZIL/Botucatu.json')
        json_string = f.read()
        f.close()
    else:
        flash('wrong password!')
    plantas.close()
    return mestre()

@app.route("/EntradaSemente")
def checagrava():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      return render_template('EntradaSemente.html')


@app.route("/EntradaSemente/incluirbd")
def incluibd():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      #entra_semente=MySQLdb.connect(host="localhost",user="root",passwd="guto73",db="HORTA")
      #entra_sementedb=entra_semente.cursor()
      #entra_sementedb.execute("SELECT tempext,umidadeext,orvalho,umidadesolo,DIA FROM SENSOR where DIA = (SELECT MAX(dia) FROM SENSOR)")
      #entra_sementeres=entra_sementedb.fetchall() 
      #entra_semente.close()
      nome=request.form['nome']
      nome_cien=request.form['nome-cien']
      colheita_verao=request.form['tempo_colheita_verao']
      colheita_inv=request.form['tempo_colheita_inv']
      tipo_planta=request.form['tipo']
      distancia_linha=request.form['dist_linha']
      distancia_planta=request.form['dist_planta']
      consumo_agua=request.form['consumo_agua']
      unidade=request.form['unidade']
      mes_1=request.form['janeiro']
      mes_2=request.form['fevereiro']
      mes_3=request.form['marco']
      mes_4=request.form['abril']
      mes_5=request.form['maio']
      mes_6=request.form['junho']
      mes_7=request.form['julho']
      mes_8=request.form['agosto']
      mes_9=request.form['setembro']
      mes_10=request.form['outubro']
      mes_11=request.form['novembro']
      mes_12=request.form['dezembro']
      ativo=request.form['ativo_sim']

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return mestre()

@app.route("/<pino>/<estado>")

def pinoestado(pino,estado):

   if not session.get('logged_in'):
      return render_template('login.html')
   else:
   
      pino=int(pino)

      if estado == "lig":
    #     GPIO.output(portas[pino],GPIO.LOW)
         gravadb(1,1,pino,nome,pino)
      if estado == "deslig":
    #     GPIO.output(portas[pino],GPIO.HIGH)       
         gravadb(1,0,pino,nome,pino)

      return redirect(url_for('mestre'))         


if __name__ == "__main__":
   app.secret_key = os.urandom(12)
   app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
