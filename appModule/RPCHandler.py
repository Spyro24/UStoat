import appModule.httpRPCServer
import secrets
import json

class RPCHandler:
    def __init__(self, app):
        self.app = app
        self.port = 19200
        self.server = appModule.httpRPCServer.HTTPServerWithQueue('localhost', self.port)
        self.perms = {}
        self.paths = {"auth": self.auth}
    
    def handleRequests(self):
        requests = self.server.get_requests()    
        if requests:
            for request in requests:
                path = request['path'].split("/")
                if path[1] == "":
                    self.server.response(request['rid'], {}, status=400)
                else:
                    #try:
                        curElement = self.paths
                        path.append(None)
                        for element in path[1:]:
                            if callable(curElement):
                                curElement(path, request['header'], request['content'], request['request'], request["rid"])
                                break
                            else:
                                curElement = curElement[element]
                    #except: self.server.response(request['rid'], {}, status=400)
                #print(request)
                #print(json.loads(request["content"]))
                #http_server.response(request['rid'], {'message': 'Erfolgreich verarbeitet', 'received_path': request['path']}, status=404)
    
    def auth(self, path, header, content, method, rid):
        print(header)
        if method == "GET":
            try:
                content = json.loads(content)
                print(content)
                token = secrets.token_hex(16)
                self.perms[token] = {}
                self.perms[token]
                self.server.response(rid, {'token': str(token)})
                return
            except: pass
        elif method == "DELETE":
            if "Authorization" in header and header["Authorization"] in self.perms:
                self.perms.pop(header["Authorization"])
                self.server.response(rid, {}, status=200)
            else:
                self.server.response(rid, {}, status=401)
            return
        else:
            self.server.response(rid, {}, status=405)
        self.server.response(rid, {}, status=400)
