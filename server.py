#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def read_request(self, request, host):
        # check method
        if request[0] != 'GET':
            header = "HTTP/1.1 405 Method Not Allowed\r\n"
            return header, '405 Method Not Allowed'
        
        root_path = './www'
        file_path = os.path.abspath(root_path+request[1])
        # check if path inside directory & if path exists
        if not file_path.startswith(os.getcwd()) or not os.path.exists(file_path):
            header = "HTTP/1.1 404 Not Found\r\n"
            return header, '404 Not Found'

        # if directory
        if os.path.isdir(file_path):
            content = ''
            if request[1][-1] != '/':
                host = 'http://' + host
                print('host === ', bytearray(host, 'utf-8'))
                location = 'Location: ' + host + request[1] + '/\r\n'
                header = "HTTP/1.1 301 Moved Permanently\r\n"
                header += location
            else:
                header = "HTTP/1.1 200 OK\r\n"
                f = open(file_path + '/index.html', 'r')
                content = f.read(1024)
                header += 'Content-Type: text/html\r\n'
            return header, content

        # else, read file
        f = open(file_path, 'r')
        content = f.read(1024)
        # check file type
        if file_path.endswith('.html'):
            type = 'Content-Type: text/html\r\n'
        elif file_path.endswith('.css'):
            type = 'Content-Type: text/css\r\n'
        return "HTTP/1.1 200 OK\r\n" + type, content
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        re = self.data.decode('utf-8').split('\n')
        # read request
        host = [h for h in re if h.startswith('Host:')]
        host = host[0].split(' ')
        header, content = self.read_request(re[0].split(' '), host[1].strip('\r'))
        self.request.sendall(bytearray(header + "\r\n\r\n" + content, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
