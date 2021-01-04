/******************************************************************************
* Copyright (c) 2000-2021 Ericsson Telecom AB
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Eclipse Public License v2.0
* which accompanies this distribution, and is available at
* https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
*
* Contributor: david.ferenc.vranics@ericsson.com
******************************************************************************/

#include "TCPPacket_PT.hh"

namespace TCPPacketmsg__PortType {

TCPPacket__PT::TCPPacket__PT(const char *par_port_name)
	: TCPPacket__PT_BASE(par_port_name)
{
      srand(time(NULL));
      
      iph = (struct iphdr *) datagram;
      tcph = (struct tcphdr *) (datagram + sizeof (struct ip));
      
	    sin.sin_family = AF_INET;
	    sin.sin_port = htons(80);
	    sin.sin_addr.s_addr = inet_addr ("127.0.0.1");
	    memset (datagram, 0, 4096);	/* zero out the buffer */
	    
	    //Fill in the IP Header
	    iph->ihl = 5;
	    iph->version = 4;
	    iph->tos = 0;
	    iph->tot_len = sizeof (struct ip) + sizeof (struct tcphdr);
	    iph->id = 0;	//Id of this packet
	    iph->frag_off = 0;
	    iph->ttl = 255;
	    iph->protocol = IPPROTO_TCP;
	    iph->check = 0;	/* if you set a checksum to zero, your kernel's IP stack
				                 should fill in the correct checksum during transmission */
	    iph->saddr = inet_addr ("127.0.0.1");
	    iph->daddr = inet_addr ("127.0.0.1");
	    iph->check = csum ((unsigned short *) datagram, iph->tot_len >> 1);
	    
	    //TCP Header
	    tcph->source = htons (9999);
	    tcph->dest = htons (80);
	    tcph->seq = 0;
	    tcph->ack_seq = 0;
	    tcph->doff = 5;		/* first and only tcp segment */
	    tcph->fin=0;
	    tcph->syn=0;
	    tcph->rst=0;
	    tcph->psh=0;
	    tcph->ack=0;
	    tcph->urg=0;
	    tcph->window = htons (5840);	/* maximum allowed window size */
	    tcph->check = 0;
	    tcph->urg_ptr = 0;

      //Pseudo header for checksum calculation
	    psh.source_address = inet_addr ("127.0.0.1");
	    psh.dest_address = inet_addr ("127.0.0.1");
	    psh.placeholder = 0;
	    psh.protocol = IPPROTO_TCP;
	    psh.tcp_length = htons(20);
}

TCPPacket__PT::~TCPPacket__PT()
{

}

void TCPPacket__PT::Handle_Fd_Event_Readable(int fd)
{
    log_debug("entering TCPPacket__PT::Handle_Fd_Event() - event received on a connection");
    
    unsigned char inbuf[4096];
    struct iphdr *iphin;
    struct tcphdr *tcphin;
    
    recv(fd, inbuf, 4096, O_NONBLOCK);

    iphin = (struct iphdr *) inbuf;
    tcphin = (struct tcphdr *) (inbuf + sizeof (struct ip));
    if (1/*TODO smart condition here*/)
    {
      incoming_message(
        TCPPacketmsg__Types::TCPPacket(
          TCPPacketmsg__Types::IPHeader(
            inet_ntoa(*(struct in_addr*)&iphin->saddr),
            inet_ntoa(*(struct in_addr*)&iphin->daddr)
          ),
          TCPPacketmsg__Types::TCPHeader(
            ntohs(tcphin->source),
            ntohs(tcphin->dest),
            ntohs(tcphin->seq),
            ntohs(tcphin->ack_seq),
            ntohs(tcphin->doff),
            ntohs(tcphin->res1),
            ntohs(tcphin->res2),
            tcphin->urg,
            tcphin->ack,
            tcphin->psh,
            tcphin->rst,
            tcphin->syn,
            tcphin->fin,
            ntohs(tcphin->window),
            ntohs(tcphin->check),
            ntohs(tcphin->urg_ptr)
          )
        )
      );
    }

    log_debug("leaving TCPPacket__PT::Handle_Fd_Event()");
}

void TCPPacket__PT::user_map(const char *system_port)
{
  log_debug("entering TCPPacket__PT::user_map()");
  log_debug("Creating RAW socket...");
  s = socket(AF_INET, SOCK_RAW, IPPROTO_TCP); //TODO makefilepatch!
  if (s < 0) {
    log_error("Error creating socket...");
    return;
  }

  log_debug("Setting the socket in RAW mode...");
  int optval = 1;
  if ((setsockopt(s, IPPROTO_IP, IP_HDRINCL, &optval, sizeof(optval))) < 0) {
    log_error("Failed to set socket in RAW mode... Do you have the permission to create RAW socket?");
    return;
  }
  log_debug("Successful.");
  
  Handler_Add_Fd_Read(s);
  log_debug("leaving TCPPacket__PT::user_map()");
}

void TCPPacket__PT::user_unmap(const char *system_port)
{
  log_debug("entering TCPPacket__PT::user_unmap()");
  Handler_Remove_Fd_Read(s);
  close(s);
  log_debug("leaving TCPPacket__PT::user_unmap()");
}

void TCPPacket__PT::user_start()
{
}

void TCPPacket__PT::user_stop()
{
}

void TCPPacket__PT::outgoing_send(const TCPPacketmsg__Types::TCPPacket& send_par)
{
  if (send_par.IP().src().is_bound())
  {
    iph->saddr = inet_addr (send_par.IP().src());
    psh.source_address = inet_addr (send_par.IP().src());
  }
  else
    log_error("IP.src is mandatory!");
  
  if (send_par.IP().dst().is_bound())
  {
    sin.sin_addr.s_addr = inet_addr (send_par.IP().dst());
    iph->daddr = inet_addr (send_par.IP().dst());
    psh.dest_address = inet_addr (send_par.IP().dst());
	}
  else
    log_error("IP.dst is mandatory!");
  
  if (send_par.TCP().src().is_bound() && send_par.TCP().src().is_present())
	  tcph->source = htons (send_par.TCP().src()());
  else
    tcph->source = htonl(rand());

  if (send_par.TCP().dst().is_bound())
    tcph->dest = htons (send_par.TCP().dst());
  else
    log_error("TCP.dst is mandatory!");
  
  if (send_par.TCP().seq().is_bound() && send_par.TCP().seq().is_present())
    tcph->seq = send_par.TCP().seq()();
  else
    tcph->seq = htonl(rand());
  
  if (send_par.TCP().ackseq().is_bound() && send_par.TCP().ackseq().is_present())
    tcph->ack_seq = send_par.TCP().ackseq()();
  else
  {
    if (send_par.TCP().ack().is_bound() && send_par.TCP().ack().is_present())
      tcph->ack_seq = htonl(rand());
    else
      tcph->ack_seq = 0;
  }
  
  if (send_par.TCP().doff().is_bound() && send_par.TCP().doff().is_present())
    tcph->doff = send_par.TCP().doff()();
  else
    tcph->doff = 5;
    
  if (send_par.TCP().res1().is_bound() && send_par.TCP().res1().is_present())
    tcph->res1 = send_par.TCP().res1()();
  else
    tcph->res1 = 0;
    
  if (send_par.TCP().res2().is_bound() && send_par.TCP().res2().is_present())
    tcph->res2 = send_par.TCP().res2()();
  else
    tcph->res2 = 0;
  
  if (send_par.TCP().fin().is_bound() && send_par.TCP().fin().is_present())
    tcph->fin = send_par.TCP().fin()();
  else
    tcph->fin = 0;
  
  if (send_par.TCP().syn().is_bound() && send_par.TCP().syn().is_present())
    tcph->syn = send_par.TCP().syn()();
  else
    tcph->syn = 0;
  
  if (send_par.TCP().rst().is_bound() && send_par.TCP().rst().is_present())
    tcph->rst = send_par.TCP().rst()();
  else
    tcph->rst = 0;
  
  if (send_par.TCP().psh().is_bound() && send_par.TCP().psh().is_present())
    tcph->psh = send_par.TCP().psh()();
  else
    tcph->psh = 0;
  
  if (send_par.TCP().ack().is_bound() && send_par.TCP().ack().is_present())
    tcph->ack = send_par.TCP().ack()();
  else
    tcph->ack = 0;
  
  if (send_par.TCP().urg().is_bound() && send_par.TCP().urg().is_present())
    tcph->urg = send_par.TCP().urg()();
  else
    tcph->urg = 0;
  
  if (send_par.TCP().window().is_bound() && send_par.TCP().window().is_present())
    tcph->window = send_par.TCP().window()();
  else
    tcph->window = htons (5840);
  
  if (send_par.TCP().checksum().is_bound() && send_par.TCP().checksum().is_present())
    tcph->check = send_par.TCP().checksum()();
  else
  {
    memcpy(&psh.tcp , tcph , sizeof (struct tcphdr));
	  tcph->check = csum( (unsigned short*) &psh , sizeof (struct pseudo_header));
  }
  
  if (send_par.TCP().urgptr().is_bound() && send_par.TCP().urgptr().is_present())
    tcph->urg_ptr = send_par.TCP().urgptr()();
  else
    tcph->urg_ptr = 0;
  
  iph->id = htonl(rand());
  
  ////////////////////

  if (sendto (s,		/* our socket */
		  datagram,	/* the buffer containing headers and data */
		  iph->tot_len,	/* total length of our datagram */
		  0,		/* routing flags, normally always 0 */
		  (struct sockaddr *) &sin,	/* socket addr, just like in */
		  sizeof (sin)) < 0)		/* a normal send() */
  {
	  log_error("Error sending packet...");
  }
  else
  {
	  log_debug("Packet sent...");
  }  
}

// Checksums - IP and TCP
unsigned short TCPPacket__PT::csum(unsigned short *ptr,int nbytes) {
	register long sum;
	unsigned short oddbyte;
	register short answer;
	sum=0;
	while(nbytes>1) {
		sum+=*ptr++;
		nbytes-=2;
	}
	if(nbytes==1) {
		oddbyte=0;
		*((u_char*)&oddbyte)=*(u_char*)ptr;
		sum+=oddbyte;
	}
	sum = (sum>>16)+(sum & 0xffff);
	sum = sum + (sum>>16);
	answer=(short)~sum;
	return(answer);
}
//=========================================================================
//==== Working Functions independent from sending and receiving:===
//=========================================================================

void TCPPacket__PT::log_debug(const char *msg)
{
  TTCN_Logger::begin_event(TTCN_DEBUG);
  TTCN_Logger::log_event("TCPPacket_PT: DEBUG: %s", (const char*)(msg));
  TTCN_Logger::end_event();
}


void TCPPacket__PT::log_warning(const char *msg)
{
  TTCN_Logger::begin_event(TTCN_DEBUG);
  TTCN_Logger::log_event("TCPPacket_PT: WARNING: %s", (const char*)(msg));
  TTCN_Logger::end_event();
}

void TCPPacket__PT::log_error(const char *msg)
{
  TTCN_Logger::begin_event(TTCN_DEBUG);
  TTCN_Logger::log_event("TCPPacket_PT: ERROR: %s", (const char*)(msg));
  TTCN_Logger::end_event();
}

}//namespace
