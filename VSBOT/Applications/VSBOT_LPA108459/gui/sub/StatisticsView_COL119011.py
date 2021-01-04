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
  
from StatArea import StatArea
from StatTreeWidgetItem import StatTreeWidgetItem

class StatisticsView(QTreeWidget):
    
    def __init__(self):
        super(StatisticsView, self).__init__()
        self.setAlternatingRowColors(True)
        self.header().hide()
        self.statAreas = list()
        self.setToolTip("The returned verdicts/statistics appear in this area.")
        
    def newStatFLOODING(self, idx, data):
        self.statAreas[idx].newStat(data)
        
    def newStatSCANNING(self, tcIdx, wordlistIdx, verdict, word, note):
        if note != "":
          word = word + ": "
        
        #refactor this using a design pattern
        color = QColor()
        if verdict == "PASS":
          color = QColor(137, 186, 23)
        elif verdict == "FAIL":
          color = QColor(227, 34, 25)
        elif verdict == "INCONCLUSIVE":
          color = QColor(250, 187, 0)
        elif verdict == "NONE":
          color = QColor(0, 169, 212)
        elif verdict == "ERROR":
          color = QColor(0, 0, 0)
          
        componentItem = self.topLevelItem(tcIdx)
        verdictItem = StatTreeWidgetItem()
        if componentItem.childCount() <= wordlistIdx: #no verdict yet
          verdictItem = StatTreeWidgetItem(componentItem)
          verdictItem.setBackground(0, color)
          verdictItem.setText(0, word + note)
          verdictItem.verdict = verdict          
        else:
          verdictItem = componentItem.child(wordlistIdx)
          
          if ((verdictItem.background(0).color().rgb() == QColor(0, 169, 212).rgb()) or
              (verdictItem.background(0).color().rgb() == QColor(137, 186, 23).rgb() and verdict != "NONE") or
              (verdictItem.background(0).color().rgb() == QColor(250, 187, 0).rgb() and verdict != "NONE" and verdict != "PASS") or
              (verdictItem.background(0).color().rgb() == QColor(227, 34, 25).rgb() and verdict != "NONE" and verdict != "PASS" and verdict != "INCONCLUSIVE")):
            verdictItem.setBackground(0, color)
            verdictItem.setText(0, word + note)
            verdictItem.verdict = verdict
          elif verdict == "ERROR":
            verdictItem.setBackground(0, color)
            verdictItem.setForeground(0, Qt.red)
            verdictItem.setText(0, word + note)
            verdictItem.verdict = verdict
        
    def component(self, compName, compType, params):
        if compType == "SynFlood" or compType == "SynFloodOverGTP":
            componentItem = StatTreeWidgetItem(self)
            componentItem.setText(0, compName + " (" + str(params[0]) + " p/s)")
            statItem = StatTreeWidgetItem(componentItem)
            statArea = StatArea(params[0])
            self.setItemWidget(statItem, 0, statArea);
            self.statAreas.extend([statArea])
        elif compType == "XSS" or compType == "SQLi" or compType == "DirectoryTraversal":
            componentItem = QTreeWidgetItem(self)
            componentItem.setText(0, compName)
            self.statAreas.extend(["DUMMY"]) #TODO: fix this
            
    def serialize(self, path):
        for i in xrange(self.invisibleRootItem().childCount()):
          self.emit(SIGNAL("reportTC(PyQt_PyObject)"), self.topLevelItem(i).text(0))
          if self.statAreas[i] == "DUMMY":
            for j in xrange(self.topLevelItem(i).childCount()):
              self.emit(SIGNAL("reportSCANNING(PyQt_PyObject, PyQt_PyObject)"), self.topLevelItem(i).child(j).text(0), self.topLevelItem(i).child(j).verdict)
          else:
            pic = QPixmap(self.statAreas[i].w.size())
            self.statAreas[i].w.render(pic)
            pic.save(path + "/component" + str(i) + ".png")
            self.emit(SIGNAL("reportFLOODING(PyQt_PyObject)"), "component" + str(i) + ".png")
        self.emit(SIGNAL("done()"))
    
    def clear(self):
        while self.topLevelItemCount() != 0:
            self.takeTopLevelItem(0)
            self.statAreas.pop(0)
