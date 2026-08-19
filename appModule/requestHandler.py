import time
import threading

class requestHandler:
    def __init__(self):
        self.responses = []
        self.requestQuee = []
        self.lock = threading.Lock()
        self.thread = None
        self.running = True
        self.start()
    
    def start(self):
        def worker():
            while self.running:
                if len(self.requestQuee) == 0:
                    time.sleep(0.05)
                else:
                    #try:
                        request = self.requestQuee.pop(0)
                        answer = request[2]()
                        self.responses.append((request[0], request[1], answer))
                    #except BaseException as e :
                       # print(e)
                       # self.responses.append((request[0], request[1], None))
                    
            print("request handler stoped")
        
        self.thread = threading.Thread(target=worker, daemon=True)
        self.thread.start()
    
    def getResponses(self):
        with self.lock:
            msgs = self.responses.copy()
            self.responses.clear()
            return msgs
    
    def placeOnCallStack(self, moduleName, useCase, lambdaFunc):
        self.requestQuee.append((moduleName, useCase, lambdaFunc))
        return 20
    
    def stop(self):
        self.running = False