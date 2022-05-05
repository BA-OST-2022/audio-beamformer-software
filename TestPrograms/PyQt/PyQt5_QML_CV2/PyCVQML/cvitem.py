from PyQt5 import QtCore, QtGui, QtQuick


class CVItem(QtQuick.QQuickPaintedItem):
    imageChanged = QtCore.pyqtSignal()
    xChanged = QtCore.pyqtSignal()
    yChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CVItem, self).__init__(parent)
        # self.setRenderTarget(QtQuick.QQuickPaintedItem.FramebufferObject)
        self.m_image = QtGui.QImage()
        self.m_x = 0
        self.m_y = 0

    def paint(self, painter):
        if self.m_image.isNull(): return
        # image = self.m_image.scaled(self.size().toSize())
        image = self.m_image
        painter.drawImage(QtCore.QPoint(self.m_x, self.m_y), image)

    def image(self):
        return self.m_image

    def setImage(self, image):
        if self.m_image == image: return
        self.m_image = image
        self.imageChanged.emit()
        self.update()
        
        
    def x(self):
        return self.m_x
    
    def setX(self, x):
        if self.m_x == x: return
        self.m_x = x
        self.xChanged.emit()
        
    def y(self):
        return self.m_y
    
    def setY(self, y):
        if self.m_y == y: return
        self.m_y = y
        self.yChanged.emit()

    image = QtCore.pyqtProperty(QtGui.QImage, fget=image, fset=setImage, notify=imageChanged)
    x = QtCore.pyqtProperty(int, fget=x, fset=setX, notify=xChanged)
    y = QtCore.pyqtProperty(int, fget=y, fset=setY, notify=yChanged)