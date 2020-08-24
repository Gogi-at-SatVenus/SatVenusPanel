from Components.Pixmap import Pixmap
from Tools.Directories import SCOPE_CURRENT_SKIN, resolveFilename
from enigma import eTimer
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

class MileSettings_Menu(Screen):

    def __init__(self, session):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = skin_path + 'MSmenuHD.xml'
        else:
            skin = skin_path + 'MSmenuFHD.xml'
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
        self.drawList.append(self.buildListEntry(_('</ Motor Settings >'), 'downloads.png'))
        self.drawList.append(self.buildListEntry(_('</ Multifeed Settings >'), 'downloads.png'))
        self['list'].setList(self.drawList)

    def openSelected(self):
        index = self['list'].getIndex()
        if index == 0:
            MotorHelper(self.session).load()
        elif index == 1:
            MultifeedHelper(self.session).load()

    def quit(self):
        self.close()

from Components.config import getConfigListEntry, config
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePicLoad
from urlparse import urlparse
import xml.etree.cElementTree
import httplib
import datetime
MOTOR_HOST = '178.63.156.75'
MOTOR_PATH = '/tarGz/'

class MotorHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(MOTOR_HOST)
            conn.request('GET', MOTOR_PATH + 'motor.xml')
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
                        url = 'http://' + MOTOR_HOST + MOTOR_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download motor list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download motor list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading motor list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(Satvenus, self.list)

MULTI_HOST = '178.63.156.75'
MULTI_PATH = '/tarGz/'

class MultifeedHelper(Screen):

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(MULTI_HOST)
            conn.request('GET', MULTI_PATH + 'multi.xml')
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
                        url = 'http://' + MULTI_HOST + MULTI_PATH + node.get('filename')
                        self.list.append([sat, date, url])

            else:
                self.session.open(ScreenBox, _('Cannot download multifeed list'), ScreenBox.TYPE_ERROR, timeout=2)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download multifeed list'), ScreenBox.TYPE_ERROR, timeout=2)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, ActionBox, _('Downloading multifeed list'), _('Downloading ...'), self.download)

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