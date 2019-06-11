#!/anaconda3/bin/python

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import re

# datetimestamp according to RFC3339, 2019-06-11
"""
Tested at https://www.regextester.com/96683
9999-12-09T16:39:57-08:00
1937-01-01T12:00:27.87+00:20
1990-12-31T23:59:60Z
1985-04-12T23:20:50.52Z
1996-12-09T16:39:57-08:00
1996-12-09T16:39:57+08:00
"""

deadline_re = "^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])T(([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(.\d{2}|)(Z|(-|\+)([01][0-9]|2[0-3]):([0-5][0-9])))$"

class Records():
    records = {"events":[]}

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type','application/json')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')[1:]
        # print (self.path, path_elements)

        if not ( (len(path_elements) != 3 or len(path_elements) != 4) and path_elements[:3] == ["api", "v1","event"] ):
            self._set_headers(400)
            return
        
        else:
            # get all registered data 
            if len(path_elements) == 3:
                self._set_headers(200)
                str_json = json.dumps(Records.records) #,indent= 1)
                self.wfile.write(str.encode(str_json)) 
                return

            # get registered data by index
            elif len(path_elements) == 4:
                try:
                    id = int(path_elements[3])
                    print (id)
                    if id > 0 and len(Records.records["events"]) > 0 and len(Records.records["events"]) >= (id - 1 ):
                        data = Records.records["events"][id-1]
                        print (data)
                        self._set_headers(200)
                        str_json = json.dumps(data)
                        self.wfile.write(str.encode(str_json))
                        return

                    else:
                        self._set_headers(404)
                        return

                except Exception as e:
                    print (e)
                    self._set_headers(400)
                    return
        

    def register_data(self, data):
        print (data)
        deadline = data["deadline"]

        pattern = re.compile(deadline_re)

        if bool(pattern.match(deadline)):
            entry = {}
            entry["id"] = len(Records.records["events"]) + 1
            entry["deadline"] = data["deadline"]
            entry["title"] = data["title"] 
            entry["memo"] = data["memo"] 

            Records.records["events"].append(entry)
            id = len(Records.records["events"]) # newest data is at the end of list
            print ("Latest data: ",id, Records.records["events"])
            return id

        else:
            print ("data error")
            return -1

    def do_POST(self):

        if str(self.headers['Content-type']) != "application/json":
            self._set_headers(400)
            return

        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')[1:]
        # print (path_elements)     # path after the localhost:port

        if not ( len(path_elements) ==3 and path_elements ==  ["api", "v1" ,"event"]):
            self._set_headers(400)
            self.end_headers()
            return

        else:
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            
            id = self.register_data(data)
            if id == -1:
                self._set_headers(400)
                str_json = json.dumps({'result': 'failure','message':'invalid date format'})
                self.wfile.write(str.encode(str_json))     
                return
            else:
                self._set_headers(200)
                str_json = json.dumps({'result': 'success','message':'registered', 'id': id})
                self.wfile.write(str.encode(str_json))  
                return     



def main():
    server = HTTPServer(('', 8080), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
