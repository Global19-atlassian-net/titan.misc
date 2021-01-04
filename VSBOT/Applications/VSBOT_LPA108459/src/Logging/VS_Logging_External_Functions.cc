/******************************************************************************
* Copyright (c) 2000-2021 Ericsson Telecom AB
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Eclipse Public License v2.0
* which accompanies this distribution, and is available at
* https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
*
* Contributor: david.ferenc.vranics@ericsson.com
******************************************************************************/

#include "VS_Logging_External_Functions.hh"

namespace VS__Logging__Functions
{
  ////////////////////////////////////////////////////////////////////////
  /////    Default log functions
  /////    (Based on the corresponding functions of the Abstract_Socket TestPort)
  ////////////////////////////////////////////////////////////////////////
  void log__debug(const CHARSTRING &msg)
  {
      TTCN_Logger::begin_event(TTCN_DEBUG);
      TTCN_Logger::log_event("Vulnerability Scanner: DEBUG: %s", (const char*)(msg));
      TTCN_Logger::end_event();
  }

  void log__warning(const CHARSTRING &msg)
  {
    TTCN_Logger::begin_event(TTCN_WARNING);
    TTCN_Logger::log_event("Vulnerability Scanner: WARNING: %s", (const char*)(msg));
    TTCN_Logger::end_event();
  }

  void log__error(const CHARSTRING &msg)
  {
    TTCN_Logger::begin_event(TTCN_ERROR);
    TTCN_Logger::log_event("Vulnerability Scanner: ERROR: %s", (const char*)(msg));
    TTCN_Logger::end_event();
  }
  
  void log__user(const CHARSTRING &msg)
  {
    TTCN_Logger::begin_event(TTCN_USER);
    TTCN_Logger::log_event("Vulnerability Scanner: USER: %s", (const char*)(msg));
    TTCN_Logger::end_event();
  }
  
  void log__testcase(const CHARSTRING &msg)
  {
    TTCN_Logger::begin_event(TTCN_USER);
    TTCN_Logger::log_event("Vulnerability Scanner: TESTCASE: %s", (const char*)(msg));
    TTCN_Logger::end_event();
  }
}
