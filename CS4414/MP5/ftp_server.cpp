/*
 * Gabriel  Groover (gtg3vv)
 * HW5 - Simple FTP Server
 * Due: 5/1/2018
 * ftp_server.cpp
 * A simple ftp server that is capable of connecting to a single ftp client at a time.
 * It implements the barebones operations of an ftp server.
 * Code for the server and client connections was taken from the wikipedia page shown in class.
 */

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <iostream>
#include <string.h>
#include <vector>
#include <string>
#include <sys/wait.h>
#include <fcntl.h>
  
using namespace std;

//Split string into vector based on delim
vector<string> tokenize(string s, const char* delim) 
{
    vector<string> tokens;
    size_t start = 0;
    size_t loc = s.find(delim);
    
    //While delim in string
    while (loc != string::npos)
    {   
        //Add string from last delim to current to vector
        tokens.push_back(s.substr(start, loc-start));
        start = loc+strlen(delim);
        
        loc = s.find(delim, loc+1);
    }
    //Push remainder
    tokens.push_back(s.substr(start, s.length()));
    return tokens;
}

//Remove leading/trailing/doubled spaces
string removeSpace(string s)
{
    string oneSpace = "";
    bool afterSpace = true;    
    size_t lastLetter = s.find_last_not_of(" \r\n");

    for (int i = 0; i < s.length(); i++)
    {
        //If repeated space, skip
        if (s[i] == ' ' && afterSpace)
           continue;

        afterSpace = s[i] == ' ';
        if (i <= lastLetter) oneSpace += s[i];
    }
    return oneSpace;
}

//Create and return a socket file descriptor for use in data connections
int setUpSocket(struct sockaddr* ca, int size)
{
    int dataSocketFD;
    dataSocketFD = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (dataSocketFD == -1) {
        perror("cannot create socket");
        exit(EXIT_FAILURE);
    }
        
    if (connect(dataSocketFD, ca, size) == -1) {
        perror("connect failed");
        close(dataSocketFD);
        exit(EXIT_FAILURE);
    }
    return dataSocketFD;
}
  
//Main server functionality
int main(int argc, char **argv)
{
    //Socket variables
    struct sockaddr_in sa,ca;
    int ca_size = sizeof(ca);
    int SocketFD = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    char* buffer = (char*) malloc(100);
    bool binary = false;
    
    //Attempt to create the socket
    if (SocketFD == -1) {
      perror("cannot create socket");
      exit(EXIT_FAILURE);
    }
  
    //Initialize connection types
    memset(&sa, 0, sizeof(sa));
    sa.sin_family = AF_INET;
    sa.sin_port = htons(atoi(argv[1]));
    sa.sin_addr.s_addr = inet_addr("127.0.0.1");
    memset(&ca, 0, sizeof ca);
    ca.sin_family = AF_INET;
    ca.sin_port = htons(atoi(argv[1]));
    
    //Attempt to bind socket
    if (bind(SocketFD,(struct sockaddr *)&sa, sizeof sa) == -1) {
      perror("bind failed");
      close(SocketFD);
      exit(EXIT_FAILURE);
    }
  
    //Listen for connections on socket
    if (listen(SocketFD, 10) == -1) {
      perror("listen failed");
      close(SocketFD);
      exit(EXIT_FAILURE);
    }
    
    //Loop over connections
    for (;;) {
        
        int ConnectFD = accept(SocketFD, (struct sockaddr*)&ca, (socklen_t*)&ca_size);
    
        //Check if connection successful
        if (0 > ConnectFD) {
            perror("accept failed");
            close(SocketFD);
            exit(EXIT_FAILURE);
        }
        send(ConnectFD, "220\r\n", 5, 0);
        
        //Loop over input received
        while (1)
        {
            memset(buffer, 0, 100);
            int  numBytes = recv(ConnectFD, buffer, 100, 0);
            
            //If bytes received
            if (numBytes > 0)
            {
                //Tokenize command
                string command = removeSpace(string(buffer));
                vector<string> tokens = tokenize(command, " ");
                
                //Handle port command
                if (tokens[0].compare("PORT") == 0)
                {
                    vector<string> byteVals = tokenize(tokens[1], ",");
                    string dec_addr = byteVals[0] + "." + 
                                      byteVals[1] + "." + 
                                      byteVals[2] + "." + 
                                      byteVals[3];
                                      
               
                    memset(&ca, 0, sizeof ca);
                    ca.sin_family = AF_INET;
                    ca.sin_port = htons(atoi(byteVals[4].c_str())*256 + atoi(byteVals[5].c_str()));
                    int res = inet_pton(AF_INET, dec_addr.c_str(), &ca.sin_addr);
                
                    send(ConnectFD, "200\r\n", 5, 0);         
                } 
                //Handle user command
                else if (tokens[0].compare("USER") == 0)
                {
                    if (tokens.size() == 2)
                        send(ConnectFD, "230\r\n", 5, 0);
                    else
                        send(ConnectFD, "501\r\n", 5, 0);
                  
                }
                //Handle Quit
                else if (tokens[0].compare("QUIT") == 0)
                {
                    send(ConnectFD, "221\r\n", 5, 0);
                    binary = false;
                    break;
                  
                } 
                //Handle type
                else if (tokens[0].compare("TYPE") == 0)
                {
                    if (tokens[1].compare("I") != 0 or tokens.size() > 2) 
                        send(ConnectFD, "504\r\n", 5, 0);
                    else
                    {
                        binary = true;
                        send(ConnectFD, "200\r\n", 5,0);
                    }
                    
                }
                //Handle mode
                else if (tokens[0].compare("MODE") == 0)
                {
                    if (tokens[1].compare("S") != 0 or tokens.size() != 2) 
                    {
                        send(ConnectFD, "504\r\n", 5, 0);
                        continue;
                    } 
                    send(ConnectFD, "200\r\n", 5,0);
                } 
                //Handle STRU
                else if (tokens[0].compare("STRU") == 0)
                {
                    if (tokens[1].compare("F") != 0 or tokens.size() != 2) 
                    {
                        send(ConnectFD, "504\r\n", 5, 0);
                        continue;
                    } 
                    send(ConnectFD, "200\r\n", 5,0);
                  
                } 
                //Handle RETR
                else if (tokens[0].compare("RETR") == 0)
                {
                    if (!binary)
                    {
                        send(ConnectFD, "451\r\n", 5, 0);
                        continue;
                    }
                    
                    if (open(tokens[1].c_str(), O_RDONLY) < 0)
                    {
                        send(ConnectFD, "550\r\n", 5, 0);
                        continue;
                    }
                    
                    int dataSocketFD = setUpSocket((struct sockaddr *)&ca, sizeof ca);
                    send(ConnectFD, "150\r\n", 5, 0);
                        
                    int pid = fork();
                    if (pid == 0)
                    {
                        dup2(dataSocketFD, 1);
                        if (tokens.size() > 1)
                            execl("/bin/cat", "/bin/cat", tokens[1].c_str(), (char*) NULL);
                        else
                            execl("/bin/cat", "/bin/cat", (char*) NULL);
                    } else
                    {
                        waitpid(pid, NULL, 0);
                        close(dataSocketFD);
                        send(ConnectFD, "250\r\n", 5, 0);
                    }
                } 
                //Handle STOR
                else if (tokens[0].compare("STOR") == 0)
                {
                    if (!binary)
                    {
                        send(ConnectFD, "451\r\n", 5, 0);
                        continue;
                    }
                    int dataSocketFD = setUpSocket((struct sockaddr *)&ca, sizeof ca);
                    send(ConnectFD, "150\r\n", 5, 0);
                    remove(tokens[1].c_str());
                    int outfile = open(tokens[1].c_str(), O_RDWR | O_CREAT, 0666);
                        
                    int pid = fork();
                    if (pid == 0)
                    {
                        dup2(dataSocketFD, 0);
                        dup2(outfile, 1);
                        execl("/bin/cat", "/bin/cat", (char*) NULL);
                    } else
                    {
                        waitpid(pid, NULL, 0);
                        close(dataSocketFD);
                        send(ConnectFD, "250\r\n", 5, 0);
                    }
                } 
                //Handle no-op
                else if (tokens[0].compare("NOOP") == 0)
                {
                    send(ConnectFD, "200\r\n", 5, 0);
                  
                } 
                //Handle List
                else if (tokens[0].compare("LIST") == 0)
                {
                    if (!binary)
                    {
                        send(ConnectFD, "451\r\n", 5, 0);
                        continue;
                    }
                    int dataSocketFD = setUpSocket((struct sockaddr *)&ca, sizeof ca);
                    send(ConnectFD, "150\r\n", 5, 0);
                    
                    int pid = fork();
                    if (pid == 0)
                    {
                        dup2(dataSocketFD, 1);
                        if (tokens.size() > 1)
                            execl("/bin/ls", "/bin/ls", "-l", tokens[1].c_str(), (char*) NULL);
                        else
                            execl("/bin/ls", "/bin/ls", "-l", (char*) NULL);
                        
                    } else
                    {
                        int status;
                        waitpid(pid, &status, 0);
                        if (status > 0)
                            send(ConnectFD, "450\r\n", 5, 0);
                        else
                            send(ConnectFD, "250\r\n", 5, 0);
                        close(dataSocketFD);
                        
                    }
                  
                } 
                //Respond to unknown command
                else {
                    send(ConnectFD, "502\r\n", 5, 0);
                }
            }
        }
        
        //Close connection
        if (shutdown(ConnectFD, SHUT_RDWR) == -1) {
            perror("shutdown failed");
            close(ConnectFD);
            close(SocketFD);
            exit(EXIT_FAILURE);
        }
        close(ConnectFD);
    }

    close(SocketFD);
    return EXIT_SUCCESS;  
}