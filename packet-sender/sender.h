#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#include <cstdio>
#include <string>
#include <vector>

struct Sock_Temp {
  static std::string _ip_addr;
  static const int _domain = AF_INET;

  sockaddr_in _s_addr;
  unsigned short _port;

  Sock_Temp(unsigned short _port) : _port(_port) {
    _s_addr.sin_family = Sock_Temp::_domain;
    _s_addr.sin_port = htons(_port);
    _s_addr.sin_addr.s_addr = inet_addr(_ip_addr.c_str());
  }
};

class Sender
{
  static const unsigned int threads = 10;
  std::vector<std::string> packets;
  std::vector<int> sockets;
  
 public:
  Sender(FILE * &, const std::string &);
  ~Sender();
  
  int   createSocks(FILE * &);
  void  sendPackets();
  /* void  createTemplate(char * &, int &); */
  
};

