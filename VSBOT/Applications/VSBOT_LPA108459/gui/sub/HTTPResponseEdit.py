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

class HTTPResponseEdit(QWidget):
  def __init__(self, parent = None):
    super(HTTPResponseEdit, self).__init__(parent)
    
    self.packetType = "response"
    
    self.vLayout = QVBoxLayout()

    self.responsesLabel = QLabel("Responses:")
    self.responsesEdit = QTextEdit()
    self.responsesEdit.setPlainText("\
{\n\
  timerResult :=\n\
  { // if the delayThreshold is exceeded -> fail, else pass\n\
    delayThreshold := 1.0,\n\
    ifOver := fail,\n\
    ifUnder:= pass\n\
  }\n\
},\n\
{\n\
  regexpResult :=\n\
  { // if regexp matches on response's body -> fail\n\
    regexpPattern := \"*(aaa)*(bbb)*\",\n\
    ifMatches := fail\n\
  }\n\
},\n\
{\n\
  statusCodeResult :=\n\
  { // if returned status code is 404 -> fail\n\
    statusCode := 404,\n\
    ifMatches := fail\n\
  }\n\
}")
   
    self.vLayout.addWidget(self.responsesLabel)
    self.vLayout.addWidget(self.responsesEdit)
    
    self.setLayout(self.vLayout)
    
  #this should convert things to text
  def serialize(self, param = None):
    offset = "          "
    s = str(self.responsesEdit.toPlainText()).replace("\n", "\n  " + offset)
    return s
