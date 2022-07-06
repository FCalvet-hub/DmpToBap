from threading import Thread
import socket
import queue
import logging

class BapReceiving(Thread):
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
                
                        
class BapSending(Thread):
    def __init__(self, mysocket: socket.socket, bapQueue: queue.Queue):
        super().__init__()
        self.mysocket = mysocket
        self.queue = bapQueue
        
    def run(self):
        try:
            while True:
                dataIn = self.queue.get()          
                sndmsg = dataIn.encode('utf-8')     
                self.mysocket.sendto(sndmsg, ('192.168.0.229', 2000))
                logging.debug(f'Mensaje enviado a BAPMgr: {sndmsg} a {self.mysocket.getpeername()}')
        except Exception as e:
            logging.error(f'Algo salio mal: {e}')


class Baplistening(Thread):
    def __init__(self):
        super().__init__()
        self.bapSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind, asignacion de ip y puerto... si 0.0.0.0 escucha en la ip de la maquina
        self.bapSocket.bind(('0.0.0.0',2000))                    
        
    def run(self):
        while True:
            mysocket, address = self.bapSocket.accept()
            logging.info(f'Nueva conexion desde {address}')
            
            #se crea la cola para scsVr
            bapQueue = queue.Queue(500)
            
            # se crea thread de envio
            bapSendThread = BapSending(mysocket, bapQueue)
            
            # se crea thread de escucha
            bapRecvThread = BapReceiving(mysocket, bapQueue)
            
            # start de ambos threads    
            bapSendThread.start()
            bapRecvThread.start()     




class BapMgrHandler(asyncio.DatagramProtocol):
    def __init__(self, queueBap: asyncio.Queue, queueDmp: asyncio.Queue):
        super().__init__()
        print('se creo datagram')
        self.colaDMP = queueDmp
        self.colaCID = queueBap
        
    def calcCidChecksum(self, cidmsg) -> str:
        digitmap = {
            0xA : '0',
            0xB : '*',
            0xC : '#',
            0xD : 'A',
            0xE : 'B',
            0xF : 'C'
        }
        suma=0
        for i in cidmsg:
            suma += (int(i,base=16) if (i != '0') else 10)
            resto = 15 - (suma % 15)
            #print(f'{i}  {suma}  {hex(suma)}  {hex(resto)}')
        if resto in digitmap.keys():
            return digitmap[resto]
        else:
            return f'{resto}'
        
    def rndCidCreator(self) -> str:
        acct = random.choice([4,5,6,7])#random.randint(1,9999)
        q = random.choice([1,3])
        evc = random.randint(1,999)
        gg = random.randint(1,32)
        CCC = random.randint(1,999)
        cidmsg = f'{acct:04d}18{q}{evc:03d}{gg:02d}{CCC:03d}'
        chksum = self.calcCidChecksum(cidmsg)
        #print(f'{cidmsg}{chksum:X}')
        return (f'{cidmsg}{chksum}')
        
    def decrypt_bap_msg(self, MsgBapMgr) -> str:
        result = []
        if len(MsgBapMgr) > 3:
            bkey = MsgBapMgr[1]										# El segundo byte es un caracter random generado por el que envia el mensaje
            MsgBapMgr[1] = 0										# Cuando se encripta el mensaje, al primer elemento se le aplica XOR pero no se suma con nada!!!!*

            for i in range(2,len(MsgBapMgr)):
                result.append((uint8(MsgBapMgr[i]) - uint8(MsgBapMgr[i-1])) ^ bkey)                 
            
            return bytes(result).decode()

    def encrypt_bap_msg(self, msg: str) -> list: 
        aux = []
        result = []  
        
        #print(f'enviado: {msg}')
        shkey = random.randint(0,255)            
        for i in msg:
            aux.append(ord(i) ^ shkey) 
        
        for i in range(1,len(aux)):
            aux[i] = aux[i] + aux[i-1] & 0xFF        
            
        result.append(1)
        result.append(shkey)
        result.extend(aux)    
        return result

    def connection_made(self, transport):
        self.transport = transport      
        task = asyncio.create_task(self.udpsender())
        print(transport.get_extra_info('socket'))
        #self.udpsender()

    def datagram_received(self, data, addr):
        logger.debug(f'Mensaje desde BapMgr: {data}')
        decryptBapMsg = decrypt_bap_msg(bytearray(data))
        spltMsg = decryptBapMsg.split(',')        
        if spltMsg[0] == 'ACK':                         #esperamos ACK desde el BAPMgr, si OK ponemos mensaje en cola para el servidor de DMP         
            self.colaCID.put_nowait(decryptBapMsg)
            logger.debug(f'Mensaje desencriptado BapMgr: {decryptBapMsg}')

    '''SEGUIR ACAAAAAAAAAAAA'''
    def run(self):        
        try:
            while True:
                self.
                logging.debug(f'Mensaje desde BapMgr: {data}')
                decryptBapMsg = self.decrypt_bap_msg(bytearray(data))
                spltMsg = decryptBapMsg.split(',')        
                if spltMsg[0] == 'ACK':                         #esperamos ACK desde el BAPMgr, si OK ponemos mensaje en cola para el servidor de DMP         
                    self.colaCID.put_nowait(decryptBapMsg)
                    logger.debug(f'Mensaje desencriptado BapMgr: {decryptBapMsg}')
        except Exception as e:
            logging.error(f'ERROR: {e}')
    
    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Connection closed")
        #self.on_con_lost.set_result(True)       
    async def udpsender(self):
        incremental = 0       
        while True:                        
            #await asyncio.sleep(0.5)        
            # try:
            #     mensajeCola = await asyncio.wait_for(self.colaCID.get(), 2)
            # except Exception as e:
            #     mensajeCola = f'nada por aqui {e}'            
            # print(mensajeCola)
            
            incremental += 1        
            # cidRndMsg = rndCidCreator()
            cidRndMsg = await self.colaDMP.get()                   #espero que haya algo en la cola que llena el servicio DMP
            msg_to_send = encrypt_bap_msg(f'DE,{incremental:04X},0000,CID,{cidRndMsg}')
            logger.info(f'Enviando: DE,{incremental:04X},0000,CID,{cidRndMsg}')
            self.transport.sendto(bytes(msg_to_send), (HOST, PORT))            
        
