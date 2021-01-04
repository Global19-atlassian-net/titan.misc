#!/usr/bin/env python

###############################################################################
# Copyright (c) 2000-2021 Ericsson Telecom AB
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
#
# Contributor: david.ferenc.vranics@ericsson.com
###############################################################################

#to import from subfolder
import os, sys, inspect

#cd to gui/ folder
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
#add gui/sub/ to PATH
cmd_subfolder = os.path.realpath(os.path.join(os.getcwd(),"sub"))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

#try to import Qt
try:
  from PyQt4.QtGui import QApplication 
except:
  print "\nPlease install python-qt4 package!\n"
  sys.exit(1)

from GUI_CNL121538 import GUI

################################

if __name__ == "__main__":
  app = QApplication(sys.argv)
  ui = GUI()
  ui.repaint()
  app.exec_()
