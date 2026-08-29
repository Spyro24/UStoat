import websocket
import threading
import json
import time
import ssl
import certifi

class WSSClient:
    def __init__(self, url, logger=None):
        self.logger = logger
        self.url = url
        self.messages = []
        self.lock = threading.Lock()
        self.thread = None
        self.ws = None
        self.connected = False
        self.connection_error = None
        self.start()
    
    def start(self):
        def worker():
            def on_message(ws, msg):
                with self.lock:
                    self.messages.append(msg)
            
            def on_open(ws):
                with self.lock:
                    self.connected = True
                    self.connection_error = None
                    if self.logger:
                        self.logger.log("Websocket", "Connected")
            
            def on_close(ws, close_status_code, close_msg):
                with self.lock:
                    self.connected = False
                    if self.logger:
                        self.logger.log("Websocket", f"Closed: {close_status_code} - {close_msg}")
            
            def on_error(ws, err):
                with self.lock:
                    self.connection_error = str(err)
                    if self.logger:
                        self.logger.log("Websocket", f"Error: {err}")
            
            # SSL context configuration
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            self.logger.log("Websocket", "Starting Connection ...")
            try:
                ssl_context.load_verify_locations(certifi.where())
            except Exception as e:
                if self.logger:
                    self.logger.log("Websocket", f"Failed to load CA bundle: {e}, using default")
            
            self.ws = websocket.WebSocketApp(
                self.url,
                on_message=on_message,
                on_open=on_open,
                on_close=on_close,
                on_error=on_error,
            )
            self.ws.run_forever(http_proxy_host=None, http_proxy_port=None, proxy_type=None, sslopt={"cert_reqs": ssl.CERT_REQUIRED, "ca_certs": certifi.where()})
        
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
            if self.logger != None:
                self.logger.log("Websockte", "connection not established")
            raise RuntimeError("WebSocket connection not established")
    
    def is_ready(self):
        with self.lock:
            return self.connected and self.ws is not None
    
    def wait_until_ready(self, timeout=10):
        start = time.time()
        while time.time() - start < timeout:
            time.sleep(0.5)
            if self.is_ready():
                return True
        return False
