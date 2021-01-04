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

class CloseEdit(QWidget):
  def __init__(self, parent = None):
    super(CloseEdit, self).__init__(parent)
    
    self.packetType = "close"
    
    self.vLayout = QVBoxLayout()

    self.label = QLabel("Packet contents:")
    self.packetEdit = QTextEdit()
    self.packetEdit.setPlainText("\
client_id := omit")
   
    self.vLayout.addWidget(self.label)
    self.vLayout.addWidget(self.packetEdit)
    
    self.setLayout(self.vLayout)
    
  #this should convert things to text
  def serialize(self, param = None):
    offset = "          "
    s = ""
    s = s + offset + "HTTPMessageType :=\n"
    s = s + offset + "{\n"
    s = s + offset + "  " + "close :=\n"
    s = s + offset + "  " + "{\n"
    s = s + offset + "    " + str(self.packetEdit.toPlainText()).replace("\n", "\n    " + offset) + "\n"
    s = s + offset + "  " + "}\n"
    s = s + offset + "}\n"
    return s
