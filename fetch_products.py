import time
import os
import re
import sys
import requests
import random
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import pymongo
from pymongo import MongoClient
from time import sleep
import urllib2
if sys.version_info[0] > 2:
    from http.cookiejar import LWPCookieJar
    from urllib.request import Request, urlopen
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from cookielib import LWPCookieJar
    from urllib import quote_plus
    from urllib2 import Request, urlopen
    from urlparse import urlparse, parse_qs
    
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

client= MongoClient('mongodb://localhost:27017/')
db=client.SME
collection=db.website


def get_page(url):
    request = Request(url)
    browse=random.randint(1,8)
    if browse==1:
		  request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    elif browse==2:		
		  request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    elif browse==3:		
		  request.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)')
    elif browse==4:		
		  request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1)')
    elif browse==5:		
		  request.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.1; AOLBuild 4334.5012; Windows NT 6.0; WOW64; Trident/5.0)')
    elif browse==6:		
		  request.add_header('User-Agent','Opera/9.27 (X11; Linux i686; U; en)')
    elif browse==7:		
		  request.add_header('User-Agent','Opera 9.4 (Windows NT 6.1; U; en)')
    elif browse==8:		
		  request.add_header('User-Agent','Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/417.9 (KHTML, like Gecko) NetNewsWire/2.0')
    cookie_jar.add_cookie_header(request)
    try:
			response = urlopen(request)
			cookie_jar.extract_cookies(response, request)
			html = response.read()
			response.close()
 			cookie_jar.save()
			return html
    except urllib2.HTTPError:
			html = 'no data'
			return html
			#return html = 'no data'
			
			
		
def product_fetch(url):
	sleep(1)
	#print 'website '+url
	query2 = quote_plus('site:'+url+' product')
	#url = 'https://www.google.com/search?hl=en&as_q=site%3Awww.sunilagro.in%2F+product&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=&as_occt=any&safe=images&as_filetype=&as_rights='
	url='https://www.google.com/search?hl=en&as_q='+query2+'&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=&as_occt=any&safe=images&as_filetype=&as_rights='
	#print url
	html=get_page(url)
	soup = BeautifulSoup(html ,'html.parser')
	l = soup.find('div',{'class':'g'})
	x = l.findAll('a',href=True)
	hi = x[0].get('href').split('&')
	hi2 = hi[0].split('=')
	print hi2[1]
# 	ll = soup.findAll('cite')
# 	url=ll[0].text
# 	for x in cite:
# 		print 'x val'+x+'/n'


# importing csv file #
columns = defaultdict(list)         # each value in each column is appended to a list
with open('company_master_data_upto_Mar_2015_Karnataka.csv') as f:
    reader = csv.DictReader(f)      # read rows into a dictionary format
    for row in reader:              # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items():   # go over each column name and value 
            columns[k].append(v)    # append the value into the appropriate list
                                    # based on column name k
              
row = (columns['COMPANY_NAME'])
row2 = (columns['CORPORATE_IDENTIFICATION_NUMBER'])
for x in range(3,15):
  cname = row[x]
  print cname
  if (x!=0):
    sleep(1)
    #query = urllib.quote(query)
    query = quote_plus(cname+' +website')
    
    url='https://www.google.com/search?hl=en&as_q='+query+'&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=&as_occt=any&safe=images&as_filetype=&as_rights='
    #r = requests.get('https://www.google.co.in/search?hl=en&as_q='+cname +'+website&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=&as_occt=any&safe=images&as_filetype=&as_rights=',  headers=headers)
    #print url
    html = get_page(url)
    if not html == 'no data':
			soup = BeautifulSoup(html ,'html.parser')
			#print(soup.prettify().encode('utf8'))
			#gfile2=open('anchors.txt','w')
			#gfile2.write(soup.prettify().encode('utf8'))
			#y=soup.find_all('p')
			#print y[0]
			#l = soup.findAll('div',{'class':"s"})
			l = soup.findAll('cite')
			url=l[0].text
			print url
			product_fetch(url)
			try:
				collection.insert({
				'_id' : row2[x] ,
				'website':l[0].text})
				
				
			except pymongo.errors.DuplicateKeyError:
				pass
			

			#print l[0].text
			time.sleep(1)
			#clear(0)

			#print soup.text.encode('utf8')

	
	
	
	
	
	
	
	