from Screens.ChoiceBox import ChoiceBox
from Screens.InputBox import InputBox
from Components.FileList import FileList
import urllib
from urllib2 import urlopen
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Sources.List import List
from Components.MenuList import MenuList
import xml.dom.minidom
import os
import gettext
from Components.Button import Button
from Tools.Directories import fileExists
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from enigma import eListboxPythonMultiContent, getDesktop, gFont, loadPNG
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ServiceEventTracker import ServiceEventTracker
from enigma import iPlayableService, iServiceInformation, eServiceReference, eListboxPythonMultiContent, getDesktop, gFont, loadPNG
from Tools.LoadPixmap import LoadPixmap
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import config, ConfigDirectory, ConfigSubsection, ConfigSubList, ConfigEnableDisable, ConfigNumber, ConfigText, ConfigSelection, ConfigYesNo, ConfigPassword, getConfigListEntry, configfile
config.plugins.Cradio = ConfigSubsection()
config.plugins.Cradio.stations = ConfigSubList()
config.plugins.Cradio.stations_count = ConfigNumber(default=1)
version = ''
DESKHEIGHT = getDesktop(0).size().height()

def initProfileConfig():
    s = ConfigSubsection()
    s.name = ConfigText(default='')
    s.code = ConfigText(default='')
    config.plugins.Cradio.stations.append(s)
    return s

def initConfig():
    count = config.plugins.Cradio.stations_count.value
    if count != 0:
        i = 0
        while i < count:
            initProfileConfig()
            i += 1

initConfig()

def lsSelected():
    lst = []
    count = config.plugins.Cradio.stations_count.value
    if count != 0:
        for i in range(0, count):
            name = config.plugins.Cradio.stations[i].name.value
            code = config.plugins.Cradio.stations[i].code.value
            lst.append(name)

    else:
        lst = []
    return lst

Amenu_list = [_('Bosnia and Herzegovina'),
 _('Croatia'),
 _('Macedonia'),
 _('Montenegro'),
 _('Serbia'),
 _('Slovenia'),
 _('International'),
 _('Rock')]

class AmenuList(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        if DESKHEIGHT < 1000:
            self.l.setItemHeight(40)
            self.l.setFont(0, gFont('Days', 38))
        else:
            self.l.setItemHeight(72)
            self.l.setFont(0, gFont('Days', 70))

def AmenuListEntry(name, idx):
    res = [name]
    if idx == 0:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/icons/bosna.png'
    elif idx == 1:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/icons/hrvatska.png'
    elif idx == 2:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/icons/makedonija.png'
    if idx == 3:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/icons/crnagora.png'
    elif idx == 4:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/icons/srbija.png'
    elif idx == 5:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/icons/slovenija.png'
    elif idx == 6:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/icons/inter.png'
    elif idx == 7:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/icons/rock.png'
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 20), size=(40, 40), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(70, 5), size=(1000, 320), font=0, text=name))
    return res

class SatVenusScr(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self['text'] = AmenuList([])
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        self.working = False
        self.selection = 'all'
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'red': self.close,
         'green': self.okClicked,
         'cancel': self.close}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]

        list = []
        idx = 0
        for x in Amenu_list:
            list.append(AmenuListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1

        self['text'].setList(list)

    def okClicked(self):
        self.keyNumberGlobal(self['text'].getSelectedIndex())

    def keyNumberGlobal(self, idx):
        sel = self.menu_list[idx]
        if sel == _('Bosnia and Herzegovina'):
            self.session.open(BosScreen)
        elif sel == _('Croatia'):
            self.session.open(CroScreen)
        elif sel == _('Macedonia'):
            self.session.open(MacScreen)
        elif sel == _('Montenegro'):
            self.session.open(MonScreen)
        elif sel == _('Serbia'):
            self.session.open(SerScreen)
        elif sel == _('Slovenia'):
            self.session.open(SloScreen)
        elif sel == _('International'):
            self.session.open(IntScreen)
        elif sel == _('Rock'):
            self.session.open(SaleScreen)


class Favscreen(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radiofavHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radiofavFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self['key_red'] = Button(_('Exit'))
        self['key_yellow'] = Button(_('Delete'))
        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        try:
            self.session.nav.stopService()
        except:
            pass

        self.onClose.append(self.__onClose)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.ok,
         'green': self.ok,
         'yellow': self.Delselected,
         'red': self.close,
         'cancel': self.close}, -2)
        self.list = MenuList([])
        self['ButtonGreen'] = Pixmap()
        self['ButtonGreentext'] = Label(_('Play'))
        self['ButtonYellow'] = Pixmap()
        self['ButtonYellowtext'] = Label(_('Delete'))
        self['ButtonRed'] = Pixmap()
        self['ButtonRedtext'] = Label(_('Exit'))
        self['stationmenu'] = self.list
        lst = lsSelected()
        self.list.setList(lst)

    def Delselected(self):
        try:
            sel = self['stationmenu'].getSelectedIndex()
            config.plugins.Cradio.stations_count.value = config.plugins.Cradio.stations_count.value - 1
            config.plugins.Cradio.stations_count.save()
            del config.plugins.Cradio.stations[sel]
            config.plugins.Cradio.stations.save()
            config.plugins.Cradio.save()
            configfile.save()
            lst = []
            lst = lsSelected()
            self['stationmenu'].setList(lst)
            if config.plugins.Cradio.stations_count.value == 0:
                self['key_green'].hide()
            else:
                self['key_green'].show()
        except:
            pass

    def playServiceStream(self, url):
        try:
            self.session.nav.stopService()
            sref = eServiceReference(4097, 0, url)
            self.session.nav.playService(sref)
            self.currentStreamingURL = url
        except:
            pass

    def ok(self):
        try:
            station = self.list.getSelectionIndex()
            currentindex = station
            cname = config.plugins.Cradio.stations[station].code.value
            tup1 = cname.split(',')
            cstation = tup1[0]
            curl = tup1[1]
            self.currentStreamingURL = ''
            self.currentStreamingStation = ''
            self.session.nav.stopService()
            self.currentStreamingStation = cstation
            self.playServiceStream(curl)
            currentservice = self.CurrentService
            self.session.open(Playscreen, cstation, currentservice, currentindex)
        except:
            pass

    def playServiceStream(self, url):
        try:
            self.session.nav.stopService()
            sref = eServiceReference(4097, 0, url)
            self.session.nav.playService(sref)
            self.currentStreamingURL = url
        except:
            pass

    def __onClose(self):
        self.session.nav.playService(self.CurrentService)


class Playscreen(Screen):
    skin = '\n\t<screen name="Menu" position="center,center" size="1280,720" flags="wfNoBorder">\n\t<ePixmap position="0,0" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/menu.png" zPosition="-10" />\n\t<eLabel text="SatVenus Radio" position="40,12" size="600,60" noWrap="1" transparent="1" font="Regular;44" foregroundColor="red" valign="center" halign="center" />\n\t<eLabel text="Now playing ..." position="400,30" size="1280,80" noWrap="1" transparent="1" font="Regular; 36" foregroundColor="yellow" valign="center" halign="center" />\n\t<ePixmap position="910,500" size="300,150" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/pics/curafhd.png" alphatest="blend" transparent="1" />\n\t<widget name="station" position="100,350" zPosition="1" size="800,40" font="Regular;26" transparent="1" backgroundColor="#00000000"/>\n\t<widget name="titel" position="100,400" zPosition="1" size="1200,130" font="Regular;26" transparent="1"  backgroundColor="#00000000"/>\n\t</screen>'

    def __init__(self, session, stitle = None, currentservice = None, currentindex = None):
        self.skin = Playscreen.skin
        Screen.__init__(self, session)
        self['titel'] = Label()
        self['station'] = Label()
        self.currentindex = currentindex
        self['station'].setText(stitle)
        self.CurrentService = currentservice
        self.currentindex = currentindex
        self.onClose.append(self.__onClose)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evUpdatedInfo: self.__evUpdatedInfo})
        self['actions'] = ActionMap(['PiPSetupActions', 'SetupActions'], {'cancel': self.close}, -2)

    def playServiceStream(self, url):
        try:
            self.session.nav.stopService()
            sref = eServiceReference(4097, 0, url)
            self.session.nav.playService(sref)
            self.currentStreamingURL = url
        except:
            pass

    def __evUpdatedInfo(self):
        sTitle = ''
        currPlay = self.session.nav.getCurrentService()
        if currPlay is not None:
            sTitle = currPlay.info().getInfoString(iServiceInformation.sTagTitle)
        self['titel'].setText(sTitle)
        return

    def cancel(self):
        self.close

    def __onClose(self):
        self.session.nav.stopService()
	
class SaleScreen(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.onClose.append(self.__onClose)
        list = []
        self['ButtonGreentext'] = Label(_('Play'))
        self['ButtonRedtext'] = Label(_('Exit'))
        myfile = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/xml/rock'
        xmlparse = xml.dom.minidom.parse(myfile)
        self.xmlparse = xmlparse
        for stations in self.xmlparse.getElementsByTagName('rock'):
            for station in stations.getElementsByTagName('station'):
                list.append(station.getAttribute('name').encode('utf8'))
                list.sort()

        self['stationmenu'] = MenuList(list)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.selstation,
         'green': self.selstation,
         'cancel': self.close}, -2)

    def selstation(self):
        selection_station = self['stationmenu'].getCurrent()
        for stations in self.xmlparse.getElementsByTagName('rock'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    urlserver = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    pluginname = station.getAttribute('name').encode('utf8')
                    self.prombt(urlserver, pluginname)

    def prombt(self, com, dom):
        self.currentStreamingURL = ''
        self.currentStreamingStation = ''
        self.session.nav.stopService()
        self.currentStreamingStation = dom
        self.playServiceStream(com)

    def playServiceStream(self, url):
        self.session.nav.stopService()
        sref = eServiceReference(4097, 0, url)
        self.session.nav.playService(sref)
        self.currentStreamingURL = url

    def saveParameters(self):
        selection_station = self['stationmenu'].getCurrent()
        self.station = selection_station
        for stations in self.xmlparse.getElementsByTagName('rock'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    stationname = selection_station
                    url = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    self.url = url
                    self.station = stationname
                    current = initProfileConfig()
                    current.name.value = stationname
                    current.code.value = stationname + ',' + url
                    current.save()
                    config.plugins.Cradio.stations_count.value += 1
                    config.plugins.Cradio.stations_count.save()
                    config.plugins.Cradio.save()
                    configfile.save()

        self.session.open(MessageBox, _('Saved to Favorites'), MessageBox.TYPE_INFO, 2)

    def __onClose(self):
        self.session.nav.playService(self.CurrentService)

class IntScreen(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.onClose.append(self.__onClose)
        list = []
        self['ButtonGreentext'] = Label(_('Play'))
        self['ButtonRedtext'] = Label(_('Exit'))
        myfile = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/xml/inter'
        xmlparse = xml.dom.minidom.parse(myfile)
        self.xmlparse = xmlparse
        for stations in self.xmlparse.getElementsByTagName('inter'):
            for station in stations.getElementsByTagName('station'):
                list.append(station.getAttribute('name').encode('utf8'))

        list.sort()
        self['stationmenu'] = MenuList(list)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.selstation,
         'green': self.selstation,
         'red': self.close,
         'cancel': self.close}, -2)

    def selstation(self):
        selection_station = self['stationmenu'].getCurrent()
        for stations in self.xmlparse.getElementsByTagName('inter'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    urlserver = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    pluginname = station.getAttribute('name').encode('utf8')
                    self.prombt(urlserver, pluginname)

    def prombt(self, com, dom):
        self.currentStreamingURL = ''
        self.currentStreamingStation = ''
        self.session.nav.stopService()
        self.currentStreamingStation = dom
        self.playServiceStream(com)

    def playServiceStream(self, url):
        self.session.nav.stopService()
        sref = eServiceReference(4097, 0, url)
        self.session.nav.playService(sref)
        self.currentStreamingURL = url

    def saveParameters(self):
        selection_station = self['stationmenu'].getCurrent()
        self.station = selection_station
        for stations in self.xmlparse.getElementsByTagName('inter'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    stationname = selection_station
                    url = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    self.url = url
                    self.station = stationname
                    current = initProfileConfig()
                    current.name.value = stationname
                    current.code.value = stationname + ',' + url
                    current.save()
                    config.plugins.Cradio.stations_count.value += 1
                    config.plugins.Cradio.stations_count.save()
                    config.plugins.Cradio.save()
                    configfile.save()

        self.session.open(MessageBox, _('Saved to Favorites'), MessageBox.TYPE_INFO, 2)

    def __onClose(self):
        self.session.nav.playService(self.CurrentService)


class CroScreen(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.onClose.append(self.__onClose)
        list = []
        self['ButtonGreentext'] = Label(_('Play'))
        self['ButtonRedtext'] = Label(_('Exit'))
        myfile = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/xml/hrvatska'
        xmlparse = xml.dom.minidom.parse(myfile)
        self.xmlparse = xmlparse
        for stations in self.xmlparse.getElementsByTagName('hrvatska'):
            for station in stations.getElementsByTagName('station'):
                list.append(station.getAttribute('name').encode('utf8'))

        list.sort()
        self['stationmenu'] = MenuList(list)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.selstation,
         'green': self.selstation,
         'red': self.close,
         'cancel': self.close}, -2)

    def selstation(self):
        selection_station = self['stationmenu'].getCurrent()
        for stations in self.xmlparse.getElementsByTagName('hrvatska'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    urlserver = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    pluginname = station.getAttribute('name').encode('utf8')
                    self.prombt(urlserver, pluginname)

    def prombt(self, com, dom):
        self.currentStreamingURL = ''
        self.currentStreamingStation = ''
        self.session.nav.stopService()
        self.currentStreamingStation = dom
        self.playServiceStream(com)

    def playServiceStream(self, url):
        self.session.nav.stopService()
        sref = eServiceReference(4097, 0, url)
        self.session.nav.playService(sref)
        self.currentStreamingURL = url

    def saveParameters(self):
        selection_station = self['stationmenu'].getCurrent()
        self.station = selection_station
        for stations in self.xmlparse.getElementsByTagName('hrvatska'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    stationname = selection_station
                    url = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    self.url = url
                    self.station = stationname
                    current = initProfileConfig()
                    current.name.value = stationname
                    current.code.value = stationname + ',' + url
                    current.save()
                    config.plugins.Cradio.stations_count.value += 1
                    config.plugins.Cradio.stations_count.save()
                    config.plugins.Cradio.save()
                    configfile.save()

        self.session.open(MessageBox, _('Saved to Favorites'), MessageBox.TYPE_INFO, 2)

    def __onClose(self):
        self.session.nav.playService(self.CurrentService)


class BosScreen(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.onClose.append(self.__onClose)
        list = []
        self['ButtonGreentext'] = Label(_('Play'))
        self['ButtonRedtext'] = Label(_('Exit'))
        myfile = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/xml/bosna'
        xmlparse = xml.dom.minidom.parse(myfile)
        self.xmlparse = xmlparse
        for stations in self.xmlparse.getElementsByTagName('bosna'):
            for station in stations.getElementsByTagName('station'):
                list.append(station.getAttribute('name').encode('utf8'))

        list.sort()
        self['stationmenu'] = MenuList(list)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.selstation,
         'green': self.selstation,
         'cancel': self.close}, -2)

    def selstation(self):
        selection_station = self['stationmenu'].getCurrent()
        for stations in self.xmlparse.getElementsByTagName('bosna'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    urlserver = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    pluginname = station.getAttribute('name').encode('utf8')
                    self.prombt(urlserver, pluginname)

    def prombt(self, com, dom):
        self.currentStreamingURL = ''
        self.currentStreamingStation = ''
        self.session.nav.stopService()
        self.currentStreamingStation = dom
        self.playServiceStream(com)

    def playServiceStream(self, url):
        self.session.nav.stopService()
        sref = eServiceReference(4097, 0, url)
        self.session.nav.playService(sref)
        self.currentStreamingURL = url

    def saveParameters(self):
        selection_station = self['stationmenu'].getCurrent()
        self.station = selection_station
        for stations in self.xmlparse.getElementsByTagName('bosna'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    stationname = selection_station
                    url = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    self.url = url
                    self.station = stationname
                    current = initProfileConfig()
                    current.name.value = stationname
                    current.code.value = stationname + ',' + url
                    current.save()
                    config.plugins.Cradio.stations_count.value += 1
                    config.plugins.Cradio.stations_count.save()
                    config.plugins.Cradio.save()
                    configfile.save()

        self.session.open(MessageBox, _('Saved to Favorites'), MessageBox.TYPE_INFO, 2)

    def __onClose(self):
        self.session.nav.playService(self.CurrentService)


class SloScreen(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.onClose.append(self.__onClose)
        list = []
        self['ButtonGreentext'] = Label(_('Play'))
        self['ButtonRedtext'] = Label(_('Exit'))
        myfile = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/xml/slovenija'
        xmlparse = xml.dom.minidom.parse(myfile)
        self.xmlparse = xmlparse
        for stations in self.xmlparse.getElementsByTagName('slovenija'):
            for station in stations.getElementsByTagName('station'):
                list.append(station.getAttribute('name').encode('utf8'))
                list.sort()

        self['stationmenu'] = MenuList(list)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.selstation,
         'green': self.selstation,
         'cancel': self.close}, -2)

    def selstation(self):
        selection_station = self['stationmenu'].getCurrent()
        for stations in self.xmlparse.getElementsByTagName('slovenija'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    urlserver = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    pluginname = station.getAttribute('name').encode('utf8')
                    self.prombt(urlserver, pluginname)

    def prombt(self, com, dom):
        self.currentStreamingURL = ''
        self.currentStreamingStation = ''
        self.session.nav.stopService()
        self.currentStreamingStation = dom
        self.playServiceStream(com)

    def playServiceStream(self, url):
        self.session.nav.stopService()
        sref = eServiceReference(4097, 0, url)
        self.session.nav.playService(sref)
        self.currentStreamingURL = url

    def saveParameters(self):
        selection_station = self['stationmenu'].getCurrent()
        self.station = selection_station
        for stations in self.xmlparse.getElementsByTagName('slovenija'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    stationname = selection_station
                    url = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    self.url = url
                    self.station = stationname
                    current = initProfileConfig()
                    current.name.value = stationname
                    current.code.value = stationname + ',' + url
                    current.save()
                    config.plugins.Cradio.stations_count.value += 1
                    config.plugins.Cradio.stations_count.save()
                    config.plugins.Cradio.save()
                    configfile.save()

        self.session.open(MessageBox, _('Saved to Favorites'), MessageBox.TYPE_INFO, 2)

    def __onClose(self):
        self.session.nav.playService(self.CurrentService)


class MacScreen(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.onClose.append(self.__onClose)
        list = []
        self['ButtonGreentext'] = Label(_('Play'))
        self['ButtonRedtext'] = Label(_('Exit'))
        myfile = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/xml/makedonija'
        xmlparse = xml.dom.minidom.parse(myfile)
        self.xmlparse = xmlparse
        for stations in self.xmlparse.getElementsByTagName('makedonija'):
            for station in stations.getElementsByTagName('station'):
                list.append(station.getAttribute('name').encode('utf8'))

        list.sort()
        self['stationmenu'] = MenuList(list)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.selstation,
         'green': self.selstation,
         'cancel': self.close}, -2)

    def selstation(self):
        selection_station = self['stationmenu'].getCurrent()
        for stations in self.xmlparse.getElementsByTagName('makedonija'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    urlserver = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    pluginname = station.getAttribute('name').encode('utf8')
                    self.prombt(urlserver, pluginname)

    def prombt(self, com, dom):
        self.currentStreamingURL = ''
        self.currentStreamingStation = ''
        self.session.nav.stopService()
        self.currentStreamingStation = dom
        self.playServiceStream(com)

    def playServiceStream(self, url):
        self.session.nav.stopService()
        sref = eServiceReference(4097, 0, url)
        self.session.nav.playService(sref)
        self.currentStreamingURL = url

    def saveParameters(self):
        selection_station = self['stationmenu'].getCurrent()
        self.station = selection_station
        for stations in self.xmlparse.getElementsByTagName('makedonija'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    stationname = selection_station
                    url = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    self.url = url
                    self.station = stationname
                    current = initProfileConfig()
                    current.name.value = stationname
                    current.code.value = stationname + ',' + url
                    current.save()
                    config.plugins.Cradio.stations_count.value += 1
                    config.plugins.Cradio.stations_count.save()
                    config.plugins.Cradio.save()
                    configfile.save()

        self.session.open(MessageBox, _('Saved to Favorites'), MessageBox.TYPE_INFO, 2)

    def __onClose(self):
        self.session.nav.playService(self.CurrentService)


class MonScreen(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.onClose.append(self.__onClose)
        list = []
        self['ButtonGreentext'] = Label(_('Play'))
        self['ButtonRedtext'] = Label(_('Exit'))
        myfile = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/xml/crnagora'
        xmlparse = xml.dom.minidom.parse(myfile)
        self.xmlparse = xmlparse
        for stations in self.xmlparse.getElementsByTagName('crnagora'):
            for station in stations.getElementsByTagName('station'):
                list.append(station.getAttribute('name').encode('utf8'))

        list.sort()
        self['stationmenu'] = MenuList(list)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.selstation,
         'green': self.selstation,
         'cancel': self.close}, -2)

    def selstation(self):
        selection_station = self['stationmenu'].getCurrent()
        for stations in self.xmlparse.getElementsByTagName('crnagora'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    urlserver = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    pluginname = station.getAttribute('name').encode('utf8')
                    self.prombt(urlserver, pluginname)

    def prombt(self, com, dom):
        self.currentStreamingURL = ''
        self.currentStreamingStation = ''
        self.session.nav.stopService()
        self.currentStreamingStation = dom
        self.playServiceStream(com)

    def playServiceStream(self, url):
        self.session.nav.stopService()
        sref = eServiceReference(4097, 0, url)
        self.session.nav.playService(sref)
        self.currentStreamingURL = url

    def saveParameters(self):
        selection_station = self['stationmenu'].getCurrent()
        self.station = selection_station
        for stations in self.xmlparse.getElementsByTagName('crnagora'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    stationname = selection_station
                    url = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    self.url = url
                    self.station = stationname
                    current = initProfileConfig()
                    current.name.value = stationname
                    current.code.value = stationname + ',' + url
                    current.save()
                    config.plugins.Cradio.stations_count.value += 1
                    config.plugins.Cradio.stations_count.save()
                    config.plugins.Cradio.save()
                    configfile.save()

        self.session.open(MessageBox, _('Saved to Favorites'), MessageBox.TYPE_INFO, 2)

    def __onClose(self):
        self.session.nav.playService(self.CurrentService)


class SerScreen(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllHD.xml'
        else:
            skin = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/radioAllFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.CurrentService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.onClose.append(self.__onClose)
        list = []
        self['ButtonGreentext'] = Label(_('Play'))
        self['ButtonRedtext'] = Label(_('Exit'))
        myfile = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/xml/srbija'
        xmlparse = xml.dom.minidom.parse(myfile)
        self.xmlparse = xmlparse
        for stations in self.xmlparse.getElementsByTagName('srbija'):
            for station in stations.getElementsByTagName('station'):
                list.append(station.getAttribute('name').encode('utf8'))

        list.sort()
        self['stationmenu'] = MenuList(list)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': self.selstation,
         'ok': self.selstation,
         'red': self.close,
         'cancel': self.close}, -2)

    def selstation(self):
        selection_station = self['stationmenu'].getCurrent()
        for stations in self.xmlparse.getElementsByTagName('srbija'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    urlserver = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    pluginname = station.getAttribute('name').encode('utf8')
                    self.prombt(urlserver, pluginname)

    def prombt(self, com, dom):
        self.currentStreamingURL = ''
        self.currentStreamingStation = ''
        self.session.nav.stopService()
        self.currentStreamingStation = dom
        self.playServiceStream(com)

    def playServiceStream(self, url):
        self.session.nav.stopService()
        sref = eServiceReference(4097, 0, url)
        self.session.nav.playService(sref)
        self.currentStreamingURL = url

    def saveParameters(self):
        selection_station = self['stationmenu'].getCurrent()
        self.station = selection_station
        for stations in self.xmlparse.getElementsByTagName('srbija'):
            for station in stations.getElementsByTagName('station'):
                if station.getAttribute('name').encode('utf8') == selection_station:
                    stationname = selection_station
                    url = str(station.getElementsByTagName('url')[0].childNodes[0].data)
                    self.url = url
                    self.station = stationname
                    current = initProfileConfig()
                    current.name.value = stationname
                    current.code.value = stationname + ',' + url
                    current.save()
                    config.plugins.Cradio.stations_count.value += 1
                    config.plugins.Cradio.stations_count.save()
                    config.plugins.Cradio.save()
                    configfile.save()

        self.session.open(MessageBox, _('Saved to Favorites'), MessageBox.TYPE_INFO, 2)

    def __onClose(self):
        self.session.nav.playService(self.CurrentService)