/******************************************************************************
* Copyright (c) 2000-2021 Ericsson Telecom AB
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Eclipse Public License v2.0
* which accompanies this distribution, and is available at
* https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
*modified by Elemer Lelik 03.03.2016
******************************************************************************/
//
//  File:               DIAMETER_EncDec.cc
//  Description:	Encoder/Decoder and external functions for DPMG
//  Rev:                R34A
//  Prodnr:             CNL 113 462
///////////////////////////////////////////////

#include "DIAMETER_Types.hh"
//#include <sys/timeb.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdint.h>

namespace DIAMETER__Types{
static const unsigned char os_h_or_e_id_octets[] = { 0, 0, 0, 0 };
static const OCTETSTRING os_h_or_e_id_oct(4, os_h_or_e_id_octets);


INTEGER f__DIAMETER__genEndToEnd__int()
{
  timeval precise;                        // requires <sys/time.h>
  static bool inititalized = false;
  static uint32_t l_value = 0;
  if(!inititalized){
    long int seed = getpid();
    if ( gettimeofday(&precise, NULL) != -1 ) {
      seed <<= 8;
      seed +=  (precise.tv_sec) & 0xFF;
      seed <<= 8;
      seed +=  (precise.tv_usec) & 0xFF;
    }
    srand48(seed);
    l_value =lrand48();
    if ( gettimeofday(&precise, NULL) != -1 ) {
      l_value = (((uint32_t)precise.tv_sec) << 20) + ( l_value >> 12);
    }
    inititalized = true;
  }
  
  l_value+=1;  // unsigned int -> can be overflowed safely
  
  if(l_value==0){
    l_value+=1;
  }
  
  INTEGER ret;
  ret.set_long_long_val(l_value);
  return ret;
}


OCTETSTRING f__DIAMETER__genEndToEnd__oct()
{
  return int2oct(f__DIAMETER__genEndToEnd__int(),4);
}

INTEGER f__DIAMETER__genHopByHop__int()
{
  return f__DIAMETER__genEndToEnd__int();
}

OCTETSTRING f__DIAMETER__genHopByHop__oct()
{
  return int2oct(f__DIAMETER__genHopByHop__int(),4);
}

bool chk_zero(INTEGER var) {return var==0;}
bool chk_zero(OCTETSTRING var) {return var==os_h_or_e_id_oct;}



}
TTCN_Module DIAMETER_EncDec("DIAMETER_EncDec", __DATE__, __TIME__);
