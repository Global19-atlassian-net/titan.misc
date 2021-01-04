###############################################################################
# Copyright (c) 2000-2021 Ericsson Telecom AB
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
#
# Contributor: david.ferenc.vranics@ericsson.com
###############################################################################

#try to import Qt
try:
  import sys
  
  from PyQt4.QtGui import *
  from PyQt4.QtCore import *
except:
  print "\nPlease install python-qt4 package!\n"
  sys.exit(1)
  
class StatWidget(QWidget):
    
    def __init__(self, configured):
        super(StatWidget, self).__init__()
        self.configured = configured
        
        self.setGeometry(10,10,0,100)
        self.statPath = QPainterPath()
        self.statPath.moveTo(0, 100)
        self.configuredPath = QPainterPath()
        self.configuredPath.moveTo(0, 51)
        self.qp = QPainter()
        self.statPen = QPen(Qt.red, 2, Qt.SolidLine)
        self.configuredPen = QPen(Qt.darkGreen, 2, Qt.SolidLine)
        self.brush = QBrush(Qt.white, Qt.SolidPattern)

        self.y = 0

    def newStat(self, y):
        self.y = int(y * 50.0 / float(self.configured))
        self.resize(self.geometry().width() + 10, self.geometry().height())
        
    def paintEvent(self, e):
        self.qp.begin(self)
        self.qp.setRenderHint(QPainter.Antialiasing)
        self.qp.setBrush(self.brush)
        self.qp.drawRect(0, 0, self.geometry().width(), 100)
        self.qp.setPen(self.statPen)
        self.statPath.lineTo(self.geometry().width(), 100 - self.y)
        self.qp.drawPath(self.statPath)
        self.qp.setPen(self.configuredPen)
        self.configuredPath.lineTo(self.geometry().width(), 51)
        self.qp.drawPath(self.configuredPath)
        self.qp.end()
