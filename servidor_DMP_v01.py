import logging
import asyncio

from serial3tocid import Serial3_to_CID

logger = logging.getLogger(__name__)


class dmpServerProtocol(asyncio.Protocol):
    def __init__(self) -> None:
        super().__init__()

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
            if cid != None:
                logging.debug(f'Traduccion a CID: {cid}')
            else:
                logging.warning(f'Mensaje procesado no correcponde a un mensaje traducible a CID')
                        
            msgSnd = chr(6)
            msgSnd = msgSnd.encode('utf-8')
            logger.info(f'Datos enviados: {msgSnd}')
            self.transport.write(msgSnd)        
        except Exception as e:
            logger.error(e)
               

async def main(ipLocal, puertoLocal):
    logger.info(f'Iniciando server en ip: {ipLocal}  puerto: {puertoLocal}')    
    loop = asyncio.get_running_loop()
    dmpServer = await loop.create_server(lambda: dmpServerProtocol(), 
                                         ipLocal, 
                                         puertoLocal)    
    async with dmpServer:
        await dmpServer.serve_forever()
    
    #loop.create_server()

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
        
    ipLocal ='0.0.0.0'
    puertoLocal = 2002
    asyncio.run(main(ipLocal, puertoLocal))