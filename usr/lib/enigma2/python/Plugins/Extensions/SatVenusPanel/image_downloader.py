import sys
import urllib, urllib2, re, os
from urllib import urlencode
from urllib2 import urlopen
from HTMLParser import HTMLParser

module_path = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/'
temppath = '/tmp/'

list2=[]

def readnet(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data
    except:
        return None

    return None

def gethostname(url):
    from urlparse import parse_qs, urlparse
    query = urlparse(url)
    return query.hostname

def main_cats():
            cats=[]
            cats.append(('VuPlus Images',''))
            cats.append(('Dream Multimedia Images',''))
            cats.append(('Xtrend Images',''))
            cats.append(('GigaBlue Images',''))
            cats.append(('Formuler Images',''))
            for cat in cats:
             print 'cat',cat
#             cats.sort()
             addDir(cat[0], cat[0], 100, cat[1], '', 1)

def getteams(name,url,page):
       if name=='Dream Multimedia Images':
          mode=102
          teams=[#('Demonisat Images', 'http://www.demonisat.info/demonisat-e2Img-OE2.0/', ''),
                 #('DreamMultimedia Images', 'http://www.dreamboxupdate.com/opendreambox/2.0.0/images/', ''),
                 #('Dream-Elite Images', 'http://images.dream-elite.net/DE4/index.php?dir=', ''),			 
                 #('Merlin3 Images', 'http://feed.merlin3.info/', ''),
                 ('NewNigma2 Images', 'http://feed.newnigma2.to/daily/', ''),
                 #('NonSoloSat Images', 'http://www.nonsolosat.net/upload/index.php?dir=Dreambox/', ''),		 
                 #('OoZooN Images', 'https://www.oozoon-download.de/opendreambox/images/', ''),
                 ('OpenATV Images', 'http://images.mynonpublic.com/openatv/6.3/index.php?open=', '')]
                 #('OpenESI Images', 'http://www.openesi.eu/images/Dreambox/', ''),
                 #('OpenPLi Images', 'https://openpli.org/download/dreambox/', ''),
                 #('Power-Sat Images', 'http://www.power-sat.org/power-plus/Powersat_2.0/', ''),
                 #('SatDreamGR Images', 'http://sgcpm.com/satdreamgr-images/dreambox/', ''),
                 #('TSimage Images', 'http://tunisia-dreambox.info/tsimage-feed/unstable/3.0/images/', '')]

       elif name=='VuPlus Images':#Check OpenSPA #Check OpenLD
           mode=103
           teams=[('BlackHole Images', 'http://178.63.156.75/VuPlusImages/BlackHole/vu', ''),#On VenusCS
                  ('Custom Build Images', 'http://178.63.156.75/VuPlusImages/Custom/', ''),#On VenusCS
                  ('OpenVuplus Images', 'http://code.vuplus.com/index.php?action=image&image=30&model=', ''),
#                  ('HDMU Images', 'http://www.hdmedia-universe.com/board/pages.php?pageid=1&box=vu', ''),
#                  ('OpenLD Images', 'https://www.odisealinux.com/Test/images/Vuplus/', ''),
                  ('OpenATV Images', 'http://images.mynonpublic.com/openatv/6.3/index.php?open=vu', ''),
                  ('OpenBlackHole Images', 'http://178.63.156.75/VuPlusImages/OpenBlackHole/vu', ''),#On VenusCS
#                  ('OpenBOX Images', 'http://www.fatima.sic.pt/imagenes/?dir=vuplus/vu', ''),
                  ('OpenDROID Images', 'http://images.opendroid.org/6.8/Vu+/vu', ''),
                  ('OpenESI Images', 'http://www.openesi.eu/images/Vu+/vu', ''),
                  ('OpenHDF Images', 'http://v64.hdfreaks.cc/vu', ''),
                  ('OpenPLi Images', 'https://openpli.org/download/vuplus/', ''),
#                  ('OpenPlus Images', 'http://images.open-plus.es/?dir=./', ''),
                  ('OpenSPA Images', 'https://openspa.webhop.info/Descarga%20de%20Im%C3%A1genes/Vuplus/vu', ''),
                  ('OpenTen Images', 'http://vuplus-images.spdns.eu/openten/latest-build/', ''),
                  ('OpenTr Images', 'http://178.63.156.75/VuPlusImages/OpenTr/vu', ''),#On VenusCS
                  ('OpenViX Images', 'http://www.openvix.co.uk/index.php/downloads/vu-plus-images/', ''),
                  ('OpenVision Images', 'https://openvision.tech/stb-images/vu', ''),
                  ('PKTeam Images', 'http://e2.pkteam.pl/IMAGE%20VU%2B/HYPERION%206.4/', ''),
                  ('PurE2 Images', 'http://pur-e2.club/OU/images/index.php?dir=6.2/', ''),
                  ('ruDREAM Images', 'http://178.63.156.75/VuPlusImages/ruDREAM/vu', ''),#On VenusCS
                  ('SatDreamGR Images', 'http://sgcpm.com/satdreamgr-images-6/vu/vu', ''),
#                  ('SFTeam Images', 'http://178.63.156.75/VuPlusImages/SFteam/vu', ''),#On VenusCS
                  ('VTi Images', 'http://178.63.156.75/VuPlusImages/VTi/vu', '')]#On VenusCS

       elif name=='Xtrend Images':
           mode=114
           teams=[('HDMU Images', 'http://www.hdmedia-universe.com/board/pages.php?pageid=1&box=', ''),
                  ('OpenATV Images', 'http://images.mynonpublic.com/openatv/6.3/index.php?open=', ''),
#                  ('OpenESI Images', 'http://www.openesi.eu/images/index.php?dir=Xtrend/', ''),
                  ('OpenHDF Images', 'http://v63.hdfreaks.cc/', ''),
                  ('OpenPLi Images', 'https://openpli.org/download/xtrend/', ''),
#                  ('OpenPlus Images', 'http://images.open-plus.es/?dir=', ''),				  
                  ('OpenViX Images', 'http://www.openvix.co.uk/index.php/downloads/xtrend-images/', ''),
                  ('SatDreamGR Images', 'http://sgcpm.com/satdreamgr-images-6/et/', '')]

       elif name=='GigaBlue Images':#Check OpenLD
           mode=116
           teams=[#('HDMU Images', 'http://www.hdmedia-universe.com/board/pages.php?pageid=1&box=', ''),
                  ('OpenNFR Images', 'http://dev.nachtfalke.biz/nfr/feeds/6.3/images/', ''),		   
#                  ('OpenLD Images', 'https://www.odisealinux.com/Test/', ''),
                  ('OpenATV Images', 'http://images.mynonpublic.com/openatv/6.3/index.php?open=', ''),
                  ('OpenDROID Images', 'http://images.opendroid.org/6.8/GigaBlue/', ''),
                  ('OpenESI Images', 'http://www.openesi.eu/images/index.php?dir=GigaBlue/', ''),
                  ('OpenHDF Images', 'http://v64.hdfreaks.cc/', ''),
#                  ('OpenPlus Images', 'http://images.open-plus.es/?dir=', ''),
                  ('OpenSPA Images', 'https://openspa.webhop.info/#Descarga%20de%20Im%C3%A1genes%2FGigaBlue/', ''),
                  ('OpenViX Images', 'http://www.openvix.co.uk/index.php/downloads/gigablue-images/',''),
                  ('PurE2 Images', 'http://pur-e2.club/OU/images/index.php?dir=6.2/', ''),
                  ('TeamBlue Images', 'http://images.teamblue.tech/6.3-release/index.php?open=','')]

       elif name=='Formuler Images':#Check OpenSPA
           mode=118
           teams=[#('HDMU Images', 'http://www.hdmedia-universe.com/board/pages.php?pageid=1&box=', ''),
                  ('OpenNFR Images', 'http://dev.nachtfalke.biz/nfr/feeds/6.3/images/', ''),		   
                  ('OpenATV Images', 'http://images.mynonpublic.com/openatv/6.3/index.php?open=', ''),
                  ('OpenDROID Images', 'http://images.opendroid.org/6.8/Formuler/', ''),
                  ('OpenHDF Images', 'http://v64.hdfreaks.cc/', ''),
                  ('OpenPLi Images', 'https://openpli.org/download/formuler/',''),
#                  ('OpenPlus Images', 'http://images.open-plus.es/?dir=', ''),
                  ('OpenSPA Images', 'https://openspa.webhop.info/#Descarga%20de%20Im%C3%A1genes%2FFormuler/', ''),
                  ('OpenViX Images', 'http://www.openvix.co.uk/index.php/downloads/forumler-images/',''),
                  ('PKTeam Images', 'http://e2.pkteam.pl/IMAGE%20FORMULER/', '')]

       for team in teams:
         teams.sort()
         addDir(team[0], team[1], mode, team[2], '', 1)
######################
######################
def formulermodels(name,url,page):
         if 'pkteam' in url:
            models = ['All_Models'
			]
         else:
          models =['formuler1',
                   'formuler3',
                   'formuler4',
                   'formuler4turbo']
         for model in models:
           print 'model',model
           href=url+model
           addDir(model, href,119, '','', 1)
######################
def extract_formulerimages(model,url,page):
    if 'openpli' in url: 
       if model=='formuler1':
        model='F1'
       if model=='formuler3':
        model='F3'
       if model=='formuler4':
        model='F4' 
       if model=='formuler4turbo':
        model='F4+Turbo'  			
       url='https://openpli.org/download/formuler/'+model
    if 'hdmedia' in url: 
       if model=='formuler1':
        model='FormulerF1'
       if model=='formuler3':
        model='FormulerF3'	
       url='http://www.hdmedia-universe.com/board/pages.php?pageid=1&box='+model
    if 'openatv' in url: 
       url='http://images.mynonpublic.com/openatv/6.3/index.php?open='+model
    if 'opendroid' in url: 	
        url='http://images.opendroid.org/6.8/Formuler/'+model	   
    if 'hdfreaks' in url: 
        url='http://v64.hdfreaks.cc/'+model		   
    if 'openvix' in url: 
       if model=='formuler1':
        model='formuler-1'
       if model=='formuler3':
        model='' 
       if model=='formuler4':
        model='' 
       if model=='formuler4turbo':
        model='formuler-f4-turbo' 		
       url='http://www.openvix.co.uk/index.php/downloads/forumler-images/'+model 
    if 'pkteam' in url: 			
       url='http://e2.pkteam.pl/IMAGE%20FORMULER/HYPERION%206.4/'
    if 'openspa' in url:
       if model=='formuler1':
        model='F1 '
       if model=='formuler3':
        model='F3 '
       if model=='formuler4':
        model='F4 ' 
       if model=='formuler4turbo':
        model='F4 turbo'
       print 'model',model
       url='https://openspa.webhop.info/#Descarga%20de%20Im%C3%A1genes%2FFormuler/'+model
    if 'nachtfalke' in url:
        url='http://dev.nachtfalke.biz/nfr/feeds/6.3/images/'+model
    if 'open-plus' in url:
        url='http://images.open-plus.es/?dir='+model
	   
    print "image_url",url		   
    data=readnet(url)    
    if data is None:
       print 'download error'
       return (False, 'Download error')
    url=url.lower()
    listdata=[]

    if 'open-plus' in url:	
       regx='''<a href="(.*?)" target="_parent" class="item _blank zip">\n\t\t\t\t\t\t\t\t\t\t\t\t(.*?)\t\t\t\t\t\t\t\t\t\t\t</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://images.open-plus.es/'+href
           listdata.append((name,href))
	
    if 'nachtfalke' in url:
     regx='''<td><a href=(.*?)" title="(.*?)">.*?</a></td>'''	
     images=re.findall(regx,data, re.M|re.I)
     print "images",images   
     for href,name in images:        
      print href
      href='http://dev.nachtfalke.biz/nfr/feeds/6.3/images/'+model+'/'+href			  
     listdata.append((name.strip(),href))
		   
    if 'openspa' in url:	
#     print "image_url",url   
     data=readnet('https://openspa.webhop.info/scan.php')
     listdata=[]#added this line
     import json
     jdata=json.loads(data)
     #print "name", jdata["items"][0]['name']
     info= jdata.get('items', {})
     teams=[]
     print "modelxx",model
     for item in info:
        modela=item['items']
        for item in modela:
            submodel=item['name']
            print "submode",submodel
            if not model.strip() in submodel:
               continue		   
            images=item['items']
            for image in images:
                image_name=image['name']
                image_path=image['path']
                #https://openspa.webhop.info/Descarga%20de%20Im%C3%A1genes/AZBox/AzboxHD
                image_path='https://openspa.webhop.info/'+image_path.replace(" ","%20")
                print 'image_name',image_name
                listdata.append((image_name,image_path.encode("utf-8")))
            listdata.reverse()#added - list it by newest

    if 'pkteam' in url: 	
     regx='''<a href="(.*?)">(.*?)</a>'''
     images=re.findall(regx,data, re.M|re.I)
     for name,href in images:
           if not '.zip' in name:
              continue
           href='http://e2.pkteam.pl/IMAGE%20FORMULER/HYPERION%206.4/'+name
           listdata.append((name,href))	
		   		
    if 'openvix' in url: 
       regx='''<.*?href="(.*?)" download="(.*?)".*?>'''
       images=re.findall(regx,data, re.M|re.I)
       print "images",images   
       for href,name in images:         
           print href           
           listdata.append((name.strip(),href))
       listdata.reverse()
	
    if 'hdfreaks' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:

           if not '.zip' in href:
              continue
           href='http://v64.hdfreaks.cc/'+model+'/'+href	  
           listdata.append((name.strip(),href))	
	
    if 'opendroid' in url: 	
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
              continue
           href='http://images.opendroid.org/6.8/Formuler/'+model+'/'+href	  
           listdata.append((name.strip(),href))		
	
    if 'hdmedia' in url: 
       regx='''<td class="list_files_table_file_link"><font color="#ff0000"><b>Flash Image: </b></font><a href="(.*?)">(.*?)</a></td>'''
       images=re.findall(regx,data, re.M|re.I)
       print "images",images   
       for href,name in images:         
           print href           
           listdata.append((name.strip(),href))

    if 'openatv' in url: 
       regx='''<a href='(.*?)'>(.*?)</a><br/>'''       
       images=re.findall(regx,data, re.M|re.I)
       print 'images',images
       for href,name in images:
           href='http://images.mynonpublic.com/openatv/6.3/'+href
           listdata.append((name.strip(),href)) 
		   
    if 'openpli' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not ".zip" in href:
              continue
           listdata.append((name.strip(),href))			   

    print 'listdata',listdata
    for item in listdata:
        addDir(item[0],item[1],10,'','',1,True)
    return True,listdata	
###################### 
######################       
def dreamboxmodels(name,url,page):
         if 'merlin3' in url:
            models = ['All_Models'
			]
         elif 'newnigma2' in url:
            models = ['All_Models'
			]
         elif 'nonsolosat' in url:
            models = ['All_Models'
			]
         elif 'power-sat' in url:
            models = ['All_Models'
			]
         else:
            models = ['dm500hd',
             'dm500hdv2',			
             'dm800se',
             'dm800sev2',
             'dm7020hd',			 
             'dm7020hdv2',
             'dm8000']
         for model in models:
           print 'model',model				 
           href=url+model  
           addDir(model, href,104, '','', 1)
######################				          		   
def extract_dreamboximages(model,url,page):
    if 'openpli' in url: 		
       if model=='dm500hd':
        model='DM500+HD'	
       if model=='dm800se':
        model='DM800+SE'	
       if model=='dm7020hd':
        model='DM7020+HD'		
       if model=='dm8000':
        model='DM8000'			
       url='https://openpli.org/download/dreambox/'+model	   
    if 'openatv' in url: 
       url='http://images.mynonpublic.com/openatv/6.3/index.php?open='+model 
    if 'openesi' in url: 
        url='http://www.openesi.eu/images/index.php?dir=Dreambox/'+model	
    if 'demonisat' in url: 
       if model=='dm500hd':
        model='DM%20500%20HD'	
       if model=='dm800se':
        model='DM%20800se%20HD'	
       if model=='dm7020hd':
        model='DM%207020%20HD'		
       if model=='dm7020hdv2':
        model='DM%207020%20HDv2'
       if model=='dm800sev2':
        model='DM%20800sev2%20HD'
       if model=='dm500hdv2':
        model='DM%20500HDv2'
       if model=='dm8000':
        model='DM%208000%20HD'		
       print 'model',model
       url='http://www.demonisat.info/demonisat-e2Img-OE2.0/'+model		
    if 'oozoon' in url: 
        url='https://www.oozoon-download.de/opendreambox/images/'+model
    if 'dreamboxupdate' in url: 
        url='http://www.dreamboxupdate.com/opendreambox/2.0.0/images/'+model		
    if 'tsimage' in url: 
        url='http://tunisia-dreambox.info/tsimage-feed/unstable/3.0/images/'+model
    if 'merlin3' in url: 			
       url='http://feed.merlin3.info/images/'
    if 'power-sat' in url: 	
       url='http://www.power-sat.org/power-plus/index.php?dir=Powersat_2.0/Immagini_OE_2.0_powersat/'
    if 'newnigma2' in url: 		
       url='http://feed.newnigma2.to/daily/images/'
    if 'dream-elite' in url: 
       if model=='dm500hd':
        model='DM500HD'
       if model=='dm800se':
        model='DM800SE'
       if model=='dm7020hd':
        model='DM7020HD'	
       if model=='dm7020hdv2':
        model='DM7020HDv2'
       if model=='dm800sev2':
        model='DM800SEv2'
       if model=='dm500hdv2':
        model='DM500HDv2'
       if model=='dm8000':
        model='DM8000'
       print 'model',model
       url='http://images.dream-elite.net/DE4/index.php?dir='+model	   
    if 'nonsolosat' in url:		
       url='http://www.nonsolosat.net/upload/index.php?dir=Dreambox/Nonsolosat%208.7/'
	   
    print 'image_url',url

    data=readnet(url)
    if data is None:
       return (False, 'Download error')
    url=url.lower()
    listdata=[]

    if 'nonsolosat' in url:
     regx='''<a class="autoindex_a" href="(.*?)">'''
     images=re.findall(regx,data, re.M|re.I)
     for href in images:
      try:href=href.split("file=")[1]
      except:continue
      name=href		   
      href='http://www.nonsolosat.net/upload/Image-Nonsolosat/Dreambox/Nonsolosat%208.7/'+href
      listdata.append((name.strip(),href))
	
    if 'dream-elite' in url:
       regx='''<a class="autoindex_a" href="(.*?)">'''
       images=re.findall(regx,data, re.M|re.I)
       for href in images:
           try:href=href.split("file=")[1]
           except:continue
           name=href
           href='http://images.dream-elite.net/DE4/'+model+"/"+href
           listdata.append((name.strip(),href))	
	
    if 'merlin3' in url: 
       regx='''<td><a href="(.*?)">(.*?)</a></td>'''	   
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.nfi' in href:
              continue           
           href='http://feed.merlin3.info/images/'+href
           listdata.append((name,href))
       listdata.reverse()
			
    if 'newnigma2' in url: 
       regx='''<td><a href="(.*?)">(.*?)</a></td>''' 	   
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.nfi' in href:
              continue           
           href='http://feed.newnigma2.to/daily/images/'+href
           listdata.append((name,href))		   
	
    if 'power-sat' in url: 
     regx='''<a class="autoindex_a" href="(.*?)">'''
     images=re.findall(regx,data, re.M|re.I)
     for href in images:
           if not '.zip' in href:
              continue		   
           try:href=href.split("file=")[1]
           except:continue
           name=href   
           href='http://www.power-sat.org/power-plus/Powersat_2.0/Immagini_OE_2.0_powersat/'+href
           listdata.append((name,href))
		   
    if 'tsimage' in url: 
       regx='''<li><a href="(.*?)">(.*?)</a></li>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.nfi' in href:
              continue           
           href='http://tunisia-dreambox.info/tsimage-feed/unstable/3.0/images/'+model+'/'+href
           listdata.append((name,href))
       listdata.reverse()
	   
    if 'dreamboxupdate' in url: 
       regx='''<a class="nfi" href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.nfi' in href:
              continue           
           href='http://www.dreamboxupdate.com/opendreambox/2.0.0/images/'+model+'/'+href
           listdata.append((name,href))
		   
    if 'oozoon' in url:  
       regx='''<td><a href="(.*?)">(.*?)</a></td>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.nfi' in href:
              continue           
           href='https://www.oozoon-download.de/opendreambox/images/'+model+'/'+href
           listdata.append((name,href))			   
       listdata.reverse()	
	   
    if 'demonisat' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://www.demonisat.info/demonisat-e2Img-OE2.0/'+model+'/'+href	  
           listdata.append((name.strip(),href))
       listdata.reverse()
			   
    if 'openesi' in url:
       regx='''<a class="autoindex_a" href="(.*?)">'''
       images=re.findall(regx,data, re.M|re.I)
       for href in images:
           try:href=href.split("file=")[1]
           except:continue
           name=href
           href='http://www.openesi.eu/images/Dreambox/'+model+'/'+href
           listdata.append((name.strip(),href))
       listdata.reverse()
			
    if 'satdreamgr' in url: 
       regx='''<li><a href="(.*?)">(.*?)</a></li>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if 'parent' in name.lower():
              continue           
           href='http://sgcpm.com/satdreamgr-images/dreambox/'+model+'/'+href
           listdata.append((name.strip(),href))
       listdata.reverse()
	   
    if 'openatv' in url: 
       regx='''<a href='(.*?)'>(.*?)</a><br/>'''       
       images=re.findall(regx,data, re.M|re.I)
       print 'images',images
       for href,name in images:
           href='http://images.mynonpublic.com/openatv/6.3/'+href
           listdata.append((name.strip(),href)) 
		   
    if 'openpli' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not ".zip" in href:
              continue
           listdata.append((name.strip(),href))		   
                 
    print 'listdata',listdata
    for item in listdata:
        addDir(item[0],item[1],10,'','',1,True)
    return True,listdata 
######################	
######################	   
def vuplusmodels(name,url,page):
#         if 'odisealinux' in url:
#            models = ['All_Models'
#			]
         if 'pkteam' in url:
            models = ['All_Models'
			]
         elif 'openten' in url:
            models = ['All_Models'
			]
         elif 'pur-e2' in url:
            models = ['All_Models'
			]
         elif 'Custom' in url:
            models = ['Build_By_Ten_Below'
			]
         else:
            models = ['zero',
             'uno',
             'solo',
             'solo2',
             'ultimo',
             'duo',
             'duo2',
             'solose',
             'solo4k',
             'zero4k',
             'uno4k',
             'uno4kse',
             'ultimo4k',
             'duo4k'
             ]            
         for model in models:
           print 'model',model
           href=url+model  
           addDir(model, href,105, '','', 1)  
######################	
def extract_vuplusimages(model,url,page):
    if 'openatv' in url: 
       url='http://images.mynonpublic.com/openatv/6.3/index.php?open=vu'+model 
    if 'openvix' in url:
       if model=='duo2':
        model='duo-2'
       if model=='solose':
        model='solo-se'
       if model=='solo2':
        model='solo-2'
       if model=='uno4kse':
        model='uno4k-se'
       if model=='zero4k':
        model='zero-4k'
       if model=='duo4k':
        model='duo-4k'
       url='http://www.openvix.co.uk/index.php/downloads/vu-plus-images/vu-'+model  
    if 'satdreamgr' in url: 
        url='http://sgcpm.com/satdreamgr-images-6/vu/vu'+model
    if 'openesi' in url: 
        url='http://www.openesi.eu/images/index.php?dir=Vu%2B/vu'+model
    if 'opendroid' in url: 
        url='http://images.opendroid.org/6.8/Vu+/vu'+model
    if 'openblackhole' in url: 
        url='http://178.63.156.75/VuPlusImages/OpenBlackHole/vu'+model
    if 'vti' in url:
        url='http://178.63.156.75/VuPlusImages/VTi/vu'+model
#    if 'sfteam' in url:
#        url='http://178.63.156.75/VuPlusImages/SFTeam/vu'+model
    if 'blackhole' in url:
        url='http://178.63.156.75/VuPlusImages/BlackHole/vu'+model
    if 'Custom' in url:
        print 'model',model
        url='http://178.63.156.75/VuPlusImages/Custom/'
    if 'opentr' in url:
        url='http://178.63.156.75/VuPlusImages/OpenTr/vu'+model
    if 'rudream' in url:
        url='http://178.63.156.75/VuPlusImages/ruDREAM/vu'+model
    if 'openvision' in url:
        url='https://openvision.tech/stb-images/vu'+model
    if 'hdfreaks' in url:
        url='http://v64.hdfreaks.cc/vu'+model
    if 'openpli' in url:
       if model=='uno':
        model='Uno'
       if model=='solo':
        model='Solo'
       if model=='solo2':
        model='Solo2'
       if model=='zero':
        model='Zero'
       if model=='ultimo':
        model='Ultimo'
       if model=='solose':
        model='Solo+SE'
       if model=='uno4k':
        model='Uno+4K'
       if model=='ultimo4k':
        model='Ultimo+4K'
       if model=='uno4kse':
        model='Uno+4K+SE'
       if model=='zero4k':
        model='Zero+4K'
       if model=='solo4k':
        model='Solo+4K'
       if model=='duo':
        model='Duo'
       if model=='duo2':
        model='Duo2'
       if model=='duo4k':
        model='Duo+4K'
       print 'model',model		
       url='https://openpli.org/download/vuplus/'+model
    if 'pkteam' in url:
       print 'model',model
       url='http://e2.pkteam.pl/IMAGE%20VU%2B/HYPERION%206.4/'
    if 'openten' in url:
       print 'model',model
       url='http://vuplus-images.spdns.eu/openten/latest-build/'
    if 'code.vuplus' in url:
       print 'model',model	
       if model=='duo':
        model='bm750'	
        url='http://code.vuplus.com/index.php?action=image&image=30&model='+model
       else:
        url='http://code.vuplus.com/index.php?action=image&image=30&model=vu'+model	   
#    if 'hdmedia' in url:    
#       url='http://www.hdmedia-universe.com/board/pages.php?pageid=1&box=vu'+model
#    if 'odisealinux' in url:
#       print 'model',model
#       url='https://www.odisealinux.com/Test/images/Vuplus/'
    if 'pur-e2' in url:
       print 'model',model
       url='http://pur-e2.club/OU/images/index.php?dir=6.2/vuplus/'
#    if 'open-plus' in url:
#        print 'model',model
#        url='http://images.open-plus.es/?dir=vu'+model
    if 'openspa' in url:
       if model=='uno':
        model='vuuno'
       if model=='solo':
        model='vusolo'
       if model=='solo2':
        model='vusolo2'
       if model=='zero':
        model='vuzero'
       if model=='ultimo':
        model='vuultimo'
       if model=='solose':
        model='vusolose'
       if model=='uno4k':
        model='vuuno4k'
       if model=='ultimo4k':
        model='vuultimo4k'
       if model=='uno4kse':
        model='vuuno4kse'
       if model=='zero4k':
        model='vuzero4k'
       if model=='solo4k':
        model='vusolo4k'
       if model=='duo':
        model='vuduo'
       if model=='duo2':
        model='vuduo2'
       print 'model',model
       url='https://openspa.webhop.info/#Descarga%20de%20Im%C3%A1genes/Vuplus/'+model
#    if 'fatima' in url:
#       print 'model',model
#       url='http://www.fatima.sic.pt/imagenes/?dir=vuplus/vu'+model

    print "image_url",url
    data=readnet(url)
    if data is None:
       print 'download error'
       return (False, 'Download error')
    url=url.lower()
    listdata=[]

    if 'custom' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://178.63.156.75/VuPlusImages/Custom/'+href	  
           listdata.append((name.strip(),href))

#    if 'fatima' in url:	
#     regx='''<a href="(.*?)" class="clearfix" data-name="(.*?)">'''       
#     images=re.findall(regx,data, re.M|re.I)
#     print 'images',images
#     for href,name in images:
#        if not '.zip' in href:
#         continue
#        href='http://www.fatima.sic.pt/imagenes/'+href
#        listdata.append((name.strip(),href)) 
#    listdata.reverse()

    if 'openspa' in url:	
     print "image_url",url   
     data=readnet('https://openspa.webhop.info/scan.php')
     if data is None:
       print "download error"
       return (False, 'Download error')
     listdata=[]#added this line
     import json
     jdata=json.loads(data)
     #print "name", jdata["items"][0]['name']
     info= jdata.get('items', {})
     teams=[]
     print "modelxx",model
     for item in info:
        modela=item['items']
        for item in modela:
            submodel=item['name']
            print "submode",submodel
            if not model.strip() in submodel:
               continue			   
            images=item['items']
            for image in images:
                image_name=image['name']
                image_path=image['path']
                #https://openspa.webhop.info/Descarga%20de%20Im%C3%A1genes/AZBox/AzboxHD
                image_path='https://openspa.webhop.info/'+image_path.replace(" ","%20")
                print 'image_name',image_name
                listdata.append((image_name,image_path.encode("utf-8")))
            listdata.reverse()#added - list it by newest

#    if 'open-plus' in url:
#       regx='''<a href="(.*?)" target="_parent" class="item _blank zip">\n\t\t\t\t\t\t\t\t\t\t\t\t(.*?)\t\t\t\t\t\t\t\t\t\t\t</a>'''
#       images=re.findall(regx,data, re.M|re.I)
#       for href,name in images:
#           if not '.zip' in href:
#              continue
#           href='http://images.open-plus.es/'+href
#           listdata.append((name,href))			   

    if 'pur-e2' in url:
       regx='''<a class="autoindex_a" href="(.*?)">'''
       images=re.findall(regx,data, re.M|re.I)
       for href in images:
           try:href=href.split("file=")[1]
           except:continue
           name=href
           href='http://pur-e2.club/OU/images/6.2/vuplus/'+href
           listdata.append((name.strip(),href))		   
       listdata.reverse()
       
#    if 'sfteam' in url: 
#       regx='''<a href="(.*?)">(.*?)</a>'''
#       images=re.findall(regx,data, re.M|re.I)
#       for href,name in images:
#           if not '.zip' in href:
#              continue
#           href='http://178.63.156.75/VuPlusImages/SFTeam/vu'+model+'/'+href
#           listdata.append((name.strip(),href))

#    if 'odisealinux' in url: 
#     regx='''<td><a href='(.*?)' class='name'>(.*?)</a></td>'''	
#     images=re.findall(regx,data, re.M|re.I)
#     for href,name in images:
##           if not '.zip' in href:
#           if not '.zip' in name:
#              continue
##           href='https://www.odisealinux.com/Test/images/Vuplus/'+href
#           href='https://www.odisealinux.com/Test/images/Vuplus/'+name
#           listdata.append((name.strip(),href))

#    if 'hdmedia' in url: 
#       regx='''<td class="list_files_table_file_link"><font color="#ff0000"><b>Flash Image: </b></font><a href="(.*?)">(.*?)</a></td>'''
#       images=re.findall(regx,data, re.M|re.I)
#       print "images",images   
#       for href,name in images:        
#           print href           
#           listdata.append((name.strip(),href))

    if 'code.vuplus' in url: 
       regx='''<tr><td><a href="(.*?)" rel="external">(.*?)</a></td></tr>'''
       images=re.findall(regx,data, re.M|re.I)
       print 'images',images
       for href,name in images:
           href='http://code.vuplus.com'+href
           listdata.append((name.strip(),href))

    if 'pkteam' in url: 
     regx='''<a href="(.*?)">(.*?)</a>'''
     images=re.findall(regx,data, re.M|re.I)
     for name,href in images:
           if not '.zip' in name:
              continue
           href='http://e2.pkteam.pl/IMAGE%20VU%2B/HYPERION%206.4/'+name
           listdata.append((name.strip(),href))
           
    if 'openten' in url: 
     regx='''<a href="(.*?)">(.*?)</a>'''
     images=re.findall(regx,data, re.M|re.I)
     for name,href in images:
           if not '.zip' in name:
              continue
           href='http://vuplus-images.spdns.eu/openten/latest-build/'+name
           listdata.append((name.strip(),href))

    if 'openvision' in url: 
     regx='''<a href="(.*?)">(.*?)</a>'''
     images=re.findall(regx,data, re.M|re.I)
     for name,href in images:
           if not '.zip' in name:
              continue
           href='https://openvision.tech/stb-images/vu'+model+'/'+name
           listdata.append((name.strip(),href))

    if 'openpli' in url:
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           listdata.append((name.strip(),href))

    if 'hdfreaks' in url:
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://v64.hdfreaks.cc/vu'+model+'/'+href	  
           listdata.append((name.strip(),href))
		   
    if 'rudream' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://178.63.156.75/VuPlusImages/ruDREAM/vu'+model+'/'+href	  
           listdata.append((name.strip(),href))		   
		   		   
    if 'opendroid' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
              continue
           href='http://images.opendroid.org/6.8/Vu+/vu'+model+'/'+href	  
           listdata.append((name.strip(),href))		    
    		   		   
    if 'satdreamgr' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://sgcpm.com/satdreamgr-images-6/vu/vu'+model+'/'+href
           listdata.append((name.strip(),href))   
#       listdata.reverse()    

    if 'openesi' in url:
       regx='''<a class="autoindex_a" href="(.*?)">'''
       images=re.findall(regx,data, re.M|re.I)
       for href in images:
           try:href=href.split("file=")[1]
           except:continue
           name=href
           href='http://www.openesi.eu/images/Vu%2B/vu'+model+'/'+href
           listdata.append((name.strip(),href))
       listdata.reverse()
		   
    if 'openblackhole' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://178.63.156.75/VuPlusImages/OpenBlackHole/vu'+model+'/'+href	  
           listdata.append((name.strip(),href))		   	   

    if 'vti' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://178.63.156.75/VuPlusImages/VTi/vu'+model+'/'+href	  
           listdata.append((name.strip(),href))
           
    if 'opentr' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://178.63.156.75/VuPlusImages/OpenTr/vu'+model+'/'+href		  
           listdata.append((name.strip(),href))

    if 'blackhole' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://178.63.156.75/VuPlusImages/BlackHole/vu'+model+'/'+href	  
           listdata.append((name.strip(),href))
		   
    if 'openatv' in url: 
       regx='''<a href='(.*?)'>(.*?)</a><br/>'''       
       images=re.findall(regx,data, re.M|re.I)
       print 'images',images
       for href,name in images:
           href='http://images.mynonpublic.com/openatv/6.3/'+href
           listdata.append((name.strip(),href)) 
		   	   
    if 'openvix' in url: 
       regx='''<.*?href="(.*?)" download="(.*?)".*?>'''
       images=re.findall(regx,data, re.M|re.I)
       print "images",images   
       for href,name in images:        
           print href           
           listdata.append((name.strip(),href))
       listdata.reverse()
       
    print 'listdata',listdata
    for item in listdata:
        addDir(item[0],item[1],10,'','',1,True)
    return True,listdata 
######################
###################### 
def xtrendmodels(name,url,page):
          models =['ET4x00',
                   'ET5x00',
                   'ET6x00',
                   'ET7x00',
                   'ET8x00',
                   'ET8500',				   
                   'ET9x00',
                   'ET10000']            
          for model in models:
                print 'model',model
                href=url+model  
                addDir(model, href,115, '','', 1)  
######################
def extract_xtrendimages(model,url,page):
    if 'openatv' in url: 
       url='http://images.mynonpublic.com/openatv/6.3/index.php?open='+model.lower()
    if 'openvix' in url: 
       if model=='ET4x00':
        model='et4x00'    
        url='http://www.openvix.co.uk/index.php/downloads/xtrend-images/xtrend-'+model+'-images/'
       if model=='ET5x00':
        model='et-5x00'    
        url='http://www.openvix.co.uk/index.php/downloads/xtrend-images/xtrend-'+model+'-images/'
       if model=='ET6x00':
        model='et6x00'    
        url='http://www.openvix.co.uk/index.php/downloads/xtrend-images/xtrend-'+model+'-images/'
       if model=='ET7x00':
        model='et-7x00'    
        url='http://www.openvix.co.uk/index.php/downloads/xtrend-images/xtrend-'+model+'-images/'
       if model=='ET8000':
        model='et-8000'    
        url='http://www.openvix.co.uk/index.php/downloads/xtrend-images/xtrend-'+model+'-images/'
       if model=='ET8500':
        model='et-8500'    
        url='http://www.openvix.co.uk/index.php/downloads/xtrend-images/xtrend-'+model+'-images/'
       if model=='ET9x00':
        model='et-9x00'    
        url='http://www.openvix.co.uk/index.php/downloads/xtrend-images/xtrend-'+model+'-images/'
       if model=='ET10000':
        model='et-10x00'    
        url='http://www.openvix.co.uk/index.php/downloads/xtrend-images/xtrend-'+model+'-images/'
    if 'satdreamgr' in url: 
       url='http://sgcpm.com/satdreamgr-images-6/et/'+model.lower()
    if 'openesi' in url: 
       url='http://www.openesi.eu/images/index.php?dir=Xtrend/'+model.lower()
    if 'openpli' in url:              
       url='https://openpli.org/download/xtrend/'+model
    if 'hdfreaks' in url: 
        url='http://v64.hdfreaks.cc/'+model.lower()
    if 'hdmedia' in url:        
       url='http://www.hdmedia-universe.com/board/pages.php?pageid=1&box='+model.lower()
    if 'open-plus' in url:        
       url='http://images.open-plus.es/?dir='+model.lower()		   

    print "image_url",url		   
    data=readnet(url)    
    if data is None:
       print 'download error'
       return (False, 'Download error')
    url=url.lower()
    listdata=[]	  

    if 'open-plus' in url:
       regx='''<a href="(.*?)" target="_parent" class="item _blank zip">\n\t\t\t\t\t\t\t\t\t\t\t\t(.*?)\t\t\t\t\t\t\t\t\t\t\t</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://images.open-plus.es/'+href
           listdata.append((name,href))		

    if 'hdmedia' in url: 
       regx='''<td class="list_files_table_file_link"><font color="#ff0000"><b>Flash Image: </b></font><a href="(.*?)">(.*?)</a></td>'''
       images=re.findall(regx,data, re.M|re.I)
       print "images",images   
       for href,name in images:         
           print href           
           listdata.append((name.strip(),href))

    if 'hdfreaks' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://v64.hdfreaks.cc/'+model.lower()+'/'+href	  
           listdata.append((name.strip(),href))
		   
    if 'openatv' in url: 
       regx='''<a href='(.*?)'>(.*?)</a><br/>'''       
       images=re.findall(regx,data, re.M|re.I)
       print 'images',images
       for href,name in images:
           href='http://images.mynonpublic.com/openatv/6.3/'+href
           listdata.append((name.strip(),href))

    if 'openvix' in url: 
       regx='''<.*?href="(.*?)" download="(.*?)".*?>'''
       images=re.findall(regx,data, re.M|re.I)
       print "images",images   
       for href,name in images:         
           print href           
           listdata.append((name.strip(),href))
       listdata.reverse()
       
    if 'satdreamgr' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if 'parent' in name.lower():
              continue           
           href='http://sgcpm.com/satdreamgr-images-6/et/'+model.lower()+'/'+href
           listdata.append((name.strip(),href))		   
       listdata.reverse()
       
    if 'openesi' in url:
       regx='''<a class="autoindex_a" href="(.*?)">'''
       images=re.findall(regx,data, re.M|re.I)
       for href in images:
           try:href=href.split("file=")[1]
           except:continue
           name=href
           href='http://www.openesi.eu/images/GigaBlue/'+model+'/'+href
           listdata.append((name.strip(),href))
       listdata.reverse()	   
		   
    if 'openpli' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not ".zip" in href:
              continue
           listdata.append((name.strip(),href))			   

    print 'listdata',listdata
    for item in listdata:
        addDir(item[0],item[1],10,'','',1,True)
    return True,listdata 	   
######################
######################  
def gigabluemodels(name,url,page):
         if 'pur-e2' in url:
            models = ['All_Models'
			]
         elif 'odisealinux' in url:
            models = ['All_Models'
			]
         elif 'open-plus' in url:
            models = ['gb7252',
			'gb7325',
			'gb7356',
			'gb7362',
			'gb800solo'
			]
         else:
          models = ['gb800solo',
             'gb800se',
             'gb800seplus',
             'gb800ue',
             'gb800ueplus',
             'gbultraue',
             'gbquad',
             'gbquadplus',
             'gbx1',
             'gbx2',
             'gbx3',
             'gbipbox',
             'gbue4k',
             'gbquad4k']            
         for model in models:
           print 'model',model
           href=url+model  
           addDir(model, href,117, '','', 1)  
######################
def extract_gigablueimages(model,url,page):
    if 'openatv' in url: 
       url='http://images.mynonpublic.com/openatv/6.3/index.php?open='+model
    if 'openesi' in url: 
       url='http://www.openesi.eu/images/index.php?dir=GigaBlue/'+model	   
    if 'opendroid' in url: 
        url='http://images.opendroid.org/6.8/GigaBlue/'+model
    if 'hdfreaks' in url: 
        url='http://v64.hdfreaks.cc/'+model	
    if 'teamblue' in url: 
        url='http://images.teamblue.tech/6.3-release/index.php?open='+model
    if 'hdmedia' in url:    
       url='http://www.hdmedia-universe.com/board/pages.php?pageid=1&box='+model		
    if 'odisealinux' in url: 
       url='https://www.odisealinux.com/Test/images/Gigablue/'
    if 'openvix' in url: 
       if model=='gb800solo':
        model='hd800-solo-images'	
       if model=='gb800se':
        model='hd800-se-images'	
       if model=='gb800seplus':
        model='hd800-se-plus-images'	
       if model=='gb800ue':
        model='hd800-ue-images'
       if model=='gb800ueplus':
        model='hd800-ue-plus-images'		
       if model=='gbultraue':
        model='hd-ultra-ue-images'	
       if model=='gbquad':
        model='quad'	
       if model=='gbquadplus':
        model='hd-quad-plus'	
       if model=='gbx1':
        model='hd-x1-images/'	
       if model=='gbx2':
        model='hd-x2-images'	
       if model=='gbx3':
        model='hd-x3'	
       if model=='gbipbox':
        model='GiGaBlue-IPBOX'
       if model=='gbue4k':
        model='uhd-ue-4k'
       if model=='gbquad4k':
        model='uhd-quad-4k'		
       print 'model',model   
       url='http://www.openvix.co.uk/index.php/downloads/gigablue-images/gigablue-'+model
    if 'pur-e2' in url:
       url='http://pur-e2.club/OU/images/index.php?dir=6.2/gigablue/'
    if 'openspa' in url:
        url='https://openspa.webhop.info/#Descarga%20de%20Im%C3%A1genes%2FGigaBlue/'+model
    if 'nachtfalke' in url:
        url='http://dev.nachtfalke.biz/nfr/feeds/6.3/images/'+model
    if 'open-plus' in url:
        url='http://images.open-plus.es/?dir='+model
	   
    print "image_url",url		   
    data=readnet(url)    
    if data is None:
       print 'download error'
       return (False, 'Download error')
    url=url.lower()
    listdata=[]		   
	
    if 'openspa' in url:	
     print "image_url",url   
     data=readnet('https://openspa.webhop.info/scan.php')
     listdata=[]#added this line
     import json
     jdata=json.loads(data)
     #print "name", jdata["items"][0]['name']
     info= jdata.get('items', {})
     teams=[]
     print "modelxx",model
     for item in info:
        modela=item['items']
        for item in modela:
            submodel=item['name']
            print "submode",submodel
            if not model.strip() in submodel:
               continue			   
            images=item['items']
            for image in images:
                image_name=image['name']
                image_path=image['path']
                #https://openspa.webhop.info/Descarga%20de%20Im%C3%A1genes/AZBox/AzboxHD
                image_path='https://openspa.webhop.info/'+image_path.replace(" ","%20")
                print 'image_name',image_name
                listdata.append((image_name,image_path.encode("utf-8")))
            listdata.reverse()#added - list it by newest
			
    if 'nachtfalke' in url:
     regx='''<td><a href=(.*?)" title="(.*?)">.*?</a></td>'''	
     images=re.findall(regx,data, re.M|re.I)
     print "images",images   
     for href,name in images:        
      print href
      href='http://dev.nachtfalke.biz/nfr/feeds/6.3/images/'+model+'/'+href			  
     listdata.append((name.strip(),href))	

    if 'pur-e2' in url:
       regx='''<a class="autoindex_a" href="(.*?)">'''
       images=re.findall(regx,data, re.M|re.I)
       for href in images:
           try:href=href.split("file=")[1]
           except:continue
           name=href
           href='http://pur-e2.club/OU/images/6.2/gigablue/'+href
           listdata.append((name.strip(),href))
		   
    if 'open-plus' in url:	
       regx='''<a href="(.*?)" target="_parent" class="item _blank zip">\n\t\t\t\t\t\t\t\t\t\t\t\t(.*?)\t\t\t\t\t\t\t\t\t\t\t</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://images.open-plus.es/'+href
           listdata.append((name,href))
		   
    if 'openatv' in url: 
       regx='''<a href='(.*?)'>(.*?)</a><br/>'''       
       images=re.findall(regx,data, re.M|re.I)
       print 'images',images
       for href,name in images:
           href='http://images.mynonpublic.com/openatv/6.3/'+href
           listdata.append((name.strip(),href))

    if 'openesi' in url:
       regx='''<a class="autoindex_a" href="(.*?)">'''
       images=re.findall(regx,data, re.M|re.I)
       for href in images:
           try:href=href.split("file=")[1]
           except:continue
           name=href
           href='http://www.openesi.eu/images/GigaBlue/'+model+'/'+href
           listdata.append((name.strip(),href))
       listdata.reverse()
		   
    if 'teamblue' in url: 
       regx='''<a href='(.*?)' class="button"><span class="mif-download mif-lg fg-darkCyan"></span>(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
              continue
           href='http://images.teamblue.tech/6.3-release/'+href	  
           listdata.append((name.strip(),href))
	   
    if 'openvix' in url: 
       regx='''<.*?href="(.*?)" download="(.*?)".*?>'''
       images=re.findall(regx,data, re.M|re.I)
       print "images",images   
       for href,name in images:          
           print href           
           listdata.append((name.strip(),href))
       listdata.reverse()
       
    if 'hdmedia' in url: 
       regx='''<td class="list_files_table_file_link"><font color="#ff0000"><b>Flash Image: </b></font><a href="(.*?)">(.*?)</a></td>'''
       images=re.findall(regx,data, re.M|re.I)
       print "images",images   
       for href,name in images:         
           print href           
           listdata.append((name.strip(),href))

    if 'odisealinux' in url: 
     regx='''<td><a href='(.*?)' class='name'>(.*?)</a></td>'''	
     images=re.findall(regx,data, re.M|re.I)
     for href,name in images:
           if not '.zip' in href:
              continue
           href='https://www.odisealinux.com/Test/images/Gigablue/'+href
           listdata.append((name.strip(),href))
		   
    if 'opendroid' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
              continue
           href='http://images.opendroid.org/6.8/GigaBlue/'+model+'/'+href	  
           listdata.append((name.strip(),href))

    if 'hdfreaks' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://v64.hdfreaks.cc/'+model+'/'+href	  
           listdata.append((name.strip(),href))		   
		   
    print 'listdata',listdata
    for item in listdata:
        addDir(item[0],item[1],10,'','',1,True)
    return True,listdata 	
######################
######################
def addDir(name, url, mode, iconimage, desc = '', page = '',link=False):
    global list2
    if not page == '':
        u = module_path + '?url=' + urllib.quote_plus(url) + '&mode=' + str(mode) + '&name=' + urllib.quote_plus(name) + '&desc=' + urllib.quote_plus(desc) + '&page=' + str(page)
    else:
        u = module_path + '?url=' + urllib.quote_plus(url) + '&mode=' + str(mode) + '&name=' + urllib.quote_plus(name) + '&desc=' + urllib.quote_plus(desc) + '&page='
    if link:
        u=url
        list2.append((name,
         u,
         iconimage,
         page))
    else:
        list2.append((name,
         u,
         iconimage,
         page))
def get_params(action_param):
    param = []
    paramstring = action_param
    if paramstring is None or paramstring == '':
        paramstring = ''
    else:
        paramstring = '?' + action_param.split('?')[1]
    if len(paramstring) >= 2:
        params = paramstring
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if len(splitparams) == 2:
                param[splitparams[0]] = splitparams[1]
    print 'input,output', paramstring, param
    return param
def process_mode(action_param=None):
    global list2
    try:        
        if os.path.exists(temppath+'Downloader.log'):
            os.remove(temppath+'Downloader.log')
        list2 = []
        print 'action_param',action_param
        try:params = get_params(action_param)
        except:params={}
        url = None
        name = None
        mode = None
        page = ''
        try:
            url = urllib.unquote_plus(params['url'])
        except:
            pass

        try:
            name = urllib.unquote_plus(params['name'])
        except:
            pass

        try:
            mode = int(params['mode'])
        except:
            pass

        try:
            page = str(params['pageToken'])
        except:
            page = 1
        print 'Mode: ' + str(mode)
        print 'URL: ' + str(url)
        print 'Name: ' + str(name)
        print 'page: ' + str(page)
        if type(url) == type(str()):
            url = urllib.unquote_plus(url)
        if mode == None :            
            main_cats()
        elif mode == 100:
            print '' + url
            getteams(name, url, page)
        elif mode == 102:
            print '' + url
            dreamboxmodels(name, url, page)			
        elif mode == 103:
            print '' + url
            vuplusmodels(name, url, page)
        elif mode == 114:
            print '' + url
            xtrendmodels(name, url, page)
        elif mode == 116:
            print '' + url
            gigabluemodels(name, url, page)	
        elif mode == 118:
            print '' + url
            formulermodels(name, url, page)				
        elif mode==104:
            extract_dreamboximages(name,url,1)
        elif mode==105:
            extract_vuplusimages(name,url,1)
        elif mode==108:
            extract_xtrendimages(name,url,1)
        elif mode==109:
            extract_tsdreamboximages(name,url,1)
        elif mode==115:
            extract_xtrendimages(name,url,1)
        elif mode==117:
            extract_gigablueimages(name,url,1)
        elif mode==119:
            extract_formulerimages(name,url,1)            
    except:
        addDir('Error:script error [error 1050]', '', '', '', desc='', page='')
    print 'list2',list2
    return list2
