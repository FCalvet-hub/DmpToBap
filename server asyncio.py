import socket
import asyncio
import os, random

HOST, PORT = '192.168.0.10', 2000

def encrypt_bap_msg(msg: str) -> list: 
    aux = []
    result = []  
      
    shkey = random.randint(0,255)            
    for i in msg:
        aux.append(ord(i) ^ shkey) 
    
    for i in range(1,len(aux)):
        aux[i] = aux[i] + aux[i-1] & 0xFF        
        
    result.append(1)
    result.append(shkey)
    result.extend(aux)    
    return result

def send_test_message(message: 'Message to send to UDP port 514') -> None:
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP    
    sock.sendto(bytes(message), (HOST, PORT))


async def write_messages(transport) -> "Continuously write messages to UDP port 514":
    print("writing")
    incremental = 0
    for line in range(500):
        await asyncio.sleep(random.uniform(0.1, 1.0))
        incremental += 1
        msg_to_send = encrypt_bap_msg(f'DE,{incremental:04d},0000,CID,0056181122010030')
        send_test_message(msg_to_send)


class SyslogProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport) -> "Used by asyncio":
        self.transport = transport
        incremental = 0        
        incremental += 1
        msg_to_send = encrypt_bap_msg(f'DE,{incremental:04d},0000,CID,0056181122010030')
        self.transport.sendto(bytes(msg_to_send), (HOST, PORT))

    def datagram_received(self, data, addr) -> "Main entrypoint for processing message":
        # Here is where you would push message to whatever methods/classes you want.
        print(f"Received Syslog message: {data}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()    
    t = loop.create_datagram_endpoint(SyslogProtocol, local_addr=('0.0.0.0', PORT))    
    loop.run_until_complete(t) # Server starts listening
    #loop.run_until_complete(write_messages()) # Start writing messages (or running tests)
    loop.run_forever()