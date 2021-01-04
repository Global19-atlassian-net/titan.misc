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

class ConfigParser(QObject):
  def __init__(self, parent = None):
    super(ConfigParser, self).__init__(parent)
    
    self.offsetData = ""
    self.testCases = list()
    self.l = ""

  def parse(self, filename):
    self.f = open(filename, "r")
    
    self.offsetData = ""
    self.testCases = list()
    self.l = ""
    
    self.readOffsetData()
    self.readTestCases()
    
    self.f.close()
    
  def readOffsetData(self):
    while self.l != "tsp_VS_testCases :=\n":
      self.l = self.f.readline()
      self.offsetData = self.offsetData + self.l
    #TODO: signal offset out here
    
  def readTestCases(self):
    if self.f.readline() != "{\n":
      print "Error!"
      
    while self.l != "}\n" and self.l != "":
      self.readTestCase()
    
  def readTestCase(self):
    x = self.l.lstrip().split(" ", 2)
    if x[0] == "testCaseName":
      self.emit(SIGNAL("newTC(PyQt_PyObject)"), x[2].split("\"")[1])
    elif x[0] == "host":
      self.emit(SIGNAL("host(PyQt_PyObject)"), x[2].split("\"")[1])
    elif x[0] == "testCaseType":
      #FIXME: { error check
      self.l = self.f.readline()
    elif x[0] == "wordListIdx":
      self.emit(SIGNAL("wordlistidx(int)"), int(x[2]))

    if x[0] == "SynFlood":
      self.emit(SIGNAL("synflood()"))
      self.readSynFlood()
    elif x[0] == "SynFloodOverGTP":
      self.emit(SIGNAL("synfloodovergtp()"))
      self.readSynFloodOverGTP()
    elif x[0] == "XSS":
      self.emit(SIGNAL("xss()"))
      self.readXSS()
    elif x[0] == "SQLi":
      self.emit(SIGNAL("sqli()"))
      self.readSQLi()
    elif x[0] == "DirectoryTraversal":
      self.emit(SIGNAL("dirtrav()"))
      self.readDirectoryTraversal()
    self.l = self.f.readline()
    
  def readSynFlood(self):
    while self.l != "      }\n":
      x = self.l.lstrip().split(" ", 2)
      if x[0] == "packetPerSec":
        self.emit(SIGNAL("pps(PyQt_PyObject)"), x[2].split(",")[0])
      elif x[0] == "packet":
        self.f.readline()
        self.l = self.f.readline()
        self.readPacket()
      elif x[0] == "srcPortHigh":
        self.emit(SIGNAL("srcPortHigh(int)"), int(x[2].split(",")[0]))
      elif x[0] == "dstPortHigh":
        self.emit(SIGNAL("dstPortHigh(int)"), int(x[2].split(",")[0]))
      elif x[0] == "srcIPHigh":
        self.emit(SIGNAL("srcIPHigh(PyQt_PyObject)"), x[2].split("\"")[1])
      elif x[0] == "dstIPHigh":
        self.emit(SIGNAL("dstIPHigh(PyQt_PyObject)"), x[2].split("\"")[1])
      self.l = self.f.readline()
    self.emit(SIGNAL("disconnectSynFloodSpecificSignals()"))
    
  def readSynFloodOverGTP(self):
    while self.l != "      }\n":
      x = self.l.lstrip().split(" ", 2)
      if x[0] == "packetPerSec":
        self.emit(SIGNAL("pps(PyQt_PyObject)"), x[2].split(",")[0])
      elif x[0] == "packet":
        self.f.readline()
        self.l = self.f.readline()
        self.readPacket()
      elif x[0] == "srcPortHighUDP":
        self.emit(SIGNAL("srcPortHighUDP(int)"), int(x[2].split(",")[0]))
      elif x[0] == "dstPortHighUDP":
        self.emit(SIGNAL("dstPortHighUDP(int)"), int(x[2].split(",")[0]))
      elif x[0] == "srcIPHighIP1":
        self.emit(SIGNAL("srcIPHighIP1(PyQt_PyObject)"), x[2].split("\"")[1])
      elif x[0] == "dstIPHighIP1":
        self.emit(SIGNAL("dstIPHighIP1(PyQt_PyObject)"), x[2].split("\"")[1])
      elif x[0] == "srcPortHighTCP":
        self.emit(SIGNAL("srcPortHighTCP(int)"), int(x[2].split(",")[0]))
      elif x[0] == "dstPortHighTCP":
        self.emit(SIGNAL("dstPortHighTCP(int)"), int(x[2].split(",")[0]))
      elif x[0] == "srcIPHighIP2":
        self.emit(SIGNAL("srcIPHighIP2(PyQt_PyObject)"), x[2].split("\"")[1])
      elif x[0] == "dstIPHighIP2":
        self.emit(SIGNAL("dstIPHighIP2(PyQt_PyObject)"), x[2].split("\"")[1])
      self.l = self.f.readline()
    self.emit(SIGNAL("disconnectSynFloodOverGTPSpecificSignals()"))
    
  def readXSS(self):
    self.l = self.f.readline()
    while self.l != "        }\n":
      self.l = self.f.readline()
      self.readAttackStep()
    self.emit(SIGNAL("disconnectXSSSpecificSignals()"))
      
  def readSQLi(self):
    self.l = self.f.readline()
    while self.l != "        }\n":
      self.l = self.f.readline()
      self.readAttackStep()
    self.emit(SIGNAL("disconnectSQLiSpecificSignals()"))
    
  def readDirectoryTraversal(self):
    self.l = self.f.readline()
    while self.l != "        }\n":
      self.l = self.f.readline()
      self.readAttackStep()
    self.emit(SIGNAL("disconnectDirectoryTraversalSpecificSignals()"))
      
  def readAttackStep(self):
    while self.l != "        }\n" and self.l != "        },\n":
      self.l = self.f.readline()
      x = self.l.lstrip().split(" ", 2)
      if x[0] == "HTTPMessageType":
        self.readHTTPMessageType()
      elif x[0] == "templateParameters":
        self.readTemplateParameters()
      elif x[0] == "testResults":
        self.readTestResults()
      elif x[0] == "depth":
        self.emit(SIGNAL("depth(int)"), int(x[2].rstrip(",\n")))
      
  def readHTTPMessageType(self):
    self.l = self.f.readline()
    self.l = self.f.readline()
    while self.l.split(",")[0].split("\n")[0] != "          }":
      y = self.l.lstrip().split(" ", 2)
      if y[0] == "connectTo":
        self.emit(SIGNAL("connectto(PyQt_PyObject)"), self.readMsg())
      elif y[0] == "close":
        self.emit(SIGNAL("close(PyQt_PyObject)"), self.readMsg())
      elif y[0] == "HTTPMessage":
        self.emit(SIGNAL("httprequest(PyQt_PyObject)"), self.readMsg())
      self.l = self.f.readline()
    
    #self.l = self.f.readline()
    
  def readTemplateParameters(self):
    x = ""
    self.l = self.f.readline()
    self.l = self.f.readline()
    while self.l.split(",")[0].split("\n")[0] != "          }":
      x = x + self.l
      self.l = self.f.readline()      
    
    x = x.replace("            ", "")
    self.emit(SIGNAL("templateparams(PyQt_PyObject)"), x)
  
  def readTestResults(self):
    x = ""
    self.l = self.f.readline()
    self.l = self.f.readline()
    while self.l.split(",")[0].split("\n")[0] != "          }":
      x = x + self.l
      self.l = self.f.readline()
    
    x = x.replace("            ", "")
    self.emit(SIGNAL("testresults(PyQt_PyObject)"), x)
    self.l = self.f.readline()
  
  def readMsg(self):
    x = ""
    self.l = self.f.readline()
    self.l = self.f.readline()
    while self.l != "            }\n":
      x = x + self.l.replace("              ", "")
      self.l = self.f.readline()
    return x
    
  def readPacket(self):
    x = ""
    while self.l != "        }\n" and self.l != "        },\n":
      x = x + self.l.replace("          ", "")
      self.l = self.f.readline()
    x = x.replace("}\n", "}")
    self.emit(SIGNAL("packet(PyQt_PyObject)"), x)
