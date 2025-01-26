#!/usr/bin/env python3

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

Author: Laszlo Szathmary, alias Jabba Laci, 2016, 2025
Email:  jabba.laci@gmail.com
GitHub: https://github.com/jabbalaci/FirefoxChecker
"""

import sys
from time import sleep

import psutil
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QDialog, QMenu, QMessageBox, QSystemTrayIcon

import systray_rc

# PROCESS_NAME = 'gedit'  # for testing
PROCESS_NAME = "firefox"
WAIT = 1.0


def is_process_running(name):
    """
    Tell if a process is running.

    The proc object is cached so it doesn't need to be looked up every time.
    """
    if not hasattr(is_process_running, "proc"):
        is_process_running.proc = None  # Initialize cache

    if is_process_running.proc:
        if is_process_running.proc.is_running():
            return True
        else:
            is_process_running.proc = None
            return False
    else:
        for p in psutil.process_iter():
            if p.name() == name:
                is_process_running.proc = p
                return True
        return False


class FirefoxCheckThread(QThread):
    changeIcon = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
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
            sleep(WAIT)


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.collect_icons()

        self.create_actions()
        self.create_tray_icon()

        self.current_icon = None  # Initial state not set
        self.update_initial_icon()
        self.tray_icon.show()

        self.firefox_check_thread = FirefoxCheckThread(self)
        self.firefox_check_thread.changeIcon.connect(self.set_icon)
        self.firefox_check_thread.start()

    def update_initial_icon(self):
        if is_process_running(PROCESS_NAME):
            self.set_icon(0)
        else:
            self.set_icon(1)

    def set_icon(self, index):
        if index == self.current_icon:
            return
        icon = self.icons[index]
        self.tray_icon.setIcon(icon)
        self.current_icon = index

    def collect_icons(self):
        self.icons = [QIcon(":/images/firefox.svg"), QIcon(":/images/firefox_bw.svg")]

    def create_actions(self):
        self.quit_action = QAction("&Quit", self, triggered=self.quit_app)

    def create_tray_icon(self):
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(self.quit_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setContextMenu(self.tray_icon_menu)

    def quit_app(self):
        self.firefox_check_thread.stop()
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray", "No system tray detected on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)

    window = Window()
    sys.exit(app.exec())
