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

class SynFloodOverGTPEdit(QWidget):
  def __init__(self, parent = None):
    super(SynFloodOverGTPEdit, self).__init__(parent)
    
    self.tcType = "SynFloodOverGTP"
    
    self.vLayout = QVBoxLayout()
    
    self.ppsLabel = QLabel("Packet/sec:")
    self.ppsEdit = QLineEdit("1.0")
    self.ppsSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.ppsLayout = QHBoxLayout()
    self.ppsLayout.addWidget(self.ppsLabel)
    self.ppsLayout.addWidget(self.ppsEdit)
    self.ppsLayout.addSpacerItem(self.ppsSpacer)
    
    self.packetLabel = QLabel("Packet:")
    self.packetEdit = QTextEdit()
    self.packetEdit.setPlainText("\
IP :=\n\
{\n\
  src := omit,\n\
  dst := omit\n\
},\n\
UDP :=\n\
{\n\
  src := omit,\n\
  dst := omit\n\
},\n\
GTP :=\n\
{\n\
  GTPhdr :=\n\
  {\n\
    TEID := omit\n\
  },\n\
  IPhdr := \n\
  {\n\
    src := omit,\n\
    dst := omit\n\
  },\n\
  TCPhdr :=\n\
  {\n\
    src := omit,\n\
    dst := omit,\n\
    seq := omit,\n\
    ackseq := omit,\n\
    doff := omit,\n\
    res1 := omit,\n\
    res2 := omit,\n\
    urg := 0,\n\
    ack := 0,\n\
    psh := 0,\n\
    rst := 0,\n\
    syn := 1,\n\
    fin := 0,\n\
    window := omit,\n\
    checksum := omit,\n\
    urgptr := omit\n\
  }\n\
}")

    self.srcPortHighUDPCheckBox = QCheckBox()
    self.srcPortHighUDPLabel = QLabel("Source port range upper bound:")
    self.srcPortHighUDPEdit = QSpinBox()
    self.srcPortHighUDPEdit.setMaximum(65535)
    self.srcPortHighUDPEdit.setEnabled(False)
    self.srcPortHighUDPSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.srcPortHighUDPLayout = QHBoxLayout()
    self.srcPortHighUDPLayout.addWidget(self.srcPortHighUDPCheckBox)
    self.srcPortHighUDPLayout.addWidget(self.srcPortHighUDPLabel)
    self.srcPortHighUDPLayout.addWidget(self.srcPortHighUDPEdit)
    self.srcPortHighUDPLayout.addSpacerItem(self.srcPortHighUDPSpacer)
    
    self.dstPortHighUDPCheckBox = QCheckBox()
    self.dstPortHighUDPLabel = QLabel("Destination port range upper bound:")
    self.dstPortHighUDPEdit = QSpinBox()
    self.dstPortHighUDPEdit.setMaximum(65535)
    self.dstPortHighUDPEdit.setEnabled(False)
    self.dstPortHighUDPSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.dstPortHighUDPLayout = QHBoxLayout()
    self.dstPortHighUDPLayout.addWidget(self.dstPortHighUDPCheckBox)
    self.dstPortHighUDPLayout.addWidget(self.dstPortHighUDPLabel)
    self.dstPortHighUDPLayout.addWidget(self.dstPortHighUDPEdit)
    self.dstPortHighUDPLayout.addSpacerItem(self.dstPortHighUDPSpacer)
    
    self.srcIPHighIP1CheckBox = QCheckBox()
    self.srcIPHighIP1Label = QLabel("Source IP range upper bound:")
    self.srcIPHighIP1Edit = QLineEdit()
    self.srcIPHighIP1Edit.setEnabled(False)
    self.srcIPHighIP1Spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.srcIPHighIP1Layout = QHBoxLayout()
    self.srcIPHighIP1Layout.addWidget(self.srcIPHighIP1CheckBox)
    self.srcIPHighIP1Layout.addWidget(self.srcIPHighIP1Label)
    self.srcIPHighIP1Layout.addWidget(self.srcIPHighIP1Edit)
    self.srcIPHighIP1Layout.addSpacerItem(self.srcIPHighIP1Spacer)
    
    self.dstIPHighIP1CheckBox = QCheckBox()
    self.dstIPHighIP1Label = QLabel("Destination IP range upper bound:")
    self.dstIPHighIP1Edit = QLineEdit()
    self.dstIPHighIP1Edit.setEnabled(False)
    self.dstIPHighIP1Spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.dstIPHighIP1Layout = QHBoxLayout()
    self.dstIPHighIP1Layout.addWidget(self.dstIPHighIP1CheckBox)
    self.dstIPHighIP1Layout.addWidget(self.dstIPHighIP1Label)
    self.dstIPHighIP1Layout.addWidget(self.dstIPHighIP1Edit)
    self.dstIPHighIP1Layout.addSpacerItem(self.dstIPHighIP1Spacer)
    
    self.srcPortHighTCPCheckBox = QCheckBox()
    self.srcPortHighTCPLabel = QLabel("Source port range upper bound:")
    self.srcPortHighTCPEdit = QSpinBox()
    self.srcPortHighTCPEdit.setMaximum(65535)
    self.srcPortHighTCPEdit.setEnabled(False)
    self.srcPortHighTCPSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.srcPortHighTCPLayout = QHBoxLayout()
    self.srcPortHighTCPLayout.addWidget(self.srcPortHighTCPCheckBox)
    self.srcPortHighTCPLayout.addWidget(self.srcPortHighTCPLabel)
    self.srcPortHighTCPLayout.addWidget(self.srcPortHighTCPEdit)
    self.srcPortHighTCPLayout.addSpacerItem(self.srcPortHighTCPSpacer)
    
    self.dstPortHighTCPCheckBox = QCheckBox()
    self.dstPortHighTCPLabel = QLabel("Destination port range upper bound:")
    self.dstPortHighTCPEdit = QSpinBox()
    self.dstPortHighTCPEdit.setMaximum(65535)
    self.dstPortHighTCPEdit.setEnabled(False)
    self.dstPortHighTCPSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.dstPortHighTCPLayout = QHBoxLayout()
    self.dstPortHighTCPLayout.addWidget(self.dstPortHighTCPCheckBox)
    self.dstPortHighTCPLayout.addWidget(self.dstPortHighTCPLabel)
    self.dstPortHighTCPLayout.addWidget(self.dstPortHighTCPEdit)
    self.dstPortHighTCPLayout.addSpacerItem(self.dstPortHighTCPSpacer)
    
    self.srcIPHighIP2CheckBox = QCheckBox()
    self.srcIPHighIP2Label = QLabel("Source IP range upper bound:")
    self.srcIPHighIP2Edit = QLineEdit()
    self.srcIPHighIP2Edit.setEnabled(False)
    self.srcIPHighIP2Spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.srcIPHighIP2Layout = QHBoxLayout()
    self.srcIPHighIP2Layout.addWidget(self.srcIPHighIP2CheckBox)
    self.srcIPHighIP2Layout.addWidget(self.srcIPHighIP2Label)
    self.srcIPHighIP2Layout.addWidget(self.srcIPHighIP2Edit)
    self.srcIPHighIP2Layout.addSpacerItem(self.srcIPHighIP2Spacer)
    
    self.dstIPHighIP2CheckBox = QCheckBox()
    self.dstIPHighIP2Label = QLabel("Destination IP range upper bound:")
    self.dstIPHighIP2Edit = QLineEdit()
    self.dstIPHighIP2Edit.setEnabled(False)
    self.dstIPHighIP2Spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.dstIPHighIP2Layout = QHBoxLayout()
    self.dstIPHighIP2Layout.addWidget(self.dstIPHighIP2CheckBox)
    self.dstIPHighIP2Layout.addWidget(self.dstIPHighIP2Label)
    self.dstIPHighIP2Layout.addWidget(self.dstIPHighIP2Edit)
    self.dstIPHighIP2Layout.addSpacerItem(self.dstIPHighIP2Spacer)

    self.vLayout.addLayout(self.ppsLayout)
    self.vLayout.addWidget(self.packetLabel)
    self.vLayout.addWidget(self.packetEdit)
    self.vLayout.addLayout(self.srcPortHighUDPLayout)
    self.vLayout.addLayout(self.dstPortHighUDPLayout)
    self.vLayout.addLayout(self.srcIPHighIP1Layout)
    self.vLayout.addLayout(self.dstIPHighIP1Layout)
    self.vLayout.addLayout(self.srcPortHighTCPLayout)
    self.vLayout.addLayout(self.dstPortHighTCPLayout)
    self.vLayout.addLayout(self.srcIPHighIP2Layout)
    self.vLayout.addLayout(self.dstIPHighIP2Layout)
    
    self.setLayout(self.vLayout)
    
    QObject.connect(self.srcPortHighUDPCheckBox, SIGNAL("stateChanged(int)"), self.switchSrcPortHighUDP)
    QObject.connect(self.dstPortHighUDPCheckBox, SIGNAL("stateChanged(int)"), self.switchDstPortHighUDP)
    QObject.connect(self.srcIPHighIP1CheckBox, SIGNAL("stateChanged(int)"), self.switchSrcIPHighIP1)
    QObject.connect(self.dstIPHighIP1CheckBox, SIGNAL("stateChanged(int)"), self.switchDstIPHighIP1)
    QObject.connect(self.srcPortHighTCPCheckBox, SIGNAL("stateChanged(int)"), self.switchSrcPortHighTCP)
    QObject.connect(self.dstPortHighTCPCheckBox, SIGNAL("stateChanged(int)"), self.switchDstPortHighTCP)
    QObject.connect(self.srcIPHighIP2CheckBox, SIGNAL("stateChanged(int)"), self.switchSrcIPHighIP2)
    QObject.connect(self.dstIPHighIP2CheckBox, SIGNAL("stateChanged(int)"), self.switchDstIPHighIP2)
 
  #this should convert things to text
  def serialize(self):
    offset = "        "
    s = ""
    s = s + "      " + "SynFloodOverGTP :=\n"
    s = s + "      " + "{\n"
    s = s + offset + "packetPerSec := " + self.ppsEdit.text() + ",\n"
    s = s + offset + "packet :=\n" + offset + "{\n  " + offset + str(self.packetEdit.toPlainText()).replace("\n", "\n  " + offset) + "\n" + offset + "}"
    if self.srcPortHighUDPCheckBox.checkState():
      s = s + ",\n" + offset + "srcPortHighUDP := " + str(self.srcPortHighUDPEdit.value())
    if self.dstPortHighUDPCheckBox.checkState():
      s = s + ",\n" + offset + "dstPortHighUDP := " + str(self.dstPortHighUDPEdit.value())
    if self.srcIPHighIP1CheckBox.checkState():
      s = s + ",\n" + offset + "srcIPHighIP1 := \"" + self.srcIPHighIP1Edit.text() + "\""
    if self.dstIPHighIP1CheckBox.checkState():
      s = s + ",\n" + offset + "dstIPHighIP1 := \"" + self.dstIPHighIP1Edit.text() + "\""
    if self.srcPortHighTCPCheckBox.checkState():
      s = s + ",\n" + offset + "srcPortHighTCP := " + str(self.srcPortHighTCPEdit.value())
    if self.dstPortHighTCPCheckBox.checkState():
      s = s + ",\n" + offset + "dstPortHighTCP := " + str(self.dstPortHighTCPEdit.value())
    if self.srcIPHighIP2CheckBox.checkState():
      s = s + ",\n" + offset + "srcIPHighIP2 := \"" + self.srcIPHighIP2Edit.text() + "\""
    if self.dstIPHighIP2CheckBox.checkState():
      s = s + ",\n" + offset + "dstIPHighIP2 := \"" + self.dstIPHighIP2Edit.text() + "\""
    s = s + "\n      " + "}"
    return s
    
  def switchSrcPortHighUDP(self, state):
    self.srcPortHighUDPEdit.setEnabled(state)
    
  def switchDstPortHighUDP(self, state):
    self.dstPortHighUDPEdit.setEnabled(state)
    
  def switchSrcIPHighIP1(self, state):
    self.srcIPHighIP1Edit.setEnabled(state)
    
  def switchDstIPHighIP1(self, state):
    self.dstIPHighIP1Edit.setEnabled(state)
    
  def switchSrcPortHighTCP(self, state):
    self.srcPortHighTCPEdit.setEnabled(state)
    
  def switchDstPortHighTCP(self, state):
    self.dstPortHighTCPEdit.setEnabled(state)
    
  def switchSrcIPHighIP2(self, state):
    self.srcIPHighIP2Edit.setEnabled(state)
    
  def switchDstIPHighIP2(self, state):
    self.dstIPHighIP2Edit.setEnabled(state) 
    
  def newPacket(self, packet):
    self.packetEdit.setText(packet)
    
  def newPPS(self, pps):
    self.ppsEdit.setText(pps)
    
  def newSrcPortHighUDP(self, value):
    self.srcPortHighUDPCheckBox.setCheckState(Qt.Checked)
    self.srcPortHighUDPEdit.setValue(value)
      
  def newDstPortHighUDP(self, value):
    self.dstPortHighUDPCheckBox.setCheckState(Qt.Checked)
    self.dstPortHighUDPEdit.setValue(value)
    
  def newSrcIPHighIP1(self, value):
    self.srcIPHighIP1CheckBox.setCheckState(Qt.Checked)
    self.srcIPHighIP1Edit.setText(value)
    
  def newDstIPHighIP1(self, value):
    self.dstIPHighIP1CheckBox.setCheckState(Qt.Checked)
    self.dstIPHighIP1Edit.setText(value)
    
  def newSrcPortHighTCP(self, value):
    self.srcPortHighTCPCheckBox.setCheckState(Qt.Checked)
    self.srcPortHighTCPEdit.setValue(value)
      
  def newDstPortHighTCP(self, value):
    self.dstPortHighTCPCheckBox.setCheckState(Qt.Checked)
    self.dstPortHighTCPEdit.setValue(value)
    
  def newSrcIPHighIP2(self, value):
    self.srcIPHighIP2CheckBox.setCheckState(Qt.Checked)
    self.srcIPHighIP2Edit.setText(value)
    
  def newDstIPHighIP2(self, value):
    self.dstIPHighIP2CheckBox.setCheckState(Qt.Checked)
    self.dstIPHighIP2Edit.setText(value)
