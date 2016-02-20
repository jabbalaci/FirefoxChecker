#!/usr/bin/env python2
# encoding: utf-8

"""
A system tray icon indicates whether Firefox is running or not.

I use Firefox and I have lots of tabs opened in it (I'm lazy to delete
the old ones). As a result, when I close Firefox before shutting down
my machine, Firefox needs several seconds to fully close (on one of
my machines it's sometimes 20 seconds). The Firefox window disappears but
the process is still in the memory. If I shut down my machine at this time,
next time I reboot the machine and start Firefox I get a recovery message that
asks if I want to restore the tabs since FF wasn't shut down tidily.

So after closing FF I used to start the command "top" to monitor when FF
falls out of the memory. It was boring.

So I wrote this little program. It puts an icon in the system tray and indicates
if FF is running. The icon is colored if FF is running, otherwise it turns
grayscale.

Author: Laszlo Szathmary, alias Jabba Laci, 2016
Email:  jabba.laci@gmail.com
GitHub: https://github.com/jabbalaci/FirefoxChecker
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
from time import sleep

import psutil
from PySide import QtGui
from PySide.QtCore import QThread, Signal

import systray_rc

#PROCESS_NAME = 'gedit'  # for testing
PROCESS_NAME = 'firefox'
WAIT = 1.0


def is_process_running(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            return True
    #
    return False


class FirefoxCheckThread(QThread):
    changeIcon = Signal(int)

    def __init__(self, parent):
        super(FirefoxCheckThread, self).__init__(parent)
        self.parent = parent
        self.go = True

    def stop(self):
        self.go = False
        sleep(WAIT + 0.1)

    def run(self):
        while self.go:
            if is_process_running(PROCESS_NAME):
                self.changeIcon.emit(0)
            else:
                self.changeIcon.emit(1)
            #
            sleep(WAIT)


class Window(QtGui.QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.collectIcons()

        self.createActions()
        self.createTrayIcon()

        self.currentIcon = None    # not yet set
        if is_process_running(PROCESS_NAME):
            self.setIcon(0)
        else:
            self.setIcon(1)
        self.trayIcon.show()

        self.firefoxCheckThread = FirefoxCheckThread(self)
        self.firefoxCheckThread.start()

        self.firefoxCheckThread.changeIcon.connect(self.setIcon)

    def setIcon(self, index):
        if index == self.currentIcon:
            return
        # else
        icon = self.icons[index]
        self.trayIcon.setIcon(icon)
        self.currentIcon = index

    def collectIcons(self):
        self.icons = []
        self.icons.append(QtGui.QIcon(':/images/firefox.svg'))
        self.icons.append(QtGui.QIcon(':/images/firefox_bw.svg'))

    def createActions(self):
        self.quitAction = QtGui.QAction("&Quit", self, triggered=self.myQuit)

    def myQuit(self):
        self.firefoxCheckThread.stop()
        QtGui.qApp.quit()

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QtGui.QApplication.setQuitOnLastWindowClosed(False)

    window = Window()
    sys.exit(app.exec_())
