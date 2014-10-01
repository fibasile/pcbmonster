#!/usr/local/bin/python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from PyQt4 import QtGui, QtCore
import time


app = None
stack = None
window = None    
controller = None


class Controller():
    
    def moveUp(self):
        print 'move up'
        
    def moveDown(self):
        print 'move down'
        
    def moveLeft(self):
        print 'move left'
        
    def moveRight(self):
        print 'move right'
        
    def moveTop(self):
        print 'move top'
        
    def moveBottom(self):
        print 'move bottom'
        
    
class SplashScreen(QtGui.QSplashScreen):
    
    def __init__(self):
        pix = QtGui.QPixmap("./gfx/splash.png")
        super(SplashScreen, self).__init__(pix)
        
        self.initUI()
        
    def initUI(self):               
        self.setGeometry(0, 0, 320, 240)
        self.show()

class PicButton(QtGui.QAbstractButton):
    def __init__(self, pixmap_path, parent=None,transparent=False):
        super(PicButton, self).__init__(parent)
        self.pixmap = QtGui.QPixmap(pixmap_path)
        self.icon = QtGui.QIcon(self.pixmap)
        self.transparent=transparent
        self.setStyleSheet("background: transparent; border: none")

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
        self.pages = ['main','newboard','control', 'settings', 'extras', 'library', 'extras', 'power']
        self.widgets = [ MainPanel(), GenericPanel(),ControlPanel(),GenericPanel(),GenericPanel(),GenericPanel(),GenericPanel(),GenericPanel() ]
        for w in self.widgets:
            self.addWidget(w)

    def setCurrentIndex(self, index):
        self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        QtGui.QStackedWidget.setCurrentIndex(self, index)
    
    def showMainPage(self):
        self.setCurrentIndex(0)
    
    def showPage(self,pagename):
        i = self.pages.index(pagename)
        self.setCurrentIndex(i)
        
        
class GenericPanel(QtGui.QWidget):
    def __init__(self):
        super(GenericPanel, self).__init__()
        self.initBG()
        self.initUI()

    def paintEvent(self, event): 
        painter = QtGui.QPainter(self)
        # self.setMask(pixmap.mask())
        painter.drawPixmap(event.rect(), self.pixmap)

    def initBG(self):
        self.setGeometry(0,0,320,240)
        self.pixmap = QtGui.QPixmap("./gfx/menubg.png")
        self.show()
        
    def initUI(self):
        backButton = PicButton('./gfx/btn_back.png',self)
        backButton.setGeometry(5,5,87,46)
        backButton.clicked.connect(self.goBack)
        backButton.show()
        
    def goBack(self):
        stack.showMainPage()


class ControlPanel(GenericPanel):
    def initBG(self):
        self.setGeometry(0,0,320,240)
        self.pixmap = QtGui.QPixmap("./gfx/control_bg.png")
        self.show()
        
    def initUI(self):
        global controller
        GenericPanel.initUI(self)
        self.x_label = QtGui.QLabel(self)
        self.x_label.setGeometry(120,12,80,30)
        self.x_label.setText("0.000")
        self.x_label.show()
        self.y_label = QtGui.QLabel(self)
        self.y_label.setGeometry(186,12,80,30)
        self.y_label.setText("0.000")
        self.y_label.show()
        self.z_label = QtGui.QLabel(self)
        self.z_label.setGeometry(250,12,80,30)
        self.z_label.setText("0.000")
        self.z_label.show()
        topButton = QtGui.QPushButton('',self)
        topButton.setIcon(QtGui.QIcon('./gfx/top.png'))
        topButton.setStyleSheet("background: rgb(241,90,36); border:none")
        topButton.setGeometry(70,72,35,35)
        topButton.clicked.connect(controller.moveTop)
        topButton.show()
        bottomButton= QtGui.QPushButton('',self)
        bottomButton.setIcon(QtGui.QIcon('./gfx/bottom.png'))
        bottomButton.setGeometry(70,160,35,35)
        bottomButton.setStyleSheet("background: rgb(241,90,36); border:none")
        bottomButton.clicked.connect(controller.moveBottom)
        bottomButton.show()
        leftButton=QtGui.QPushButton('',self)
        leftButton.setIcon(QtGui.QIcon('./gfx/left.png'))
        leftButton.setStyleSheet("background: rgb(241,90,36); border:none")
        leftButton.setGeometry(27,114,35,35)
        leftButton.clicked.connect(controller.moveLeft)
        leftButton.show()
        rightButton=QtGui.QPushButton('',self)
        rightButton.setIcon(QtGui.QIcon('./gfx/right.png'))
        rightButton.setStyleSheet("background: rgb(241,90,36); border:none")
        rightButton.setGeometry(117,114,35,35)
        rightButton.clicked.connect(controller.moveRight)
        rightButton.show()
        upButton=QtGui.QPushButton('',self)
        upButton.setIcon(QtGui.QIcon('./gfx/top.png'))
        upButton.setStyleSheet("background: rgb(241,90,36); border:none")
        upButton.setGeometry(205,72,35,35)
        upButton.clicked.connect(controller.moveUp)
        upButton.show()
        downButton=QtGui.QPushButton('',self)
        downButton.setIcon(QtGui.QIcon('./gfx/bottom.png'))
        downButton.setStyleSheet("background: rgb(241,90,36); border:none")
        downButton.setGeometry(205,160,35,35)
        downButton.clicked.connect(controller.moveDown)
        downButton.show()
        



class MainPanel(GenericPanel):
    def __init__(self):
        GenericPanel.__init__(self)
        self.initUI()

    def extrasClicked(self):
        stack.showPage('extras')
    
    def newboardClicked(self):
        stack.showPage('newboard')

    def settingsClicked(self):
        stack.showPage('settings')
        
    def libraryClicked(self):
        stack.showPage('library')
        
    def powerClicked(self):
        stack.showPage('power')

    def controlClicked(self):
        stack.showPage('control')
        

    def initUI(self):
        layout = QtGui.QGridLayout()
        newBoardButton = PicButton('./gfx/btn_new_board.png')
        newBoardButton.clicked.connect(self.newboardClicked)
        controlButton = PicButton('./gfx/btn_control.png')
        controlButton.clicked.connect(self.controlClicked)
        settingsButton = PicButton('./gfx/btn_settings.png')
        settingsButton.clicked.connect(self.settingsClicked)
        libraryButton = PicButton('./gfx/btn_library.png')
        libraryButton.clicked.connect(self.libraryClicked)        
        extrasButton = PicButton('./gfx/btn_extras.png')
        extrasButton.clicked.connect(self.extrasClicked)
        powerButton = PicButton('./gfx/btn_power.png')
        powerButton.clicked.connect(self.powerClicked)
        layout.addWidget(newBoardButton,0,0)
        layout.addWidget(controlButton,0,1)
        layout.addWidget(settingsButton,0,2)
        layout.addWidget(libraryButton,1,0)
        layout.addWidget(extrasButton,1,1)
        layout.addWidget(powerButton,1,2)
        self.setLayout(layout)






if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    controller = Controller()
    splash = SplashScreen()
    window = QtGui.QWidget()
    window.setGeometry(0,0,320,240)
    stack = StackedWidget(window)


    

    
    start = time.time()
    while time.time() < start + 3:
        app.processEvents()


    window.show()
    splash.finish(window)
    
    sys.exit(app.exec_())
