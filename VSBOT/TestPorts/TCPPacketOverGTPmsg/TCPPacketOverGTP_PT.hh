/******************************************************************************
* Copyright (c) 2000-2021 Ericsson Telecom AB
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Eclipse Public License v2.0
* which accompanies this distribution, and is available at
* https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
*
* Contributor: david.ferenc.vranics@ericsson.com
******************************************************************************/

#ifndef TCPPacketOverGTP__PT_HH
#define TCPPacketOverGTP__PT_HH

#include "TCPPacketOverGTPmsg_PortType.hh"
#include <arpa/inet.h> //inet_addr
#include <iostream> //FIXME remove me
#include <time.h> //random
#include <string.h> //memset
#include <sys/socket.h> //socket
#include <stdlib.h> //for exit(0);
#include <errno.h> //For errno - the error number
#include <netinet/udp.h>	//Provides declarations for udp header
#include <netinet/tcp.h>	//Provides declarations for tcp header
#include <netinet/ip.h>	//Provides declarations for ip header
#include <fcntl.h>
#include <unistd.h>

//==============================
namespace TCPPacketOverGTPmsg__PortType {
//==============================
class TCPPacketOverGTP__PT : public TCPPacketOverGTP__PT_BASE {

public:

    TCPPacketOverGTP__PT(const char *par_port_name = NULL);
    ~TCPPacketOverGTP__PT();

    //void set_parameter(const char *parameter_name, const char *parameter_value);

protected:
    void user_map(const char *system_port);
    void user_unmap(const char *system_port);

    void user_start();
    void user_stop();

    void outgoing_send(const TCPPacketOverGTPmsg__Types::TCPPacketOverGTP& send_par);

    void Handle_Fd_Event_Readable(int fd);
    
    void log_debug(const char *msg);
    void log_warning(const char *msg);
    void log_error(const char *msg);
private:
    unsigned short csum(unsigned short *ptr,int nbytes);

    struct pseudo_header_udp    //needed for checksum calculation
    {
      unsigned int source_address;
      unsigned int dest_address;
      unsigned char placeholder;
      unsigned char protocol;
      unsigned short udp_length;
      struct udphdr udp;
    };
    
    struct pseudo_header_tcp    //needed for checksum calculation
    {
      unsigned int source_address;
      unsigned int dest_address;
      unsigned char placeholder;
      unsigned char protocol;
      unsigned short tcp_length;
      struct tcphdr tcp;
    };
    
    struct gtphdr    //needed for checksum calculation
    {
      unsigned char reserved:1;
      unsigned char extensionHeader:1;
      unsigned char sequenceNr:1;
      unsigned char nPDUNr:1;
      unsigned char protocolType:1;
      unsigned char version:3;
      unsigned char messageType;
      unsigned short totalLength;
      unsigned long TEID;
    };
	
    char datagram[4096];
    struct iphdr *iph1;
    struct udphdr *udph;
    struct gtphdr *gtph;
    struct iphdr *iph2;
    struct tcphdr *tcph;
    struct sockaddr_in sin;
    struct pseudo_header_udp pshu;
    struct pseudo_header_tcp psht;
    int s; //socket
};
}//namespace
#endif
