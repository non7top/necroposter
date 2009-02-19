

import glob, os, re, sip, time,sys
from dbus.service import method

'''
from PyQt4.QtCore import QObject, QString, QTimer, QVariant, Qt, SIGNAL
from PyQt4.QtGui import QActionGroup, QLabel, QStackedWidget, QWidget
from PyKDE4.kdecore import KConfig, KGlobal, KUrl, i18n
from PyKDE4.kdeui import (
    KActionMenu, KApplication, KDialog, KIcon, KLineEdit, KMessageBox,
    KStandardAction, KVBox)
from PyKDE4.kparts import KParts
from PyKDE4.ktexteditor import KTextEditor
'''
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic


class necroMediaMainWindow(KMainWindow):
    def __init__(self, *args):
        KMainWindow.__init__(self, *args)
        self.ui=uic.loadUi("nm.ui", self)
        self.setWindowTitle("NecroMedia")
        self.mainlist=[]

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 0)
        self.progressBar.setVisible(False)
        self.progressBar.setMaximumSize(90,25)
        self.statusBar().addWidget(self.progressBar)
        self.addActions()
        self.addMenu()
        self.readdirs()
        self.populateList()
        self.connect(self.ui.main_lw, SIGNAL("itemClicked(QListWidgetItem*)"),
                self.refresh_info)

    def addActions(self):
        actions = KActionCollection(self)
        self.quitAction = KStandardAction.quit(self.close, actions)
        #self.configureAction = KAction(self)
        #self.configureAction.setIcon(QIcon (self.icons.loadIcon("configure", KIconLoader.Desktop)))
        #self.connect(self.configureAction, SIGNAL("triggered()"), self.showConfigDialog)
        #self.updateAction = KAction(self)
        #self.updateAction.setIcon(QIcon (self.icons.loadIcon("knetattach", KIconLoader.Desktop)))
        #self.configureAction.setIcon(QIcon('package_settings.png'))
        #self.connect(self.updateAction, SIGNAL("triggered()"), self.checkForUpdate)
        self.helpAction = KAction(self)
        #self.helpAction.setIcon(QIcon (installPath + "/icons/" + 'info.png'))
        #self.connect(self.helpAction, SIGNAL("triggered()"), self.showAboutAppDialog)

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
        dir='/home/non7top/anime'
        d=QDir(dir)
        #d.setFilter(QDir.NoDotAndDotDot)
        flist=QStringList()
        flist=d.entryList()
        k=0
        while k < flist.count():
            f=flist[k]
            if f not in ('.', '..'):
                self.mainlist.append(f)
            k+=1

    def refresh_info(self):
        self.ui.lb_name.setText("kjds")
        cover=QPixmap()
        cover.load('/home/non7top/.necroposter/cover/6714.jpg')
        self.ui.lb_cover.setPixmap(cover)




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


