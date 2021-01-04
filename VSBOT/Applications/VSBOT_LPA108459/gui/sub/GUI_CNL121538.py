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

from CentralWidget import *

################################################

class GUI(QMainWindow):
  def __init__(self, parent = None):
    super(GUI, self).__init__(parent)
    
  def repaint(self):
  
    self.setWindowTitle("Vulnerability Scanner (VSBOT)")
    self.setWindowFlags(Qt.FramelessWindowHint) 
    self.setMinimumHeight(334)
    self.setMinimumWidth(500)
    self.resize(500, 334)
    
    #style
    self.setStyleSheet("\
    QMainWindow {\
      background: #e2e2e2;\
      border: 1px solid #cecdcd;\
    }\
    \
    QWidget {\
      font-size: 13px;\
      font-family: \"Arial\";\
    }\
    \
    QWidget#eFullBlendWidget {\
      background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,\
                  stop: 0 #a1c517, stop: 0.25 #009045,\
                  stop: 0.5 #0082b6, stop: 0.75 #151f77,\
                  stop: 1.0 #db004f);\
    }\
    \
    QWidget#eHeaderWidget {\
      background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                  stop: 0 #ffffff,\
                  stop: 1.0 #cecdcd);\
    }\
    QTabWidget#menuTabWidget::pane {\
      background: #ffffff;\
      border: none;\
    }\
    \
    QTabBar::tab {\
      background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                    stop: 0 #f3f3f3, stop: 1.0 #d4d4d4);\
      border-top: none;\
      border-left: 1px solid #e6e7e8;\
      border-bottom: 2px solid #b9bbbb;\
      border-right: 2px solid #b9bbbb;\
      max-height: 48px;\
      padding: 4px;\
    }\
    \
    QTabBar::tab:selected {\
      background: #ffffff;\
      border: none;\
      border-bottom: 2px solid #b9bbbb;\
    }\
    \
    QLabel#titleLabel {\
      color: #00285e;\
    }\
    \
    QPushButton {\
      color: #ffffff;\
      border: 1px solid #bfbebe;\
      border-radius: 6px;\
      padding-top: 7px;\
      padding-bottom: 8px;\
      padding-left: 10px;\
      padding-right: 10px;\
      min-width: 67px;\
      background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                  stop: 0.0 #ffffff,\
                  stop: 0.1 #abbfd4,\
                  stop: 0.2 #316196,\
                  stop: 0.9 #1b3d6f,\
                  stop: 1.0 #1d335a);\
    }\
    \
    QPushButton:hover {\
      border: 3px solid #00a9d4;\
      background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                  stop: 0.0 #ffffff,\
                  stop: 0.1 #98d5ea,\
                  stop: 0.2 #0697cb,\
                  stop: 1.0 #0a5097);\
    }\
    \
    QPushButton:pressed {\
      border: 1px solid #bfbebe;\
      background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                  stop: 0.0 #ffffff,\
                  stop: 0.1 #abbfd4,\
                  stop: 0.2 #316196,\
                  stop: 0.9 #316196,\
                  stop: 1.0 #1d335a);\
    }\
    \
    QPushButton#minimizeButton, QPushButton#maximizeButton, QPushButton#closeButton {\
      min-width: 0px;\
      background: none;\
      border: none;\
    }\
    \
    QTreeView::branch:open:has-children {\
      image: url(icons/arrowdown.png);\
    }\
    \
    QTreeView::branch:closed:has-children {\
      image: url(icons/arrowright.png);\
    }/*\
    \
    QScrollBar:vertical {\
	    border: none;\
	    margin: 20px 0px 20px 0px;\
	  }\
	  \
    QScrollBar::add-line:vertical {\
	    image: url(icons/arrowdown.png);\
	  }\
    \
    QScrollBar::sub-line:vertical {\
	    image: url(icons/arrowup.png);\
	  }*/")
    
    self.centralWidget = CentralWidget()
    QObject.connect(self.centralWidget, SIGNAL("minimizeClicked()"), self.minimize)
    QObject.connect(self.centralWidget, SIGNAL("maximizeClicked()"), self.maximize)
    QObject.connect(self.centralWidget, SIGNAL("closeClicked()"), self.close)
    
    self.setCentralWidget(self.centralWidget)
    self.show()
  
  def minimize(self):
    self.showMinimized()
    
  def maximize(self):
    if self.windowState() & Qt.WindowMaximized:
      self.showNormal()
    else:
      self.showMaximized()

  def mousePressEvent(self, event):
    self.mouseClickX = event.x()
    self.mouseClickY = event.y()
    self.geometryBeforeMove = self.geometry()

  def mouseReleaseEvent(self, event):
    self.mouseClickX = event.x()
    self.mouseClickY = event.y()

  def mouseMoveEvent(self, event):
    try:
      #if bottomright corner is grabbed, resize the window
      if self.mouseClickX >= self.geometryBeforeMove.width() - 10 and self.mouseClickY >= self.geometryBeforeMove.height() - 10:
        self.resize(event.x(), event.y())
      #if header is grabbed, move the window
      elif self.mouseClickY < 34:
	      self.move(event.globalX()-self.mouseClickX, event.globalY()-self.mouseClickY)
    except:
	    return None
