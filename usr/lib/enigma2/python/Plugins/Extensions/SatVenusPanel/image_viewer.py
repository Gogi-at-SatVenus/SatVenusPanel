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
import datetime
import urllib2
import gettext
import os
from image_downloader import process_mode
config.plugins.ImageDownLoader2 = ConfigSubsection()
config.plugins.ImageDownLoader2.Downloadlocation = ConfigText(default='/media/', visible_width=50, fixed_size=False)
dwidth = getDesktop(0).size().width()
currversion = 'eo2.0'
mountedDevs = []
for p in harddiskmanager.getMountedPartitions(True):
    mountedDevs.append((p.mountpoint, _(p.description) if p.description else ''))

mounted_string = 'Nothing mounted at '

p_path = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel'

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
		
class Feeds(Screen):

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
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
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
        self.data=process_mode(None)		
        if dwidth == 1280:
            self['text'].l.setItemHeight(34)
            self['text'].l.setFont(0, gFont('Sansation-Bold', 28))
            for i in range(0, len(self.data)):	
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 35), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 5), size=(720, 35), font=0, flags=RT_HALIGN_LEFT, text=str(self.data[i][0])))
                theevents.append(res)
                res = []

        else:
            self['text'].l.setItemHeight(50)
            self['text'].l.setFont(0, gFont('Sansation-Bold', 40))
            for i in range(0, len(self.data)):			
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 50), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 2), size=(720, 50), font=0, flags=RT_HALIGN_LEFT, text=str(self.data[i][0])))
                theevents.append(res)
                res = []

        self['text'].l.setList(theevents)
        self['text'].show()

    def okClicked(self):
        cindex = self['text'].getSelectionIndex()
        param=self.data[cindex][1]
        self.session.open(Servers,param)

class Servers(Screen):

    def __init__(self, session,param=None):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/serversHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/serversFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        self.list = []
        self['list'] = MenuList([], True, eListboxPythonMultiContent)
        self.addon = 'emu'
        self.icount = 0
        self.downloading = False
        self.param=param
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'green': self.okClicked,
         'red': self.close,
         'cancel': self.close}, -2)
        self.ListToMulticontent()
        return

    def ListToMulticontent(self):
        res = []
        theevents = []
        self.data=process_mode(self.param)
        if dwidth == 1280:
            self['list'].l.setItemHeight(34)
            self['list'].l.setFont(0, gFont('Sansation-Bold', 30))
            for i in range(0, len(self.data)):		
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 30), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 2), size=(840, 30), font=0, flags=RT_HALIGN_LEFT, text=str(self.data[i][0])))	
                theevents.append(res)
                res = []

        else:
            self['list'].l.setItemHeight(50)
            self['list'].l.setFont(0, gFont('Sansation-Bold', 40))
            for i in range(0, len(self.data)):
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 50), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 2), size=(1040, 50), font=0, flags=RT_HALIGN_LEFT, text=str(self.data[i][0])))
                theevents.append(res)
                res = []

        self['list'].l.setList(theevents)
		
    def okClicked(self):
        cindex = self['list'].getSelectionIndex()            
        param=self.data[cindex][1]
        print "param1",param
        self.session.open(ServerModels, param)		
			
class ServerModels(Screen):

    def __init__(self, session,param=None):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/serversHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/serversFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        self.list = []
        self['list'] = MenuList([], True, eListboxPythonMultiContent)
        self.addon = 'emu'
        self.icount = 0
        self.downloading = False
        self.downloading = True		
        self.param=param
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'green': self.okClicked,
         'red': self.close,
         'cancel': self.close}, -2)
        self.ListToMulticontent()
        return		

    def ListToMulticontent(self):
        res = []
        theevents = []
        self.data=process_mode(self.param)
        if dwidth == 1280:
            self['list'].l.setItemHeight(34)
            self['list'].l.setFont(0, gFont('Sansation-Bold', 30))
            for i in range(0, len(self.data)):		
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 30), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 2), size=(840, 30), font=0, flags=RT_HALIGN_LEFT, text=str(self.data[i][0])))	
                theevents.append(res)
                res = []

        else:
            self['list'].l.setItemHeight(50)
            self['list'].l.setFont(0, gFont('Sansation-Bold', 40))
            for i in range(0, len(self.data)):
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 50), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(30, 2), size=(1040, 50), font=0, flags=RT_HALIGN_LEFT, text=str(self.data[i][0])))
                theevents.append(res)
                res = []

        self['list'].l.setList(theevents)

    def okClicked(self):  
        cindex = self['list'].getSelectionIndex()
        param=self.data[cindex][1]        
        print "paramxx",param
        self.session.open(Images, param)
        return			
	
class Images(Screen):

    def __init__(self, session,param=None):
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/imagesHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/imagesFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['menu'] = MenuList([], True, eListboxPythonMultiContent)
        list = []
        self.list = list
        self.param=param 	
        self.status = []
        self.slist = []
        self['actions'] = ActionMap(['SetupActions', 'MenuActions', 'ColorActions'], {'ok': self.selclicked,
         'green': self.selclicked,
         'red': self.close,
         'cancel': self.close}, -2)
        self.itempreview = False
        self.timer = eTimer()
        self.timer.callback.append(self.ListToMulticontent)
        self.timer.start(100, 1)		

    def ListToMulticontent(self, result = None):
        downloadpath = getDownloadPath()
        res = []
        theevents = []
        print "self.param1",self.param		
        if dwidth == 1280:
            self['menu'].l.setItemHeight(80)
            self['menu'].l.setFont(0, gFont('Sansation-Bold', 24))
            self.data=process_mode(self.param)
            if len(self.data)==0:
              self['info'].setText("Failed to get or no images available !")
              return
            self['info'].setText("Press OK to download image !")			
            for i in range(0, len(self.data)):
                name=str(self.data[i][0])
                url = str(self.data[i][1])
                localname=os.path.split(url)[1]
                nfiname=localname.replace(".zip","nfi")
                if os.path.exists(downloadpath + localname) or os.path.exists(downloadpath + nfiname):
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/button_red.png'
                else:
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/button_green.png'
                res.append(MultiContentEntryText(pos=(0, 1), size=(5, 5), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryPixmapAlphaTest(pos=(20, 25), size=(30, 30), png=loadPNG(png)))
                res.append(MultiContentEntryText(pos=(40, 20), size=(930, 25), font=0, flags=RT_HALIGN_LEFT, text=name))
                theevents.append(res)
                res = []

        else:
            self['menu'].l.setItemHeight(80)
            self['menu'].l.setFont(0, gFont('Sansation-Bold', 34))
            self.data=process_mode(self.param)
            if len(self.data)==0:
              self['info'].setText("Failed to get or no images available !")
              return
            self['info'].setText("Press OK to download image !")			
            for i in range(0, len(self.data)):
                name=str(self.data[i][0])
                url = str(self.data[i][1])
                localname=os.path.split(url)[1]
                nfiname=localname.replace(".zip","nfi")
                if os.path.exists(downloadpath + localname) or os.path.exists(downloadpath + nfiname):
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/button_red.png'
                else:
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/button_green.png'
                res.append(MultiContentEntryText(pos=(0, 1), size=(5, 40), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 25), size=(30, 30), png=loadPNG(png)))
                res.append(MultiContentEntryText(pos=(40, 15), size=(1100, 40), font=0, flags=RT_HALIGN_LEFT, text=name))
                theevents.append(res)
                res = []

        self.theevents = []
        self.theevents = theevents
        self['menu'].l.setList(theevents)
        self['menu'].show()

    def selclicked(self):
        cindex = self['menu'].getSelectionIndex()
        try:
            param = self.data[cindex][1]
        except:
            return
        self.session.openWithCallback(self.ListToMulticontent, SelectLocation, param)

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
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        self.text = ''
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

    def cancel(self, result = None):
        self.close(None)
        return

    def runUpgrade(self, result):
        if result:
            self.session.open()
		
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
         '/srv',
         '/etc',
         '/share',
         '/usr',
         '/ba',
         '/MB_Images']
        inhibitMounts = ['/mnt', '/ba', '/MB_Images']
        self['filelist'] = FileList(currDir, showDirectories=True, showFiles=False, inhibitMounts=inhibitMounts, inhibitDirs=inhibitDirs)
#        self['mountlist'] = MenuList(mountedDevs)
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
            self.session.openWithCallback(self.removefile, ScreenBox, _(filename + '\nWill Be Removed,\nAre You Sure ?'), ScreenBox.TYPE_YESNO)

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
#                res.append(MultiContentEntryText(pos=(660, 5), size=(150, 35), font=0, flags=RT_HALIGN_LEFT, text=msize))
                theevents.append(res)
                res = []

        else:
            self['menu'].l.setItemHeight(45)
            self['menu'].l.setFont(0, gFont('Sansation-Bold', 35))
            for i in range(0, len(self.events)):
                mfile = self.events[i][0]
                msize = self.events[i][1] + 'MB'
                res.append(MultiContentEntryText(pos=(0, 5), size=(2, 40), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(10, 5), size=(860, 40), font=0, flags=RT_HALIGN_LEFT, text=mfile))
#                res.append(MultiContentEntryText(pos=(660, 5), size=(150, 40), font=0, flags=RT_HALIGN_LEFT, text=msize))
                theevents.append(res)
                res = []

        self['menu'].l.setList(theevents)
        self['menu'].show()

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

class ScreenBox(Screen):
    TYPE_YESNO = 0
    TYPE_INFO = 1
    TYPE_WARNING = 2
    TYPE_ERROR = 3
    TYPE_MESSAGE = 4

    def __init__(self, session, text, type = TYPE_YESNO, timeout = -1, close_on_any_key = False, default = True, enable_input = True, msgBoxID = None, picon = None, simple = False, list = [], timeout_default = None):
        self.type = type
        self.session = session
        if dwidth == 1280:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/sboxHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/sboxFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.msgBoxID = msgBoxID
        self['text'] = Label(text)
        self['Text'] = StaticText(text)
        self['selectedChoice'] = StaticText()
        self.text = text
        self.close_on_any_key = close_on_any_key
        self.timeout_default = timeout_default
        self['ErrorPixmap'] = Pixmap()
        self['QuestionPixmap'] = Pixmap()
        self['InfoPixmap'] = Pixmap()
        self['WarningPixmap'] = Pixmap()
        self.timerRunning = False
        self.initTimeout(timeout)
        picon = picon or type
        if picon != self.TYPE_ERROR:
            self['ErrorPixmap'].hide()
        if picon != self.TYPE_YESNO:
            self['QuestionPixmap'].hide()
        if picon != self.TYPE_INFO:
            self['InfoPixmap'].hide()
#        if picon != self.TYPE_WARNING:
#            self['WarningPixmap'].hide()
        self.title = self.type < self.TYPE_MESSAGE and [_('Question'),
         _('Information'),
         _('Warning'),
         _('Error')][self.type] or _('Message')
        if type == self.TYPE_YESNO:
            if list:
                self.list = list
            elif default == True:
                self.list = [(_('Yes'), True), (_('No'), False)]
            else:
                self.list = [(_('No'), False), (_('Yes'), True)]
        else:
            self.list = []
        self['list'] = MenuList(self.list)
        if self.list:
            self['selectedChoice'].setText(self.list[0][0])
        else:
            self['list'].hide()
        if enable_input:
            self['actions'] = ActionMap(['MsgBoxActions', 'DirectionActions'], {'cancel': self.cancel,
             'ok': self.ok,
             'alwaysOK': self.alwaysOK,
             'up': self.up,
             'down': self.down,
             'left': self.left,
             'right': self.right,
             'upRepeated': self.up,
             'downRepeated': self.down,
             'leftRepeated': self.left,
             'rightRepeated': self.right}, -1)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(self.title)

    def initTimeout(self, timeout):
        self.timeout = timeout
        if timeout > 0:
            self.timer = eTimer()
            try:
             self.timer_conn = self.timer.timeout.connect(self.timerTick)
            except:		
             self.timer.callback.append(self.timerTick)
            self.onExecBegin.append(self.startTimer)
            self.origTitle = None
            if self.execing:
                self.timerTick()
            else:
                self.onShown.append(self.__onShown)
            self.timerRunning = True
        else:
            self.timerRunning = False
        return

    def __onShown(self):
        self.onShown.remove(self.__onShown)
        self.timerTick()

    def startTimer(self):
        self.timer.start(1000)

    def stopTimer(self):
        if self.timerRunning:
            del self.timer
            self.onExecBegin.remove(self.startTimer)
            self.setTitle(self.origTitle)
            self.timerRunning = False

    def timerTick(self):
        if self.execing:
            self.timeout -= 1
            if self.origTitle is None:
                self.origTitle = self.instance.getTitle()
            self.setTitle(self.origTitle + ' (' + str(self.timeout) + ')')
            if self.timeout == 0:
                self.timer.stop()
                self.timerRunning = False
                self.timeoutCallback()
        return

    def timeoutCallback(self):
        print 'Timeout!'
        if self.timeout_default is not None:
            self.close(self.timeout_default)
        else:
            self.ok()
        return

    def cancel(self):
        self.close(False)

    def ok(self):
        if self.list:
            self.close(self['list'].getCurrent()[1])
        else:
            self.close(True)

    def alwaysOK(self):
        self.close(True)

    def up(self):
        self.move(self['list'].instance.moveUp)

    def down(self):
        self.move(self['list'].instance.moveDown)

    def left(self):
        self.move(self['list'].instance.pageUp)

    def right(self):
        self.move(self['list'].instance.pageDown)

    def move(self, direction):
        if self.close_on_any_key:
            self.close(True)
        self['list'].instance.moveSelection(direction)
        if self.list:
            self['selectedChoice'].setText(self['list'].getCurrent()[0])
        self.stopTimer()

    def __repr__(self):
        return str(type(self)) + '(' + self.text + ')'