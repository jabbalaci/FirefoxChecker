# Firefox Checker

A system tray icon indicates whether Firefox is running or not.

### Motivation

I use Firefox and I have lots of tabs opened in it (I'm too lazy to close
the old ones). As a result, when I close Firefox before shutting down
my machine, Firefox needs several seconds to fully close (on one of
my machines it's sometimes 20 seconds). The Firefox window disappears but
the process is still in the memory. If I shut down my machine at this time,
next time I reboot the machine and start Firefox I get a recovery message that
asks if I want to restore the tabs since FF wasn't shut down tidily.

So after closing FF I used to start the command `top` to monitor when FF
falls out of the memory. It was boring.

So I wrote this little program. It puts an icon in the system tray and indicates
if FF is running. The icon is colored if FF is running, otherwise it turns
grayscale.

### Screenshots

Firefox is running:

![FF is running](https://raw.githubusercontent.com/jabbalaci/FirefoxChecker/master/screenshots/firefox_on.png)

Firefox is NOT running:

![FF is NOT running](https://raw.githubusercontent.com/jabbalaci/FirefoxChecker/master/screenshots/firefox_off.png)

### Usage

Just start it in the background:

    $ ./systray.py &

If you want to close it, right click on the icon and click on "Quit".

### Requirements

* PySide
* psutil

I tried it under Linux with Manjaro and Ubuntu.

### Acknowledgements

The "systray" example of PySide ([link](https://github.com/PySide/Examples/tree/master/examples/desktop/systray)) helped me a lot to figure out how to use the system tray.
