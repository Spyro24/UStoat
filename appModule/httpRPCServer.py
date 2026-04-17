from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue, Empty
import json
import threading
import uuid
import time

class HTTPServerWithQueue:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.request_queue = Queue()
        self.response_dict = {}
        handler = self._create_handler()
        self.server = HTTPServer((host, port), handler)
        
        # Server im Background starten
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        print(f'Server runs on http://{self.host}:{self.port}')
    
    def _create_handler(self):
        """Erstellt eine Handler-Klasse mit Zugriff auf die Queue und Response-Dict"""
        queue = self.request_queue
        response_dict = self.response_dict
        
        class RequestHandler(BaseHTTPRequestHandler):
            def handle_request(self, request_type):
                content_length = int(self.headers.get('Content-Length', 0))
                content = self.rfile.read(content_length).decode('utf-8', errors='ignore')
                
                headers = dict(self.headers.items())
                rid = str(uuid.uuid4())
                
                request_dict = {
                    'rid': rid,
                    'request': request_type,
                    'path': self.path,
                    'header': headers,
                    'content': content
                }
                
                queue.put(request_dict)
                
                while rid not in response_dict:
                    threading.Event().wait(0.01)
                
                response_data = response_dict.pop(rid)
                
                self.send_response(response_data.get('status', 200))
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                try:
                    self.wfile.write(json.dumps(response_data.get('data', {})).encode('utf-8'))
                except BrokenPipeError: pass
            
            def do_GET(self):
                self.handle_request('GET')
            
            def do_POST(self):
                self.handle_request('POST')
            
            def do_PUT(self):
                self.handle_request('PUT')
            
            def do_DELETE(self):
                self.handle_request('DELETE')
            
            def do_PATCH(self):
                self.handle_request('PATCH')
            
            def log_message(self, format, *args):
                pass
        
        return RequestHandler
    
    def get_requests(self):
        requests = []
        
        while True:
            try:
                requests.append(self.request_queue.get_nowait())
            except Empty:
                break
        
        return requests if requests else None
    
    def response(self, rid, data, status=200):
        self.response_dict[rid] = {'status': status, 'data': data}
    
    def stop(self):
        self.server.shutdown()