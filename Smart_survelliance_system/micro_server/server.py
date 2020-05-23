from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse,parse_qs
import json
from FaceRecog import recognize_video

PORT_NUMBER = 5081
camFiles = ['','','','']
camData = ['','','','']
camSentFile = ['','','','']
camSentData = ['','','','']
names = []
RealTimes = []
RealVids = []
RealImages = []
ReturnDict = {}
class myHandler(BaseHTTPRequestHandler):
    
    def writeanotherResponse(self,id,response):
        self.send_response(200,'success')
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('apns-id', id)
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
        return 
    
    def writeResponse(self,response):
        self.send_response(200,'success')
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
        return 
    
    def do_HEAD(self):
        pass
    
    def log_message(self, format, *args):
        return
       
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        command = query_components["cmd"][0]
        if command=="crowd_alert":
            #read file
            #send details
            with open("../shared_file/shared.txt", "r") as f:
                d = f.readlines()
                f.seek(0)
                for i in d: 
                    linesplit = i.split(" ")
                    if linesplit[0]=="cam1":
                        if camFiles[0]==linesplit[1]:
                            camSentFile[0]="NA"
                            camSentData[0]="NA"
                        else:
                            camFiles[0] = linesplit[1]
                            camData[0] = linesplit[2]
                            camSentData[0] = camData[0]
                            camSentFile[0] = camFiles[0]

                    elif linesplit[0]=="cam2":
                        if camFiles[1]==linesplit[1]:
                            camSentFile[1]="NA"
                            camSentData[1]="NA"
                        else:
                            camFiles[1] = linesplit[1]
                            camData[1] = linesplit[2]
                            camSentData[1] = camData[1]
                            camSentFile[1] = camFiles[1]

                    elif linesplit[0]=="cam3":
                        if camFiles[2]==linesplit[1]:
                            camSentFile[2]="NA"
                            camSentData[2]="NA"
                        else:
                            camFiles[2] = linesplit[1]
                            camData[2] = linesplit[2]
                            camSentData[2] = camData[2]
                            camSentFile[2] = camFiles[2]

                    elif linesplit[0]=="cam4":
                        if camFiles[3]==linesplit[1]:
                            camSentFile[3]="NA"
                            camSentData[3]="NA"
                        else:
                            camFiles[3] = linesplit[1]
                            camData[3] = linesplit[2]
                            camSentData[3] = camData[3]
                            camSentFile[3] = camFiles[3]      
            self.writeResponse({"cam1File": camSentFile[0],"cam2File":camSentFile[1],"cam3File":camSentFile[2],"cam4File":camSentFile[3],"cam1Data": camSentData[0],"cam2Data":camSentData[1],"cam3Data":camSentData[2],"cam4Data":camSentData[3]})
        
        elif command=="people_search":
            name = query_components["name"][0]
            image_response = recognize_video.getImages(name)
            self.writeResponse(image_response)

        elif command =="realTimePeople":
            #read content of file
            ReturnDict = {}
            upCont = 0
            with open("FaceRecog//shared_file//shared.txt", "r") as f:
                d = f.readlines()
                f.seek(0)
                for i in d: 
                    linesplit = i.split(" ")
                    co = 0
                    flag = 0
                    for nam in names:
                        if nam==linesplit[0]:
                            flag = 1  
                            break
                        co = co+1

                    if (flag ==1):
                        #CHECKING FOR ANY UPDATE
                        if RealVids[co]!=linesplit[1] or RealImages[co]!=linesplit[2] or RealTimes[co] !=linesplit[3]:
                            #Update Found
                            #Update All Variables
                            RealVids[co]=linesplit[1] 
                            RealImages[co]=linesplit[2] 
                            RealTimes[co] =linesplit[3]
                            ReturnDict[upCont] = RealImages[co]
                            upCont = upCont + 1

                    if (flag ==0):
                        #Name is not Present
                        #add name and details
                        names.append(linesplit[0])
                        RealVids.append(linesplit[1])
                        RealImages.append(linesplit[2])
                        RealTimes.append(linesplit[3])
                        ReturnDict[upCont] = RealImages[co]
                        upCont = upCont + 1


            self.writeResponse(ReturnDict)
            #read if name is added or not
            #if added
            #check for new entry
            #if not added
            #add person
            #add details
            #return latest img's

        
        #image = query_components["image"][0]                 
        #def log_message(self, format, *args):
        #return           
    
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    
    

if __name__ == "__main__":
    
    try:
        server = ThreadedHTTPServer(('', PORT_NUMBER), myHandler)
        #sys.stderr = open("/var/log/stream.log", "w")
        #print 'Starting httpserver on port ' , PORT_NUMBER
        server.serve_forever()
    
    except KeyboardInterrupt:
        server.socket.close()

