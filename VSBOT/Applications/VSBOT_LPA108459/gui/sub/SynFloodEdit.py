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

class SynFloodEdit(QWidget):
  def __init__(self, parent = None):
    super(SynFloodEdit, self).__init__(parent)
    
    self.tcType = "SynFlood"
    
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
TCP :=\n\
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
}")

    self.srcPortHighCheckBox = QCheckBox()
    self.srcPortHighLabel = QLabel("Source port range upper bound:")
    self.srcPortHighEdit = QSpinBox()
    self.srcPortHighEdit.setMaximum(65535)
    self.srcPortHighEdit.setEnabled(False)
    self.srcPortHighSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.srcPortHighLayout = QHBoxLayout()
    self.srcPortHighLayout.addWidget(self.srcPortHighCheckBox)
    self.srcPortHighLayout.addWidget(self.srcPortHighLabel)
    self.srcPortHighLayout.addWidget(self.srcPortHighEdit)
    self.srcPortHighLayout.addSpacerItem(self.srcPortHighSpacer)
    
    self.dstPortHighCheckBox = QCheckBox()
    self.dstPortHighLabel = QLabel("Destination port range upper bound:")
    self.dstPortHighEdit = QSpinBox()
    self.dstPortHighEdit.setMaximum(65535)
    self.dstPortHighEdit.setEnabled(False)
    self.dstPortHighSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.dstPortHighLayout = QHBoxLayout()
    self.dstPortHighLayout.addWidget(self.dstPortHighCheckBox)
    self.dstPortHighLayout.addWidget(self.dstPortHighLabel)
    self.dstPortHighLayout.addWidget(self.dstPortHighEdit)
    self.dstPortHighLayout.addSpacerItem(self.dstPortHighSpacer)
    
    self.srcIPHighCheckBox = QCheckBox()
    self.srcIPHighLabel = QLabel("Source IP range upper bound:")
    self.srcIPHighEdit = QLineEdit()
    self.srcIPHighEdit.setEnabled(False)
    self.srcIPHighSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.srcIPHighLayout = QHBoxLayout()
    self.srcIPHighLayout.addWidget(self.srcIPHighCheckBox)
    self.srcIPHighLayout.addWidget(self.srcIPHighLabel)
    self.srcIPHighLayout.addWidget(self.srcIPHighEdit)
    self.srcIPHighLayout.addSpacerItem(self.srcIPHighSpacer)
    
    self.dstIPHighCheckBox = QCheckBox()
    self.dstIPHighLabel = QLabel("Destination IP range upper bound:")
    self.dstIPHighEdit = QLineEdit()
    self.dstIPHighEdit.setEnabled(False)
    self.dstIPHighSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.dstIPHighLayout = QHBoxLayout()
    self.dstIPHighLayout.addWidget(self.dstIPHighCheckBox)
    self.dstIPHighLayout.addWidget(self.dstIPHighLabel)
    self.dstIPHighLayout.addWidget(self.dstIPHighEdit)
    self.dstIPHighLayout.addSpacerItem(self.dstIPHighSpacer)

    self.vLayout.addLayout(self.ppsLayout)
    self.vLayout.addWidget(self.packetLabel)
    self.vLayout.addWidget(self.packetEdit)
    self.vLayout.addLayout(self.srcPortHighLayout)
    self.vLayout.addLayout(self.dstPortHighLayout)
    self.vLayout.addLayout(self.srcIPHighLayout)
    self.vLayout.addLayout(self.dstIPHighLayout)
    
    self.setLayout(self.vLayout)
    
    QObject.connect(self.srcPortHighCheckBox, SIGNAL("stateChanged(int)"), self.switchSrcPortHigh)
    QObject.connect(self.dstPortHighCheckBox, SIGNAL("stateChanged(int)"), self.switchDstPortHigh)
    QObject.connect(self.srcIPHighCheckBox, SIGNAL("stateChanged(int)"), self.switchSrcIPHigh)
    QObject.connect(self.dstIPHighCheckBox, SIGNAL("stateChanged(int)"), self.switchDstIPHigh)
 
  #this should convert things to text
  def serialize(self):
    offset = "        "
    s = ""
    s = s + "      " + "SynFlood :=\n"
    s = s + "      " + "{\n"
    s = s + offset + "packetPerSec := " + self.ppsEdit.text() + ",\n"
    s = s + offset + "packet :=\n" + offset + "{\n  " + offset + str(self.packetEdit.toPlainText()).replace("\n", "\n  " + offset) + "\n" + offset + "}"
    if self.srcPortHighCheckBox.checkState():
      s = s + ",\n" + offset + "srcPortHigh := " + str(self.srcPortHighEdit.value())
    if self.dstPortHighCheckBox.checkState():
      s = s + ",\n" + offset + "dstPortHigh := " + str(self.dstPortHighEdit.value())
    if self.srcIPHighCheckBox.checkState():
      s = s + ",\n" + offset + "srcIPHigh := \"" + self.srcIPHighEdit.text() + "\""
    if self.dstIPHighCheckBox.checkState():
      s = s + ",\n" + offset + "dstIPHigh := \"" + self.dstIPHighEdit.text() + "\""
    s = s + "\n      " + "}"
    return s
    
  def switchSrcPortHigh(self, state):
    self.srcPortHighEdit.setEnabled(state)
    
  def switchDstPortHigh(self, state):
    self.dstPortHighEdit.setEnabled(state)
    
  def switchSrcIPHigh(self, state):
    self.srcIPHighEdit.setEnabled(state)
    
  def switchDstIPHigh(self, state):
    self.dstIPHighEdit.setEnabled(state)
    
  def newPacket(self, packet):
    self.packetEdit.setText(packet)
    
  def newPPS(self, pps):
    self.ppsEdit.setText(pps)
    
  def newSrcPortHigh(self, value):
    self.srcPortHighCheckBox.setCheckState(Qt.Checked)
    self.srcPortHighEdit.setValue(value)
      
  def newDstPortHigh(self, value):
    self.dstPortHighCheckBox.setCheckState(Qt.Checked)
    self.dstPortHighEdit.setValue(value)
    
  def newSrcIPHigh(self, value):
    self.srcIPHighCheckBox.setCheckState(Qt.Checked)
    self.srcIPHighEdit.setText(value)
    
  def newDstIPHigh(self, value):
    self.dstIPHighCheckBox.setCheckState(Qt.Checked)
    self.dstIPHighEdit.setText(value)
