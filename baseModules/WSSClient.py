import websocket
import threading
import json
import time

class WSSClient:
    def __init__(self, url):
        self.url = url
        self.messages = []
        self.lock = threading.Lock()
        self.thread = None
        self.ws = None
        self.start()
    
    def start(self):
        def worker():
            def on_message(ws, msg):
                with self.lock:
                    self.messages.append(msg)
            
            self.ws = websocket.WebSocketApp(self.url, on_message=on_message)
            self.ws.run_forever()
        
        self.thread = threading.Thread(target=worker, daemon=True)
        self.thread.start()
    
    def get_messages(self):
        with self.lock:
            msgs = self.messages.copy()
            self.messages.clear()
            return msgs
    
    def has_new_data(self):
        with self.lock:
            return len(self.messages) > 0
    
    def send_data(self, data):
        if self.ws:
            self.ws.send(data)
        else:
            raise RuntimeError("WebSocket connection not established")
