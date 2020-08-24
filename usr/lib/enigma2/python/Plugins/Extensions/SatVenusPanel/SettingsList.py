from Screens.Screen import Screen
from Components.config import getConfigListEntry, config
from Components.Sources.List import List
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.Button import Button
from urlparse import urlparse
import xml.etree.cElementTree
from enigma import getDesktop
from Components.Label import Label
from Components.Pixmap import Pixmap
from Tools.Directories import SCOPE_CURRENT_SKIN, resolveFilename
from enigma import eTimer, getDesktop
from Screens.MessageBox import MessageBox
from image_viewer import ScreenBox
import os
import sys
import httplib
import shutil
import os
dwidth = getDesktop(0).size().width()
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

class SettingsList(Screen):

    def __init__(self, session, list):
        Screen.__init__(self, session)
        self.session = session
        self.drawList = []
        self.list = list
        for entry in self.list:
            self.drawList.append(self.buildListEntry(entry[0], entry[1]))

        self['list'] = List(self.drawList)
        self['ButtonRedtext'] = Label(_('Exit'))
        self['key_green'] = Label(_('OK'))
        self['info'] = Label(_('Please select to install ...'))
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': self.ok,
         'green': self.ok,
         'red': self.quit,
         'cancel': self.quit}, -2)

    def buildListEntry(self, sat, date):
        return (sat, date)

    def download(self):
        try:
            shutil.rmtree(TMP_IMPORT_PWD)
        except:
            pass

        os.mkdir(TMP_IMPORT_PWD)
        url = urlparse(self.url)
        try:
            conn = httplib.HTTPConnection(url.netloc)
            conn.request('GET', url.path)
            httpres = conn.getresponse()
            if httpres.status == 200:
                tmp = url.path.split('/')
                filename = TMP_IMPORT_PWD + '/' + tmp[len(tmp) - 1]
                out = open(filename, 'w')
                out.write(httpres.read())
                out.close()
                Deflate().deflate(filename)
            else:
                self.session.open(ScreenBox, _('Cannot download settings (%s)') % self.url, ScreenBox.TYPE_ERROR)
                return
        except Exception as e:
            print e
            self.session.open(ScreenBox, _('Cannot download settings (%s)') % self.url, ScreenBox.TYPE_ERROR)
            return

        settings = Settings()
        settings.apply()
        try:
            shutil.rmtree(TMP_SETTINGS_PWD)
        except Exception as e:
            print e

        try:
            shutil.rmtree(TMP_IMPORT_PWD)
        except Exception as e:
            print e

        self.session.open(ScreenBox, _('Settings installed'), type=ScreenBox.TYPE_INFO, timeout=2)

    def ok(self):
        if len(self.list) == 0:
            return
        index = self['list'].getIndex()
        self.url = self.list[index][2]
        self.session.open(ActionBox, _('Downloading settings'), _('Downloading ...'), self.download)

    def quit(self):
        self.close()

class Deflate:

    def __init__(self):
        pass

    def deflateZip(self, filename):
        zip = zipfile.ZipFile(filename, 'r')
        try:
            shutil.rmtree(TMP_SETTINGS_PWD)
        except:
            pass

        os.mkdir(TMP_SETTINGS_PWD)
        files = zip.namelist()
        for file in files:
            if file[-1:] == '/':
                continue
            buff = zip.read(file)
            tmp = file.split('/')
            file = tmp[len(tmp) - 1]
            out = open(TMP_SETTINGS_PWD + '/' + file, 'w')
            out.write(buff)
            out.close()

    def deflateTar(self, filename):
        try:
            shutil.rmtree(TMP_SETTINGS_PWD)
        except:
            pass

        os.mkdir(TMP_SETTINGS_PWD)
        os.system('tar zxf ' + filename + ' -C ' + TMP_SETTINGS_PWD)
        os.system('cd ' + TMP_SETTINGS_PWD + ' && find -type f -exec mv {} . \\;')

    def deflateIpk(self, filename):
        try:
            shutil.rmtree(TMP_SETTINGS_PWD)
        except:
            pass

        os.mkdir(TMP_SETTINGS_PWD)
        os.system('cp ' + filename + ' ' + TMP_SETTINGS_PWD + '/tmp.ipk')
        os.system('cd ' + TMP_SETTINGS_PWD + ' && ar -x tmp.ipk')
        os.system('tar zxf ' + TMP_SETTINGS_PWD + '/data.tar.gz -C ' + TMP_SETTINGS_PWD)
        os.system('cd ' + TMP_SETTINGS_PWD + ' && find -type f -exec mv {} . \\;')

    def deflate(self, filename):
        if filename[-4:] == '.zip':
            self.deflateZip(filename)
        elif filename[-7:] == '.tar.gz' or filename[-8:] == '.tgz':
            self.deflateTar(filename)
        elif filename[-4:] == '.ipk':
            self.deflateIpk(filename)

from enigma import eDVBDB
from Components.config import config
import re
import shutil

class Settings:

    def __init__(self):
        self.providers = []
        self.providersT = []
        self.services = []
        self.servicesT = []

    def read(self, pwd):
        self.providers = []
        self.services = []
        try:
            f = open(pwd + '/lamedb')
        except Exception as e:
            print e
            return

        while True:
            line = f.readline()
            if line == '':
                return
            line = line.strip()
            if line == 'transponders':
                break

        while True:
            line = f.readline()
            if line == '':
                return
            line = line.strip()
            if line == 'end':
                break
            line2 = f.readline().strip()
            line3 = f.readline().strip()
            self.providers.append([line.split(':'), line2.split(':'), line3.split(':')])

        while True:
            line = f.readline()
            if line == '':
                return
            line = line.strip()
            if line == 'services':
                break

        while True:
            line = f.readline()
            if line == '':
                return
            line = line.strip()
            if line == 'end':
                break
            line2 = f.readline().strip('\n')
            line3 = f.readline().strip('\n')
            self.services.append([line.split(':'), line2.split(':'), line3.split(':')])

        f.close()

    def write(self, pwd):
        try:
            f = open(pwd + '/lamedb', 'w')
        except Exception as e:
            print e
            return

        f.write('eDVB services /4/\n')
        f.write('transponders\n')
        for provider in self.providers:
            f.write(':'.join(provider[0]) + '\n')
            f.write('\t' + ':'.join(provider[1]) + '\n')
            f.write(':'.join(provider[2]) + '\n')

        f.write('end\n')
        f.write('services\n')
        for service in self.services:
            f.write(':'.join(service[0]) + '\n')
            f.write(':'.join(service[1]) + '\n')
            f.write(':'.join(service[2]) + '\n')

        f.write('end\n')
        f.write('Have a lot of bugs!\n')
        f.close()

    def saveTerrestrial(self):
        providersT = []
        servicesT = []
        for provider in self.providers:
            if provider[1][0][:1] == 't':
                providersT.append(provider)

        for service in self.services:
            for provider in providersT:
                if service[0][1] == provider[0][0] and service[0][2] == provider[0][1] and service[0][3] == provider[0][2]:
                    servicesT.append(service)

        self.providersT = providersT
        self.servicesT = servicesT

    def restoreTerrestrial(self):
        tmp = self.providersT
        for provider in self.providers:
            if provider[1][0][:1] != 't':
                tmp.append(provider)

        self.providers = tmp
        tmp = self.servicesT
        for service in self.services:
            if service[0][1][:4] != 'eeee':
                tmp.append(service)

        self.services = tmp

    def readBouquetsTvList(self, pwd):
        return self.readBouquetsList(pwd, 'bouquets.tv')

    def readBouquetsRadioList(self, pwd):
        return self.readBouquetsList(pwd, 'bouquets.radio')

    def readBouquetsList(self, pwd, bouquetname):
        try:
            f = open(pwd + '/' + bouquetname)
        except Exception as e:
            print e
            return

        ret = []
        while True:
            line = f.readline()
            if line == '':
                break
            if line[:8] != '#SERVICE':
                continue
            tmp = line.strip().split(':')
            line = tmp[len(tmp) - 1]
            filename = None
            if line[:12] == 'FROM BOUQUET':
                tmp = line[13:].split(' ')
                filename = tmp[0].strip('"')
            else:
                filename = line
            if filename:
                try:
                    fb = open(pwd + '/' + filename)
                except Exception as e:
                    print e
                    continue

                tmp = fb.readline().strip()
                if tmp[:6] == '#NAME ':
                    ret.append([filename, tmp[6:]])
                else:
                    ret.append([filename, filename])
                fb.close()

        return ret

    def copyBouquetsTv(self, srcpwd, dstpwd, keeplist):
        return self.copyBouquets(srcpwd, dstpwd, 'bouquets.tv', keeplist)

    def copyBouquetsRadio(self, srcpwd, dstpwd, keeplist):
        return self.copyBouquets(srcpwd, dstpwd, 'bouquets.radio', keeplist)

    def copyBouquets(self, srcpwd, dstpwd, bouquetname, keeplist):
        srclist = self.readBouquetsList(srcpwd, bouquetname)
        dstlist = self.readBouquetsList(dstpwd, bouquetname)
        if srclist is None:
            srclist = []
        if dstlist is None:
            dstlist = []
        count = 0
        for item in dstlist:
            if item[0] in keeplist:
                found = False
                for x in srclist:
                    if x[0] == item[0]:
                        found = True
                        break

                if not found:
                    srclist.insert(count, item)
            else:
                os.remove(dstpwd + '/' + item[0])
            count += 1

        for x in srclist:
            if x[0] not in keeplist:
                try:
                    shutil.copyfile(srcpwd + '/' + x[0], dstpwd + '/' + x[0])
                except:
                    pass

        try:
            f = open(dstpwd + '/' + bouquetname, 'w')
        except Exception as e:
            print e
            return

        if bouquetname[-3:] == '.tv':
            f.write('#NAME Bouquets (TV)\n')
        else:
            f.write('#NAME Bouquets (Radio)\n')
        for x in srclist:
            if bouquetname[-3:] == '.tv':
                f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + x[0] + '" ORDER BY bouquet\n')
            else:
                f.write('#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "' + x[0] + '" ORDER BY bouquet\n')

        return

    def apply(self):
        if config.settingsloader.keepterrestrial.value:
            self.read(ENIGMA2_SETTINGS_PWD)
            self.saveTerrestrial()
            self.read(TMP_SETTINGS_PWD)
            self.restoreTerrestrial()
            self.write(ENIGMA2_SETTINGS_PWD)
            keeplist = config.settingsloader.keepbouquets.value.split('|')
        else:
            self.read(TMP_SETTINGS_PWD)
            self.write(ENIGMA2_SETTINGS_PWD)
            keeplist = []
        self.copyBouquets(TMP_SETTINGS_PWD, ENIGMA2_SETTINGS_PWD, 'bouquets.tv', keeplist)
        self.copyBouquets(TMP_SETTINGS_PWD, ENIGMA2_SETTINGS_PWD, 'bouquets.radio', keeplist)
        if not config.settingsloader.keepsatellitesxml.value:
            try:
                shutil.copyfile(TMP_SETTINGS_PWD + '/satellites.xml', ENIGMA2_TUXBOX_PWD + '/satellites.xml')
            except Exception as e:
                print e

        if not config.settingsloader.keepcablesxml.value:
            try:
                shutil.copyfile(TMP_SETTINGS_PWD + '/cables.xml', ENIGMA2_TUXBOX_PWD + '/cables.xml')
            except Exception as e:
                print e

        if not config.settingsloader.keepterrestrialxml.value:
            try:
                shutil.copyfile(TMP_SETTINGS_PWD + '/terrestrial.xml', ENIGMA2_TUXBOX_PWD + '/terrestrial.xml')
            except Exception as e:
                print e

        try:
            shutil.copyfile(TMP_SETTINGS_PWD + '/whitelist', ENIGMA2_SETTINGS_PWD + '/whitelist')
        except Exception as e:
            print e

        try:
            shutil.copyfile(TMP_SETTINGS_PWD + '/blacklist', ENIGMA2_SETTINGS_PWD + '/blacklist')
        except Exception as e:
            print e

        eDVBDB.getInstance().reloadServicelist()
        eDVBDB.getInstance().reloadBouquets()

class ActionBox(Screen):

    def __init__(self, session, message, title, action):
        self.session = session
        if DESKHEIGHT < 1000:
            skin = skin_path + 'akcionHD.xml'
        else:
            skin = skin_path + 'akcionFHD.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.ctitle = title
        self.caction = action
        self['message'] = Label(message)
        self['logo'] = Pixmap()
        self.timer = eTimer()
        try:
            self.timer_conn = self.timer.timeout.connect(self.__setTitle)
        except:
            self.timer.callback.append(self.__setTitle)
        self.timer.start(200, 1)

    def __setTitle(self):
        if self['logo'].instance is not None:
            self['logo'].instance.setPixmapFromFile(os.path.dirname(sys.modules[__name__].__file__) + '/images/run.png')
        self.setTitle(self.ctitle)
        self.timer = eTimer()
        try:
            self.timer_conn = self.timer.timeout.connect(self.__start)
        except:
            self.timer.callback.append(self.__start)
        self.timer.start(200, 1)
        return

    def __start(self):
        self.close(self.caction())