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
        self.connected = False
        self.start()
    
    def start(self):
        def worker():
            def on_message(ws, msg):
                with self.lock:
                    self.messages.append(msg)
            
            def on_open(ws):
                with self.lock:
                    self.connected = True
            
            self.ws = websocket.WebSocketApp(self.url, on_message=on_message, on_open=on_open)
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
    
    def is_ready(self):
        with self.lock:
            return self.connected and self.ws is not None
    
    def wait_until_ready(self, timeout=10):
        start = time.time()
        while time.time() - start < timeout:
            if self.is_ready():
                return True
            time.sleep(0.5)
        return False
