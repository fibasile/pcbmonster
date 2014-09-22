#!/usr/local/bin/python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from PyQt4 import QtGui, QtCore
import time


app = None
stack = None
window = None    
    
class SplashScreen(QtGui.QSplashScreen):
    
    def __init__(self):
        pix = QtGui.QPixmap("./gfx/splash.png")
        super(SplashScreen, self).__init__(pix)
        
        self.initUI()
        
    def initUI(self):               
        self.setGeometry(0, 0, 320, 240)
        self.show()

class PicButton(QtGui.QAbstractButton):
    def __init__(self, pixmap_path, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = QtGui.QPixmap(pixmap_path)
        self.icon = QtGui.QIcon(self.pixmap)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        state = QtGui.QIcon.Normal
        if self.isDown():
            state = QtGui.QIcon.Selected
        px = self.icon.pixmap(event.rect().size(), state, QtGui.QIcon.On) 
        painter.drawPixmap(event.rect(), px)

    def sizeHint(self):
        return self.pixmap.size()

class FaderWidget(QtGui.QWidget):

    def __init__(self, old_widget, new_widget):
    
        QtGui.QWidget.__init__(self, new_widget)
        
        self.old_pixmap = QtGui.QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0
        
        self.timeline = QtCore.QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(333)
        self.timeline.start()
        
        self.resize(new_widget.size())
        self.show()
    
    def paintEvent(self, event):
    
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()
    
    def animate(self, value):
    
        self.pixmap_opacity = 1.0 - value
        self.repaint()

class StackedWidget(QtGui.QStackedWidget):

    def __init__(self, parent = None):
        QtGui.QStackedWidget.__init__(self, parent)
    
    def setCurrentIndex(self, index):
        self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        QtGui.QStackedWidget.setCurrentIndex(self, index)
    
    def showMainPage(self):
        self.setCurrentIndex(0)
    
    def showExtrasPage(self):
        self.setCurrentIndex(1)
        
        
class GenericPanel(QtGui.QWidget):
    def __init__(self):
        super(GenericPanel, self).__init__()
        self.initBG()


    def paintEvent(self, event): 
        painter = QtGui.QPainter(self)
        # self.setMask(pixmap.mask())
        painter.drawPixmap(event.rect(), self.pixmap)

    def initBG(self):
        self.setGeometry(0,0,320,240)
        self.pixmap = QtGui.QPixmap("./gfx/menubg.png")
        self.show()
        



class MainPanel(GenericPanel):
    def __init__(self):
        GenericPanel.__init__(self)
        self.initUI()

    def extrasClicked(self):
        print 'extras clicked!'
        stack.showExtrasPage()
    

    def initUI(self):
        layout = QtGui.QGridLayout()
        newBoardButton = PicButton('./gfx/btn_new_board.png')
        controlButton = PicButton('./gfx/btn_control.png')
        settingsButton = PicButton('./gfx/btn_settings.png')
        libraryButton = PicButton('./gfx/btn_library.png')        
        extrasButton = PicButton('./gfx/btn_extras.png')
        extrasButton.clicked.connect(self.extrasClicked)
        powerButton = PicButton('./gfx/btn_power.png')
        layout.addWidget(newBoardButton,0,0)
        layout.addWidget(controlButton,0,1)
        layout.addWidget(settingsButton,0,2)
        layout.addWidget(libraryButton,1,0)
        layout.addWidget(extrasButton,1,1)
        layout.addWidget(powerButton,1,2)
        self.setLayout(layout)






if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    splash = SplashScreen()
    window = QtGui.QWidget()
    window.setGeometry(0,0,320,240)
    stack = StackedWidget(window)
    
    m = MainPanel()
    stack.addWidget(m)
    
    e = GenericPanel()
    stack.addWidget(e)
    

    
    start = time.time()
    while time.time() < start + 3:
        app.processEvents()


    window.show()
    splash.finish(window)
    
    sys.exit(app.exec_())
