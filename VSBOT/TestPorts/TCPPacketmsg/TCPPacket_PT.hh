/******************************************************************************
* Copyright (c) 2000-2021 Ericsson Telecom AB
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Eclipse Public License v2.0
* which accompanies this distribution, and is available at
* https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
*
* Contributor: david.ferenc.vranics@ericsson.com
******************************************************************************/

#ifndef TCPPacket__PT_HH
#define TCPPacket__PT_HH

#include "TCPPacketmsg_PortType.hh"
#include <arpa/inet.h> //inet_addr
#include <iostream> //FIXME remove me
#include <time.h> //random
#include <string.h> //memset
#include <sys/socket.h> //socket
#include <stdlib.h> //for exit(0);
#include <errno.h> //For errno - the error number
#include <netinet/tcp.h>	//Provides declarations for tcp header
#include <netinet/ip.h>	//Provides declarations for ip header
#include <fcntl.h>
#include <unistd.h>

//==============================
namespace TCPPacketmsg__PortType {
//==============================
class TCPPacket__PT : public TCPPacket__PT_BASE {

public:

    TCPPacket__PT(const char *par_port_name = NULL);
    ~TCPPacket__PT();

    //void set_parameter(const char *parameter_name, const char *parameter_value);

protected:
    void user_map(const char *system_port);
    void user_unmap(const char *system_port);

    void user_start();
    void user_stop();

    void outgoing_send(const TCPPacketmsg__Types::TCPPacket& send_par);

    void Handle_Fd_Event_Readable(int fd);
    
    void log_debug(const char *msg);
    void log_warning(const char *msg);
    void log_error(const char *msg);
private:
    unsigned short csum(unsigned short *ptr,int nbytes);

    struct pseudo_header    //needed for checksum calculation
    {
      unsigned int source_address;
      unsigned int dest_address;
      unsigned char placeholder;
      unsigned char protocol;
      unsigned short tcp_length;
      struct tcphdr tcp;
    };
	
    char datagram[4096];
    struct iphdr *iph;
    struct tcphdr *tcph;
    struct sockaddr_in sin;
    struct pseudo_header psh;
    int s; //socket
};
}//namespace
#endif
