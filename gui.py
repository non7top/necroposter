

import glob, os, re, sip, time,sys
from dbus.service import method

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.kio import KFile, KFileDialog, KIO
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic

import dirs_ui

class dirsWidget(QWidget,dirs_ui.Ui_Widget):
    def __init__(self,parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.kcfg_url.setMode(KFile.Directory)

class PreferencesDialog(KConfigDialog):
    def __init__(self, parent, name, preferences):
        KConfigDialog.__init__(self, parent, name, preferences)
        self.page = dirsWidget(self)
        self.addPage(self.page, i18n("Storage setup"), 'media-dirs')

class Preferences(KConfigSkeleton):
    def __init__(self):
        KConfigSkeleton.__init__(self)
        self.setCurrentGroup("Storage")
        self.url = QString()
        #self.dirs.append('/mnt/storage/Anime')
        #self.dirs.append('/mnt/large/Anime')
        self.dirs = self.addItemString("url",self.url)
        self.readConfig()

    def url(self):
        return self.dirs.property().toString()

class necroMediaMainWindow(KXmlGuiWindow):
    def __init__(self):
        KXmlGuiWindow.__init__(self)
        #KMainWindow.__init__(self, *args)
        self.ui=uic.loadUi("nm.ui", self)
        #self.setupGUI()
        self.setWindowTitle("NecroMedia")
        self.mainlist=[]

        self.setupActions()
        #self.addMenu()
        self.readdirs()
        self.populateList()
        self.connect(self.ui.main_lw, SIGNAL("itemClicked(QListWidgetItem*)"),
                self.refresh_info)
        self.config=Preferences()
        self.setupGUI()         #after setup actions
        #self.showSettings()

    def setupActions(self):
        KStandardAction.preferences(self.showSettings, self.actionCollection())
        KStandardAction.quit(app.quit, self.actionCollection())

    def addMenu(self):
        helpMenu = KHelpMenu(self, KCmdLineArgs.aboutData())
        self.menuBar().addMenu(helpMenu.menu())
        #helpMenu.action(KHelpMenu.menuReportBug).setIcon(
        #    KIcon('tools-report-bug'))
        #helpMenu.action(KHelpMenu.menuAboutApp).setIcon(self._appIcon)
        whatsThis = helpMenu.action(KHelpMenu.menuWhatsThis)
        # TODO not added by default,
        # currently added to the wrong
        # place
        helpMenu.menu().addAction(whatsThis)
        return


        #create menu
        self.file = KMenu(self)
        #self.file.addAction(self.configureAction)
        #self.file.addAction(self.updateAction)
        self.file.addAction(self.quitAction)
        self.help = KMenu(self)
        self.help.addAction(self.helpAction)
 
        #create menu bar
        self.menuBar = KMenuBar(self)
        self.menuBar.addMenu(self.file)
        self.menuBar.addMenu(self.help)

    def populateList(self):
        for f in self.mainlist:
            self.ui.main_lw.addItem(f)

    def readdirs(self):
        dir='/mnt/virtual/Anime'
        d=QDir(dir)
        #d.setFilter(QDir.NoDotAndDotDot)
        flist=QStringList()
        flist=d.entryList()
        print flist.count()
        k=0
        while k < flist.count():
            f=flist[k]
            if f not in ('.', '..'):
                self.mainlist.append(f)
            k+=1

    def refresh_info(self):
        self.ui.lb_name.setText("kjds")
        cover=QPixmap()
        #pict='/home/non7top/.necroposter/cover/6714.jpg'
        if cover.load(pict):
            self.ui.lb_cover.setPixmap(cover)

    def showSettings(self):
       if(KConfigDialog.showDialog("settings")):
           return
       dialog = PreferencesDialog(self, "settings", self.config)
       dialog.show()



def about():
    appName     = "necromedia"
    catalog     = ""
    programName = ki18n("Necro Media")
    version     = "0.1"
    description = ki18n("Anime collection manager")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2009 Vladimir V. Berezhnoy")
    text        = ki18n("Very very long description")
    homePage    = "http://needsthinki.ng"
    bugEmail    = "non7top@gmail.com"

    aboutData = KAboutData(appName, catalog, programName, version, description,
        license, copyright, text, homePage, bugEmail)
    aboutData.addAuthor(ki18n("Vladimir V. Berezhnoy"), ki18n("Developer"),
        "non7top@gmail.com",
        "http://a.ru")

    return aboutData


def main():
    aboutdata = KAboutData(about())
    KCmdLineArgs.init(sys.argv, aboutdata)
    global app
    app = KApplication(1)
    #icon = KIcon("klxdvdrip.png")
    app.mainWindow=necroMediaMainWindow()
    #app.mainWindow.setWindowIcon(icon)
    app.mainWindow.show()
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    app.exec_()
    def quit(self):
        KApplication.quit(self)

if __name__=="__main__":
    main()


