from Screens.Screen import Screen
from Components.Sources.List import List
from Components.ActionMap import ActionMap
from Components.config import config
from Tools.LoadPixmap import LoadPixmap
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePicLoad
from Components.Label import Label
from Components.Button import Button
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.Harddisk import harddiskmanager
from Components.PluginComponent import plugins
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Plugins.Plugin import PluginDescriptor
from SettingsList import SettingsList, ActionBox
from image_viewer import ScreenBox
from Screens.MessageBox import MessageBox
import os
import shutil
import sys
from enigma import *
from Components.config import config, ConfigSubsection, ConfigText, ConfigYesNo
from time import *
from Components.Pixmap import Pixmap
from Components.config import getConfigListEntry, config
from urlparse import urlparse
import xml.etree.cElementTree
import httplib
import datetime
DESKHEIGHT = getDesktop(0).size().height()
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/fonts'
skin_path = '/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/Skin/'
from enigma import addFont
try:
    addFont('%s/Sansation-Bold.ttf' % plugin_path, 'Sansation-Bold', 100, 1)
except Exception as ex:
    print ex

TMP_SETTINGS_PWD = '/tmp/sl_settings_tmp'
TMP_IMPORT_PWD = '/tmp/sl_import_tmp'
ENIGMA2_SETTINGS_PWD = '/etc/enigma2'
ENIGMA2_TUXBOX_PWD = '/etc/tuxbox'
config.settingsloader = ConfigSubsection()
config.settingsloader.keepterrestrial = ConfigYesNo(False)
config.settingsloader.keepsatellitesxml = ConfigYesNo(False)
config.settingsloader.keepcablesxml = ConfigYesNo(False)
config.settingsloader.keepterrestrialxml = ConfigYesNo(False)
config.settingsloader.keepbouquets = ConfigText('', False)

class Settings_Menu(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = skin_path + 'SmenuHD.xml'
        else:
            skin = skin_path + 'SmenuFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.drawList = []
        self['list'] = List()
        self['ButtonRedtext'] = Label(_('Exit'))
        self['ButtonGreentext'] = Label(_('Please select ...'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'cancel': self.quit,
         'red': self.close,
         'green': self.openSelected,
         'ok': self.openSelected}, -2)
        self.refresh()

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='%s/images/%s' % (os.path.dirname(sys.modules[__name__].__file__), image))
        return (pixmap, description)

    def refresh(self):
        self.drawList = []
        self.drawList.append(self.buildListEntry(_('</ ciefp Settings >'), 'downloads.png'))
        self.drawList.append(self.buildListEntry(_('</ malimali Settings >'), 'downloads.png'))
        self.drawList.append(self.buildListEntry(_('</ Predr@g Settings >'), 'downloads.png'))
        self.drawList.append(self.buildListEntry(_('</ GioppyGio Settings >'), 'downloads.png'))
        self.drawList.append(self.buildListEntry(_('</ Catseye Settings >'), 'downloads.png'))
        self.drawList.append(self.buildListEntry(_('</ Vhannibal Settings >'), 'downloads.png'))
        self.drawList.append(self.buildListEntry(_('</ HDSC Settings >'), 'downloads.png'))
        self.drawList.append(self.buildListEntry(_('</ Bi58 Settings >'), 'downloads.png'))
        self.drawList.append(self.buildListEntry(_('</ Chveneburi  >'), 'downloads.png'))
#        self.drawList.append(self.buildListEntry(_('</ jprekpa2 >'), 'downloads.png'))		
        self['list'].setList(self.drawList)

    def openSelected(self):
        index = self['list'].getIndex()
        if index == 0:
            CiefpHelper(self.session).load()
        elif index == 1:
            MalimaliHelper(self.session).load()
        elif index == 2:
            PredragHelper(self.session).load()
        elif index == 3:
            GioppyGioHelper(self.session).load()
        elif index == 4:
            CatseyeHelper(self.session).load()
        elif index == 5:
            VhannibalHelper(self.session).load()
        elif index == 6:
            HDSCHelper(self.session).load()
        elif index == 7:
            Bi58Helper(self.session).load()
        elif index == 8:
            ChveneburiHelper(self.session).load()
        elif index == 9:
            jprekpa2Helper(self.session).load()			

    def quit(self):
        self.close()

Chveneburi_HOST = '178.63.156.75'
Chveneburi_PATH = '/paneladdons/Chveneburi/'

class ChveneburiHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(Chveneburi_HOST)
            conn.request('GET',Chveneburi_PATH + 'Chveneburi.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + Chveneburi_HOST +Chveneburi_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download Chveneburi list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download Chveneburi list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading Chveneburi list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

jprekpa2_HOST = '178.63.156.75'
jprekpa2_PATH = '/paneladdons/jprekpa2/'

class jprekpa2Helper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(jprekpa2_HOST)
            conn.request('GET', jprekpa2_PATH + 'jprekpa2.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + jprekpa2_HOST + jprekpa2_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download jprekpa2 list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download jprekpa2 list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading jprekpa2 list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)		

Bi58_HOST = '178.63.156.75'
Bi58_PATH = '/paneladdons/Bi58/'

class Bi58Helper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(Bi58_HOST)
            conn.request('GET', Bi58_PATH + 'bi58.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + Bi58_HOST + Bi58_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download Bi58 list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download Bi58 list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading Bi58 list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

HDSC_HOST = '178.63.156.75'
HDSC_PATH = '/paneladdons/HDSC/'

class HDSCHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(HDSC_HOST)
            conn.request('GET', HDSC_PATH + 'hdsc.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + HDSC_HOST + HDSC_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download HDSC list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download HDSC list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading HDSC list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

CIEFP_HOST = '178.63.156.75'
CIEFP_PATH = '/paneladdons/Ciefp/'

class CiefpHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(CIEFP_HOST)
            conn.request('GET', CIEFP_PATH + 'ciefp.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + CIEFP_HOST + CIEFP_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download ciefp list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download ciefp list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading ciefp list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

MALIMALI_HOST = '178.63.156.75'
MALIMALI_PATH = '/paneladdons/Malimali/'

class MalimaliHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(MALIMALI_HOST)
            conn.request('GET', MALIMALI_PATH + 'malimali.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + MALIMALI_HOST + MALIMALI_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download malimali list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download malimali list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading malimali list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

PREDRAG_HOST = '178.63.156.75'
PREDRAG_PATH = '/paneladdons/Predr@g/'

class PredragHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(PREDRAG_HOST)
            conn.request('GET', PREDRAG_PATH + 'predr@g.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + PREDRAG_HOST + PREDRAG_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download Predr@g list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download Predr@g list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading Predr@g list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

DONA_HOST = '178.63.156.75'
DONA_PATH = '/paneladdons/Don@/'

class DonaHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(DONA_HOST)
            conn.request('GET', DONA_PATH + 'don@.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + DONA_HOST + DONA_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download Don@ list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download Don@ list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading Don@ list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

GIOPPYGIO_HOST = '178.63.156.75'
GIOPPYGIO_PATH = '/paneladdons/GioppyGio/'

class GioppyGioHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(GIOPPYGIO_HOST)
            conn.request('GET', GIOPPYGIO_PATH + 'gioppygio.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + GIOPPYGIO_HOST + GIOPPYGIO_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download GioppyGio list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download GioppyGio list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading GioppyGio list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

CATSEYE_HOST = '178.63.156.75'
CATSEYE_PATH = '/paneladdons/Catseye/'

class CatseyeHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(CATSEYE_HOST)
            conn.request('GET', CATSEYE_PATH + 'catseye.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + CATSEYE_HOST + CATSEYE_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download Catseye list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download Catseye list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading Catseye list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

VHANNIBAL_HOST = '178.63.156.75'
VHANNIBAL_PATH = '/paneladdons/Vhannibal/'

class VhannibalHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(VHANNIBAL_HOST)
            conn.request('GET', VHANNIBAL_PATH + 'vhannibal.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + VHANNIBAL_HOST + VHANNIBAL_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download Vhannibal list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download Vhannibal list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading Vhannibal list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

class Satvenus(SettingsList):

    def __init__(self, session, list):
        self.session = session
        SettingsList.__init__(self, session, list)
        if DESKHEIGHT < 1000:
            skin = skin_path + 'SallHD.xml'
        else:
            skin = skin_path + 'SallFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()