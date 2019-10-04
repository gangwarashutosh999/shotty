import sys
import mss
import platform
import time
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui import Shotty

_platform = platform.system()

if _platform == 'Linux':
    import pyxhook

    # This function is called every time a key is presssed
    def kbevent(event):
        global running
        # print key info
        print(event)

        # If the ascii value matches spacebar, terminate the while loop
        if event.Ascii == 44:
            running = False

elif _platform == 'Windows':
    import pythoncom
    from pyHook import HookManager, GetKeyState, HookConstants

    def OnKeyboardEvent(event):
        print(repr(event), event.KeyID, HookConstants.IDToName(event.KeyID), event.ScanCode , event.Ascii, event.flags)
        if event.KeyID == 44:
            print("snapshot pressed")
            startApp(screenshot())
        return True

elif _platform == 'Darwin':
    print('[ERROR] macOS not supported!')

def main():
    if _platform == 'Linux':
        '''
        # Create hookmanager
        hookman = pyxhook.HookManager()
        # Define our callback to fire when a key is pressed down
        hookman.KeyDown = kbevent
        # Hook the keyboard
        hookman.HookKeyboard()
        # Start our listener
        hookman.start()

        # Create a loop to keep the application running
        running = True
        while running:
            time.sleep(0.1)
        '''

        startApp(screenshot())
    
    elif _platform == 'Windows':
        # create a hook manager
        hm = HookManager()
        # watch for all mouse events
        hm.KeyDown = OnKeyboardEvent
        # set the hook
        hm.HookKeyboard()
        # wait forever
        pythoncom.PumpMessages()

    '''
    # Close the listener when we are done
    hookman.cancel()
    '''
def screenshot():
    with mss.mss() as sct:
        # Get raw pixels from the screen, save it to a Numpy array
        im = np.array(sct.grab(sct.monitors[1]))
    return im

def startApp(im):
    app = QApplication(sys.argv)
    '''
    app.setQuitOnLastWindowClosed(False)
    qIcon = QIcon('icons/screenshot.png')
    trayIcon = SystemTrayIcon(app, qIcon, 'Shotty')
    trayIcon.show()
    app.setWindowIcon(qIcon)
    '''

    shotty = Shotty(im)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
