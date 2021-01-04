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

class HTTPRequestEdit(QWidget):
  def __init__(self, parent = None):
    super(HTTPRequestEdit, self).__init__(parent)
    
    self.packetType = "request"
    
    self.vLayout = QVBoxLayout()

    self.templatesLabel = QLabel("Template parameters:")
    self.templatesEdit = QLineEdit("\"ATTACKSTRING1\", \"ATTACKSTRING2\"")
    self.packetLabel = QLabel("Request contents:")
    self.packetEdit = QTextEdit()
    self.packetEdit.setPlainText("\
client_id := omit,\n\
method := \"GET\",\n\
uri := \"http://localhost/index.php?param=ATTACKSTRING1\",\n\
version_major := 1,\n\
version_minor := 1,\n\
header := {\n\
  {\n\
    header_name := \"Host\",\n\
    header_value := \"127.0.0.1\"\n\
  },\n\
  {\n\
    header_name := \"Connection\",\n\
    header_value := \"close\"\n\
  }\n\
},\n\
body := \"\"")
    
    self.vLayout.addWidget(self.templatesLabel)
    self.vLayout.addWidget(self.templatesEdit)
    self.vLayout.addWidget(self.packetLabel)
    self.vLayout.addWidget(self.packetEdit)
    
    self.setLayout(self.vLayout)
    
  #this should convert things to text
  def serialize(self, param = None):
    offset = "          "
    s = ""
    s = s + offset + "templateParameters :=\n"
    s = s + offset + "{"
    if self.templatesEdit.text() != "":
      s = s + "\n" + offset + "  " + self.templatesEdit.text()
    s = s + "\n" + offset + "},\n"
    s = s + offset + "HTTPMessageType :=\n"
    s = s + offset + "{\n"
    s = s + offset + "  " + "HTTPMessage :=\n"
    s = s + offset + "  " + "{\n"
    s = s + offset + "    " + "request :=\n"
    s = s + offset + "    " + "{\n"
    s = s + offset + "      " + str(self.packetEdit.toPlainText()).replace("\n", "\n      " + offset) + "\n"
    s = s + offset + "    " + "}\n"
    s = s + offset + "  " + "}\n"
    if param != None:
      s = s + offset + "},\n"
      s = s + offset + "testResults :=\n"
      s = s + offset + "{\n"
      s = s + offset + "  " + str(param) + "\n"
    s = s + offset + "}\n"
    return s
