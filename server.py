#  coding: utf-8 

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

import SocketServer, os, mimetypes, sys
import datetime

class MyWebServer(SocketServer.BaseRequestHandler):

    def handle_GET(self):
        #I should guard against requests with relative pathing eg ..\..\someimportantfile.secret
        basedir = os.getcwd()+'/www'
        request_dir = basedir + self.request_line[1]
        header = 'HTTP/1.1 200 OK\r\n' #assume that we will be sending a 200 response packet

        if request_dir.endswith('/'):
            request_dir += 'index.html' #if this is a directory, we want the index.
        #TODO: handle 302 moved if the user is requesting a directory with no '/'. Currently that should just serve a 404

        #get the file if it exists or serve a 404
        if os.path.isfile(request_dir):
            file = open(request_dir)
            os.path.realpath(file.name)
        else:
            file = open(basedir+'/404.html')
            request_dir = basedir+'/404.html'
            header = 'HTTP/1.1 404 Not Found\r\n' #send a 404 packet

        #make sure we only serve out of www/
        if basedir not in os.path.realpath(request_dir):
            #we have someone trying to access something outside of /www/
            file.close()
            file = open(basedir+'/404.html')
            request_dir = basedir+'/404.html'
            header = 'HTTP/1.1 404 Not Found\r\n' #send a 404 packet

        mimetypes.init()
        mtype = mimetypes.MimeTypes()
        filetype, endcoding = mtype.guess_type(request_dir)

        resp_packet = header + \
            'Date: '+str(datetime.datetime.now())+'\r\n'+\
            'Connection: close\r\n'+\
            'Server: mattServer\r\n'+\
            'Content-Type: '+filetype+'\r\n'+\
            'Content-Length: '+ str(os.path.getsize(request_dir))+'\r\n'+\
            '\r\n'+\
            file.read()

        file.close()

        self.request.sendall(resp_packet)


    def send_405(self):
        basedir = os.getcwd()+'/www'
        request_dir = basedir+'/405.html'
        file = open(request_dir)

        mimetypes.init()
        mtype = mimetypes.MimeTypes()
        filetype, endcoding = mtype.guess_type(request_dir)

        resp_packet = 'HTTP/1.1 405 Method Not Allowed\r\n' + \
            'Date: '+str(datetime.datetime.now())+'\r\n'+\
            'Connection: close\r\n'+\
            'Server: mattServer\r\n'+\
            'Content-Type: '+filetype+'\r\n'+\
            'Content-Length: '+ str(os.path.getsize(request_dir))+'\r\n'+\
            '\r\n'+\
            file.read()

        file.close()

        self.request.sendall(resp_packet)
        

    def handle(self):
        self.data = self.request.recv(1024).strip()

        #parse request data
        parsed = self.data.split('\r\n') #split into an array of lines
        self.request_line = parsed[0].split() #now a list (method, directory, htmlversion)

        #determine if we can handle request (only GET for now) and send '405 Method Not Allowed' for other cases
        if self.request_line[0] == 'GET':
            self.handle_GET()
        else:
            self.send_405()
        
        
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
