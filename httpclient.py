#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
import errno
import time

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False

        start = time.time()
        while not done:
            if (time.time() - start) > 2:
                    done = True
            part = sock.recv(4096)
            if (part):
                buffer.extend(part)
                
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        parse = urllib.parse.urlparse(url)
        #print(parse)
        #if split has no port, add default from https or http
        pathSplit = parse.netloc.split(":")
        address = pathSplit[0]
        if len(pathSplit) <= 1:
            if parse.scheme.lower() == "https":
                port = "443"
            else:
                port = "80"
        else:
            #port given
            port = pathSplit[1]

        #print(address,port)
        
        self.connect(address,int(port))

        request = "GET "+parse.path +" HTTP/1.1 \r\nHost: "+address+":"+port+"\r\n"
        request += "Connection: Keep-Alive\r\n"
        #print("Request:\n"+request)

        self.sendall(request)

        response = self.recvall(self.socket)
        #print("Response:\n"+response)

        self.close()


        resList = response.split("\r\n")

        self.close()

        code = resList[0]
        body = ""

        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        parse = urllib.parse.urlparse(url)
        #print(parse)
        #if split has no port, add default from https or http
        pathSplit = parse.netloc.split(":")
        address = pathSplit[0]
        if len(pathSplit) <= 1:
            if parse.scheme.lower() == "https":
                port = "443"
            else:
                port = "80"
        else:
            #port given
            port = pathSplit[1]

        #print(address,port)
        
        self.connect(address,int(port))

        request = "POST "+parse.path +" HTTP/1.1 \r\nHost: "+address+":"+port+"\r\n"
        request += "Content-Type: application/x-www-form-urlencoded\r\n"
        #print("Request:\n"+request)

        body = "\r\n"
        length = 0
        if (args):
            for arg in args:
                length += len(arg)
                body += arg
            request += "Content-Length: " + str(length)
            request += body

        self.sendall(request)

        response = self.recvall(self.socket)

        resList = response.split("\r\n")

        self.close()

        code = resList[0]
        body = ""

        #print(code,body)
        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command.upper() == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    elif (len(sys.argv) == 4):
        print(client.command( sys.argv[2], sys.argv[1], sys.argv[4] ))
    else:
        print(client.command( sys.argv[1] ))
