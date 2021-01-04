/******************************************************************************
* Copyright (c) 2000-2021 Ericsson Telecom AB
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Eclipse Public License v2.0
* which accompanies this distribution, and is available at
* https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
*
* Contributor: david.ferenc.vranics@ericsson.com
******************************************************************************/

#include "TCPPacketOverGTP_PT.hh"

namespace TCPPacketOverGTPmsg__PortType {

TCPPacketOverGTP__PT::TCPPacketOverGTP__PT(const char *par_port_name)
	: TCPPacketOverGTP__PT_BASE(par_port_name)
{
      srand(time(NULL));
      
      iph1 = (struct iphdr *) datagram;
      udph = (struct udphdr *) (datagram + sizeof (struct iphdr));
      gtph = (struct gtphdr *) (datagram + sizeof (struct udphdr) + sizeof (struct iphdr));
      iph2 = (struct iphdr *) (datagram + sizeof (struct gtphdr) + sizeof (struct udphdr) + sizeof (struct iphdr));
      tcph = (struct tcphdr *) (datagram + sizeof (struct iphdr)+ sizeof (struct gtphdr) + sizeof (struct udphdr) + sizeof (struct iphdr));
      
	    sin.sin_family = AF_INET;
	    sin.sin_port = htons(80);
	    sin.sin_addr.s_addr = inet_addr ("127.0.0.1");
	    memset (datagram, 0, 4096);	/* zero out the buffer */
	    
	    //Fill in the IP Header 1
	    iph1->ihl = 5;
	    iph1->version = 4;
	    iph1->tos = 0;
	    iph1->tot_len = sizeof (struct iphdr) + sizeof (struct udphdr) + sizeof (struct gtphdr) + sizeof (struct iphdr) + sizeof (struct tcphdr);
	    iph1->id = 0; //Will be randomized when sending
	    iph1->frag_off = 0;
	    iph1->ttl = 255;
	    iph1->protocol = IPPROTO_UDP;
	    iph1->check = 0;	/* if you set a checksum to zero, your kernel's IP stack
				                 should fill in the correct checksum during transmission */
	    iph1->saddr = inet_addr ("127.0.0.1");
	    iph1->daddr = inet_addr ("127.0.0.1");
	    
	    //UDP Header
	    udph->source = htons (9999);
	    udph->dest = htons (80);
	    udph->len = 56;
	    udph->check = 0;
	    
	    //GTP Header
      gtph->version = 1;
      gtph->protocolType = 1;
      gtph->reserved = 0;
      gtph->extensionHeader = 0;
      gtph->sequenceNr = 0;
      gtph->nPDUNr = 0;
      gtph->messageType = 255;
      gtph->totalLength = 40;
      gtph->TEID = 1;
	    	    
	    //IP Header 2
	    iph2->ihl = 5;
	    iph2->version = 4;
	    iph2->tos = 0;
	    iph2->tot_len = htons (sizeof (struct iphdr) + sizeof (struct tcphdr));
	    iph2->id = 0;	//Id of this packet
	    iph2->frag_off = 0;
	    iph2->ttl = 255;
	    iph2->protocol = IPPROTO_TCP;
	    iph2->check = 0;
	    iph2->saddr = inet_addr ("127.0.0.1");
	    iph2->daddr = inet_addr ("127.0.0.1");
	    
	    //TCP Header
	    tcph->source = htons (9999);
	    tcph->dest = htons (80);
	    tcph->seq = 0;
	    tcph->ack_seq = 0;
	    tcph->doff = 5;
	    tcph->fin=0;
	    tcph->syn=0;
	    tcph->rst=0;
	    tcph->psh=0;
	    tcph->ack=0;
	    tcph->urg=0;
	    tcph->window = htons (5840);
	    tcph->check = 0;
	    tcph->urg_ptr = 0;

      //Pseudo header for udp checksum calculation
	    pshu.source_address = inet_addr ("127.0.0.1");
	    pshu.dest_address = inet_addr ("127.0.0.1");
	    pshu.placeholder = 0;
	    pshu.protocol = IPPROTO_UDP;
	    pshu.udp_length = htons(20);
	    
	    //Pseudo header for tcp checksum calculation
	    psht.source_address = inet_addr ("127.0.0.1");
	    psht.dest_address = inet_addr ("127.0.0.1");
	    psht.placeholder = 0;
	    psht.protocol = IPPROTO_TCP;
	    psht.tcp_length = htons(20);
}

TCPPacketOverGTP__PT::~TCPPacketOverGTP__PT()
{

}

void TCPPacketOverGTP__PT::Handle_Fd_Event_Readable(int fd)
{
    log_debug("entering TCPPacketOverGTP__PT::Handle_Fd_Event() - event received on a connection");
    
    unsigned char inbuf[4096];
    struct iphdr *iph1in;
    struct udphdr *udphin;
    struct gtphdr *gtphin;
    struct iphdr *iph2in;
    struct tcphdr *tcphin;
    
    recv(fd, inbuf, 4096, O_NONBLOCK);

    iph1in = (struct iphdr *) inbuf;
    udphin = (struct udphdr *) (inbuf + sizeof (struct iphdr));
    gtphin = (struct gtphdr *) (inbuf + sizeof (struct udphdr) + sizeof (struct iphdr));
    iph2in = (struct iphdr *) (inbuf + sizeof (struct gtphdr) + sizeof (struct udphdr) + sizeof (struct iphdr));
    tcphin = (struct tcphdr *) (inbuf + sizeof (struct iphdr)+ sizeof (struct gtphdr) + sizeof (struct udphdr) + sizeof (struct iphdr));
    
    if (ntohs(gtphin->version)==1/*TODO check this on site*/)
    {
      incoming_message(
        TCPPacketOverGTPmsg__Types::TCPPacketOverGTP(
          TCPPacketmsg__Types::IPHeader(
            inet_ntoa(*(struct in_addr*)&iph1in->saddr),
            inet_ntoa(*(struct in_addr*)&iph1in->daddr)
          ),
          TCPPacketOverGTPmsg__Types::UDPHeader(
            ntohs(udphin->source),
            ntohs(udphin->dest),
            ntohs(udphin->len),
            ntohs(udphin->check)
          ),
          TCPPacketOverGTPmsg__Types::GTPPacket(
            TCPPacketOverGTPmsg__Types::GTPHeader(
              ntohs(gtphin->version),
              gtphin->protocolType,
              gtphin->extensionHeader,
              gtphin->sequenceNr,
              gtphin->nPDUNr,
              ntohs(gtphin->messageType),
              ntohs(gtphin->totalLength),
              ntohs(gtphin->TEID)
            ),
            TCPPacketmsg__Types::IPHeader(
              inet_ntoa(*(struct in_addr*)&iph2in->saddr),
              inet_ntoa(*(struct in_addr*)&iph2in->daddr)
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
        )
      );
    }

    log_debug("leaving TCPPacketOverGTP__PT::Handle_Fd_Event()");
}

void TCPPacketOverGTP__PT::user_map(const char *system_port)
{
  log_debug("entering TCPPacketOverGTP__PT::user_map()");
  log_debug("Creating RAW socket...");
  s = socket(AF_INET, SOCK_RAW, IPPROTO_TCP); //TODO makefilepatch setcap!
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
  log_debug("leaving TCPPacketOverGTP__PT::user_map()");
}

void TCPPacketOverGTP__PT::user_unmap(const char *system_port)
{
  log_debug("entering TCPPacketOverGTP__PT::user_unmap()");
  Handler_Remove_Fd_Read(s);
  close(s);
  log_debug("leaving TCPPacketOverGTP__PT::user_unmap()");
}

void TCPPacketOverGTP__PT::user_start()
{
}

void TCPPacketOverGTP__PT::user_stop()
{
}

void TCPPacketOverGTP__PT::outgoing_send(const TCPPacketOverGTPmsg__Types::TCPPacketOverGTP& send_par)
{
  //IP
  if (send_par.IP().src().is_bound())
  {
    iph1->saddr = inet_addr (send_par.IP().src());
    pshu.source_address = inet_addr (send_par.IP().src());
  }
  else
    log_error("IP.src is mandatory!");
  
  if (send_par.IP().dst().is_bound())
  {
    sin.sin_addr.s_addr = inet_addr (send_par.IP().dst());
    iph1->daddr = inet_addr (send_par.IP().dst());
    pshu.dest_address = inet_addr (send_par.IP().dst());
	}
  else
    log_error("IP.dst is mandatory!");
  
  //UDP
  if (send_par.UDP().src().is_bound() && send_par.UDP().src().is_present())
	  udph->source = htons (send_par.UDP().src()());
  else
    udph->source = htonl(rand());

  if (send_par.UDP().dst().is_bound())
    udph->dest = htons (send_par.UDP().dst());
  else
    log_error("UDP.dst is mandatory!");
  
  if (send_par.UDP().totalLength().is_bound() && send_par.UDP().totalLength().is_present())
	  udph->len = htons (send_par.UDP().totalLength()());
  else
    udph->len = htons (56);
    
  if (send_par.UDP().checksum().is_bound() && send_par.UDP().checksum().is_present())
    udph->check = send_par.UDP().checksum()();
  else
  {
    memcpy(&pshu.udp , udph , sizeof (struct udphdr));
	  udph->check = csum( (unsigned short*) &pshu , sizeof (struct pseudo_header_udp));
  }
  
  //GTP/GTP
  if (send_par.GTP().GTPhdr().version().is_bound() && send_par.GTP().GTPhdr().version().is_present())
	  gtph->version = send_par.GTP().GTPhdr().version()();
  else
    gtph->version = 1;
    
  if (send_par.GTP().GTPhdr().protocolType().is_bound() && send_par.GTP().GTPhdr().protocolType().is_present())
	  gtph->protocolType = send_par.GTP().GTPhdr().protocolType()();
  else
    gtph->protocolType = 1;
    
  if (send_par.GTP().GTPhdr().extensionHeader().is_bound() && send_par.GTP().GTPhdr().extensionHeader().is_present())
	  gtph->extensionHeader = send_par.GTP().GTPhdr().extensionHeader()();
  else
    gtph->extensionHeader = 0;
    
  if (send_par.GTP().GTPhdr().sequenceNr().is_bound() && send_par.GTP().GTPhdr().sequenceNr().is_present())
	  gtph->sequenceNr = send_par.GTP().GTPhdr().sequenceNr()();
  else
    gtph->sequenceNr = 0;
    
  if (send_par.GTP().GTPhdr().nPDUNr().is_bound() && send_par.GTP().GTPhdr().nPDUNr().is_present())
	  gtph->nPDUNr = send_par.GTP().GTPhdr().nPDUNr()();
  else
    gtph->nPDUNr = 0;
    
  if (send_par.GTP().GTPhdr().messageType().is_bound() && send_par.GTP().GTPhdr().messageType().is_present())
	  gtph->messageType = htons (send_par.GTP().GTPhdr().messageType()());
  else
    gtph->messageType = 255; //Data
    
  if (send_par.GTP().GTPhdr().totalLength().is_bound() && send_par.GTP().GTPhdr().totalLength().is_present())
	  gtph->totalLength = htons (send_par.GTP().GTPhdr().totalLength()());
  else
    gtph->totalLength = htons (40);

  if (send_par.GTP().GTPhdr().TEID().is_bound())
    gtph->TEID = htonl (send_par.GTP().GTPhdr().TEID());
  else
    log_error("GTP.TEID is mandatory!");
  
  //GTP/IP
  if (send_par.GTP().IPhdr().src().is_bound())
  {
    iph2->saddr = inet_addr (send_par.GTP().IPhdr().src());
    psht.source_address = inet_addr (send_par.GTP().IPhdr().src());
  }
  else
    log_error("IP.src is mandatory!");
  
  if (send_par.GTP().IPhdr().dst().is_bound())
  {
    iph2->daddr = inet_addr (send_par.GTP().IPhdr().dst());
    psht.dest_address = inet_addr (send_par.GTP().IPhdr().dst());
	}
  else
    log_error("IP.dst is mandatory!");
    
  //GTP/TCP
  if (send_par.GTP().TCPhdr().src().is_bound() && send_par.GTP().TCPhdr().src().is_present())
	  tcph->source = htons (send_par.GTP().TCPhdr().src()());
  else
    tcph->source = htonl(rand());

  if (send_par.GTP().TCPhdr().dst().is_bound())
    tcph->dest = htons (send_par.GTP().TCPhdr().dst());
  else
    log_error("TCP.dst is mandatory!");
  
  if (send_par.GTP().TCPhdr().seq().is_bound() && send_par.GTP().TCPhdr().seq().is_present())
    tcph->seq = send_par.GTP().TCPhdr().seq()();
  else
    tcph->seq = htonl(rand());
  
  if (send_par.GTP().TCPhdr().ackseq().is_bound() && send_par.GTP().TCPhdr().ackseq().is_present())
    tcph->ack_seq = send_par.GTP().TCPhdr().ackseq()();
  else
  {
    if (send_par.GTP().TCPhdr().ack().is_bound() && send_par.GTP().TCPhdr().ack().is_present())
      tcph->ack_seq = htonl(rand());
    else
      tcph->ack_seq = 0;
  }
  
  if (send_par.GTP().TCPhdr().doff().is_bound() && send_par.GTP().TCPhdr().doff().is_present())
    tcph->doff = send_par.GTP().TCPhdr().doff()();
  else
    tcph->doff = 5;
    
  if (send_par.GTP().TCPhdr().res1().is_bound() && send_par.GTP().TCPhdr().res1().is_present())
    tcph->res1 = send_par.GTP().TCPhdr().res1()();
  else
    tcph->res1 = 0;
    
  if (send_par.GTP().TCPhdr().res2().is_bound() && send_par.GTP().TCPhdr().res2().is_present())
    tcph->res2 = send_par.GTP().TCPhdr().res2()();
  else
    tcph->res2 = 0;
  
  if (send_par.GTP().TCPhdr().fin().is_bound() && send_par.GTP().TCPhdr().fin().is_present())
    tcph->fin = send_par.GTP().TCPhdr().fin()();
  else
    tcph->fin = 0;
  
  if (send_par.GTP().TCPhdr().syn().is_bound() && send_par.GTP().TCPhdr().syn().is_present())
    tcph->syn = send_par.GTP().TCPhdr().syn()();
  else
    tcph->syn = 0;
  
  if (send_par.GTP().TCPhdr().rst().is_bound() && send_par.GTP().TCPhdr().rst().is_present())
    tcph->rst = send_par.GTP().TCPhdr().rst()();
  else
    tcph->rst = 0;
  
  if (send_par.GTP().TCPhdr().psh().is_bound() && send_par.GTP().TCPhdr().psh().is_present())
    tcph->psh = send_par.GTP().TCPhdr().psh()();
  else
    tcph->psh = 0;
  
  if (send_par.GTP().TCPhdr().ack().is_bound() && send_par.GTP().TCPhdr().ack().is_present())
    tcph->ack = send_par.GTP().TCPhdr().ack()();
  else
    tcph->ack = 0;
  
  if (send_par.GTP().TCPhdr().urg().is_bound() && send_par.GTP().TCPhdr().urg().is_present())
    tcph->urg = send_par.GTP().TCPhdr().urg()();
  else
    tcph->urg = 0;
  
  if (send_par.GTP().TCPhdr().window().is_bound() && send_par.GTP().TCPhdr().window().is_present())
    tcph->window = send_par.GTP().TCPhdr().window()();
  else
    tcph->window = htons (5840);
  
  if (send_par.GTP().TCPhdr().checksum().is_bound() && send_par.GTP().TCPhdr().checksum().is_present())
    tcph->check = send_par.GTP().TCPhdr().checksum()();
  else
  {
    memcpy(&psht.tcp , tcph , sizeof (struct tcphdr));
	  tcph->check = csum( (unsigned short*) &psht , sizeof (struct pseudo_header_tcp));
  }
  
  if (send_par.GTP().TCPhdr().urgptr().is_bound() && send_par.GTP().TCPhdr().urgptr().is_present())
    tcph->urg_ptr = send_par.GTP().TCPhdr().urgptr()();
  else
    tcph->urg_ptr = 0;
  
  iph1->id = htonl(rand());
  iph2->id = htonl(rand());
  
  iph2->check = 0;
	iph2->check = csum ((unsigned short *) iph2, iph2->ihl<<2);
  
  ////////////////////

  if (sendto (s,
		  datagram,
		  iph1->tot_len,
		  0,
		  (struct sockaddr *) &sin,
		  sizeof (sin)) < 0)
  {
	  log_error("Error sending packet...");
  }
  else
  {
	  log_debug("Packet sent...");
  }  
}

// Checksums - IP + TCP
unsigned short TCPPacketOverGTP__PT::csum(unsigned short *ptr,int nbytes) {
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

void TCPPacketOverGTP__PT::log_debug(const char *msg)
{
  TTCN_Logger::begin_event(TTCN_DEBUG);
  TTCN_Logger::log_event("TCPPacketOverGTP_PT: DEBUG: %s", (const char*)(msg));
  TTCN_Logger::end_event();
}


void TCPPacketOverGTP__PT::log_warning(const char *msg)
{
  TTCN_Logger::begin_event(TTCN_DEBUG);
  TTCN_Logger::log_event("TCPPacketOverGTP_PT: WARNING: %s", (const char*)(msg));
  TTCN_Logger::end_event();
}

void TCPPacketOverGTP__PT::log_error(const char *msg)
{
  TTCN_Logger::begin_event(TTCN_DEBUG);
  TTCN_Logger::log_event("TCPPacketOverGTP_PT: ERROR: %s", (const char*)(msg));
  TTCN_Logger::end_event();
}

}//namespace
