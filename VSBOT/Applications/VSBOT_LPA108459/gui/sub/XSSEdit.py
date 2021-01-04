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

from MsgFlow import MsgFlow
from ConnectEdit import ConnectEdit
from CloseEdit import CloseEdit
from HTTPRequestEdit import HTTPRequestEdit
from HTTPResponseEdit import HTTPResponseEdit

################################################

class XSSEdit(QWidget):
  def __init__(self, parent = None):
    super(XSSEdit, self).__init__(parent)
    
    self.tcType = "XSS"
    
    self.templateParamsBuffer = ""
    
    self.setMinimumHeight(300)
    
    self.widgets = list()
    
    self.hLayout = QHBoxLayout()
    
    self.msgFlow = MsgFlow()
    self.scrollArea = QScrollArea()
    self.scrollArea.setMinimumHeight(180)
    self.scrollArea.setMaximumWidth(180)
    self.scrollArea.setMinimumWidth(180)
    self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.scrollArea.setWidget(self.msgFlow)
    self.widgetStack = QStackedWidget()
   
    self.hLayout.addWidget(self.scrollArea)
    self.hLayout.addWidget(self.widgetStack)
    
    self.setLayout(self.hLayout)
    
    QObject.connect(self.msgFlow, SIGNAL("currentChanged(int)"), self.widgetStack.setCurrentIndex)
       
    self.addConnectAction = QAction("Add a Connect message", self)
    QObject.connect(self.addConnectAction, SIGNAL("triggered()"), self.addConnect)
    
    self.addHTTPRequestAction = QAction("Add a HTTP request message", self)
    QObject.connect(self.addHTTPRequestAction, SIGNAL("triggered()"), self.addHTTPRequest)
    
    self.addHTTPResponseAction = QAction("Add a HTTP response message", self)
    QObject.connect(self.addHTTPResponseAction, SIGNAL("triggered()"), self.addHTTPResponse)
        
    self.addCloseAction = QAction("Add a Close message", self)
    QObject.connect(self.addCloseAction, SIGNAL("triggered()"), self.addClose)
     
    self.deleteAction = QAction("Delete current message", self)
    QObject.connect(self.deleteAction, SIGNAL("triggered()"), self.deleteCurrent)
    
  def addConnect(self):
    w = ConnectEdit()
    self.widgetStack.addWidget(w)
    self.widgets.extend([w])
    self.msgFlow.newOut("Connect")
    
  def addHTTPRequest(self):
    w = HTTPRequestEdit()
    self.widgetStack.addWidget(w)
    self.widgets.extend([w])
    self.msgFlow.newOut("HTTP request")
    
  def addHTTPResponse(self):
    w = HTTPResponseEdit()
    self.widgetStack.addWidget(w)
    self.widgets.extend([w])
    self.msgFlow.newIn("HTTP response")
    
  def addClose(self):
    w = CloseEdit()
    self.widgetStack.addWidget(w)
    self.widgets.extend([w])
    self.msgFlow.newOut("Close")
    
  def newTemplateParams(self, msg):
    self.templateParamsBuffer = msg
    
  def newConnect(self, msg):
    self.addConnect()
    self.widgets[len(self.widgets) - 1].packetEdit.setPlainText(msg.rstrip("\n"))
    
  def newHTTPRequest(self, msg):
    self.addHTTPRequest()
    self.widgets[len(self.widgets) - 1].templatesEdit.setText(self.templateParamsBuffer)
    self.templateParamsBuffer = ""
    x = ""
    lines = msg.split("\n")
    for i in xrange(len(lines)):
      if lines[i] != "request :=" and lines[i] != "{" and lines[i] != "}" and lines[i] != "":
        x = x + lines[i].replace("  ", "", 1) + "\n"
    x = x.rstrip("\n")
    self.widgets[len(self.widgets) - 1].packetEdit.setPlainText(x)
    
  def newHTTPResponse(self, msg):
    self.addHTTPResponse()
    self.widgets[len(self.widgets) - 1].responsesEdit.setPlainText(msg.rstrip("\n"))
    
  def newClose(self, msg):
    self.addClose()
    self.widgets[len(self.widgets) - 1].packetEdit.setPlainText(msg.rstrip("\n"))
    
  def deleteCurrent(self):
    msgBox = QMessageBox()
    msgBox.setText("Deleting message.")
    msgBox.setInformativeText("Do you really want to delete the message?")
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.No)
    if msgBox.exec_() == QMessageBox.Yes:
      self.msgFlow.deleteIdx(self.widgetStack.currentIndex())
      self.widgets.pop(self.widgetStack.currentIndex())
      self.widgetStack.removeWidget(self.widgetStack.currentWidget())
    else:
      return
    
  def contextMenuEvent(self, event):
     menu = QMenu()
     menu.addAction(self.addConnectAction)
     menu.addAction(self.addHTTPRequestAction)
     menu.addAction(self.addHTTPResponseAction)
     menu.addAction(self.addCloseAction)
     menu.addSeparator()
     menu.addAction(self.deleteAction)
     menu.exec_(event.globalPos())
     
  #this should convert things to text
  def serialize(self):
    offset = "      "
    s = ""
    s = s + offset + "XSS :=\n"
    s = s + offset + "{\n"
    if len(self.widgets) != 0:
      s = s + offset + "  " + "{\n"
      if len(self.widgets) > 1 and self.widgets[1].packetType == "response":
        s = s + self.widgets[0].serialize(self.widgets[1].serialize())
      else:
        s = s + self.widgets[0].serialize()
      s = s + offset + "  " + "}"
      for i in range(1, len(self.widgets)):
        if self.widgets[i].packetType != "response":
          s = s + ",\n" + offset + "  " + "{\n"
          if len(self.widgets) > i+1 and self.widgets[i+1].packetType == "response":
            s = s + self.widgets[i].serialize(self.widgets[i+1].serialize())
          else:
            s = s + self.widgets[i].serialize()
          s = s + offset + "  " + "}"
      s = s + "\n"
    s = s + offset + "}"
    return s
