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

from ConfigParser import ConfigParser
from XSSEdit import XSSEdit
from SQLiEdit import SQLiEdit
from DirectoryTraversalEdit import DirectoryTraversalEdit
from SynFloodEdit import SynFloodEdit
from SynFloodOverGTPEdit import SynFloodOverGTPEdit

################################################

class ConfigurationEditor(QWidget):
  def __init__(self, parent = None):
    super(ConfigurationEditor, self).__init__(parent)
    self.configParser = ConfigParser()
    
    self.filename = ""
    
    self.defaultOffset = "\
[INCLUDE]\n\
\"main.cfg\"\n\
\"wordlists.cfg\"\n\
\"common_result_patterns.cfg\"\n\
\n\
[MODULE_PARAMETERS]\n\
tsp_VS_testCases :=\n"
    
    #dirty workarounds because python is not good at casting
    self.hosts = list()
    self.wordlistIndices = list()
    self.tcEdits = list()
    self.configAreas = list()
    
    self.vLayout = QVBoxLayout()
    self.hLayout = QHBoxLayout()
    
    self.newButton = QPushButton("New")
    self.newButton.setToolTip("Create new configuration.")
    self.saveButton = QPushButton("Save")
    self.saveButton.setToolTip("Save configuration.")
    self.openButton = QPushButton("Open")
    self.openButton.setToolTip("Open existing configuration.")
    self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    
    self.hLayout.addWidget(self.newButton)
    self.hLayout.addWidget(self.saveButton)
    self.hLayout.addWidget(self.openButton)
    self.hLayout.addSpacerItem(self.spacer)
    
    self.hLayout.setSpacing(10)
    
    self.tree = QTreeWidget()
    self.tree.setAlternatingRowColors(True)
    self.tree.setExpandsOnDoubleClick(False)
    self.tree.setToolTip("Right click to add/remove testcases!")
    self.tree.header().hide()
    
    self.vLayout.addLayout(self.hLayout)
    self.vLayout.addWidget(self.tree)
    
    self.setLayout(self.vLayout)
    
    self.newXSSAction = QAction("New XSS TC", self)
    QObject.connect(self.newXSSAction, SIGNAL("triggered()"), self.newXSS)

    self.newSQLiAction = QAction("New SQLi TC", self)
    QObject.connect(self.newSQLiAction, SIGNAL("triggered()"), self.newSQLi)
    
    self.newDirectoryTraversalAction = QAction("New Directory Traversal TC", self)
    QObject.connect(self.newDirectoryTraversalAction, SIGNAL("triggered()"), self.newDirectoryTraversal)
    
    self.newSynFloodAction = QAction("New Syn Flood TC", self)
    QObject.connect(self.newSynFloodAction, SIGNAL("triggered()"), self.newSynFlood)
    
    self.newSynFloodOverGTPAction = QAction("New Syn Flood over GTP TC", self)
    QObject.connect(self.newSynFloodOverGTPAction, SIGNAL("triggered()"), self.newSynFloodOverGTP)
    
    self.deleteAction = QAction("Delete selected TC", self)
    QObject.connect(self.deleteAction, SIGNAL("triggered()"), self.deleteSelected)
    
    QObject.connect(self.newButton, SIGNAL("clicked()"), self.newConfig)
    QObject.connect(self.saveButton, SIGNAL("clicked()"), self.saveConfig)
    QObject.connect(self.openButton, SIGNAL("clicked()"), self.openConfig)
    #parse should signal out testcases
    QObject.connect(self.configParser, SIGNAL("newTC(PyQt_PyObject)"), self.newTC)
    QObject.connect(self.configParser, SIGNAL("host(PyQt_PyObject)"), self.loadHost)
    QObject.connect(self.configParser, SIGNAL("wordlistidx(int)"), self.loadWordListIdx)
    QObject.connect(self.configParser, SIGNAL("synflood()"), self.loadSynFlood)
    QObject.connect(self.configParser, SIGNAL("synfloodovergtp()"), self.loadSynFloodOverGTP)
    QObject.connect(self.configParser, SIGNAL("xss()"), self.loadXSS)
    QObject.connect(self.configParser, SIGNAL("sqli()"), self.loadSQLi)
    QObject.connect(self.configParser, SIGNAL("dirtrav()"), self.loadDirectoryTraversal)
  
  def contextMenuEvent(self, event):
     menu = QMenu()
     menu.addAction(self.newXSSAction)
     menu.addAction(self.newSQLiAction)
     menu.addAction(self.newDirectoryTraversalAction)
     menu.addAction(self.newSynFloodAction)
     menu.addAction(self.newSynFloodOverGTPAction)
     menu.addSeparator()
     menu.addAction(self.deleteAction)
     menu.exec_(event.globalPos())
  
  def newConfig(self):
    if self.tree.topLevelItemCount() != 0:
      msgBox = QMessageBox()
      msgBox.setText("Erasing configuration.")
      msgBox.setInformativeText("Do you really want to erase the list of TCs?")
      msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
      msgBox.setDefaultButton(QMessageBox.No)
      if msgBox.exec_() == QMessageBox.Yes:
        while self.tree.topLevelItemCount() != 0:
          self.removeAt(0)
        self.filename = ""
      else:
        return
    
  def removeAt(self, index):
    self.hosts.pop(index)
    self.wordlistIndices.pop(index)
    self.tcEdits.pop(index)
    self.configAreas.pop(index)
    self.tree.takeTopLevelItem(index)
        
  def deleteSelected(self):
    msgBox = QMessageBox()
    msgBox.setText("Deleting testcase.")
    msgBox.setInformativeText("Do you really want to delete the testcase?")
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.No)
    if msgBox.exec_() == QMessageBox.Yes:
      self.removeAt(self.tree.currentIndex().row())
    else:
      return
  
  def saveConfig(self):
    f = QFileDialog.getSaveFileName(self, "Save configuration", "", "*.cfg")
    offset = self.configParser.offsetData
    if offset == "":
      offset = self.defaultOffset
    if f != "":
      self.filename = f
      wordlistIdxField = ""
      if self.wordlistIndices[0] != "dummy":
        wordlistIdxField = ",\n    wordListIdx := " + str(self.wordlistIndices[0].value()) + "\n"
      else:
        wordlistIdxField = "\n"
      s = (offset +
           "{\n" +
           "  {\n" +
           "    testCaseName := \"" + self.tree.topLevelItem(0).text(0) + "\",\n" +
           "    host := \"" + self.hosts[0].text() + "\",\n" +    
           "    testCaseType :=\n" +
           "    {\n" +
           self.tcEdits[0].serialize() + "\n" +
           "    }" +
           wordlistIdxField +
           "  }")
      for i in range(1, self.tree.topLevelItemCount()):
        if self.wordlistIndices[i] != "dummy":
          wordlistIdxField = ",\n    wordListIdx := " + str(self.wordlistIndices[i].value()) + "\n"
        else:
          wordlistIdxField = "\n"
        s = (s +
             ",\n" +
             "  {\n" +
             "    testCaseName := \"" + self.tree.topLevelItem(i).text(0) + "\",\n" +
             "    host := \"" + self.hosts[i].text() + "\",\n" +    
             "    testCaseType :=\n" +
             "    {\n" +
             self.tcEdits[i].serialize() + "\n" +
             "    }" +
             wordlistIdxField +
             "  }")           
      s = s+ "\n}\n"
      
      outfile = open(self.filename, "w")
      outfile.write(s)
      outfile.close()
  
  def openConfig(self):
    if self.tree.topLevelItemCount() != 0:
      msgBox = QMessageBox()
      msgBox.setText("You have unsaved changes.")
      msgBox.setInformativeText("Do you really want to erase the list of TCs?")
      msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
      msgBox.setDefaultButton(QMessageBox.No)
      if msgBox.exec_() == QMessageBox.Yes:
        while self.tree.topLevelItemCount() != 0:
          self.removeAt(0)
      else:
        return
    f = QFileDialog.getOpenFileName(self, "Open configuration", "", "*.cfg")
    if f != "":
      self.filename = f
      self.configParser.parse(f)
    
  def newTC(self, name):
    configTCItem = QTreeWidgetItem(self.tree)
    configTCItem.setText(0, name)
    configTCItem.setFlags(configTCItem.flags() | (Qt.ItemIsEditable))
    configTCWidget = QWidget()
    
    configItem = QTreeWidgetItem(configTCItem)
    self.configAreas.extend([QVBoxLayout()])
    
    hostArea = QHBoxLayout()
    hostLabel = QLabel("Host:")
    hostEdit = QLineEdit("127.0.0.1")
    self.hosts.extend([hostEdit])
    hostSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    hostArea.addWidget(hostLabel)
    hostArea.addWidget(hostEdit)
    hostArea.addSpacerItem(hostSpacer)
    self.configAreas[len(self.configAreas) - 1].addLayout(hostArea)
    
    configTCWidget.setLayout(self.configAreas[len(self.configAreas) - 1])
    
    self.tree.setItemWidget(configItem, 0, configTCWidget)
    
  def loadHost(self, host):
    self.hosts[self.tree.topLevelItemCount() - 1].setText(host)
    
  def loadWordListIdx(self, idx):
    self.wordlistIndices[self.tree.topLevelItemCount() - 1].setValue(idx)
  
  def newXSS(self):
    self.newTC("Empty XSS TC")
    tcEdit = XSSEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)
    
    wordlistIdxArea = QHBoxLayout()
    wordlistIdxLabel = QLabel("Wordlist Index:")
    wordlistIdxEdit = QSpinBox()
    wordlistIdxEdit.setMinimum(0)
    wordlistIdxEdit.setValue(0)
    self.wordlistIndices.extend([wordlistIdxEdit])
    wordlistIdxSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    wordlistIdxArea.addWidget(wordlistIdxLabel)
    wordlistIdxArea.addWidget(wordlistIdxEdit)
    wordlistIdxArea.addSpacerItem(wordlistIdxSpacer)
    self.configAreas[len(self.configAreas) - 1].addLayout(wordlistIdxArea)

  def newSQLi(self):
    self.newTC("Empty SQLi TC")
    tcEdit = SQLiEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)
    
    wordlistIdxArea = QHBoxLayout()
    wordlistIdxLabel = QLabel("Wordlist Index:")
    wordlistIdxEdit = QSpinBox()
    wordlistIdxEdit.setMinimum(0)
    wordlistIdxEdit.setValue(0)
    self.wordlistIndices.extend([wordlistIdxEdit])
    wordlistIdxSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    wordlistIdxArea.addWidget(wordlistIdxLabel)
    wordlistIdxArea.addWidget(wordlistIdxEdit)
    wordlistIdxArea.addSpacerItem(wordlistIdxSpacer)
    self.configAreas[len(self.configAreas) - 1].addLayout(wordlistIdxArea)
    
  def newDirectoryTraversal(self):
    self.newTC("Empty Directory Traversal TC")
    tcEdit = DirectoryTraversalEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)
    
    wordlistIdxArea = QHBoxLayout()
    wordlistIdxLabel = QLabel("Wordlist Index:")
    wordlistIdxEdit = QSpinBox()
    wordlistIdxEdit.setMinimum(0)
    wordlistIdxEdit.setValue(0)
    self.wordlistIndices.extend([wordlistIdxEdit])
    wordlistIdxSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    wordlistIdxArea.addWidget(wordlistIdxLabel)
    wordlistIdxArea.addWidget(wordlistIdxEdit)
    wordlistIdxArea.addSpacerItem(wordlistIdxSpacer)
    self.configAreas[len(self.configAreas) - 1].addLayout(wordlistIdxArea)
    
  def newSynFlood(self):
    self.newTC("Empty Syn Flood TC")
    tcEdit = SynFloodEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)
    
  def newSynFloodOverGTP(self):
    self.newTC("Empty Syn Flood Over GTP TC")
    tcEdit = SynFloodOverGTPEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)

  def loadSynFlood(self):
    tcEdit = SynFloodEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)
        
    #FIXME:
    self.wordlistIndices.extend(["dummy"])
    
    QObject.connect(self.configParser, SIGNAL("disconnectSynFloodSpecificSignals()"), self.disconnectSynFloodSpecificSignals)
    
    QObject.connect(self.configParser, SIGNAL("pps(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newPPS)
    QObject.connect(self.configParser, SIGNAL("packet(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newPacket)
    QObject.connect(self.configParser, SIGNAL("srcPortHigh(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcPortHigh)
    QObject.connect(self.configParser, SIGNAL("dstPortHigh(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstPortHigh)
    QObject.connect(self.configParser, SIGNAL("srcIPHigh(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcIPHigh)
    QObject.connect(self.configParser, SIGNAL("dstIPHigh(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstIPHigh)
    
  def loadSynFloodOverGTP(self):
    tcEdit = SynFloodOverGTPEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)
    
    #FIXME:
    self.wordlistIndices.extend(["dummy"])
    
    QObject.connect(self.configParser, SIGNAL("disconnectSynFloodOverGTPSpecificSignals()"), self.disconnectSynFloodOverGTPSpecificSignals)
    
    QObject.connect(self.configParser, SIGNAL("pps(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newPPS)
    QObject.connect(self.configParser, SIGNAL("packet(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newPacket)
    QObject.connect(self.configParser, SIGNAL("srcPortHighUDP(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcPortHighUDP)
    QObject.connect(self.configParser, SIGNAL("dstPortHighUDP(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstPortHighUDP)
    QObject.connect(self.configParser, SIGNAL("srcIPHighIP1(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcIPHighIP1)
    QObject.connect(self.configParser, SIGNAL("dstIPHighIP1(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstIPHighIP1)
    QObject.connect(self.configParser, SIGNAL("srcPortHighTCP(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcPortHighTCP)
    QObject.connect(self.configParser, SIGNAL("dstPortHighTCP(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstPortHighTCP)
    QObject.connect(self.configParser, SIGNAL("srcIPHighIP2(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcIPHighIP2)
    QObject.connect(self.configParser, SIGNAL("dstIPHighIP2(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstIPHighIP2)
    
  def loadXSS(self):
    tcEdit = XSSEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)
    
    wordlistIdxArea = QHBoxLayout()
    wordlistIdxLabel = QLabel("Wordlist Index:")
    wordlistIdxEdit = QSpinBox()
    wordlistIdxEdit.setMinimum(-1)
    wordlistIdxEdit.setValue(-1)
    self.wordlistIndices.extend([wordlistIdxEdit])
    wordlistIdxSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    wordlistIdxArea.addWidget(wordlistIdxLabel)
    wordlistIdxArea.addWidget(wordlistIdxEdit)
    wordlistIdxArea.addSpacerItem(wordlistIdxSpacer)
    self.configAreas[len(self.configAreas) - 1].addLayout(wordlistIdxArea)
    
    QObject.connect(self.configParser, SIGNAL("disconnectXSSSpecificSignals()"), self.disconnectXSSSpecificSignals)
    
    QObject.connect(self.configParser, SIGNAL("connectto(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newConnect)
    QObject.connect(self.configParser, SIGNAL("close(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newClose)
    QObject.connect(self.configParser, SIGNAL("httprequest(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPRequest)
    QObject.connect(self.configParser, SIGNAL("testresults(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPResponse)
    QObject.connect(self.configParser, SIGNAL("templateparams(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newTemplateParams)

  def loadSQLi(self):
    tcEdit = SQLiEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)
    
    wordlistIdxArea = QHBoxLayout()
    wordlistIdxLabel = QLabel("Wordlist Index:")
    wordlistIdxEdit = QSpinBox()
    wordlistIdxEdit.setMinimum(-1)
    wordlistIdxEdit.setValue(-1)
    self.wordlistIndices.extend([wordlistIdxEdit])
    wordlistIdxSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    wordlistIdxArea.addWidget(wordlistIdxLabel)
    wordlistIdxArea.addWidget(wordlistIdxEdit)
    wordlistIdxArea.addSpacerItem(wordlistIdxSpacer)
    self.configAreas[len(self.configAreas) - 1].addLayout(wordlistIdxArea)
    
    QObject.connect(self.configParser, SIGNAL("disconnectSQLiSpecificSignals()"), self.disconnectSQLiSpecificSignals)
     
    QObject.connect(self.configParser, SIGNAL("connectto(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newConnect)
    QObject.connect(self.configParser, SIGNAL("close(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newClose)
    QObject.connect(self.configParser, SIGNAL("httprequest(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPRequest)
    QObject.connect(self.configParser, SIGNAL("testresults(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPResponse)
    QObject.connect(self.configParser, SIGNAL("templateparams(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newTemplateParams)

  def loadDirectoryTraversal(self):
    tcEdit = DirectoryTraversalEdit()
    self.tcEdits.extend([tcEdit])
    self.configAreas[len(self.configAreas) - 1].addWidget(tcEdit)
    
    wordlistIdxArea = QHBoxLayout()
    wordlistIdxLabel = QLabel("Wordlist Index:")
    wordlistIdxEdit = QSpinBox()
    wordlistIdxEdit.setMinimum(-1)
    wordlistIdxEdit.setValue(-1)
    self.wordlistIndices.extend([wordlistIdxEdit])
    wordlistIdxSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    wordlistIdxArea.addWidget(wordlistIdxLabel)
    wordlistIdxArea.addWidget(wordlistIdxEdit)
    wordlistIdxArea.addSpacerItem(wordlistIdxSpacer)
    self.configAreas[len(self.configAreas) - 1].addLayout(wordlistIdxArea)
    
    QObject.connect(self.configParser, SIGNAL("disconnectDirectoryTraversalSpecificSignals()"), self.disconnectDirectoryTraversalSpecificSignals)
     
    QObject.connect(self.configParser, SIGNAL("connectto(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newConnect)
    QObject.connect(self.configParser, SIGNAL("close(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newClose)
    QObject.connect(self.configParser, SIGNAL("httprequest(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPRequest)
    QObject.connect(self.configParser, SIGNAL("testresults(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPResponse)
    QObject.connect(self.configParser, SIGNAL("templateparams(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newTemplateParams)
    QObject.connect(self.configParser, SIGNAL("depth(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDepth)

  def disconnectXSSSpecificSignals(self):
    QObject.disconnect(self.configParser, SIGNAL("connectto(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newConnect)
    QObject.disconnect(self.configParser, SIGNAL("close(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newClose)
    QObject.disconnect(self.configParser, SIGNAL("httprequest(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPRequest)
    QObject.disconnect(self.configParser, SIGNAL("testresults(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPResponse)
    QObject.disconnect(self.configParser, SIGNAL("templateparams(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newTemplateParams)

  
  def disconnectSQLiSpecificSignals(self):
    QObject.disconnect(self.configParser, SIGNAL("connectto(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newConnect)
    QObject.disconnect(self.configParser, SIGNAL("close(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newClose)
    QObject.disconnect(self.configParser, SIGNAL("httprequest(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPRequest)
    QObject.disconnect(self.configParser, SIGNAL("testresults(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPResponse)
    QObject.disconnect(self.configParser, SIGNAL("templateparams(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newTemplateParams)

  def disconnectDirectoryTraversalSpecificSignals(self):
    QObject.disconnect(self.configParser, SIGNAL("connectto(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newConnect)
    QObject.disconnect(self.configParser, SIGNAL("close(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newClose)
    QObject.disconnect(self.configParser, SIGNAL("httprequest(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPRequest)
    QObject.disconnect(self.configParser, SIGNAL("testresults(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newHTTPResponse)
    QObject.disconnect(self.configParser, SIGNAL("templateparams(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newTemplateParams)
    QObject.disconnect(self.configParser, SIGNAL("depth(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDepth)

  def disconnectSynFloodSpecificSignals(self):
    QObject.disconnect(self.configParser, SIGNAL("pps(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newPPS)
    QObject.disconnect(self.configParser, SIGNAL("packet(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newPacket)
    QObject.disconnect(self.configParser, SIGNAL("srcPortHigh(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcPortHigh)
    QObject.disconnect(self.configParser, SIGNAL("dstPortHigh(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstPortHigh)
    QObject.disconnect(self.configParser, SIGNAL("srcIPHigh(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcIPHigh)
    QObject.disconnect(self.configParser, SIGNAL("dstIPHigh(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstIPHigh)
  
  def disconnectSynFloodOverGTPSpecificSignals(self):
    QObject.disconnect(self.configParser, SIGNAL("pps(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newPPS)
    QObject.disconnect(self.configParser, SIGNAL("packet(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newPacket)
    QObject.disconnect(self.configParser, SIGNAL("srcPortHighUDP(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcPortHighUDP)
    QObject.disconnect(self.configParser, SIGNAL("dstPortHighUDP(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstPortHighUDP)
    QObject.disconnect(self.configParser, SIGNAL("srcIPHighIP1(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcIPHighIP1)
    QObject.disconnect(self.configParser, SIGNAL("dstIPHighIP1(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstIPHighIP1)
    QObject.disconnect(self.configParser, SIGNAL("srcPortHighTCP(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcPortHighTCP)
    QObject.disconnect(self.configParser, SIGNAL("dstPortHighTCP(int)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstPortHighTCP)
    QObject.disconnect(self.configParser, SIGNAL("srcIPHighIP2(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newSrcIPHighIP2)
    QObject.disconnect(self.configParser, SIGNAL("dstIPHighIP2(PyQt_PyObject)"), self.tcEdits[self.tree.topLevelItemCount() - 1].newDstIPHighIP2)
    
  def start(self):
    if self.filename == "":
      msgBox = QMessageBox()
      msgBox.setText("Configuration not saved.")
      msgBox.setInformativeText("Do you want to save your changes?")
      msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
      msgBox.setDefaultButton(QMessageBox.Save)
      if msgBox.exec_() == QMessageBox.Save:
        self.saveConfig()
      else:
        return
    self.emit(SIGNAL("filename(PyQt_PyObject)"), self.filename)
    for i in xrange(self.tree.topLevelItemCount()):
      if self.tcEdits[i].tcType == "SynFlood" or self.tcEdits[i].tcType == "SynFloodOverGTP":
        self.emit(SIGNAL("component(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.tree.topLevelItem(i).text(0), self.tcEdits[i].tcType, [self.tcEdits[i].ppsEdit.text()])
      elif self.tcEdits[i].tcType == "XSS" or self.tcEdits[i].tcType == "SQLi" or self.tcEdits[i].tcType == "DirectoryTraversal":
        self.emit(SIGNAL("component(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.tree.topLevelItem(i).text(0), self.tcEdits[i].tcType, [])
