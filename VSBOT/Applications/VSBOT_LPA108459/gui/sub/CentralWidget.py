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
  
from MenuTabWidget import *

################################################

class CentralWidget(QWidget):
  def __init__(self):
    super(CentralWidget, self).__init__()
    self.makeGui()
    
  #GUI maker function
  def makeGui(self):    
    self.vLayout = QVBoxLayout()
    self.vLayout.setSpacing(0)
    
    self.setContentsMargins(-7,-10,-7,-7);

    self.hLayout = QHBoxLayout()
    self.hLayout.setSpacing(0)
    
    self.resizeLabel = QLabel()
    self.resizeLabel.setPixmap(QPixmap("icons/resize.png"))
    self.resizeSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    
    self.hLayout.addSpacerItem(self.resizeSpacer)
    self.hLayout.addWidget(self.resizeLabel)

    #################################
    self.eFullBlendWidget = QWidget()
    self.eFullBlendWidget.setObjectName("eFullBlendWidget")
    self.eFullBlendWidget.setFixedHeight(4)

    #################################
    self.eHeaderWidget = QWidget()
    self.eHeaderWidget.setObjectName("eHeaderWidget")
    self.eHeaderWidget.setFixedHeight(30)
    self.eHeaderWidget.setContentsMargins(15,-10,-10,-10);
    
    self.eHeaderWidgetLayout = QHBoxLayout()
    self.eHeaderWidgetLayout.setSpacing(30)
    
    self.eConLabel = QLabel()
    self.eConLabel.setObjectName("eConLabel")
    self.eConLabel.setPixmap(QPixmap("icons/econ.png"))
    #self.eConLabel.setFixedHeight(4)

    self.titleLabel = QLabel()
    self.titleLabel.setObjectName("titleLabel")
    self.titleLabel.setText("Vulnerability Scanner (VSBOT)")
    #self.titleLabel.setFixedHeight(30)
    
    self.hSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    
    self.buttonLayout = QHBoxLayout()
    self.buttonLayout.setSpacing(0)
    
    self.minimizeButton = QPushButton(QIcon(QPixmap().fromImage(QImage("icons/minimize.png"))), "")
    self.minimizeButton.setObjectName("minimizeButton")
    self.minimizeButton.setFixedHeight(20)
    self.minimizeButton.setFixedWidth(20)
    QObject.connect(self.minimizeButton, SIGNAL("clicked()"), self.minimizeClicked)
    
    self.maximizeButton = QPushButton(QIcon(QPixmap().fromImage(QImage("icons/maximize.png"))), "")
    self.maximizeButton.setObjectName("maximizeButton")
    self.maximizeButton.setFixedHeight(20)
    self.maximizeButton.setFixedWidth(20)
    QObject.connect(self.maximizeButton, SIGNAL("clicked()"), self.maximizeClicked)
    
    self.closeButton = QPushButton(QIcon(QPixmap().fromImage(QImage("icons/close.png"))), "")
    self.closeButton.setObjectName("closeButton")
    self.closeButton.setFixedHeight(20)
    self.closeButton.setFixedWidth(20)
    QObject.connect(self.closeButton, SIGNAL("clicked()"), self.closeClicked)
    
    self.buttonLayout.addWidget(self.minimizeButton)
    self.buttonLayout.addWidget(self.maximizeButton)
    self.buttonLayout.addWidget(self.closeButton)
    
    self.eHeaderWidgetLayout.addWidget(self.eConLabel)
    self.eHeaderWidgetLayout.addWidget(self.titleLabel)
    self.eHeaderWidgetLayout.addSpacerItem(self.hSpacer)
    self.eHeaderWidgetLayout.addLayout(self.buttonLayout)
    
    self.eHeaderWidget.setLayout(self.eHeaderWidgetLayout)
    
    #################################
    self.menuTabWidget = MenuTabWidget()
    self.menuTabWidget.setObjectName("menuTabWidget")
        
    #################################
    self.vLayout.addWidget(self.eFullBlendWidget)
    self.vLayout.addWidget(self.eHeaderWidget)
    self.vLayout.addWidget(self.menuTabWidget)
    self.vLayout.addLayout(self.hLayout)
    
    self.setLayout(self.vLayout)
  
  def minimizeClicked(self):
    self.emit(SIGNAL("minimizeClicked()"))
    
  def maximizeClicked(self):
    self.emit(SIGNAL("maximizeClicked()"))
    
  def closeClicked(self):
    self.emit(SIGNAL("closeClicked()"))
    
  def keyPressEvent(self, event):
    if event.key() == Qt.Key_1:
      self.menuTabWidget.setCurrentIndex(0)
    elif event.key() == Qt.Key_2:
      self.menuTabWidget.setCurrentIndex(1)
    elif event.key() == Qt.Key_3:
      self.menuTabWidget.setCurrentIndex(2)
    elif event.key() == Qt.Key_4:
      self.menuTabWidget.setCurrentIndex(3)
    elif event.key() == Qt.Key_5:
      self.menuTabWidget.setCurrentIndex(4)
    elif event.key() == Qt.Key_6:
      self.menuTabWidget.setCurrentIndex(5)
