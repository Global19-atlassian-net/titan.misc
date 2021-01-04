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
  
from StatWidget import StatWidget

class StatArea(QWidget):
    
    def __init__(self, configured):
        super(StatArea, self).__init__()
        
        self.vLayout = QVBoxLayout()
        
        self.w = StatWidget(configured)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.w)
        self.scrollArea.setMinimumHeight(117)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.configuredTitleLabel = QLabel("Configured p/s:")
        self.configuredValueLabel = QLabel(str(float(configured)))
        self.actualTitleLabel = QLabel("Actual p/s:")
        self.actualValueLabel = QLabel("0.0")
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout = QHBoxLayout()
        
        self.hLayout.addWidget(self.configuredTitleLabel)
        self.hLayout.addWidget(self.configuredValueLabel)
        self.hLayout.addWidget(self.actualTitleLabel)
        self.hLayout.addWidget(self.actualValueLabel)
        self.hLayout.addSpacerItem(self.spacer)
        
        self.vLayout.addWidget(self.scrollArea)
        self.vLayout.addLayout(self.hLayout)
        
        self.setLayout(self.vLayout)
        
    def newStat(self, y):
        self.w.newStat(y)
        self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().maximum())
        self.actualValueLabel.setText(str(float(y)))
