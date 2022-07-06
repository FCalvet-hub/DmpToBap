import asyncio
from asyncio import tasks
import random
import logging
from numpy import uint8

from serial3tocid import Serial3_to_CID

logger = logging.getLogger(__name__)

HOST, PORT = '192.168.1.22', 3000
  
 
 
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
        

class dmpServerProtocol(asyncio.Protocol):
    def __init__(self, queueBap: asyncio.Queue, queueDmp: asyncio.Queue) -> None:
        super().__init__()
        self.colaDMP = queueDmp
        self.colaCID = queueBap
        
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        logger.info(f'Conexion desde {peername}')        
        self.transport = transport
        
    def data_received(self, data):
        try:
            message = data.decode()
            logger.info(f'Datos recibidos: {message}')        
            
            traductor = Serial3_to_CID(message)
            cid = traductor.analyzeScsvrData()
            if 14 < len(cid) < 18:
                self.colaDMP.put_nowait(cid)
                logging.debug(f'ESTE ES EL CID: {cid}')
        except Exception as e:
            logger.error(e)      
                 
        msgSnd = chr(6)
        msgSnd = msgSnd.encode('utf-8')
        logger.info(f'Datos enviados: {msgSnd}')
        self.transport.write(msgSnd)        

  
        
async def main():  
    ipLocal ='0.0.0.0'
    puertoLocal = 2002      
    
    colaBap = asyncio.Queue()
    colaDmp = asyncio.Queue()
    
    logger.info(f'Iniciando server en ip: {ipLocal}  puerto: {puertoLocal}')
    
    loop = asyncio.get_running_loop()
    
    cidServer = await loop.create_datagram_endpoint(
                        lambda: BapMgrHandler(colaBap, colaDmp),
                        local_addr=('0.0.0.0',3001))   
        
    dmpServer = await loop.create_server(lambda: dmpServerProtocol(colaBap, colaDmp), 
                                         ipLocal, 
                                         puertoLocal)         

    snmpAgent = await loop.create_task()
    #loop.run_until_complete(cidServer)
    #await cidServer.serve_forever()
    await dmpServer.serve_forever()
    
    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
       # dmpServer.close()
        cidServer.close()



if __name__ == '__main__':
    logger = logging.getLogger('')
    formatter = logging.Formatter("%(asctime)s %(levelname)s " + "[%(module)s:%(lineno)d] %(message)s")
    
    logger.setLevel(logging.DEBUG)
    conLog = logging.StreamHandler()
    conLog2 = logging.FileHandler('DMPserver.log')
    conLog.setLevel(logging.DEBUG)
    conLog2.setLevel(logging.DEBUG)
    
    conLog.setFormatter(formatter)
    conLog2.setFormatter(formatter)
    logger.addHandler(conLog)
    logger.addHandler(conLog2)
        
    asyncio.run(main())

# colaloca = asyncio.Queue()    
# loop1 = asyncio.get_event_loop()
# udplistener = loop1.create_datagram_endpoint(lambda: BapMgrHandler(colaloca), local_addr=('0.0.0.0',2000),)
# loop1.run_until_complete(udplistener)
# loop1.run_forever()
