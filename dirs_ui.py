
#!/usr/bin/env python
# Generated by pykdeuic4 from dirs.ui on Fri Feb 20 21:38:22 2009
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(508, 316)
        self.gridLayout = QtGui.QGridLayout(Widget)
        self.gridLayout.setObjectName("gridLayout")
        self.dirs = QtGui.QListWidget(Widget)
        self.dirs.setObjectName("dirs")
        self.gridLayout.addWidget(self.dirs, 0, 0, 1, 2)
        self.kcfg_url = KUrlRequester(Widget)
        self.kcfg_url.setObjectName("kcfg_url")
        self.gridLayout.addWidget(self.kcfg_url, 1, 0, 1, 1)
        self.pb_addurl = QtGui.QPushButton(Widget)
        self.pb_addurl.setObjectName("pb_addurl")
        self.gridLayout.addWidget(self.pb_addurl, 1, 1, 1, 1)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(kdecore.i18n("Form"))
        self.pb_addurl.setText(kdecore.i18n("PushButton"))

from PyKDE4.kio import KUrlRequester

if __name__ == '__main__':
    import sys
    global app
    class MainWin(kdeui.KMainWindow, Ui_Widget):
        def __init__ (self, *args):
            kdeui.KMainWindow.__init__ (self)
            rootWidget = QtGui.QWidget(self)
            self.setupUi(rootWidget)
            self.resize(640, 480)
            self.setCentralWidget(rootWidget)
    
    appName     = "default"
    catalog     = ""
    programName = kdecore.ki18n("default")
    version     = "1.0"
    description = kdecore.ki18n("Default Example")
    license     = kdecore.KAboutData.License_GPL
    copyright   = kdecore.ki18n("unknown")
    text        = kdecore.ki18n("none")
    homePage    = ""
    bugEmail    = "email"

    aboutData   = kdecore.KAboutData(appName, catalog, programName, version, description,
                              license, copyright, text, homePage, bugEmail)
    kdecore.KCmdLineArgs.init(sys.argv, aboutData)
    
    app = kdeui.KApplication()
    mainWindow = MainWin(None, "main window")
    mainWindow.show()
    app.connect (app, QtCore.SIGNAL ("lastWindowClosed ()"), app.quit)
    app.exec_ ()