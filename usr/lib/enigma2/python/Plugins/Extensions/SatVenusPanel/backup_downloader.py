from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.ChoiceBox import ChoiceBox
from Screens.Screen import Screen
from Screens.InputBox import InputBox
from Screens.HelpMenu import HelpableScreen
from Components.GUIComponent import *
from Components.HTMLComponent import *
from Components.Button import Button
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ActionMap import ActionMap, NumberActionMap, HelpableActionMap
from Components.ProgressBar import ProgressBar
from Components.Input import Input
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Components.FileList import FileList
from Components.Slider import Slider
from Components.Harddisk import harddiskmanager
from Components.config import getConfigListEntry, ConfigSubsection, ConfigText, ConfigLocations
from Components.config import config, ConfigSelection, ConfigBoolean, ConfigYesNo
from Components.config import getConfigListEntry, configfile
from Components.ConfigList import ConfigListScreen
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.SelectionList import SelectionList
from Components.PluginComponent import plugins
from Components.AVSwitch import AVSwitch
from twisted.web.client import downloadPage, getPage
from socket import gethostbyname
from xml.dom.minidom import parse, getDOMImplementation
from xml.dom import Node, minidom
from Tools.Directories import *
from Tools.Directories import pathExists, fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_PLUGIN, SCOPE_CURRENT_SKIN, SCOPE_METADIR, SCOPE_MEDIA, SCOPE_LANGUAGE
from Tools.LoadPixmap import LoadPixmap
from enigma import eConsoleAppContainer, loadPNG, eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop
from cPickle import dump, load
from os import path as os_path, system as os_system, unlink, stat, mkdir, popen, makedirs, listdir, access, rename, remove, W_OK, R_OK, F_OK
from os import environ, system, path, listdir, remove
from time import time, gmtime, strftime, localtime
from stat import ST_MTIME
from image_viewer import ScreenBox
import datetime
import urllib2
import gettext
import os
config.plugins.ImageDownLoader2 = ConfigSubsection()
config.plugins.ImageDownLoader2.addstr = ConfigText(default='tsimage')
config.plugins.ImageDownLoader2.Downloadlocation = ConfigText(default='/media/', visible_width=50, fixed_size=False)
config.plugins.ImageDownLoader2.log = ConfigText(default='2> /tmp/ImageDownLoaderLog >&1')
config.plugins.ImageDownLoader2.debug = ConfigText(default='debugon')
config.plugins.ImageDownLoader2.swap = ConfigSelection([('auto', 'auto'),
 ('128', '128 MB'),
 ('256', '256 MB'),
 ('512', '512 MB'),
 ('0', 'off')], default='auto')
config.plugins.ImageDownLoader2.swapsize = ConfigText(default='128')
config.plugins.ImageDownLoader2.disclaimer = ConfigBoolean(default=True)
config.plugins.ImageDownLoader2.update = ConfigYesNo(default=False)
mounted_string = 'Nothing mounted at '
dwidth = getDesktop(0).size().width()
currversion = 'eo2.0'
mountedDevs = []
for p in harddiskmanager.getMountedPartitions(True):
    mountedDevs.append((p.mountpoint, _(p.description) if p.description else ''))

def _(txt):
    t = gettext.dgettext('ImageDownLoader', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t

def getDownloadPath():
    Downloadpath = config.plugins.ImageDownLoader2.Downloadlocation.value
    if Downloadpath.endswith('/'):
        return Downloadpath
    else:
        return Downloadpath + '/'

def freespace():
    downloadlocation = getDownloadPath()
    try:
        diskSpace = os.statvfs(downloadlocation)
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
        return fspace
    except:
        return 0

class buFeeds(Screen):

    def __init__(self, session):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/feedsHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/feedsFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.serversnames = []
        self.serversurls = []
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        if currversion == 'eo2.0':
            self.serversnames = ['</ zvonko67',
             '</ G_ogi',
             '</ dragec11',
             '</ jopidane',
             '</ mika (www.satelitin.com)']
            self.serversurls = ['http://178.63.156.75/BackUpImages/zvonko67/',
             'http://178.63.156.75/BackUpImages/G_ogi/',
             'http://178.63.156.75/BackUpImages/dragec11/',
             'http://178.63.156.75/BackUpImages/jopidane/',
             'http://178.63.156.75/BackUpImages/mika/']
        self.list = []
        self['text'] = MenuList([], True, eListboxPythonMultiContent)
        self.addon = 'emu'
        self.icount = 0
        self.downloading = False
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'red': self.close,
         'green': self.okClicked,
         'cancel': self.close}, -2)
        self.ListToMulticontent()

    def ListToMulticontent(self):
        res = []
        theevents = []
        self.events = []
        self.events = self.serversnames
        if dwidth == 1280:
            self['text'].l.setItemHeight(34)
            self['text'].l.setFont(0, gFont('Sansation-Bold', 24))
            for i in range(0, len(self.events)):
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 35), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 2), size=(720, 35), font=0, flags=RT_HALIGN_LEFT, text=self.events[i]))
                theevents.append(res)
                res = []

        else:
            self['text'].l.setItemHeight(50)
            self['text'].l.setFont(0, gFont('Sansation-Bold', 40))
            for i in range(0, len(self.events)):
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 50), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 2), size=(720, 50), font=0, flags=RT_HALIGN_LEFT, text=self.events[i]))
                theevents.append(res)
                res = []

        self['text'].l.setList(theevents)
        self['text'].show()

    def okClicked(self):
        cindex = self['text'].getSelectionIndex()
        selectedservername = self.serversnames[cindex]
        selectedserverurl = self.serversurls[cindex]
        self.session.open(Servers, selectedservername, selectedserverurl)

class Servers(Screen):

    def __init__(self, session, selectedservername = None, selectedserverurl = None):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/serversHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/serversFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.selectedservername = selectedservername
        self.rooturl = selectedserverurl
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        self.newsurl = ''
        self.list = []
        self['list'] = MenuList([], True, eListboxPythonMultiContent)
        self.addon = 'emu'
        self.icount = 0
        self.searchstr = None
        self.downloading = False
        self.data = []
        if self.selectedservername == '</ zvonko67':
            self.groups = ['VuPlus_Solo2']
            self.downloading = True
        if self.selectedservername == '</ G_ogi':
            self.groups = ['VuPlus_Uno4K', 'VuPlus_SoloSEv2', 'DM_520HD']
            self.downloading = True
        if self.selectedservername == '</ dragec11':
            self.groups = ['DM_800HDse', 'VuPlus_Zero4K']
            self.downloading = True
        if self.selectedservername == '</ jopidane':
            self.groups = ['DM_7020HD']
            self.downloading = True
        if self.selectedservername == '</ mika (www.satelitin.com)':
            self.groups = ['Golden_Intestar_Xpeed_LX_Class_S2', 'VuPlus_Uno4K', 'VuPlus_Zero4K']
            self.downloading = True
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'green': self.okClicked,
         'red': self.close,
         'cancel': self.close}, -2)
        self.ListToMulticontent()
        return

    def ListToMulticontent(self):
        res = []
        theevents = []
        self.events = []
        self.events = self.groups
        if dwidth == 1280:
            self['list'].l.setItemHeight(34)
            self['list'].l.setFont(0, gFont('Sansation-Bold', 30))
            for i in range(0, len(self.events)):
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 34), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 2), size=(740, 34), font=0, flags=RT_HALIGN_LEFT, text=self.events[i]))
                theevents.append(res)
                res = []

        else:
            self['list'].l.setItemHeight(50)
            self['list'].l.setFont(0, gFont('Sansation-Bold', 40))
            for i in range(0, len(self.events)):
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 50), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 2), size=(740, 50), font=0, flags=RT_HALIGN_LEFT, text=self.events[i]))
                theevents.append(res)
                res = []

        self['list'].l.setList(theevents)

    def okClicked(self):
        cindex = self['list'].getSelectionIndex()
        selection = str(self.groups[cindex])
        self.session.open(Images, self.selectedservername, self.searchstr, selection, self.rooturl)

class Images(Screen):

    def __init__(self, session, selectedservername, searchstr, selection, rooturl):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/imagesHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/imagesFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.rooturl = rooturl
        self.data = []
        self.selection = selection
        self.selectedservername = selectedservername
        self.url = self.rooturl + self.selection + ''
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['menu'] = MenuList([], True, eListboxPythonMultiContent)
        list = []
        self.list = list
        self.status = []
        self.slist = []
        self['actions'] = ActionMap(['SetupActions', 'MenuActions', 'ColorActions'], {'ok': self.selclicked,
         'green': self.selclicked,
         'cancel': self.close}, -2)
        self.itempreview = False
        self.timer = eTimer()
        try:
           self.timer_conn = self.timer.timeout.connect(self.extractdata)
        except:			
         self.timer.callback.append(self.extractdata)
        self.timer.start(100, 1)

    def extractdata(self):
        success = False
        if self.selectedservername == '</ zvonko67' or self.selectedservername == '</ mika (www.satelitin.com)' or self.selectedservername == '</ G_ogi' or self.selectedservername == '</ dragec11' or self.selectedservername == '</ jopidane':
            success, self.data = getdata(self.url)
            if success == True:
                pass
            else:
                self['info'].setText('Sorry, error in getting images list !')
                return
            if len(self.data) == 0:
                self['info'].setText('No images found !')
                return
        else:
            success, self.data = getplidata(self.url)
            if success == True:
                pass
            else:
                self['info'].setText('Sorry, error in getting images list !')
                return
            if len(self.data) == 0:
                self['info'].setText('No images found !')
                return
        self['info'].setText('Press OK to download selected image !')
        self.ListToMulticontent()

    def downloadxmlpage(self):
        url = self.xmlurl
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)
        self['info'].setText('Addons download failure, no internet connection or server down !')
        self.downloading = False

    def _gotPageLoad(self, data):
        try:
            newdata = ''
            self.xml = data
        except:
            self.xml = data

        if self.xml:
            xmlstr = minidom.parseString(self.xml)
        else:
            self.downloading = False
            self['info'].setText('Addons download failure, no internet connection or server down !')
            return
        self.data1 = []
        self.names = []
        icount = 0
        list = []
        xmlparse = xmlstr
        self.xmlparse = xmlstr
        self.data = []
        print '688', self.selection
        for images in self.xmlparse.getElementsByTagName('images'):
            if str(images.getAttribute('cont').encode('utf8')) == self.selection:
                for image in images.getElementsByTagName('image'):
                    item = image.getAttribute('name').encode('utf8')
                    urlserver = str(image.getElementsByTagName('url')[0].childNodes[0].data)
                    imagesize = 'image size ' + str(image.getElementsByTagName('imagesize')[0].childNodes[0].data)
                    timagesize = str(imagesize).replace('image size', '').strip()
                    print '675', str(timagesize)
                    urlserver = os.path.basename(urlserver)
                    self.data.append([urlserver,
                     '',
                     '',
                     timagesize])

        self.downloading = True
        if len(self.data) == 0:
            self['info'].setText('No images found !')
        self['info'].setText('Press OK to download selected image !')
        self.ListToMulticontent()

    def ListToMulticontent(self, result = None):
        downloadpath = getDownloadPath()
        res = []
        theevents = []
        if dwidth == 1280:
            self['menu'].l.setItemHeight(80)
            self['menu'].l.setFont(0, gFont('Sansation-Bold', 22))
            self.menulist = []
            for i in range(0, len(self.data)):
                item = str(self.data[i][0])
                idate = str(self.data[i][1])
                itime = str(self.data[i][2])
                imagesize = str(self.data[i][3])
                print item
                if os.path.exists(downloadpath + item):
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/button_red.png'
                else:
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/button_green.png'
                res.append(MultiContentEntryText(pos=(0, 1), size=(5, 5), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 25), size=(30, 30), png=loadPNG(png)))
                res.append(MultiContentEntryText(pos=(40, 20), size=(730, 25), font=0, flags=RT_HALIGN_LEFT, text=item))
                theevents.append(res)
                res = []

        else:
            self['menu'].l.setItemHeight(80)
            self['menu'].l.setFont(0, gFont('Sansation-Bold', 34))
            self.menulist = []
            for i in range(0, len(self.data)):
                item = str(self.data[i][0])
                idate = str(self.data[i][1])
                itime = str(self.data[i][2])
                imagesize = str(self.data[i][3])
                print item
                if os.path.exists(downloadpath + item):
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/button_red.png'
                else:
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/button_green.png'
                res.append(MultiContentEntryText(pos=(0, 1), size=(5, 40), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 25), size=(30, 30), png=loadPNG(png)))
                res.append(MultiContentEntryText(pos=(40, 15), size=(900, 40), font=0, flags=RT_HALIGN_LEFT, text=item))
                theevents.append(res)
                res = []

        self.theevents = []
        self.theevents = theevents
        self['menu'].l.setList(theevents)
        self['menu'].show()

    def getfreespace(self):
        fspace = freespace()
        self.freespace = fspace
        self.setTitle(self.freespace)

    def selclicked(self):
        cindex = self['menu'].getSelectionIndex()
        if self.selectedservername == '</ zvonko67':
            self.url = 'http://178.63.156.75/BackUpImages/zvonko67/' + self.selection + '/'
        if self.selectedservername == '</ G_ogi':
            self.url = 'http://178.63.156.75/BackUpImages/G_ogi/' + self.selection + '/'
        if self.selectedservername == '</ mika (www.satelitin.com)':
            self.url = 'http://178.63.156.75/BackUpImages/mika/' + self.selection + '/'
        if self.selectedservername == '</ dragec11':
            self.url = 'http://178.63.156.75/BackUpImages/dragec11/' + self.selection + '/'
        if self.selectedservername == '</ jopidane':
            self.url = 'http://178.63.156.75/BackUpImages/jopidane/' + self.selection + '/'
        try:
            imageurl = self.url + self.data[cindex][0]
        except:
            imageurl = self.url

        imageurl = imageurl.strip()
        if ' ' in imageurl:
            self.session.open(ScreenBox, _('Sorry, the web address of image containing spaces, please report to the server maintainer to fix'), type=ScreenBox.TYPE_ERROR, timeout=5, close_on_any_key=True)
            return
        self.imagesize = self.data[cindex][3]
        if self.imagesize.strip() == '':
            imagesize = '0'
        else:
            imagesize = self.data[cindex][3].replace('M', '').strip()
        print '1190', imageurl
        self.session.openWithCallback(self.ListToMulticontent, SelectLocation, imageurl, imagesize)		
######################
######################
import urllib2
import HTMLParser
import cStringIO
import datetime
import operator

class HTML2Text(HTMLParser.HTMLParser):
    """
    extract text from HTML code
    """

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.output = cStringIO.StringIO()

    def get_text(self):
        """get the text output"""
        return self.output.getvalue()

    def handle_starttag(self, tag, attrs):
        """handle  tags"""
        if tag == 'br':
            self.output.write('\n')

    def handle_data(self, data):
        """normal text"""
        self.output.write(data)

    def handle_endtag(self, tag):
        if tag == 'p':
            self.output.write('\n')

def getnew(idate = None):
    try:
        now = datetime.datetime.now()
        cdate = now.strftime('%Y-%b-%d')
        d1 = datetime.datetime.strptime(idate, '%Y-%b-%d')
        d2 = datetime.datetime.strptime(str(cdate), '%Y-%b-%d')
        delta = d2 - d1
        if delta.days < 32:
            return True
        return False
    except:
        return False

def getdata(urlStr, searchstr = None):
    data = []
    try:
        fileHandle = urllib2.urlopen(urlStr)
        html = fileHandle.read()
        fileHandle.close()
    except IOError:
        print 'Cannot open URL %s for reading' % urlStr
        return (False, data)

    try:
        p = HTML2Text()
        p.feed(html)
        text = p.get_text()
        raw_list = text.splitlines()
    except:
        return (False, data)

    textlist = []
    for line in raw_list:
        line = line.strip()
        print line
        if searchstr:
            if searchstr == 'New':
                if line != '' and '.zip' in line:
                    nfiparts = []
                    nfiparts = line.split('.zip')
                    url = nfiparts[0] + '.zip'
                    spart = nfiparts[1].strip()
                    sizdateparts = spart.split(' ')
                    idate = sizdateparts[0]
                    try:
                        itime = sizdateparts[1]
                    except:
                        print line
                        itime = ''

                    isize = sizdateparts[len(sizdateparts) - 1]
                    line = line + '\n'
                    idate = idate.strip()
                    print 'idate', idate
                    if getnew(idate):
                        try:
                            imdate = datetime.datetime.strptime(idate, '%d-%b-%Y')
                        except:
                            imdate = None

                        data.append([url,
                         imdate,
                         itime,
                         isize])
            elif line != '' and '.zip' in line and searchstr.lower() in line.lower():
                nfiparts = []
                nfiparts = line.split('.zip')
                url = nfiparts[0] + '.zip'
                spart = nfiparts[1].strip()
                sizdateparts = spart.split(' ')
                idate = sizdateparts[0]
                try:
                    itime = sizdateparts[1]
                except:
                    print line
                    itime = ''

                isize = sizdateparts[len(sizdateparts) - 1]
                line = line + '\n'
                try:
                    imdate = datetime.datetime.strptime(idate, '%d-%b-%Y')
                except:
                    imdate = None

                data.append([url,
                 imdate,
                 itime,
                 isize])
        elif line != '' and '.zip' in line:
            nfiparts = []
            nfiparts = line.split('.zip')
            url = nfiparts[0] + '.zip'
            spart = nfiparts[1].strip()
            sizdateparts = spart.split(' ')
            idate = sizdateparts[0]
            try:
                itime = sizdateparts[1]
            except:
                print line
                itime = ''

            isize = sizdateparts[len(sizdateparts) - 1]
            line = line + '\n'
            try:
                imdate = datetime.datetime.strptime(idate, '%d-%b-%Y')
            except:
                imdate = ''

            data.append([url,
             imdate,
             itime,
             isize])

    try:
        data.sort(key=operator.itemgetter(1))
    except:
        pass

    data.reverse()
    return (True, data)

def getplidata(urlStr, searchstr = None):
    data = []
    print ' ', urlStr
    try:
        fileHandle = urllib2.urlopen(urlStr)
        html = fileHandle.read()
        fileHandle.close()
    except IOError:
        print 'Cannot open URL %s for reading' % urlStr
        return (False, data)

    try:
        p = HTML2Text()
        p.feed(html)
        text = p.get_text()
        raw_list = text.splitlines()
    except:
        return (False, data)

    data = []
    textlist = []
    for line in raw_list:
        line = line.strip()
        if searchstr:
            if line != ' ' and '.zip' in line and searchstr.lower() in line.lower():
                nfiparts = []
                nfiparts = line.split('\n')
                x = len(nfiparts)
                if x == 1:
                    url = nfiparts[0]
                    idate = ''
                    itime = ''
                    isize = ''
                    data.append([url,
                     idate,
                     itime,
                     isize])
                    continue
                try:
                    url = nfiparts[1]
                except:
                    url = ''

                infoparts = nfiparts[0].split(' ')
                y = len(infoparts)
                try:
                    idate = infoparts[0]
                except:
                    idate = ''

                try:
                    isize = infoparts[y - 1]
                except:
                    isize = ''

                itime = ''
                data.append([url,
                 idate,
                 itime,
                 isize])
        elif line != '' and '.zip' in line:
            nfiparts = []
            nfiparts = line.split('\t')
            x = len(nfiparts)
            if x == 1:
                url = nfiparts[0]
                idate = ''
                itime = ''
                isize = ''
                data.append([url,
                 idate,
                 itime,
                 isize])
                continue
            try:
                url = nfiparts[1]
            except:
                url = ''

            infoparts = nfiparts[0].split(' ')
            y = len(infoparts)
            try:
                idate = infoparts[0]
            except:
                idate = ''

            try:
                isize = infoparts[y - 1]
            except:
                isize = ''

            itime = ''
            data.append([url,
             idate,
             itime,
             isize])
    print data
    return (True, data)		
######################
######################		
		
class SelectDownloadLocation(Screen, HelpableScreen):

    def __init__(self, session, text = '', filename = '', currDir = None, location = None, userMode = False, minFree = None, autoAdd = False, editDir = False, inhibitDirs = [], inhibitMounts = []):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/sellocHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/sellocFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        HelpableScreen.__init__(self)
        self['text'] = StaticText(_('Selected download location:'))
        self.text = text
        self.filename = filename
        self.minFree = minFree
        self.reallocation = location
        self.location = location and location.value[:] or []
        self.userMode = userMode
        self.autoAdd = autoAdd
        self.editDir = editDir
        self.inhibitDirs = inhibitDirs
        self.inhibitMounts = inhibitMounts
        inhibitDirs = ['/bin',
         '/boot',
         '/dev',
         '/lib',
         '/proc',
         '/sbin',
         '/sys',
         '/mnt',
         '/var',
         '/home',
         '/tmp',
         '/etc',
         '/share',
         '/usr']
        inhibitMounts = ['/mnt', '/ba', '/MB_Images']
        self['filelist'] = FileList(currDir, showDirectories=True, showFiles=False, inhibitMounts=inhibitMounts, inhibitDirs=inhibitDirs)
        self['mountlist'] = MenuList(mountedDevs)
        self['ButtonGreentext'] = Label(_('SAVE'))
        self['ButtonRedtext'] = Label(_('Exit'))
        self['target'] = Label()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'red': self.close,
         'cancel': self.close}, -2)
        if self.userMode:
            self.usermodeOn()

        class DownloadLocationActionMap(HelpableActionMap):

            def __init__(self, parent, context, actions = {}, prio = 0):
                HelpableActionMap.__init__(self, parent, context, actions, prio)

        self['WizardActions'] = DownloadLocationActionMap(self, 'WizardActions', {'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down,
         'ok': (self.ok, _('Select')),
         'back': (self.cancel, _('Cancel'))}, -2)
        self['ColorActions'] = DownloadLocationActionMap(self, 'ColorActions', {'red': self.cancel,
         'green': self.select}, -2)
        self.onLayoutFinish.append(self.switchToFileListOnStart)

    def switchToFileListOnStart(self):
        if self.reallocation and self.reallocation.value:
            self.currList = 'filelist'
            currDir = self['filelist'].current_directory
            if currDir in self.location:
                self['filelist'].moveToIndex(self.location.index(currDir))
        else:
            self.switchToFileList()

    def switchToFileList(self):
        if not self.userMode:
            self.currList = 'filelist'
            self['filelist'].selectionEnabled(1)
            self.updateTarget()

    def up(self):
        self[self.currList].up()
        self.updateTarget()

    def down(self):
        self[self.currList].down()
        self.updateTarget()

    def left(self):
        self[self.currList].pageUp()
        self.updateTarget()

    def right(self):
        self[self.currList].pageDown()
        self.updateTarget()

    def ok(self):
        if self.currList == 'filelist':
            if self['filelist'].canDescent():
                self['filelist'].descent()
                self.updateTarget()

    def updateTarget(self):
        currFolder = self.getPreferredFolder()
        if currFolder is not None:
            self['target'].setText(''.join((currFolder, self.filename)))
        else:
            self['target'].setText(_('Invalid Location'))
        return

    def cancel(self):
        self.close(None)
        return

    def getPreferredFolder(self):
        if self.currList == 'filelist':
            return self['filelist'].getSelection()[0]

    def saveSelection(self, ret):
        if ret:
            ret = ''.join((self.getPreferredFolder(), self.filename))
        config.plugins.ImageDownLoader2.Downloadlocation.value = ret
        config.plugins.ImageDownLoader2.Downloadlocation.save()
        config.plugins.ImageDownLoader2.save()
        config.save()
        self.close(None)
        return

    def checkmountDownloadPath(self, path):
        if path is None:
            self.session.open(ScreenBox, _('nothing entered'), ScreenBox.TYPE_ERROR)
            return False
        else:
            sp = []
            sp = path.split('/')
            print sp
            if len(sp) > 1:
                if sp[1] != 'media':
                    self.session.open(ScreenBox, mounted_string + path, ScreenBox.TYPE_ERROR)
                    return False
            mounted = False
            self.swappable = False
            sp2 = []
            f = open('/proc/mounts', 'r')
            m = f.readline()
            while m and not mounted:
                if m.find('/%s/%s' % (sp[1], sp[2])) is not -1:
                    mounted = True
                    print m
                    sp2 = m.split(' ')
                    print sp2
                    if sp2[2].startswith('ext') or sp2[2].endswith('fat'):
                        print '[stFlash] swappable'
                        self.swappable = True
                m = f.readline()

            f.close()
            if not mounted:
                self.session.open(ScreenBox, mounted_string + str(path), ScreenBox.TYPE_ERROR)
                return False
            if os.path.exists(config.plugins.ImageDownLoader2.Downloadlocation.value):
                try:
                    os.chmod(config.plugins.ImageDownLoader2.Downloadlocation.value, 511)
                except:
                    pass

            return True
            return

    def select(self):
        currentFolder = self.getPreferredFolder()
        foldermounted = self.checkmountDownloadPath(currentFolder)
        if foldermounted == True:
            pass
        else:
            return
        if currentFolder is not None:
            if self.minFree is not None:
                try:
                    s = os.statvfs(currentFolder)
                    if s.f_bavail * s.f_bsize / 314572800 > self.minFree:
                        return self.saveSelection(True)
                except OSError:
                    pass

                self.session.openWithCallback(self.saveSelection, ScreenBox, _('There might not be enough Space on the selected Partition.\nDo you really want to continue?'), type=ScreenBox.TYPE_YESNO)
            else:
                self.saveSelection(True)
        return

class DownloadedFiles(Screen):

    def __init__(self, session):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/dlfilesHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/dlfilesFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        list = []
        self['menu'] = MenuList([], True, eListboxPythonMultiContent)
        self['ButtonRedtext'] = Label(_('Back '))
        self['ButtonGreentext'] = Label(_(' '))
        folder = str(config.plugins.ImageDownLoader2.Downloadlocation.value)
        fspace = str(freespace()) + 'MB'
        self['menu'].onSelectionChanged.append(self.selectionChanged)
        self['info'] = Label(folder + '\n' + ' Free space: ' + fspace)
        if folder.endswith('/'):
            self.folder = folder
        else:
            self.folder = folder + '/'
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': self.delimage,
         'cancel': self.close}, -2)
        self.fillplgfolders()

    def selectionChanged(self):
        try:
            fname = self['menu'].getCurrent()
            cindex = self['menu'].getSelectionIndex()
            filename = self.nfifiles[cindex][0]
            if filename.endswith(".zip") or filename.endswith('.nfi'):
               self['ButtonGreentext'].setText('Delete Image')
            else:
                self['ButtonGreentext'].setText(' ')  
        except:
            pass		
		
    def delimage(self):
         fname = self['menu'].getCurrent()
         cindex = self['menu'].getSelectionIndex()
         filename = self.folder + self.nfifiles[cindex][0]
         if filename.endswith(".zip") or filename.endswith('.nfi'):
            self['ButtonGreentext'].setText('Delete Image')
            self.session.openWithCallback(self.removefile, ScreenBox, _(filename + '\nwill Be Removed,\nAre You Sure ?'), ScreenBox.TYPE_YESNO)

         else:
            self['ButtonGreentext'].setText(' ')
			
    def removefile(self, result):
        if result:
            try:
                fname = self['menu'].getCurrent()
                cindex = self['menu'].getSelectionIndex()
                filename = self.folder + self.nfifiles[cindex][0]
                remove(filename)
                self.fillplgfolders()
            except:
                self.session.open(ScreenBox, _('Sorry, unable to delete file!'), type=ScreenBox.TYPE_ERROR, timeout=5, close_on_any_key=True)

    def fillplgfolders(self):
        try:
            self.nfifiles = []
            for x in listdir(self.folder):
                if os.path.isfile(self.folder + x):
                    if x.endswith('.nfi') or x.endswith('.zip'):
                        msize = os.path.getsize(self.folder + x)
                        localimagesize = str(round(float(msize / 1048576.0), 2))
                        self.nfifiles.append([x, localimagesize])

            self.ListToMulticontent()
        except:
            self.session.open(ScreenBox, _('Sorry, unable to show files, check ' + self.folder + '  is available and mounted!'), type=ScreenBox.TYPE_ERROR, timeout=5, close_on_any_key=True)

    def ListToMulticontent(self):
        res = []
        theevents = []
        self.events = []
        self.events = self.nfifiles
        if dwidth == 1280:
            self['menu'].l.setItemHeight(40)
            self['menu'].l.setFont(0, gFont('Sansation-Bold', 25))
            for i in range(0, len(self.events)):
                mfile = self.events[i][0]
                msize = self.events[i][1] + 'MB'
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 35), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(10, 5), size=(650, 35), font=0, flags=RT_HALIGN_LEFT, text=mfile))
                res.append(MultiContentEntryText(pos=(660, 5), size=(150, 35), font=0, flags=RT_HALIGN_LEFT, text=msize))
                theevents.append(res)
                res = []
        else:
            self['menu'].l.setItemHeight(45)
            self['menu'].l.setFont(0, gFont('Sansation-Bold', 35))
            for i in range(0, len(self.events)):
                mfile = self.events[i][0]
                msize = self.events[i][1] + 'MB'
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 40), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(10, 5), size=(650, 40), font=0, flags=RT_HALIGN_LEFT, text=mfile))
                res.append(MultiContentEntryText(pos=(660, 5), size=(150, 40), font=0, flags=RT_HALIGN_LEFT, text=msize))
                theevents.append(res)
                res = []

        self['menu'].l.setList(theevents)
        self['menu'].show()

class SelectLocation(Screen):

    def __init__(self, session, imageurl = None, imagesize = None):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/izberiHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/izberiFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.menu = 0
        self.imagesize = imagesize
        self.imageurl = imageurl
        self.list = []
        self.oktext = _('')
        self.text = ''
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        if self.menu == 0:
            self.list.append(('Download', _('Start Download'), None))
            self.list.append(('Downloadlocation', _('Choose Download Location'), None))
            self.list.append(('files', _('View Downloaded Images'), None))
        self['menu'] = List(self.list)
        self['status'] = StaticText('')
        self['targettext'] = StaticText(_('Selected Download Location:'))
        fname = os.path.basename(self.imageurl)
        if 'DreamEliteImages' in fname:
            a = []
            a = fname.split('=')
            fname = a[2]
        self['downloadtext'] = StaticText(_('Selected image to download:\n' + fname))
        fspace = str(freespace()) + 'MB'
        self['target'] = Label(config.plugins.ImageDownLoader2.Downloadlocation.value + '\nFree space:   ' + fspace)
        self['shortcuts'] = ActionMap(['ShortcutActions', 'WizardActions', 'InfobarEPGActions'], {'ok': self.go,
         'back': self.cancel,
         'red': self.cancel}, -1)
        self.onLayoutFinish.append(self.layoutFinished)
        return

    def layoutFinished(self):
        idx = 0
        self['menu'].index = idx

    def fnameexists(self):
        path = getDownloadPath()
        filename = path + os.path.basename(self.imageurl)
        if fileExists(filename):
            return True
        else:
            return False

    def callMyMsg(self, result):
        path = getDownloadPath()
        if self.checkmountDownloadPath(path) == False:
            return
        if result:
            if fileExists('/etc/init.d/flashexpander.sh'):
                self.session.open(ScreenBox, _('FlashExpander is used,no Image DownLoad possible.'), ScreenBox.TYPE_INFO)
                self.cancel()
            else:
                runDownload = True
                self.localfile = path + os.path.basename(self.imageurl)
                self.session.openWithCallback(self.cancel, Downloader, self.imageurl, self.localfile, path)

    def callMyMsg2(self, result):
        path = config.plugins.ImageDownLoader2.Downloadlocation.value
        if self.checkmountDownloadPath(path) == False:
            return
        if result:
            if fileExists('/etc/init.d/flashexpander.sh'):
                self.session.open(ScreenBox, _('FlashExpander is used,no Image DownLoad possible.'), ScreenBox.TYPE_INFO)
                self.cancel()
            else:
                runDownload = True
                self.session.open(makeSelectTelnet, runDownload, self.imageurl, self.imagesize, console=True)

    def checkmountDownloadPath(self, path):
        if path is None:
            self.session.open(ScreenBox, _('nothing entered'), ScreenBox.TYPE_ERROR)
            return False
        elif freespace() < 60:
            self.session.open(ScreenBox, _('Free space is less than 60MB,please choose another download location,or delete files from storage device'), ScreenBox.TYPE_ERROR)
            return False
        else:
            sp = []
            sp = path.split('/')
            print sp
            if len(sp) > 1:
                if sp[1] != 'media':
                    self.session.open(ScreenBox, mounted_string % path, ScreenBox.TYPE_ERROR)
                    return False
            mounted = False
            self.swappable = False
            sp2 = []
            f = open('/proc/mounts', 'r')
            m = f.readline()
            while m and not mounted:
                if m.find('/%s/%s' % (sp[1], sp[2])) is not -1:
                    mounted = True
                    print m
                    sp2 = m.split(' ')
                    print sp2
                    if sp2[2].startswith('ext') or sp2[2].endswith('fat'):
                        print '[stFlash] swappable'
                        self.swappable = True
                m = f.readline()

            f.close()
            if not mounted:
                self.session.open(ScreenBox, mounted_string + str(path), ScreenBox.TYPE_ERROR)
                return False
            if os.path.exists(config.plugins.ImageDownLoader2.Downloadlocation.value):
                try:
                    os.chmod(config.plugins.ImageDownLoader2.Downloadlocation.value, 511)
                except:
                    pass

            return True
            return

    def go(self):
        current = self['menu'].getCurrent()
        if current:
            currentEntry = current[0]
        if self.menu == 0:
            if currentEntry == 'settings':
                self.session.openWithCallback(self.updateSwap, SelectSetting)
            if currentEntry == 'Download':
                if not self.fnameexists() == True:
                    self.session.openWithCallback(self.callMyMsg, ScreenBox, _('You selected to download:\n' + self.imageurl + '\ncontinue ?'), ScreenBox.TYPE_YESNO)
                else:
                    self.session.openWithCallback(self.callMyMsg, ScreenBox, _('The file already exists,\n' + 'overwrite ?'), ScreenBox.TYPE_YESNO)
            if currentEntry == 'console':
                if not self.fnameexists() == True:
                    self.session.openWithCallback(self.callMyMsg2, ScreenBox, _('You selected to download  ' + self.imageurl + ',continue?'), ScreenBox.TYPE_YESNO)
                else:
                    self.session.openWithCallback(self.callMyMsg2, ScreenBox, _('The file aleady exists ' + ',overwrite?'), ScreenBox.TYPE_YESNO)
            if currentEntry == 'files':
                self.session.open(DownloadedFiles)
            elif currentEntry == 'Downloadlocation':
                self.session.openWithCallback(self.Downloadlocation_choosen, SelectDownloadLocation)

    def updateSwap(self, retval):
        self['swapsize'].setText(''.join(config.plugins.ImageDownLoader2.swap.value + ' MB'))

    def Downloadlocation_choosen(self, option):
        self.updateTarget()
        if option is not None:
            config.plugins.ImageDownLoader2.Downloadlocation.value = str(option[1])
        config.plugins.ImageDownLoader2.Downloadlocation.save()
        config.plugins.ImageDownLoader2.save()
        config.save()
        self.createDownloadfolders()
        return

    def createDownloadfolders(self):
        self.Downloadpath = getDownloadPath()
        try:
            if os_path.exists(self.Downloadpath) == False:
                makedirs(self.Downloadpath)
        except OSError:
            self.session.openWithCallback(self.goagaintoDownloadlocation, ScreenBox, _('Sorry, your Download destination is not writeable.\n\nPlease choose another one.'), ScreenBox.TYPE_ERROR)

    def goagaintoDownloadlocation(self, retval):
        self.session.openWithCallback(self.Downloadlocation_choosen, SelectDownloadLocation)

    def updateTarget(self):
        fspace = str(freespace()) + 'MB'
        self['target'].setText(''.join(config.plugins.ImageDownLoader2.Downloadlocation.value + ' Freespace:' + fspace))

    def DownloadDone(self, retval = None):
        if retval is False:
            self.session.open(ScreenBox, _(''), ScreenBox.TYPE_ERROR, timeout=10)
        elif config.plugins.ImageDownLoader2.update.value == True:
            self.session.open()
        else:
            self.cancel()

    def cancel(self, result = None):
        self.close(None)
        return

    def runUpgrade(self, result):
        if result:
            self.session.open()

class Downloader(Screen):

    def __init__(self, session, url = None, target = None, path = None):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/dlHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/dlFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        print url
        self.url = url
        self.target = target
        self.path = path
        self.nfifile = target
        self['info'] = Label('')
        self['info2'] = Label('')
        self['progress'] = ProgressBar()
        self.aborted = False
        self['progress'].setRange((0, 100))
        self['progress'].setValue(0)
        self.onLayoutFinish.append(self.startDownload)
        self['actions'] = ActionMap(['OkCancelActions'], {'cancel': self.cancel}, -1)
        self.connection = None
        return

    def startDownload(self):
        from Tools.Downloader import downloadWithProgress
        info = ' Downloading :\n %s ' % self.url
        self['info2'].setText(info)
        self.downloader = downloadWithProgress(self.url, self.target)
        self.downloader.addProgress(self.progress)
        self.downloader.start().addCallback(self.responseCompleted).addErrback(self.responseFailed)

    def progress(self, current, total):
        p = int(100 * (float(current) / float(total)))
        self['progress'].setValue(p)
        info = _('Downloading') + ' ' + '%d of %d kBytes' % (current / 1024, total / 1024)
        info = 'Downloading ... ' + str(p) + '%'
        self['info'].setText(info)
        self.setTitle(info)
        self.last_recvbytes = current

    def responseCompleted(self, string = ''):
        if self.aborted:
            self.finish(aborted=True)
        else:
            info = 'The image downloaded successfully !'
            self['info2'].setText(info)
            if self.target.endswith('.zip'):
                info = 'The image downloaded successfully !'
                self.session.openWithCallback(self.close, ScreenBox, _(info), type=ScreenBox.TYPE_INFO, timeout=3)
            elif self.target.endswith('.tar.xz'):
                info = 'The image downloaded successfully !'
                self.session.openWithCallback(self.close, ScreenBox, _(info), type=ScreenBox.TYPE_INFO, timeout=3)
            elif self.target.endswith('.nfi'):
                info = 'The image downloaded successfully !'
                self.session.openWithCallback(self.close, ScreenBox, _(info), type=ScreenBox.TYPE_INFO, timeout=3)				
            else:
                self.close
                return

    def responseFailed(self, failure_instance = None, error_message = ''):
        self.error_message = error_message
        if error_message == '' and failure_instance is not None:
            self.error_message = failure_instance.getErrorMessage()
        info = 'Download failed ' + self.error_message
        self['info2'].setText(info)
        self.session.openWithCallback(self.close, ScreenBox, _(info), timeout=3, close_on_any_key=True)
        return

    def cancel(self):
        if self.downloader is not None:
            info = 'You are going to abort download, are you sure ?'
            self.session.openWithCallback(self.abort, ScreenBox, _(info), type=ScreenBox.TYPE_YESNO)
        else:
            self.aborted = True
            self.close()
        return

    def abort(self, result = None):
        if result:
            self.downloader.stop
            self.aborted = True
            self.close()

    def exit(self, result = None):
        self.close()
		
