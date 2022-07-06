import asyncio
from asyncio import tasks
import random
from numpy import uint8

HOST, PORT = '192.168.0.10', 2000

  
def calcCidChecksum(cidmsg) -> str:
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
        
def rndCidCreator() -> str:
    acct = random.choice([4,5,6,7])#random.randint(1,9999)
    q = random.choice([1,3])
    evc = random.randint(1,999)
    gg = random.randint(1,32)
    CCC = random.randint(1,999)
    cidmsg = f'{acct:04d}18{q}{evc:03d}{gg:02d}{CCC:03d}'
    chksum = calcCidChecksum(cidmsg)
    #print(f'{cidmsg}{chksum:X}')
    return (f'{cidmsg}{chksum}')
    
def decrypt_bap_msg(MsgBapMgr) -> str:
    result = []
    if len(MsgBapMgr) > 3:
        bkey = MsgBapMgr[1]										# El segundo byte es un caracter random generado por el que envia el mensaje
        MsgBapMgr[1] = 0										# Cuando se encripta el mensaje, al primer elemento se le aplica XOR pero no se suma con nada!!!!*

        for i in range(2,len(MsgBapMgr)):
            result.append((uint8(MsgBapMgr[i]) - uint8(MsgBapMgr[i-1])) ^ bkey)                 
        
        return bytes(result).decode()

def encrypt_bap_msg(msg: str) -> list: 
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
 
 
class BapMgrHandler(asyncio.DatagramProtocol):
    def __init__(self, queueBap: asyncio.Queue, queueDmp: asyncio.Queue):
        super().__init__()
        #self.colaCID = asyncio.Queue(300)
        self.colaCID = queueBap

    def connection_made(self, transport):
        self.transport = transport      
        task = asyncio.create_task(self.udpsender())
        #self.udpsender()

    def datagram_received(self, data, addr):
        decryptBapMsg = decrypt_bap_msg(bytearray(data))
        self.colaCID.put_nowait(decryptBapMsg)
        #print(f"Received Syslog message: {decryptBapMsg}")
        
    async def udpsender(self):
        incremental = 0       
        while True:
            #await asyncio.sleep(0.5)        
            try:
                mensajeCola = await asyncio.wait_for(self.colaCID.get(), 2)
                await asyncio.sleep(2)
            except Exception as e:
                mensajeCola = f'nada por aqui {e}'            
            print(mensajeCola)
            
            incremental += 1        
            cidRndMsg = rndCidCreator()
            msg_to_send = encrypt_bap_msg(f'DE,{incremental:04X},0000,CID,{cidRndMsg}')
            self.transport.sendto(bytes(msg_to_send), (HOST, PORT))
            
                
class ScsVrListenerServer(asyncio.Protocol):
    def __init__(self, queueBap: asyncio.Queue, queueDmp: asyncio.Queue):
        super().__init__()
        #self.colaCID = asyncio.Queue(300)
        self.colaCID = queueBap
            
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()
        
        
async def main():    
    print("Starting UDP server")

    loop = asyncio.get_running_loop()
    colaBap = asyncio.Queue()
    colaDmp = asyncio.Queue()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: BapMgrHandler(colaBap, colaDmp),
        local_addr=('0.0.0.0',2000))

    server = await loop.create_server(
        lambda: ScsVrListenerServer(colaBap, colaDmp),
        '0.0.0.0', 2001)

    async with server:
        await server.serve_forever()

    #noseqeuesesto = await loop.create_task(tarea(colaloca))
    
    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()

asyncio.run(main())
# colaloca = asyncio.Queue()    
# loop1 = asyncio.get_event_loop()
# udplistener = loop1.create_datagram_endpoint(lambda: BapMgrHandler(colaloca), local_addr=('0.0.0.0',2000),)
# loop1.run_until_complete(udplistener)
# loop1.run_forever()
