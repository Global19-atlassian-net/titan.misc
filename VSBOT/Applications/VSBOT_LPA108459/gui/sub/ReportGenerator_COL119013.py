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

import time

################################################

class ReportGenerator(QWidget):
  def __init__(self, parent = None):
    super(ReportGenerator, self).__init__(parent)
    
    self.html_escape_table = {
      "&": "&amp;",
      '"': "&quot;",
      "'": "&apos;",
      ">": "&gt;",
      "<": "&lt;",
      }
      
    self.verdict_counter_table = {
      "NONE": 0,
      "PASS": 0,
      "INCONCLUSIVE": 0,
      "FAIL": 0,
      "ERROR": 0
      }
      
    self.vLayout = QVBoxLayout()
    self.hLayout1 = QHBoxLayout()
    self.hLayout2 = QHBoxLayout()
    self.hLayoutButton = QHBoxLayout()
    
    self.nameLabel = QLabel("Auditor:")
    self.nameEdit = QLineEdit("EDVIVRN")
    self.reportLabel = QLabel("Report title:")
    self.reportEdit = QLineEdit("Test run")
    
    self.hLayout1.addWidget(self.nameLabel)
    self.hLayout1.addWidget(self.nameEdit)
    self.hLayout2.addWidget(self.reportLabel)
    self.hLayout2.addWidget(self.reportEdit)
    
    self.notesLabel = QLabel("Notes:")
    self.notesEdit = QTextEdit("This is a sample report from VSBOT.")

    self.generateButton = QPushButton("Generate")
    self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    self.hLayoutButton.addSpacerItem(self.spacer)
    self.hLayoutButton.addWidget(self.generateButton)

    self.vLayout.addLayout(self.hLayout1)
    self.vLayout.addLayout(self.hLayout2)
    self.vLayout.addWidget(self.notesLabel)
    self.vLayout.addWidget(self.notesEdit)
    self.vLayout.addLayout(self.hLayoutButton)
    
    self.setLayout(self.vLayout)
    
    QObject.connect(self.generateButton, SIGNAL("clicked()"), self.generate)
    
  def initCounters(self):
    self.verdict_counter_table["NONE"] = 0
    self.verdict_counter_table["PASS"] = 0
    self.verdict_counter_table["INCONCLUSIVE"] = 0
    self.verdict_counter_table["FAIL"] = 0
    self.verdict_counter_table["ERROR"] = 0
    
  def receiveTC(self, tcname):
    self.file.write("<tr><th class=\"testcase\">" + self.html_escape(tcname) + "</th></tr>\n")
  
  def receiveFLOODING(self, filename):
    self.file.write("<tr><td class=\"testcase\"><img src=\"" + self.html_escape(filename) + "\"></td></tr>\n")
  
  def receiveSCANNING(self, text, verdict):
    self.file.write("<tr><td class=\"testcase\">" + self.html_escape(text) + "</td><td><img src=\"" + self.html_escape(verdict) + ".png\"></td></tr>\n")
    self.update_stats(verdict)
    
  def done(self):
    self.file.write("\n</table>\n<table>\n<tr><th class=\"overall\">Overall statistics:</th></tr>\n")
    for i in self.verdict_counter_table.keys():
      self.file.write("<tr><td class=\"overall\">" + str(i) + ":</td><td class=\"overall number\">" + str(self.verdict_counter_table[i]) + "</td></tr>\n")
    self.file.write("\n</table>\n")
    
    if self.notesEdit.toPlainText() != "":
      self.file.write("\n<table><tr><th class=\"note\">Note:</th></tr><tr><td class=\"note\">" + self.html_escape(str(self.notesEdit.toPlainText())) + "</td></tr></table>\n")
    self.file.write("</body>\n</html>")
    self.file.close()
    msgBox = QMessageBox()
    msgBox.setText("Report generating finished.")
    msgBox.setInformativeText("Filename: report/test.html.")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.setDefaultButton(QMessageBox.Ok)
    msgBox.exec_()
    
  def generate(self):
    self.initCounters()
    self.file = open('./report/test.html','w')
    self.file.write("<!DOCTYPE html><head><title>VSBOT report</title><meta http-equiv=\"Content-Type\" content=\"text/html;charset=UTF-8\"><link rel=\"stylesheet\" type=\"text/css\" href=\"vsbot.css\"/></head><body><img src=\"vsbotlogo.png\"/><h1>" + self.html_escape(str(self.reportEdit.text())) + "</h1><h2>" + self.html_escape(str(self.nameEdit.text())) + "</h2><h2>" + self.html_escape(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())) + "</h2>\n<table>\n")
    self.emit(SIGNAL("generate(PyQt_PyObject)"), "./report/")
    
  def html_escape(self, text):
    return "".join(self.html_escape_table.get(c,c) for c in str(text))
    
  def update_stats(self, verdict):
    self.verdict_counter_table[verdict] = self.verdict_counter_table[verdict] + 1
