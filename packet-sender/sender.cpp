#include <thread>
#include "sender.h"
#include <unistd.h>

int Sender::createSocks(FILE * &file) {
  int sum = 0;

  for ( int i = 0; i < Sender::threads; ++i ) {
    unsigned short type;
    unsigned short port;
    unsigned int   len;
    
    fread(&type, sizeof(type), 1, file);
    fread(&port, sizeof(port), 2, file);
    fread(&len,  sizeof(len),  4, file);
    
    std::string packet(len, '\0');
    fread(&packet[0], sizeof(char), len, file);

    int sock_fd = socket(Sock_Temp::_domain, type, 0);
    this->packets.emplace_back(packet);

    Sock_Temp temp(port);
    sum += connect(sock_fd, (sockaddr *)&temp._s_addr, sizeof(temp._s_addr));
    
  } 
  
  return (sum == 0);
}

Sender::Sender(FILE *&file, const std::string &ip_addr) {
  Sock_Temp::_ip_addr = ip_addr;
  this->createSocks(file);
}

Sender::~Sender() {
  for (int i = 0; i < threads; ++i) {
    close(sockets[i]);
  }
}

void Sender::sendPackets() {
  std::vector<std::thread> threads;

  for (int i = 0; i < Sender::threads; ++i) {
    threads.emplace_back(std::thread(send, sockets[i], packets[i].c_str(), packets[i].size(), 0));
  }
  
  for ( int i = 0; i < Sender::threads; ++i) {
    threads[i].join();
  }
  
    return;
}

