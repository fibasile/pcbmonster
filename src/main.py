
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from PyQt4 import QtGui, QtCore
import time
import os

app = None
stack = None
window = None    
machine = None 

class Machine():
    def __init__(self):
        self.x=0
        self.y=0
        self.z=0
        self.serial='/dev/usb/lp0'
        self.move()

    def move(self):
        os.system('./rml_move_z.sh %s %s %s %s' % (self.x,self.y,self.z,self.serial))


    
   
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
        #self.setStyleSheet("background: transparent; border: none")

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
        controlPanel = ControlPanel()
        self.pages = ['main','newboard','control', 'settings', 'extras', 'library', 'extras', 'power']
        self.widgets = [ MainPanel(), GenericPanel(),controlPanel,GenericPanel(),GenericPanel(),GenericPanel(),GenericPanel(),GenericPanel() ]
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
        self.pixmap = None
        self.initBG()
        self.initUI()

    def paintEvent(self, event): 
        QtGui.QWidget.paintEvent(self,event)
        if not self.pixmap:
           return
        painter = QtGui.QPainter(self)
        # self.setMask(pixmap.mask())
        painter.drawPixmap(event.rect(), self.pixmap)

    def initBG(self):
        self.setGeometry(0,0,320,240)
        self.setStyleSheet('background-color: white')
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
        #self.pixmap = QtGui.QPixmap("./gfx/control_bg.png")
        self.setStyleSheet("background: white;") 
        self.show()
    
    def refreshGUI(self):
        self.x_label.setText('%.3f' % machine.x)
        self.y_label.setText('%.3f' % machine.y)
        self.z_label.setText('%.3f' % machine.z)
 
    def moveUp(self):
        print 'move up'
        if machine.y < 200:
           machine.y += 5
        machine.move()
        self.refreshGUI()
        
    def moveDown(self):
        print 'move down'
        if machine.y > 0:
           machine.y -= 5        
	machine.move()
        self.refreshGUI()

    def moveLeft(self):
        print 'move left'
        if machine.x > 0:
           machine.x -= 5
        machine.move()
        self.refreshGUI()

    def moveRight(self):
        print 'move right'
        if machine.x < 200:
	   machine.x += 5
        machine.move()        
        self.refreshGUI()

    def moveTop(self):
        print 'move top'
        if machine.z < 400:
           machine.z += 1
        machine.move()
        self.refreshGUI()
        
    def moveBottom(self):
        print 'move bottom'
        if machine.z > 0:
           machine.z -= 1
        machine.move()
        self.refreshGUI()

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
        topButton.clicked.connect(self.moveUp)
        topButton.show()
        bottomButton= QtGui.QPushButton('',self)
        bottomButton.setIcon(QtGui.QIcon('./gfx/bottom.png'))
        bottomButton.setGeometry(70,165,35,35)
        bottomButton.setStyleSheet("background: rgb(241,90,36); border:none")
        bottomButton.clicked.connect(self.moveDown)
        bottomButton.show()
        leftButton=QtGui.QPushButton('',self)
        leftButton.setIcon(QtGui.QIcon('./gfx/left.png'))
        leftButton.setStyleSheet("background: rgb(241,90,36); border:none")
        leftButton.setGeometry(27,118,35,35)
        leftButton.clicked.connect(self.moveLeft)
        leftButton.show()
        rightButton=QtGui.QPushButton('',self)
        rightButton.setIcon(QtGui.QIcon('./gfx/right.png'))
        rightButton.setStyleSheet("background: rgb(241,90,36); border:none")
        rightButton.setGeometry(117,118,35,35)
        rightButton.clicked.connect(self.moveRight)
        rightButton.show()
        upButton=QtGui.QPushButton('',self)
        upButton.setIcon(QtGui.QIcon('./gfx/top.png'))
        upButton.setStyleSheet("background: rgb(241,90,36); border:none")
        upButton.setGeometry(205,72,35,35)
        upButton.clicked.connect(self.moveTop)
        upButton.show()
        downButton=QtGui.QPushButton('',self)
        downButton.setIcon(QtGui.QIcon('./gfx/bottom.png'))
        downButton.setStyleSheet("background: rgb(241,90,36); border:none")
        downButton.setGeometry(205,165,35,35)
        downButton.clicked.connect(self.moveBottom)
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
    machine = Machine()
    splash = SplashScreen()
    window = QtGui.QWidget()
    window.setGeometry(0,0,320,240)
    stack = StackedWidget(window)
    stack.resize(320,240)

    

    
    start = time.time()
    while time.time() < start + 3:
        app.processEvents()


    window.show()
    splash.finish(window)
    
    sys.exit(app.exec_())
