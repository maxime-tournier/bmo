import sys

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *

app = QApplication(sys.argv)


key_press = None

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if key_press: key_press( e )
        else:
            super(Window, self).keyPressEvent(e)


win = Window()
geom = QDesktopWidget().screenGeometry( win )
# win.setWindowTitle( 'BMO!')

height = 0.8 * geom.height()
width = 0.7 * height
win.setFixedSize( width, height )

view = QDeclarativeView()
win.setCentralWidget( view )
win.adjustSize()

win.show()
# Create an URL to the QML file
url = QUrl('view.qml')

view.setSource(url)
view.show()


view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
root = view.rootObject()

import time
import math


# tx = QDeclarativeProperty(text, 'anchors.horizontalCenterOffset')
# ty = QDeclarativeProperty(text, 'anchors.verticalCenterOffset')




timer = QTimer()
def timeout():
    try:
        view.engine().clearComponentCache()
        view.setSource(url)
    except:
        print 'error !'
        pass

timer.timeout.connect( timeout )
timer.start( 1000 )

center = [ root.findChild(QObject, name) for name in 'leftCenter', 'rightCenter' ]
eye = [root.findChild(QObject, name) for name in 'leye', 'reye' ]

props = ['anchors.horizontalCenterOffset', 'anchors.verticalCenterOffset']

mouth = root.findChild(QObject, 'mouth') 
mouth_off = [QDeclarativeProperty(mouth, p) for p in props]

off = [ [QDeclarativeProperty(x, p) for p in props] for x in eye ]


# off[0][0].write( 100 )
import numpy as np

timer = QTimer()
def lookat(screen_pos):
    origin = view.mapToGlobal( view.rect().topLeft() )

    wx, wy = origin.x(), origin.y()

    mx, my, depth = screen_pos

    # print mx, wx
    
    # local
    lx, ly = float(mx - wx), float(my - wy)
    local = np.array( (lx, ly) )

    pos = [ x.scenePos() for x in center ]

    pos = [ np.array( (x.x(), x.y()) ) for x in pos ]
    delta = [ local - x for x in pos]

    sigma = 70
    sigma2 = sigma * sigma

    dist2 = [ x.dot(x) for x in delta]

    factor = [1 - math.exp( - x / sigma2 ) for x in dist2] 

    dir = [ np.array([delta[i][0], delta[i][1], depth]) for i in xrange(2) ]
    
    # normalized
    unit = [ x / math.sqrt( 1e-10 + x.dot(x) ) for x in dir ]
    
    scale = 1

    prop = ['width', 'height']
    
    for side in xrange(2):
        for axis in xrange(2):
            value = unit[side][axis]
            # old_value = scale * (factor[side] * dir[side][axis])
            # print 'check', value, 'old', old_value
            
            off[side][axis].write( value )
            expr = '{0} * parent.{1}'.format(value, prop[axis])
            # print expr
            expr = QDeclarativeExpression (view.rootContext(), eye[side], expr)
            off[side][axis].write( expr.evaluate()[0] )






def track( cb, timeout = 20 ):
    """look at the result of callback, in screen coordinates"""
    geom = QDesktopWidget().screenGeometry( view )
    
    def timeout():
        res = cb()
        if res:
            x, y, z = res
            lookat( ( x * geom.width(),
                      y * geom.height(),
                      z) )
        
    timer.timeout.connect( timeout )
    timer.start( 20 )


def exec_():
    app.exec_()
    
if __name__ == '__main__':

    geom = QDesktopWidget().screenGeometry( view )
    
    def cb():
        p = QCursor.pos()
        return (p.x() / float( geom.width() ), p.y() / float(geom.height()), 400 )

    track( cb )
    
    app.exec_()
