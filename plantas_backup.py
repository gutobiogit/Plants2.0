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




from flask import Flask, render_template, redirect, url_for, request, session, abort , flash
import RPi.GPIO as GPIO
import datetime
import time
from xbee import XBee
import serial
import datetime
import time
import sys
import os
from os.path import join
import MySQLdb


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
DEST_ADDR_LONG = "\x00\x13\xa2\x00\x40\x2d\xde\x38"

GPIO.setmode(GPIO.BCM)
portas=(18,23,24,25,12,16,20,21)
GPIO.setup(portas,GPIO.OUT,initial=GPIO.HIGH)
" GPIO.output(portas,GPIO.LOW)"







app = Flask(__name__)

@app.route("/")			

def mestre():
 
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      plantas=MySQLdb.connect(host="localhost",user="root",passwd="guto73",db="HORTA")
      plantasdb=plantas.cursor()
      plantasdb.execute("SELECT tempext,umidadeext,orvalho,umidadesolo,DIA FROM SENSOR where DIA = (SELECT MAX(dia) FROM SENSOR)")
      sensordb=plantasdb.fetchall() 

      plantasdb.execute("SELECT RELE,ATIVADO FROM RELES WHERE DIA IN (SELECT MAX(DIA) FROM RELES GROUP BY RELE)")
      releativo=plantasdb.fetchall()
      plantas.close()

      now=datetime.datetime.now()
      timeString= now.strftime("%d/%m/%Y %H:%M")
      for res in releativo:
         exec ('sole%s=res[1]')%res[0]

      sole6 = 0#GPIO.input(portas[6])
      sole7 = GPIO.input(portas[7])
  
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



      templateData = {'title':'MENU','time':timeString,'sole0':sole0,'sole1':sole1,'sole2':sole2,'sole3':sole3,'sole4':sole4,'sole5':sole5,'sole6':sole6,'sole7':sole7,'potencia':potencia,'tempext':tempext,'umidadeext':umidadeext,'orvalhoext':orvalhoext,'umidadesolo':umidadesolo}
   

      return render_template('main.html',**templateData)

@app.route('/login', methods=['POST'])
def do_admin_login():
    global nome
    nome=request.form['username']
    senha=request.form['password']
    plantas=MySQLdb.connect(host="localhost",user="root",passwd="guto73",db="HORTA")
    plantasdb=plantas.cursor()
    plantasdb.execute("""SELECT * FROM USUARIO WHERE NAME="%s" AND PASSWORD="%s" """%(nome,senha))
    if plantasdb.rowcount:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    plantas.close()
    return mestre()

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
         GPIO.output(portas[pino],GPIO.LOW)
         gravadb(1,1,pino,nome,pino)
      if estado == "deslig":
         GPIO.output(portas[pino],GPIO.HIGH)       
         gravadb(1,0,pino,nome,pino)

      return redirect(url_for('mestre'))         


if __name__ == "__main__":
   app.secret_key = os.urandom(12)
   app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
