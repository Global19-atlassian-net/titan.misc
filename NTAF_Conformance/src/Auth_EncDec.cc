/******************************************************************************
* Copyright (c) 2000-2021 Ericsson Telecom AB
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Eclipse Public License v1.0
* which accompanies this distribution, and is available at
* http://www.eclipse.org/legal/epl-v10.html
*
* Contributors:
*   Elemer Lelik - initial implementation
*   Endre Kulcsar
*   Eszter Susanszky
******************************************************************************/
//
//  File:               AuthEncDec.cc
//  Description:        NTAF Conformance Test Suite 
//  Rev:                 
//  Prodnr:              
//  Updated:            2013-09-10
//  Contact:            http://ttcn.ericsson.se
//
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
//  Module:  
//
//  Purpose:
//     
//
//  Module Parameters:
//      -
//
//  Module depends on:
//    -
//
///////////////////////////////////////////////////////////////////////////////

#include "NTAF_Auth.hh"

namespace NTAF__Auth {

CHARSTRING enc__AuthChallenge(const AuthChallenge& pdu)
{
    if (TTCN_Logger::log_this_event(TTCN_DEBUG)) {
        TTCN_Logger::begin_event(TTCN_DEBUG);
        TTCN_Logger::log_event("Encoding AuthChallenge: ");
        pdu.log();
        TTCN_Logger::end_event();
    }

    TTCN_Buffer buf;
    pdu.encode(AuthChallenge_descr_, buf, TTCN_EncDec::CT_TEXT);
    CHARSTRING ret_val(buf.get_len(), (const char *)buf.get_data());

    if (TTCN_Logger::log_this_event(TTCN_DEBUG)) {
        TTCN_Logger::begin_event(TTCN_DEBUG);
        TTCN_Logger::log_event("Encoded AuthChallenge: ");
        ret_val.log();
        TTCN_Logger::end_event();
    }

    return ret_val;
}

AuthChallenge dec__AuthChallenge(const CHARSTRING& stream)
{
    if (TTCN_Logger::log_this_event(TTCN_DEBUG)) {
        TTCN_Logger::begin_event(TTCN_DEBUG);
        TTCN_Logger::log_event("Decoding AuthChallenge: ");
        stream.log();
        TTCN_Logger::end_event();
    }

    TTCN_Buffer buf;
    buf.put_cs(stream );
    AuthChallenge pdu;



 TTCN_EncDec::error_behavior_t	eb=TTCN_EncDec::get_error_behavior(TTCN_EncDec::ET_LOG_MATCHING);
  if((boolean)tsp__AuthEncDec__debug){
    if (TTCN_Logger::log_this_event(TTCN_DEBUG))  {
      TTCN_Logger::begin_event(TTCN_DEBUG);
      TTCN_Logger::log_event("Decode buffer: /n");
      buf.log();
      TTCN_Logger::end_event();
      }
    TTCN_EncDec::set_error_behavior(TTCN_EncDec::ET_LOG_MATCHING,TTCN_EncDec::EB_WARNING);
  } else {
    TTCN_EncDec::set_error_behavior(TTCN_EncDec::ET_LOG_MATCHING,TTCN_EncDec::EB_IGNORE);
  }

   pdu.decode(AuthChallenge_descr_, buf, TTCN_EncDec::CT_TEXT);

   TTCN_EncDec::set_error_behavior(TTCN_EncDec::ET_LOG_MATCHING,eb);

   
    if (TTCN_Logger::log_this_event(TTCN_DEBUG)) {
        TTCN_Logger::begin_event(TTCN_DEBUG);
        TTCN_Logger::log_event("Decoded AuthChallenge: ");
        pdu.log();
        TTCN_Logger::end_event();
    }

    return pdu;
}


CHARSTRING enc__AuthResponse(const AuthResponse& pdu)
{
    if (TTCN_Logger::log_this_event(TTCN_DEBUG)) {
        TTCN_Logger::begin_event(TTCN_DEBUG);
        TTCN_Logger::log_event("Encoding AuthResponse: ");
        pdu.log();
        TTCN_Logger::end_event();
    }

    TTCN_Buffer buf;
    pdu.encode(AuthResponse_descr_, buf, TTCN_EncDec::CT_TEXT);
    CHARSTRING ret_val(buf.get_len(), (const char *)buf.get_data());

    if (TTCN_Logger::log_this_event(TTCN_DEBUG)) {
        TTCN_Logger::begin_event(TTCN_DEBUG);
        TTCN_Logger::log_event("Encoded AuthResponse: ");
        ret_val.log();
        TTCN_Logger::end_event();
    }

    return ret_val;
}

AuthResponse dec__AuthResponse(const CHARSTRING& stream)
{
    if (TTCN_Logger::log_this_event(TTCN_DEBUG)) {
        TTCN_Logger::begin_event(TTCN_DEBUG);
        TTCN_Logger::log_event("Decoding AuthResponse: ");
        stream.log();
        TTCN_Logger::end_event();
    }

    TTCN_Buffer buf;
    buf.put_cs(stream );
    AuthResponse pdu;

  const char *st=(const char *)stream;
  unsigned char *atm;
  size_t len=stream.lengthof()+1;
  buf.get_end(atm,len);
  int k=0;
  for(int i=0;i<stream.lengthof();i++){
    // this will copy the incoming charsting into the buffer
    // you can  pre-process the message if you want
    // e.g.: remove comments from the message
    atm[k++]=st[i]; //this line will copy the character
    };
  atm[k]='\0';
  buf.increase_length(k);



 TTCN_EncDec::error_behavior_t	eb=TTCN_EncDec::get_error_behavior(TTCN_EncDec::ET_LOG_MATCHING);
  if((boolean)tsp__AuthEncDec__debug){
    if (TTCN_Logger::log_this_event(TTCN_DEBUG))  {
      TTCN_Logger::begin_event(TTCN_DEBUG);
      TTCN_Logger::log_event("Decode buffer: /n");
      buf.log();
      TTCN_Logger::end_event();
      }
    TTCN_EncDec::set_error_behavior(TTCN_EncDec::ET_LOG_MATCHING,TTCN_EncDec::EB_WARNING);
  } else {
    TTCN_EncDec::set_error_behavior(TTCN_EncDec::ET_LOG_MATCHING,TTCN_EncDec::EB_IGNORE);
  }

   pdu.decode(AuthResponse_descr_, buf, TTCN_EncDec::CT_TEXT);

   TTCN_EncDec::set_error_behavior(TTCN_EncDec::ET_LOG_MATCHING,eb);

   
    if (TTCN_Logger::log_this_event(TTCN_DEBUG)) {
        TTCN_Logger::begin_event(TTCN_DEBUG);
        TTCN_Logger::log_event("Decoded AuthResponse: ");
        pdu.log();
        TTCN_Logger::end_event();
    }

    return pdu;
}
}//end namespace
