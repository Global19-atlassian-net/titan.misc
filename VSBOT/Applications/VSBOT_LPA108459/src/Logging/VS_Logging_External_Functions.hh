/******************************************************************************
* Copyright (c) 2000-2021 Ericsson Telecom AB
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Eclipse Public License v2.0
* which accompanies this distribution, and is available at
* https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
*
* Contributor: david.ferenc.vranics@ericsson.com
******************************************************************************/

#ifndef VS_Logging_External_Functions_HH
#define VS_Logging_External_Functions_HH

#include <TTCN3.hh>

namespace VS__Logging__Functions
{
  void log__debug(CHARSTRING const &msg);
  void log__warning(CHARSTRING const &msg);
  void log__error(CHARSTRING const &msg);
  void log__user(CHARSTRING const &msg);
  void log__testcase(CHARSTRING const &msg);
}

#endif
