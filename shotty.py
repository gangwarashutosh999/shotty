from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import sys
import mss
import numpy as np
import signal
import cv2 as cv

class Shotty(QWidget):
    def __init__(self, im):
        super().__init__()
        print('Removing alpha..')
        self.im = im[:,:,:3].copy()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        QApplication.setOverrideCursor(Qt.CrossCursor)
        # Create widget
        self.label = QLabel(self)
        self.l_mousePos = QLabel(self)
        h, w, c = self.im.shape
        print(h, w ,c)

        
        self.im = self.im[:,:,:3].copy()
        h, w, c = self.im.shape
        print('New shape: {},{},{}'.format(h, w, c))

        
        print(self.im.strides[0])
        qImg = QImage(self.im, w, h, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())

        self.label.keyPressEvent = app.quit()      

        self.label.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
        monitor = QDesktopWidget().screenGeometry(1)
        self.label.move(monitor.left(), monitor.top())
        self.label.showFullScreen()
    
    def mouseMoveEvent(self, event):
        print(event.x(), event.y())
        self.l_mousePos.setText('(%dpx, %dpx)' % (event.x(), event.y()))

def mask_image(imgdata, imgtype='jpg', size=64):
    """Return a ``QPixmap`` from *imgdata* masked with a smooth circle.

    *imgdata* are the raw image bytes, *imgtype* denotes the image type.

    The returned image will have a size of *size* × *size* pixels.

    """
    # Load image and convert to 32-bit ARGB (adds an alpha channel):
    image = QImage.fromData(imgdata, imgtype)
    image.convertToFormat(QImage.Format_ARGB32)

    # Crop image to a square:
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )
    image = image.copy(rect)

    # Create the output image with the same dimensions and an alpha channel
    # and make it completely transparent:
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # Create a texture brush and paint a circle with the original image onto
    # the output image:
    brush = QBrush(image)        # Create texture brush
    painter = QPainter(out_img)  # Paint the output image
    painter.setBrush(brush)      # Use the image texture brush
    painter.setPen(Qt.NoPen)     # Don't draw an outline
    painter.setRenderHint(QPainter.Antialiasing, True)  # Use AA
    painter.drawEllipse(0, 0, imgsize, imgsize)  # Actually draw the circle
    painter.end()                # We are done (segfault if you forget this)

    # Convert the image to a pixmap and rescale it.  Take pixel ratio into
    # account to get a sharp image on retina displays:
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    return pm

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    with mss.mss() as sct:
        # Get raw pixels from the screen, save it to a Numpy array
        im = np.array(sct.grab(sct.monitors[1]))
    '''
    cv.imshow("screenshot", im)
    cv.waitKey(0)
    cv.destroyAllWindows()
    '''
    app = QApplication(sys.argv)
    shotty = Shotty(im)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()