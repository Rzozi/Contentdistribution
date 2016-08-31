# ++++++++++++++++ API ++++++++++++++++
from flask import Flask, jsonify, request, redirect, Response, make_response, url_for, send_from_directory
import flask.ext.restless
import datetime 
import time
import requests
import ast
import json
import codecs
from json import dumps
from sortedcontainers import SortedList,SortedSet
# +++++++++++++++++ SQLALCHEMY +++++++++
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
from sqlalchemy import or_, Sequence 
import sqlite3 
# +++++++++++++++++ File Management ++++
import os
import sys
from werkzeug import secure_filename	
from paramiko import SSHClient
from scp import SCPClient
import paramiko
import pprint
import gzip
import zlib






# ++++ Where files are stored +++++

UPLOAD_FOLDER = "C:/Users/sony-vaio/Desktop/demo/uploads"

# ++++ API ++++++++++++++++++++++++

app = Flask(__name__)
#++++ Connection to Database ++++

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://loukili:passwd@192.168.1.30:5432/datab4'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)  



# ++++++ Adding visits info  ++++++++++++++++++++++++

def add_visit(file):
    vis = visits1()
    vis.name = file
    db.session.add(vis)
    db.session.commit()


# +++++ Predictor +++++++++++++++++++++++++++     


def WEMA(file,id):

    alpha = 0.8
    filename = file[0]
    current_time = datetime.datetime.now()
    
    five_minutes_ago = str(current_time - datetime.timedelta(minutes=30))
    
    req_last_five_min = db.session.query(V[id]).filter((V[id].date > five_minutes_ago),(V[id].name == filename)).count()
    a = req_last_five_min
    b = D[id].query.filter_by(name=filename).one()
    y = alpha*a + (1-alpha)*float(b.prediction)
    return y

# +++++ Module that increments number of Hits of a file ++++

def Increment_Hits(file):
    user = Content1.query.filter_by(name=file).all()
    user[0].Hits += 1
    db.session.commit()


# +++++ Topology discovery ++++


def close_cache(file):
    with open(file) as data_file:    
        data = json.load(data_file)
    mincost = 100000
    for i in range(0,len(data["topology"])):
     #node = data["topology"][i]["startpt"]
     if (mincost > data["topology"][i]["cost"]):
      mincost = data["topology"][i]["cost"]
      cachename = data["topology"][i]["finishpt"]
      address = data["topology"][i]["address"]
      continue
     else: continue

    return  (cachename,address)

# +++++ Copy visits information from Control-plane caches ++++


def get_visits():
   #sys.stdout = open('file', 'w')
   DB = "/home/loukili/Downloads/server/API/uploads/datab.db"
   conn = sqlite3.connect( DB ) 
   conn.row_factory = sqlite3.Row
   db = conn.cursor()
   
   rows = db.execute('''SELECT * FROM visits''').fetchall()
   conn.commit()
   conn.close() 
   return json.dumps( [dict(i) for i in rows] ) 
   #return rows1

# +++++ Content Hits count ++++


def count_hits():
   DB = "/home/loukili/Downloads/server/API/uploads/datab1.db"
   conn = sqlite3.connect( DB ) 
   #conn.row_factory = sqlite3.Row
   c = conn.cursor()
   c.execute("select name, count(name) from visits group by name")
   rows = c.fetchall()
  
   for i in range(0,len(rows)):
    rows[i] = list(rows[i])
    rows[i][0]=str(rows[i][0])
   return rows	



# ++++++ Database Models +++++++++++++++++++++++ 

class Router(db.Model):

  __tablename__ = 'Router'
  id = db.Column(db.Integer, Sequence('Router_id_seq', start=1, increment=1), primary_key=True)
  name = db.Column(db.String(20))
  type = db.Column(db.String(20))
  ports = db.relationship('ports', backref ='Belong to', lazy='dynamic')

class ports(db.Model):

  __tablename__ = 'ports'
  id = db.Column(db.Integer, Sequence('ports_id_seq', start=1, increment=1),primary_key=True)
  name = db.Column(db.String(20))
  type = db.Column(db.String(20))
  status = db.Column(db.String(20))
  Router_id = db.Column(db.Integer, db.ForeignKey('Router.id'))
  flux = db.relationship('flux' ,backref='Sent from ', lazy='dynamic')


class flux(db.Model):
  __tablename__ = 'flux'
  id = db.Column(db.Integer, Sequence('flux_id_seq', start=1, increment=1), primary_key=True)
  name = db.Column(db.String(20))
  type = db.Column(db.String(20))
  destination = db.Column(db.String(20))
  operation = db.Column(db.String(20))
  param = db.Column(db.Integer, db.ForeignKey('ports.id'))
  

     
class server(db.Model):
  __tablename__ = "server"
  id = db.Column(db.Integer, Sequence('Server_id_seq', start=1, increment=1), primary_key=True)
  name = db.Column(db.String(20))
  type = db.Column(db.String(20))
  content1 = db.relationship('content1', backref='served by', lazy='dynamic') 
  content2 = db.relationship('content2', backref='served by', lazy='dynamic')
  

class content1(db.Model):

  __tablename__ = 'content1'
  id = db.Column(db.Integer, Sequence('content1_id_seq', start=1, increment=1),primary_key=True)
  url = db.Column(db.String(120))
  name = db.Column(db.String(80))
  type = db.Column(db.String(20))
  Hits = db.Column(db.Integer)
  prediction = db.Column(db.Float)
  Server_id = db.Column(db.Integer, db.ForeignKey('server.id'))

  def serialize(self):
      return dict(id=self.id,
               url=self.url,
               name=self.name,
               type=self.type,
               Hits=self.Hits,
               Server_id=self.Server_id
               )

class content2(db.Model):

  __tablename__ = 'content2'
  id = db.Column(db.Integer, Sequence('content2_id_seq', start=1, increment=1), primary_key=True)
  url = db.Column(db.String(120))
  name = db.Column(db.String(80))
  type = db.Column(db.String(20))
  Hits = db.Column(db.Integer)
  prediction = db.Column(db.Float)
  Server_id = db.Column(db.Integer, db.ForeignKey('server.id'))

  def serialize(self):
      return dict(id=self.id,
               url=self.url,
               name=self.name,
               type=self.type,
               Hits=self.Hits,
               Server_id=self.Server_id
               )


class cache1(db.Model):

  __tablename__ = 'cache1'
  id = db.Column(db.Integer, Sequence('cache1_id_seq', start=1, increment=1), primary_key=True)
  name = db.Column(db.String(20))
  size = db.column(db.String(20))

  def serialize(self):
      return dict(id=self.id,
               name=self.name)

class cache2(db.Model):

  __tablename__ = 'cache2'
  id = db.Column(db.Integer, Sequence('cache2_id_seq', start=1, increment=1), primary_key=True)
  name = db.Column(db.String(20))
  size = db.column(db.String(20))

  def serialize(self):
      return dict(id=self.id,
               name=self.name)



class precache1(db.Model):

  __tablename__ = 'precache1'
  id = db.Column(db.Integer, Sequence('precache1_id_seq', start=1, increment=1), primary_key=True)
  name = db.Column(db.String(20))

class precache2(db.Model):

  __tablename__ = 'precache2'
  id = db.Column(db.Integer, Sequence('precache2_id_seq', start=1, increment=1), primary_key=True)
  name = db.Column(db.String(20))



class visits1(db.Model):

  __tablename__ = 'visits1'

    
  name = db.Column(db.String(20))
  date = db.Column(db.String(120), primary_key=True)


class visits2(db.Model):

  __tablename__ = 'visits2'

  id = db.Column(db.Integer, Sequence('visits2_id_seq', start=1, increment=1),primary_key=True)
  name = db.Column(db.String(20))
  date = db.Column(db.String(120))

class matching(db.Model):

  __tablename__ = 'matching'

  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(80))
  host = db.Column(db.String(80))
  ip_src = db.Column(db.String(80))



D = {}
V = {}
C = {}
P = {}
D[1] = content1
D[2] = content2
V[1] = visits1
V[2] = visits2
C[1] = cache1
C[2] = cache2
P[1] = precache1
P[2] = precache2


# +++++ Find most visited content ++++


@app.route('/api/controller/maxhits/', methods=['GET'])

def maxhits():
    sub1 = db.session.query(func.max(Content1.Hits).label('max_hit')).subquery()
    contenu1 = db.session.query(Content1).join(sub1, sub1.c.max_hit == Content1.Hits).first()
    return jsonify(contenu1.serialize()) 

# ++++++++++++ File download from the server ++++++++++++++++


@app.route('/api/uploads/<string:file>/', methods=['GET'])
def download(file):
      add_visit(file)
      Increment_Hits(file)
      if Cache1.query.filter_by(name = file).count() > 0:
        return redirect('http://192.168.214.129:5000%s' % url_for('download',file=file), code=302)
      elif Cache2.query.filter_by(name = file).count() > 0:  
        return redirect('http://192.168.182.132:5000%s' % url_for('download',file=file), code=302)
      else:
        return redirect('http://192.168.214.128:5000%s' % url_for('download',file=file), code=302)



# +++++++++ CONTENT POPULARITY PREDICTION ++++++++++++++++ 

@app.route('/api/controller/test/<int:redirect>', methods=['GET'])
def test(redirect):
  cache = db.session.query(C[redirect].name).all()  
  Condidat = SortedSet()
  catalogue = db.session.query(D[redirect].name).all() 
  k=10
  #return str(catalogue[99][0])
  for i in (catalogue):
    s = WEMA(i,redirect)
    if i in cache:
      s = s + k 

    filename=i[0]  
    Condidat.add((s,filename))
    cont = D[redirect].query.filter_by(name=filename).update(dict(prediction=s))  
    db.session.commit()
  Condidat1=reversed(Condidat)
  Condidat2= list(Condidat1)
  #visits1.query.delete()
  #Cache1.query.delete()  
  for i in Condidat2[0:20]:
    cach = P[redirect]()
    cach.name = i[1]
    db.session.add(cach)
    db.session.commit()
  cachedfiles = db.session.query(P[redirect].name).all() 
  return make_response(dumps(cachedfiles)) 
  
# +++++ Caching operation ++++

@app.route('/api/controller/caching', methods=['GET'])
def caching():

  p = db.session.query(precache1,precache2).filter(precache1.name == precache2.name).all()
  #return str(p[0].name)
  #q = db.session.query(p[0].name).first()
  r = db.session.query(precache1.name).all()
  s = db.session.query(precache2.name).all()
  t = db.session.query(cache1.name).all()
  v = db.session.query(cache2.name).all()
  q = []

  
  for i in p:
    q.append(i[0].name)

  for i in [r,s,t,v]:
    for j in range(0,len(i)): 
      i[j] = i[j][0]  

  
  cachename,address = close_cache('topology.json')

  if cachename == 'cache2': 
     query = v
     cache=cache2()
     source='192.168.1.23'	
  elif cachename == 'cache1': 
     query = t
     source='192.168.1.22'
     cache=cache1()


  if len(p) > 0:
   for i in q:
     
     if i not in query:

      url = 'http://%s:5000/api/cachedcontent' % address
      payload = '{"name":"%s","size":"20 kb"}' % i
      headers = {"Content-Type": "application/json"}
      req = requests.post(url, data=payload, headers=headers)
      cache = cache2()
      cache.name = i
      cache.size = '20 kb'
      db.session.add(cache)
      match = matching()
      match.name = i
      match.ip_src = source
      match.host = address
      db.session.add(match)		
      db.session.commit()      	

     else:

      print " File already in %s " % cachename

  for j in r:
    if j not in q and j not in t:
      url = 'http://192.168.1.26:5000/api/cachedcontent'
      payload = '{"name":"%s","size":"20 kb"}' % j 
      headers = {"Content-Type": "application/json"}
      req = requests.post(url, data=payload, headers=headers)
      cach = cache1()
      cach.name = j
      cach.size = '20 kb'
      db.session.add(cach)
      match = matching()
      match.name = j
      match.ip_src = '192.168.1.22'
      match.host = '192.168.1.26'
      db.session.add(match)
      db.session.commit()      	

      
    else:

      print " File already in %s " % cachename

  for k in s:
    if k not in q and k not in v:
      url = 'http://192.168.1.27:5000/api/cachedcontent'
      payload = '{"name":"%s","size":"20 kb"}' % k 
      headers = {"Content-Type": "application/json"}
      req = requests.post(url, data=payload, headers=headers)
      cach = cache2()
      cach.name = k
      cach.size = '20 kb'
      db.session.add(cach)
      match = matching()
      match.name = k
      match.ip_src = '192.168.1.23'
      match.host = '192.168.1.27'
      db.session.add(match)
      db.session.commit()      	

    else:

      print " File already in %s " % cachename



  return " Operation completed successfully "

  # ++++++ GENERATE FILE REQUESTS ++++++++++++++


@app.route('/api/controller/gener/<int:redirect>', methods=['GET','POST'])
def gener(redirect):

  r = requests.get('http://192.168.1.20:5000/gener/%d' %redirect)

  return " %s "% r.text


@app.route('/api/controller/gener', methods=['GET','POST'])
def gener1():
  seed = 123    # seed for random generation
  Lambda = 100    # rate of demands
  alpha = 1.1   # decay factor for Zipf
  N = 100     # catalog size
  NB_demands = 200  # number of demands
  demand = generate_demand(Lambda, alpha, N, NB_demands, seed)
  #return str(demand[2][1])
  timee = 0
  for i in demand:
    a = Content1.query.filter_by(id = i[1]) 
    #return str(a)
    filename = a[0].name
    time.sleep(i[0]-timee)
    #add_visit(filename)
    #Increment_Hits(filename)
    visit = visits1(name=filename)  
    db.session.add(visit)
    #db.session.commit()  
    a[0].Hits += 1
    

    timee = i[0]
  db.session.commit()   


  return " Requests sent successfully"
	
# +++++ Control plane caches copy, and main storage unit update ++++


@app.route('/api/copy1/<string:file>/', methods=['GET'])
def copy(file):
 ssh =  paramiko.SSHClient()
 #client = SSHClient()
 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 ssh.connect('192.168.1.21', username='loukili', password='LOUKILIahmed')
 #ssh.exec_command('python ~/script.py')
 

 #scpclient = SCPClient(ssh.get_transport(), socket_timeout=10)
 
 sftp = ssh.open_sftp()
 path1= '/home/loukili/Downloads/cherryproxy/cherryproxy/examples/%s' % file
 path2= '/home/loukili/Downloads/server/API/uploads/%s' % file
 #scpclient.get(path1,path2)
 sftp.get(path1,path2)
 sftp.close()
 ssh.close()
 #f1 = open('contentfile', 'w')
 f2 = open('visitsfile', 'w')
 #print >> f1,get_content()
 print >> f2,get_content()
 #f1.close()
 f2.close()
 #with open('contentfile') as data_file:
 #  data = json.load(data_file)
 #for i in range(0,len(data)):
 #  filename = data[i]["name"]
 #  filehits = data[i]["Hits"]
 #  if content1.query.filter_by(name=filename).count()>0:
 #    content = content1.query.filter_by(name=filename).first()
 #    content.Hits = content.Hits + filehits
 #    db.session.commit()
 #  else:
 #    newcontent = content1()
 #    newcontent.name = filename
 #    newcontent.Hits = filehits
 #    db.session.add(newcontent)
 with open('visitsfile') as data_file1:
   data1 = json.load(data_file1)
 for i in range(0,len(data1)):
   filename = data1[i]["name"]
   filevisit = data1[i]["date"]
   visit = visits1()
   visit.name = filename
   visit.date = filevisit
   db.session.add(visit)
   db.session.commit()
 filehits = count_hits()
 for i in range(0,len(filehits)):
   if content1.query.filter_by(name=filehits[i][0]).count()>0:
     content = content1.query.filter_by(name=filehits[i][0]).first()
     content.Hits = content.Hits + filehits[i][1]
     db.session.commit()
   else:
     newcontent = content1()
     newcontent.name = filehits[i][0]
     newcontent.Hits = filehits[i][1]
     db.session.add(newcontent)
     db.session.commit()
   
   
 return " Copied and converted successfully!"
 
db.create_all()


# +++++++++ API endpoints ++++++++++++++++++++++++++++++

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Router, methods=['GET', 'POST', 'DELETE','PUT'])
manager.create_api(ports, include_columns=['id','name','type','status','Router_id'] ,methods=['GET','POST','DELETE','PUT'])
manager.create_api(flux, include_columns=['id','destination','operation','param'] ,methods=['GET','POST','DELETE','PUT'])
manager.create_api(server, methods=['GET','POST','DELETE','PUT'])
manager.create_api(content2, include_columns=['id','name','type','url','Hits', 'prediction' ] , methods=['GET','POST','PUT','DELETE','COPY'])
manager.create_api(content1, include_columns=['id','name','type','url','Hits', 'prediction' ] , methods=['GET','POST','PUT','DELETE','COPY'])
manager.create_api(visits1, methods=['GET','POST','DELETE'])
manager.create_api(cache1, methods=['GET','POST','DELETE','PUT'])
manager.create_api(visits2, methods=['GET','POST','DELETE','PUT'])
manager.create_api(cache2, methods=['GET','POST','DELETE','PUT'])
manager.create_api(precache1, methods=['GET','POST','DELETE','PUT'])
manager.create_api(precache2, methods=['GET','POST','DELETE','PUT'])
manager.create_api(matching, methods=['GET','POST','DELETE','PUT'])






if __name__ == '__main__':

  #app.run(host='192.168.1.29')
  app.run(debug=True)
