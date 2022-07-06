from threading import Thread
import socket
import queue
import logging
from serial3tocid import Serial3_to_CID

def setup_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(message)s')
    fileHandler = logging.FileHandler(log_file)
    fileHandler.setFormatter(formatter)
    #streamHandler = logging.StreamHandler()
    #streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    #l.addHandler(streamHandler)    


setup_logger('log1', "./log1.log")
setup_logger('log2', "./log2.log")
logger_1 = logging.getLogger('log1')
logger_2 = logging.getLogger('log2')


class ScsVrReceiving(Thread):
    def __init__(self, mysocket: socket.socket, scsVrqueue: queue.Queue):
        super().__init__()
        self.mysocket = mysocket
        self.queue = scsVrqueue
        
    def run(self):
        try:
            while True:            
                    dataIn = self.mysocket.recv(2048)
                    logging.info(f'Mensaje recibido desde {self.mysocket.getpeername()} payload: {dataIn}')
                    traductor = Serial3_to_CID(dataIn.decode())
                    cid = traductor.analyzeScsvrData()
                    logging.info(f'Traduccion a CID: {cid}')
                    logger_1.info(f'Traduccion a CID: {cid}')
                    self.queue.put_nowait(dataIn)
        except Exception as e:
            logging.error(f'Algo salio mal: {e}')
                
                        
class ScsVrSending(Thread):
    def __init__(self, mysocket: socket.socket, scsVrqueue: queue.Queue):
        super().__init__()
        self.mysocket = mysocket
        self.queue = scsVrqueue
        
    def run(self):
        try:
            while True:
                dataIn = self.queue.get()          
                sndmsg = chr(6).encode('utf-8')     
                self.mysocket.send(sndmsg)
                logging.debug(f'Mensaje enviado: {sndmsg} a {self.mysocket.getpeername()}')
        except Exception as e:
            logging.error(f'Algo salio mal: {e}')


class ScsVrlistening(Thread):
    def __init__(self):
        super().__init__()
        self.dmpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind, asignacion de ip y puerto... si 0.0.0.0 escucha en la ip de la maquina
        self.dmpSocket.bind(('0.0.0.0',2002))            
        self.dmpSocket.listen()
        
    def run(self):
        while True:
            mysocket, address = self.dmpSocket.accept()
            logging.info(f'Nueva conexion desde {address}')
            
            #se crea la cola para scsVr
            scsVrqueue = queue.Queue(500)
            
            # se crea thread de envio
            scsVrSendThread = ScsVrSending(mysocket, scsVrqueue)
            
            # se crea thread de escucha
            scsVrRecvThread = ScsVrReceiving(mysocket, scsVrqueue)
            
            # start de ambos threads    
            scsVrSendThread.start()
            scsVrRecvThread.start()     


if __name__ == "__main__":
    
    FORMAT = '%(asctime)s -- %(levelname)s -- %(thread)d -- %(message)s'    
    
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    
    dmpListener = ScsVrlistening()
    dmpListener.start()
    
    # # Creacion del objeto "socket" para escuchar a la receptora virtual SCSVR
    # dmpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # # Bind, asignacion de ip y puerto... si 0.0.0.0 escucha en la ip de la maquina
    # dmpSocket.bind(('0.0.0.0',2002))
    # # se pone en escucha...
    # dmpSocket.listen()
    # # se aceptan conexiones entrantes
    # mysocket, address = dmpSocket.accept()
    
    # #se crea la cola para scsVr
    # scsVrqueue = queue.Queue(500)
    
    # # se crea thread de envio
    # scsVrSendThread = ScsVrSending(mysocket, scsVrqueue)
    
    # # se crea thread de escucha
    # scsVrRecvThread = ScsVrReceiving(mysocket, scsVrqueue)
    
    # # start de ambos threads    
    # scsVrSendThread.start()
    # scsVrRecvThread.start()
    

