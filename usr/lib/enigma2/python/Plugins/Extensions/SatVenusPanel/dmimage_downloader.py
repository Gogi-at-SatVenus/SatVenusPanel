import sys
import urllib, urllib2, re, os

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
            cats.append(('Dream Multimedia Images oe2.2',''))
            cats.append(('Dream Multimedia Images oe2.5',''))
            for cat in cats:
                print 'cat',cat
                addDir(cat[0], cat[0], 100, cat[1], '', 1)

def getteams(name,url,page):
       if name=='Dream Multimedia Images oe2.2':
          mode=112
          teams=[('Dreamboxupdate', 'http://dreamboxupdate.com/opendreambox/2.2/unstable/images/', ''),
                 ('OpenATV', 'http://images.mynonpublic.com/openatv/6.3/index.php?open=', ''),
                 ('OpenESI', 'http://www.openesi.eu/images/Dreambox/', ''),
                 ('OpenHDF', 'http://v62.hdfreaks.cc/', ''),
                 ('Power-Sat', 'http://www.power-sat.org/power-plus/Powersat_2.2/', ''),
                 ('TSimage', 'http://tunisia-dreambox.info/tsimage-feed/unstable/4.0/images/', '')]

       elif name=='Dream Multimedia Images oe2.5':
          mode=113
          teams=[('Demonisat', 'http://www.demonisat.info/demonisat-e2Img-OE2.0/Image-oe2.5/', ''),
                 ('Dreamboxupdate', 'http://dreamboxupdate.com/opendreambox/2.5/stable/images/', ''),
                 ('Dream-Elite', 'http://images.dream-elite.net/DE6/index.php?dir=', ''),
                 ('Merlin', 'http://debfeed4.merlin.xyz/oe_2.5/deb/', ''),
                 ('NewNigma2', 'http://feed.newnigma2.to/daily/', ''),
                 ('OpenATV', 'http://images.mynonpublic.com/openatv/6.3/index.php?open=', ''),
                 ('OpenESI', 'http://www.openesi.eu/images/Dreambox/', ''),
                 ('OpenHDF', 'http://v62.hdfreaks.cc/', ''),
                 ('Peter_Pan', 'http://178.63.156.75/DreamBoxImages/Peter_Pan/', ''),#On VenusCS
                 ('PowerSat', 'http://www.power-sat.org/power-plus/Powersat_2.5/', ''),
                 ('Sat-Lodge', 'http://webplus.sat-lodge.it/index.php?dir=', '')]

       for team in teams:
         addDir(team[0], team[1], mode, team[2], '', 1)
######################
######################		
def dreambox22models(name,url,page):
            models = ['dm520',
             'dm820',			 
             'dm7080']
            for model in models:					                 
                href=url+model  
                addDir(model, href,110, '','', 1)
######################
def dreambox25models(name,url,page):
            models = ['dm920',
             'dm900',
             'dm7080',
             'dm820',
             'dm520']
            for model in models:				   
                href=url+model
                addDir(model, href,111, '','', 1)
######################
def extract_dreambox22images(model,url,page):
    if 'dreamboxupdate' in url: 
        url='http://dreamboxupdate.com/opendreambox/2.2/unstable/images/'+model
    if 'openatv' in url: 
       url='http://images.mynonpublic.com/openatv/6.3/index.php?open='+model 
    if 'openesi' in url: 
        url='http://www.openesi.eu/images/Dreambox/'+model
    if 'hdfreaks' in url: 
        url='http://v62.hdfreaks.cc/'+model			
    if 'tsimage' in url: 
        url='http://tunisia-dreambox.info/tsimage-feed/unstable/4.0/images/'+model
    if 'power-sat' in url: 
       if model=='dm520':
        model='immagini_powersat_dm520'	
       if model=='dm820':
        model='immagini_powersat_dm820'	
       if model=='dm7080':
        model='immagini_powersat_dm7080'
       print 'model',model
       url='http://www.power-sat.org/power-plus/Powersat_2.2/'+model 		

    print 'image_url',url

    data=readnet(url)
    if data is None:
       return (False, 'Download error')
    url=url.lower()
    listdata=[]

    if 'power-sat' in url: 
       regx='''<td><a href="(.*?)">(.*?)..&gt;</a></td>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue           
           href='http://www.power-sat.org/power-plus/Powersat_2.2/'+model+'/'+href
           listdata.append((name,href))	
	
    if 'tsimage' in url: 
       regx='''<li><a href="(.*?)">(.*?)</a></li>'''	   
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue           
           href='http://tunisia-dreambox.info/tsimage-feed/unstable/4.0/images/'+model+'/'+href
           listdata.append((name,href))	
		
    if 'dreamboxupdate' in url: 
       regx='''<a class="tarxz" href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue           
           href='http://dreamboxupdate.com/opendreambox/2.2/unstable/images/'+model+'/'+href
           listdata.append((name,href))
		   
    if 'openatv' in url: 
       regx='''<a href='(.*?)'>(.*?)</a><br/>'''       
       images=re.findall(regx,data, re.M|re.I)
       print 'images',images
       for href,name in images:
           href='http://images.mynonpublic.com/openatv/6.3/'+href
           listdata.append((name.strip(),href))

    if 'openesi' in url: 
       regx='''<li><a href="(.*?)">(.*?)</a></li>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue
           href='http://www.openesi.eu/images/Dreambox/'+model+'/'+href	  
           listdata.append((name.strip(),href))

    if 'hdfreaks' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue
           href='http://v62.hdfreaks.cc/'+model+'/'+href	  
           listdata.append((name.strip(),href))

    print 'listdata',listdata
    for item in listdata:
        addDir(item[0],item[1],10,'','',1,True)
    return True,listdata		   
###################### 
def extract_dreambox25images(model,url,page):
    if 'demonisat' in url: 
       if model=='dm520':
        model='520'	
       if model=='dm820':
        model='820'	
       if model=='dm900':
        model='900'		
       if model=='dm920':
        model='920'
       if model=='dm7080':
        model='7080'		
       print 'model',model
       url='http://www.demonisat.info/demonisat-e2Img-OE2.0/Image-oe2.5/'+model  
    if 'dreamboxupdate' in url: 
        url='http://dreamboxupdate.com/opendreambox/2.5/stable/images/'+model
    if 'newnigma2' in url: 
       if model=='dm520':
        model='images'	
       if model=='dm820':
        model='images'	
       if model=='dm7080':
        model='images'
       if model=='dm900':
        model='images'
       if model=='dm920':
        model='images'		
       print 'model',model
       url='http://feed.newnigma2.to/daily/'+model	
    if 'openatv' in url: 
       url='http://images.mynonpublic.com/openatv/6.3/index.php?open='+model 
    if 'hdfreaks' in url: 
        url='http://v62.hdfreaks.cc/'+model
    if 'peter_pan' in url: 
        url='http://178.63.156.75/DreamBoxImages/Peter_Pan/'+model
    if 'openesi' in url: 
        url='http://www.openesi.eu/images/Dreambox/'+model
    if 'power-sat' in url: 
       if model=='dm520':
        model='immagini_powersat_dm520-525_OE2.5'	
       if model=='dm820':
        model='immagini_powersat_dm820_OE2.5'	
       if model=='dm7080':
        model='immagini_powersat_dm7080_OE2.5'
       if model=='dm900':
        model='immagini_powersat_dm900_OE2.5'
       if model=='dm920':
        model='immagini_powersat_dm920_OE2.5'		
       print 'model',model
       url='http://www.power-sat.org/power-plus/Powersat_2.5/'+model   
    if 'merlin' in url:
       if model=='dm520':
        model='images'	
       if model=='dm820':
        model='images'	
       if model=='dm7080':
        model='images'
       if model=='dm900':
        model='images'
       if model=='dm920':
        model='images'		
       url='http://debfeed4.merlin.xyz/oe_2.5/deb/'+model	   
    if 'sat-lodge' in url:
       if model=='dm520':
        model='Satlodge%202.5'	
       if model=='dm820':
        model='Satlodge%202.5'	
       if model=='dm7080':
        model='Satlodge%202.5'
       if model=='dm900':
        model='Satlodge%202.5'
       if model=='dm920':
        model='Satlodge%202.5'		
       url='http://webplus.sat-lodge.it/index.php?dir='+model
    if 'dream-elite' in url:
       if model=='dm520':
        model='DM520-DM525'	
       if model=='dm820':
        model='DM820'	
       if model=='dm7080':
        model='DM7080'
       if model=='dm900':
        model='DM900'
       if model=='dm920':
        model='DM920'
       print 'model',model		
       url='http://images.dream-elite.net/DE6/index.php?dir='+model		   
		     		
    print 'image_url',url

    data=readnet(url)
    if data is None:
       return (False, 'Download error')
    url=url.lower()
    listdata=[]

    if 'dream-elite' in url:
       regx='''<a class="autoindex_a" href="(.*?)">'''
       images=re.findall(regx,data, re.M|re.I)
       for href in images:
           try:href=href.split("file=")[1]
           except:continue
           name=href
           href='http://images.dream-elite.net/DE6/'+model+"/"+href
           listdata.append((name.strip(),href))

    if 'merlin' in url:
       regx='''<a href="(.*?)">(.*?)</a>'''	   
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue
           href='http://debfeed4.merlin.xyz'+href	  
           listdata.append((name.strip(),href))		 

    if 'sat-lodge' in url:
       regx='''<a class="autoindex_a" href="(.*?)">'''
       images=re.findall(regx,data, re.M|re.I)
       for href in images:
           try:href=href.split("file=")[1]
           except:continue
           name=href
           href='http://webplus.sat-lodge.it/'+model+'/'+href		   
           listdata.append((name.strip(),href))		   
		   
    if 'power-sat' in url: 
       regx='''<td><a href="(.*?)">(.*?)..&gt;</a></td>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue           
           href='http://www.power-sat.org/power-plus/Powersat_2.5/'+model+'/'+href
           listdata.append((name,href))

    if 'hdfreaks' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue
           href='http://v62.hdfreaks.cc/'+model+'/'+href	  
           listdata.append((name.strip(),href))		   

    if 'peter_pan' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue
           href='http://178.63.156.75/DreamBoxImages/Peter_Pan/'+model+'/'+href	  
           listdata.append((name.strip(),href))
		   
    if 'openatv' in url: 
       regx='''<a href='(.*?)'>(.*?)</a><br/>'''       
       images=re.findall(regx,data, re.M|re.I)
       print 'images',images
       for href,name in images:
           href='http://images.mynonpublic.com/openatv/6.3/'+href
           listdata.append((name.strip(),href))		   

    if 'openesi' in url: 
       regx='''<li><a href="(.*?)">(.*?)</a></li>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.zip' in href:
              continue
           href='http://www.openesi.eu/images/Dreambox/'+model+'/'+href	  
           listdata.append((name.strip(),href))
		   
    if 'demonisat' in url: 
       regx='''<a href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue
           href='http://www.demonisat.info/demonisat-e2Img-OE2.0/Image-oe2.5/'+model+'/'+href	  
           listdata.append((name.strip(),href))

    if 'dreamboxupdate' in url: 
       regx='''<a class="tarxz" href="(.*?)">(.*?)</a>'''
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue           
           href='http://dreamboxupdate.com/opendreambox/2.5/stable/images/'+model+'/'+href
           listdata.append((name,href))		   

    if 'newnigma2' in url: 
       regx='''<td><a href="(.*?)">(.*?)</a></td>''' 	   
       images=re.findall(regx,data, re.M|re.I)
       for href,name in images:
           if not '.tar.xz' in href:
              continue           
           href='http://feed.newnigma2.to/daily/'+model+'/'+href
           listdata.append((name,href))	
		   
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
        elif mode == 112:
            print '' + url
            dreambox22models(name, url, page)
        elif mode == 113:
            print '' + url
            dreambox25models(name, url, page)				
        elif mode==110:
            extract_dreambox22images(name,url,1)
        elif mode==111:
            extract_dreambox25images(name,url,1)
			            
    except:
        addDir('Error:script error [error 1050]', '', '', '', desc='', page='')
    print 'list2',list2
    return list2
