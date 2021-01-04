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

################################################

class MsgFlow(QWidget):
  def __init__(self, parent = None):
    super(MsgFlow, self).__init__(parent)
    self.setGeometry(0,0,160,45)
    self.currentIdx = -1
    self.items = list()
    self.qp = QPainter()
    self.setToolTip("Right click to add/remove messages!")
    
  def paintEvent(self, e):
    self.qp.begin(self)
    self.qp.setPen(QColor(0, 0, 0))
    self.qp.setFont(QFont("Arial", 10))
    self.qp.drawRect(5, 5, 40, 30)
    self.qp.drawText(QRect(5, 5, 40, 30), Qt.AlignCenter, "TC")
    self.qp.drawRect(115, 5, 40, 30)
    self.qp.drawText(QRect(115, 5, 40, 30), Qt.AlignCenter, "SUT")
    for i in xrange(len(self.items)):
      self.qp.drawLine(25, (i+1)*30+5, 25, (i+2)*30+10)
      self.qp.drawLine(135, (i+1)*30+5, 135, (i+2)*30+10)
      self.qp.drawLine(25, (i+2)*30, 135, (i+2)*30)
      if self.items[i][1] == "out":
        self.qp.drawLine(134, (i+2)*30, 129, (i+2)*30-5)
        self.qp.drawLine(134, (i+2)*30, 129, (i+2)*30+5)
      elif self.items[i][1] == "in":
        self.qp.drawLine(26, (i+2)*30, 31, (i+2)*30-5)
        self.qp.drawLine(26, (i+2)*30, 31, (i+2)*30+5)
      if self.currentIdx != -1 and self.currentIdx < len(self.items):
        self.qp.setPen(QColor(0, 169, 212))
        self.qp.drawRect(15, (self.currentIdx+1)*30+10, 130, 30)
        self.qp.setPen(QColor(0, 0, 0))
      self.qp.drawText(QRect(25, (i+1)*30+5, 115, 30), Qt.AlignCenter, self.items[i][0])
    self.qp.end()
  
  def mousePressEvent(self, event):
    if len(self.items) > 0 and event.y() > 35 and event.y() < (len(self.items) + 1 ) * 30 + 5:
      if (event.y() - 5) / 30 - 1 != self.currentIdx:
        self.currentIdx = (event.y() - 5) / 30 - 1
        self.emit(SIGNAL("currentChanged(int)"), self.currentIdx)
        self.update()
     
  def newIn(self, text):
    self.items.extend([[text, "in"]])
    self.currentIdx = len(self.items) - 1
    self.emit(SIGNAL("currentChanged(int)"), self.currentIdx)
    self.resize(self.geometry().width(), self.geometry().height() + 30)
    
  def newOut(self, text):
    self.items.extend([[text, "out"]])
    self.currentIdx = len(self.items) - 1
    self.emit(SIGNAL("currentChanged(int)"), self.currentIdx)
    self.resize(self.geometry().width(), self.geometry().height() + 30)
    
  def deleteIdx(self, idx):
    if len(self.items) != 0:
      self.items.pop(idx)
      if self.currentIdx == len(self.items):
        self.currentIdx = self.currentIdx - 1
      self.resize(self.geometry().width(), self.geometry().height() - 30)
