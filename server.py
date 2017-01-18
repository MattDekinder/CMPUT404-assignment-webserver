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

import SocketServer, os

class MyWebServer(SocketServer.BaseRequestHandler):

    def handle_GET(self):
        #I should guard against requests with relative pathing eg ..\..\someimportantfile.secret
        basedir = os.getcwd()+'/www'
        request_dir = basedir + self.request_line[1]

        if request_dir.endswith('/'):
            request_dir += 'index.html'

        file = open(request_dir)

        self.request.sendall(file.read()) #this has to be made into a proper http packet with this data now. 
        
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #parse data
        parsed = self.data.split('\r\n') #split into an array of lines
        self.request_line = parsed[0].split() #now a list (method, directory, htmlversion)

        #determine if we can handle request (only GET for now) and send '405 Method Not Allowed' for other cases
        if self.request_line[0] == 'GET':
            self.handle_GET()
        else:
            #return '405 Method Not Allowed'
            return
        
        
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
