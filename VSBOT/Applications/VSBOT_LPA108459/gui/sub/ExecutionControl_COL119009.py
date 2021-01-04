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
  
from time import sleep
from telnetlib import Telnet
from threading import Thread

from ConsoleView_COL119012 import *

################################################

class ExecutionControl(QWidget):
  def __init__(self, parent = None):
    super(ExecutionControl, self).__init__(parent)
    
    self.running = False

    self.timeout = 30

    self.vLayout = QVBoxLayout()
    self.gLayout = QGridLayout()
    self.hLayout = QHBoxLayout()
    
    self.hostLabel = QLabel("Host:")
    self.hostEdit = QLineEdit("10.0.0.2")
    self.portLabel = QLabel("Port:")
    self.portEdit = QLineEdit("9999")
    self.sshuserLabel = QLabel("SSH Username:")
    self.sshuserEdit = QLineEdit("ttcn")
    self.sshpassLabel = QLabel("SSH Password:")
    self.sshpassEdit = QLineEdit()
    #not supported yet
    self.sshpassEdit.setEnabled(False)
    self.sshpassEdit.setEchoMode(QLineEdit.Password)
    self.telnetuserLabel = QLabel("TELNET Username:")
    self.telnetuserEdit = QLineEdit("ttcn3")
    self.telnetpassLabel = QLabel("TELNET Password:")
    self.telnetpassEdit = QLineEdit("ttcn3ttcn3")
    self.telnetpassEdit.setEchoMode(QLineEdit.Password)
    
    self.gLayout.addWidget(self.hostLabel, 0, 0)
    self.gLayout.addWidget(self.hostEdit, 0, 1)
    self.gLayout.addWidget(self.portLabel, 0, 2)
    self.gLayout.addWidget(self.portEdit, 0, 3)
    self.gLayout.addWidget(self.sshuserLabel, 1, 0)
    self.gLayout.addWidget(self.sshuserEdit, 1, 1)
    self.gLayout.addWidget(self.sshpassLabel, 1, 2)
    self.gLayout.addWidget(self.sshpassEdit, 1, 3)
    self.gLayout.addWidget(self.telnetuserLabel, 2, 0)
    self.gLayout.addWidget(self.telnetuserEdit, 2, 1)
    self.gLayout.addWidget(self.telnetpassLabel, 2, 2)
    self.gLayout.addWidget(self.telnetpassEdit, 2, 3)
    
    self.startButton = QPushButton("Start")
    self.stopButton = QPushButton("Stop")
    self.killButton = QPushButton("Kill")
    self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    
    self.hLayout.addSpacerItem(self.spacer)    
    self.hLayout.addWidget(self.startButton)
    self.hLayout.addWidget(self.stopButton)
    self.hLayout.addWidget(self.killButton)
    
    self.hLayout.setSpacing(10)
    
    self.consoleView = ConsoleView()
    
    self.vLayout.addLayout(self.gLayout)
    self.vLayout.addWidget(self.consoleView)
    self.vLayout.addLayout(self.hLayout)
    
    self.setLayout(self.vLayout)
    
    QObject.connect(self.startButton, SIGNAL("clicked()"), self.start)
    QObject.connect(self.stopButton, SIGNAL("clicked()"), self.stop)
    QObject.connect(self.killButton, SIGNAL("clicked()"), self.kill)

  def start(self):
    self.emit(SIGNAL("start()"))
    
  def filename(self, filename):
    self.consoleView.startTITAN(filename, self.sshuserEdit.text(), self.hostEdit.text())
    Thread(target = self.__execCtrlThread).start()
    
  def __execCtrlThread(self):
    self.running = True
    while not self.connectToTelnet():
      if not self.running:
        return
      else:
        sleep(1)
    #self.sendCommand("start")
    line = self.readFromTelnet()
    while line != None:
      if line[1] == "INTEGER":
        self.emit(SIGNAL("incomingStat(int, int)"), int(line[0]), float(line[2]))
      elif line[1] == "VERDICT":
        if len(line) == 5:
          line.extend([""])
        self.emit(SIGNAL("incomingStat(int, int, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), int(line[0]), int(line[2]), line[3], line[4], line[5])
      line = self.readFromTelnet()
    
  def stop(self):
    self.sendCommand("stop")
    self.running = False
    
  def kill(self):
    self.sendCommand("kill")
    self.running = False
  
  #################################
  def connectToTelnet(self):
    try:
      self.telnetConn = Telnet(str(self.hostEdit.text()), int(self.portEdit.text()), 1)
      self.telnetConn.read_until("login: ", self.timeout)
      self.sendCommand(str(self.telnetuserEdit.text()))
      self.telnetConn.read_until("password: ", self.timeout)
      self.sendCommand(str(self.telnetpassEdit.text()))
      self.telnetConn.read_until("vsbot> ", self.timeout)
      return True
    except Exception, e:
      return False
      
  def sendCommand(self, cmd):
    try:
      if self.telnetConn:
        self.telnetConn.write(str(cmd + "\n"))
    except Exception, e:
      return
      
  def readFromTelnet(self):
    try:
      if self.telnetConn:
        returnStringList = self.telnetConn.read_until("vsbot> ", self.timeout).splitlines()[0].split("::")
        return returnStringList
    except Exception, e:
      return
