import sys, os
sys.path.append('../..')
import cherryproxy
import psycopg2
import httplib
import sqlite3
import datetime

#try:
#conn1 = sqlite3.connect('/home/loukili/Downloads/cherryproxy/cherryproxy/examples/datab1.db')
#except:
# print 'sqlite3 database not connected'

#c = conn1.cursor()

#c.execute('''CREATE TABLE content (name text, Hits real)''')
#c.execute('''CREATE TABLE visits (name text, date TIMESTAMP default CURRENT_TIMESTAMP NOT NULL)''')



try: 
 conn = psycopg2.connect("dbname='datab8' user='loukili' host='localhost' password='passwd'")
except:
 print " could not connect to db "


cur = conn.cursor()


cur.execute("SELECT name FROM matching;")
rows1 = cur.fetchall() 
#cur.execute("SELECT ip_src FROM matching;")
#rows2 = cur.fetchall()
#cur.execute("SELECT host FROM matching;")
for i in range(0,len(rows1)):
   rows1[i] = rows1[i][0]
#for i in range(0,len(rows2)):
#   rows2[i] = rows2[i][0]







class CherryProxy_redirect(cherryproxy.CherryProxy):
    def filter_request_headers(self):
	conn1 = sqlite3.connect('/home/loukili/Downloads/cherryproxy/cherryproxy/examples/datab1.db')
	c = conn1.cursor()
	c.execute("SELECT name FROM visits")
	rows2 = c.fetchall()
	for i in range(0,len(rows2)):
         rows2[i] = rows2[i][0]
	#now = datetime.datetime.now()
	print 'erre'
        # extract filename extension from URL:
        ext = os.path.basename(self.req.path)
	#print rows2[0]
	if str(ext) in rows2:
	 print 'uupdate'
	 c.execute("INSERT INTO visits(name,date) VALUES(?, ?)", (str(ext), datetime.datetime.now()))
	 conn1.commit()
	 #conn1.execute("UPDATE content SET Hits=Hits+1 WHERE name='%s';" % str(ext))
	 #conn1.commit()
	 
	 print 'ca passe'
	 
	elif (str(ext) not in rows2) or (rows2 is None)  :
	 print ' walo'
         try:
  
       	  conn1.execute("INSERT INTO visits(name,date) VALUES(?, ?)", (str(ext), datetime.datetime.now()))
	 except:	 
	  print 'mochkil'
	 conn1.commit()
	 #conn1.execute('insert into content values(?,?)', (str(ext),1))
	 #print ' why'
	 #conn1.commit()
	#sql_statment = "SELECT 1 FROM content1 WHERE content1.name ="&ext
	#cur.execute("Select ip_src FROM matching WHERE EXISTS ( SELECT 1 FROM content1 WHERE content1.name ='$ext');")
        if str(ext) in rows1:
            print ' in rows1'
	    cur.execute("SELECT ip_src, host FROM matching WHERE name ='%s' ;"% str(ext))
	    rows3 = cur.fetchall() 
	    
            #rows3[0] = rows3[0][0]
	    print rows3[0][1]
            self.req.netloc = rows3[0][1]+':5000'
	    self.req.source = rows3[0][0]
        elif str(ext) not in rows1:
	    self.req.netloc = '192.168.1.25:5000'
	    self.req.source = '192.168.1.24'
        #if str(ext) in rows2:
	 #   cur.execute("SELECT ip_src FROM matching WHERE cache='2';")
	
	  #  rows4 = cur.fetchall()
           # rows4[0] = rows4[0][0]
	    #print rows4
            #self.req.netloc = '192.168.1.27:5000'
	   # self.req.source = rows4[0]
	#elif str(ext) not in rows1 and str(ext) not in rows2:
	  #  cur.execute("SELECT ip_src FROM matching WHERE cache='0';")
	   	
           # rows3 = cur.fetchall()
            #rows3[0] = rows3[0][0]
	    #print rows3[0]
	    #self.req.netloc = '192.168.1.25:5000'
 	    #self.req.source = rows3[0]
	    
cherryproxy.main(CherryProxy_redirect)
