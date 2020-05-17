#!/usr/bin/env python
#!-*- coding: utf-8 -*-

import MySQLdb

def gravadb():
  hortadb.execute("INSERT INTO ENERGIA (fase1,fase2,neutro,ativado) VALUES(110,110,1,1)")
  hortadb.execute("INSERT INTO RELES (ativado,canteiro,usuario,RELE) VALUES(1,2,'USUARIO',4)")
  hortadb.execute("INSERT INTO SENSOR (tempext,umidadeext,orvalho,umidadesolo) VALUES(30,64,22,182)")
  horta.commit()  



horta=MySQLdb.connect(host="localhost",user="root",passwd="guto73",db="HORTA")
hortadb= horta.cursor()

gravadb()

hortadb.execute("SELECT * FROM ENERGIA")
energiadb=hortadb.fetchall()


hortadb.execute("SELECT * FROM RELES")
relesdb=hortadb.fetchall()


hortadb.execute("SELECT * FROM SENSOR")
sensordb=hortadb.fetchall()

print"---------------------"





horta.close

print energiadb
print relesdb
print sensordb



