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
  
from ConfigurationEditor_COL119010 import ConfigurationEditor
from ExecutionControl_COL119009 import ExecutionControl
from StatisticsView_COL119011 import StatisticsView
from ReportGenerator_COL119013 import ReportGenerator
from HelpMenu_COL119014 import HelpMenu


################################################

class MenuTabWidget(QTabWidget):
  def __init__(self, parent = None):
    super(MenuTabWidget, self).__init__(parent)
    
    self.__previousIndex = 0;
    
    self.setTabPosition(QTabWidget.West)
    self.setIconSize(QSize(48,48))    
    
    self.myTransform = QTransform()
    self.myTransform.rotate(90)
      
    self.configurationEditor = ConfigurationEditor()
    self.executionControl = ExecutionControl()
    self.statisticsView = StatisticsView()
    self.reportGenerator = ReportGenerator()
    self.helpMenu = HelpMenu()
    
    self.addTab(self.configurationEditor, QIcon(QPixmap().fromImage(QImage("icons/config.png").transformed(self.myTransform))), "")
    self.addTab(self.executionControl, QIcon(QPixmap().fromImage(QImage("icons/execctrl.png").transformed(self.myTransform))), "")
    self.addTab(self.statisticsView, QIcon(QPixmap().fromImage(QImage("icons/stats.png").transformed(self.myTransform))), "")
    self.addTab(self.reportGenerator, QIcon(QPixmap().fromImage(QImage("icons/report.png").transformed(self.myTransform))), "")
    self.addTab(self.helpMenu, QIcon(QPixmap().fromImage(QImage("icons/help.png").transformed(self.myTransform))), "")

    self.setTabToolTip(0, "Configuration editor")
    self.setTabToolTip(1, "Execution control")
    self.setTabToolTip(2, "Statistics view")
    self.setTabToolTip(3, "Report generator")
    self.setTabToolTip(4, "Help menu")

    QObject.connect(self.executionControl, SIGNAL("incomingStat(int, int)"), self.statisticsView.newStatFLOODING)
    QObject.connect(self.executionControl, SIGNAL("incomingStat(int, int, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.statisticsView.newStatSCANNING)
    QObject.connect(self.reportGenerator, SIGNAL("generate(PyQt_PyObject)"), self.statisticsView.serialize)
    QObject.connect(self.statisticsView, SIGNAL("reportFLOODING(PyQt_PyObject)"), self.reportGenerator.receiveFLOODING)
    QObject.connect(self.statisticsView, SIGNAL("reportSCANNING(PyQt_PyObject, PyQt_PyObject)"), self.reportGenerator.receiveSCANNING)
    QObject.connect(self.statisticsView, SIGNAL("reportTC(PyQt_PyObject)"), self.reportGenerator.receiveTC)
    QObject.connect(self.statisticsView, SIGNAL("done()"), self.reportGenerator.done)
    QObject.connect(self.configurationEditor, SIGNAL("component(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.statisticsView.component)
    QObject.connect(self.executionControl, SIGNAL("start()"), self.statisticsView.clear)
    QObject.connect(self.executionControl, SIGNAL("start()"), self.configurationEditor.start)
    QObject.connect(self.configurationEditor, SIGNAL("filename(PyQt_PyObject)"), self.executionControl.filename)
