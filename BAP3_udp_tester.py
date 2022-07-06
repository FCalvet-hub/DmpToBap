import os
import socket
import random
import msvcrt
import time
import string
from time import sleep
from threading import Thread

usleep = lambda x: time.sleep(x / 1000000.0)

usleep(100)  # sleep during 100μs

UDP_RCV_IP = "0.0.0.0"
UDP_RCV_PORT = 2000
UDP_RCV_PORT2 = 3000
UDP_RCV_PORT3 = 4000
UDP_RCV_PORT4 = 12
UDP_SND_IP = "10.54.79.38"
UDP_SND_PORT = 2001
UDP_SND_PORT2 = 3001
UDP_SND_PORT3 = 4001

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_RCV_IP, UDP_RCV_PORT))

sock2 = socket.socket(socket.AF_INET,  # Internet
                      socket.SOCK_DGRAM)  # UDP
sock2.bind((UDP_RCV_IP, UDP_RCV_PORT2))

sock3 = socket.socket(socket.AF_INET,  # Internet
                      socket.SOCK_DGRAM)  # UDP
sock3.bind((UDP_RCV_IP, UDP_RCV_PORT3))

sock4 = socket.socket(socket.AF_INET,  # Internet
                      socket.SOCK_DGRAM)  # UDP
sock4.bind((UDP_RCV_IP, UDP_RCV_PORT4))

'''
for socketess in range(3,12):
    sockarray.extend
    sockarray.append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
    print(socketess)
    sockarray[socketess].bind((UDP_RCV_IP, socketess))
    sockarray[socketess].setblocking(0)

for socketess in range(15,123):
    sockarray.extend
    sockarray.append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
    print(socketess)
    sockarray[socketess-3].bind((UDP_RCV_IP, socketess))
    sockarray[socketess-3].setblocking(0)

for jj in sockarray:
    direccion, puerto = jj.getsockname()
    print("Direccion: ", direccion,"  Puerto: ",puerto)
'''

sock.setblocking(0)
sock2.setblocking(0)
sock3.setblocking(0)
sock4.setblocking(0)

sndsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sndsock.bind((UDP_RCV_IP, 35246))
sndsock.setblocking(0)

sockarray = [sock, sock2, sock3, sndsock]

old_ts = time.time()

incremental = 0
incrnum = 1
secuenciaCmd = 99900

accionList = [
    "ENCENDER",
    "APAGAR",
    "ESTADOSALIDA",
    "PULSAR",
    "ALIVE",
    (''.join(random.choice(string.ascii_letters)))
]

secList = [
    "0",
    "1234",
    "sdfg"
]

salList = [
    "1",
    "wsf",
    "sdf"
]

def sndData2BAP(comando, puerto):
    respuesta_udp = comando

    sharedKey = random.randint(0, 255)
    respuesta_udp_byte = bytearray()
    respuesta_udp_byte += bytearray(respuesta_udp, 'ascii')

    resultado = respuesta_udp_byte

    resp_enc_udp = bytearray()
    resp_enc_udp.append(1)
    resp_enc_udp.append(sharedKey)
    resp_enc_udp += respuesta_udp_byte

    k = resp_enc_udp[1]

    for i in range(0, len(respuesta_udp_byte)):
        resultado[i] = respuesta_udp_byte[i] ^ k

    for i in range(1, len(respuesta_udp_byte)):
        resultado[i] = (resultado[i] + resultado[i - 1]) % 256

    for i in range(0, len(respuesta_udp_byte)):
        resp_enc_udp[i + 2] = resultado[i]

    '''+ bytearray(sharedKey) + bytearray(respuesta_udp)'''
    if puerto == UDP_RCV_PORT:
        puerto = UDP_SND_PORT
    if puerto == UDP_RCV_PORT2:
        puerto = UDP_SND_PORT2
    if puerto == UDP_RCV_PORT3:
        puerto = UDP_SND_PORT3
    print('envio udp: ', respuesta_udp, ' puerto: ', puerto)
    # print ('envio encriptado udp: ', list(resp_enc_udp))
    #usleep(3000)  # sleep during 10μs
    sndsock.sendto(resp_enc_udp, (UDP_SND_IP, puerto))

fallas = 0
numAnterior = 0
ackNum = 0
ackNumAnt = 0
old_resp_time=0
incrSal = 1

while True:
    resp_time = time.time()
    if (resp_time - old_resp_time) > 5:
        old_resp_time = resp_time
    for sockete in sockarray:
        try:
            data, addr = sockete.recvfrom(1024)  # buffer size is 1024 bytes
            # print(data)
            dataString = ''
            listData = bytearray(data)
            k = listData[1]
            listData[1] = 0
            for i in range(2, len(listData)):
                '''print(listData[i],' ',listData[i-1],' ',(listData[i]-listData[i-1]),' ',(listData[i]-listData[i-1])%256,' ',((listData[i]-listData[i-1])%256)^k,' ',chr(((listData[i]-listData[i-1])%256)^k))'''
                '''result[i-2] = ((listData[i]-listData[i-1]) |k)%256 '''
                dataString += (chr(((listData[i] - listData[i - 1]) % 256) ^ k))
            # print ("received message:", data)
            incremental = incremental + 1
            diror, portor = sockete.getsockname()
            print("decrypt message:", dataString, "  puerto: ", portor)
            # if numAnterior == 0:
            #     numAnterior = int(dataString, 10) - 1
            # if (int(dataString, 10) - numAnterior) != 1:
            #     fallas += 1
            #     print('FALLAS: ', fallas, '  TOTAL: ',incrnum)
            # numAnterior = int(dataString, 10)
            if (dataString[13:16] == "BAP" or dataString[13:16] == "STA" or dataString[13:16] == "CID" or dataString[13:16] == "TEL"):
                direccion, puerto = sockete.getsockname()
                sndData2BAP("ACK," + dataString[3:7], puerto)
                # ackNum = int(dataString[3:7], 16)
                # if (ackNum - ackNumAnt) != 1:
                #     fallas += 1
                #     print("Fallas: ", fallas)
                # ackNumAnt = ackNum


        except socket.error:
            pass
        else:
            # print ("recv:", data[0],"times",len(data))
            pass  # print()

    if msvcrt.kbhit() == True:
        inchar = msvcrt.getch()
        numerornd = random.randint(2, 2)
        # print('presionado: ', inchar)
        if inchar == b'1':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("PULSO_KEYSW", puerto)
        if inchar == b'2':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("STATUS_IO", puerto)
        if inchar == b'3':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("TOGLE_ZONA", puerto)
        if inchar == b'4':
            direccion, puerto = sockarray[numerornd].getsockname()
            usleep(2000)  # sleep during 10μs
            # resp_udp_byte = bytearray()
            # for i in range(0,random.randint(10,48)):
            #    resp_udp_byte.append(random.randint(0,255))
            # resp_udp_byte+=bytearray("SETIPD,0a364f24",'ascii')
            # sndsock.sendto(resp_udp_byte, (UDP_SND_IP, UDP_SND_PORT))
            # print("Envio:",resp_udp_byte)
            sndData2BAP("SETIPD,0A364F24", puerto)
            # sndData2BAP("SETIPD," + '{:02x}'.format(random.randint(0, 255)) + '{:02x}'.format(
            #     random.randint(0, 255)) + '{:02x}'.format(random.randint(0, 255)) + '{:02x}'.format(
            #     random.randint(0, 255)), puerto)
        if inchar == b'5':
            direccion, puerto = sockarray[numerornd].getsockname()
            timetemp = '{:04X}'.format(random.choice(range(1, 5)))
            sndData2BAP("SET_T_TIME," + timetemp, puerto)
            # sndData2BAP("SET_T_TIME,0300",puerto)
        if inchar == b'6':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("IPCONF", puerto)
        if inchar == b'7':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("PULSO_ZONA1", puerto)
        if inchar == b'8':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("ACK," + '{:04x}'.format(incremental), puerto)
        if inchar == b'9':
            direccion, puerto = sockarray[numerornd].getsockname()
            letras = string.printable
            sndData2BAP(letras, puerto)
        if inchar == b'p':
            byterandom = bytearray(os.urandom(255))
            print(byterandom)
            sndsock.sendto(byterandom, (UDP_SND_IP, UDP_SND_PORT))
        if inchar == b'e':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",ENCENDER," + str(random.randint(1, 4)), puerto)
            secuenciaCmd += 1
            sndData2BAP("CMD,1,ENCENDER,1", puerto)
            sndData2BAP("CMD,ssdg,ENCENDER,1", puerto)
            sndData2BAP("CMD,,ENCENDER,1", puerto)
            sndData2BAP("CMD,0,ENCENDER,1", puerto)
            sndData2BAP("CMD,ffff,ENCENDER,1", puerto)
            sndData2BAP("CMD,1,ENCENDER,sdfg", puerto)
            sndData2BAP("CMD,1,ENCENDER,", puerto)
            sndData2BAP("CMD,1,ENCENDER,0", puerto)
            sndData2BAP("CMD,1,ENCENDER,fff", puerto)
            sndData2BAP("CMD,1,ENCENDER1", puerto)
            sndData2BAP("CMD,1,ENCENDER,1,df,s,3,4,5,234,df,d", puerto)
            secuenciaCmd += 1
            sndData2BAP("CMD," + str(secuenciaCmd) + ",APAGAR," + str(random.randint(1, 4)), puerto)
            secuenciaCmd += 1
            sndData2BAP("CMD," + str(secuenciaCmd) + ",PULSAR," + str(random.randint(1, 4)), puerto)
            secuenciaCmd += 1
            sndData2BAP("CMD," + str(secuenciaCmd) + ",ESTADOSALIDA," + str(random.randint(1, 4)), puerto)
            secuenciaCmd += 1
            sndData2BAP("CMD," + str(secuenciaCmd) + ",POLL", puerto)
            secuenciaCmd += 1
        if inchar == b'a':
            accionList[len(accionList)-1] = (''.join(random.choice(string.ascii_letters) for i in range(random.randint(1, 5))))
            secList[0] = str(secuenciaCmd)
            secList[1] = (''.join(random.choice(string.ascii_letters) for i in range(random.randint(1, 5))))
            secList[2] = str(random.randint(1, 10))
            salList[0] = str(random.randint(1, 4))
            salList[1] = str(random.randint(1, 5000000000))
            salList[2] = (''.join(random.choice(string.ascii_letters) for i in range(random.randint(1, 5))))

            direccion, puerto = sockarray[numerornd].getsockname()            #sndData2BAP("CMD," + str(secuenciaCmd) + ",ENCENDER," + str(random.randint(1, 100)), puerto)
            # sndData2BAP("CMD," + (''.join(random.choice(string.ascii_letters) for i in range(random.randint(1, 5)))) + ",ENCENDER," + str(random.randint(1, 10)), puerto)
            # sndData2BAP("CMD," + str(secuenciaCmd) + "," + random.choice(accionList) +","+ str(random.randint(1, 10)), puerto)
            # sndData2BAP("CMD," + str(secuenciaCmd) + random.choice(accionList) + (''.join(random.choice(string.ascii_letters) for i in range(random.randint(1, 5)))), puerto)
            sndData2BAP("CMD," + random.choice(secList) + "," + random.choice(accionList) + "," + random.choice(salList),puerto)
            secuenciaCmd += 1
        if inchar == b's':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",ENCENDER," + str(random.randint(1, 10)), puerto)
            secuenciaCmd += random.randint(0, 1)

        if inchar == b'd':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",APAGAR," + str(random.randint(1, 10)), puerto)
            secuenciaCmd += random.randint(0, 1)
        if inchar == b'f':
            direccion, puerto = sockarray[numerornd].getsockname()
            incrSal += 1
            if incrSal > 5:
                incrSal = 1
            sndData2BAP("CMD," + str(secuenciaCmd) + ",PULSAR," + str(incrSal) + "," + str(random.randint(1, 10)), puerto)
            secuenciaCmd += random.randint(0, 1)
        if inchar == b'g':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",ESTADOSALIDA," + str(random.randint(1, 10)), puerto)
            secuenciaCmd += random.randint(0, 1)
        if inchar == b'h':
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",POLL," + str(random.randint(1, 1)), puerto)
            secuenciaCmd += random.randint(0, 1)
        if inchar == b'j':
            direccion, puerto = sockarray[numerornd].getsockname()
            incrSal += 1
            if incrSal > 10:
                incrSal = 1
            if incrSal <= 5:
                sndData2BAP("CMD," + str(secuenciaCmd) + ",APAGAR," + str(incrSal), puerto)
                secuenciaCmd += 1
            else:
                sndData2BAP("CMD," + str(secuenciaCmd) + ",ENCENDER," + str(incrSal-5), puerto)
                secuenciaCmd += 1

    ts = time.time()

    if (ts - old_ts) > 0.025:
        old_ts = time.time()
        rndnum = random.randint(16, 16)
        #rndnum = random.choice([1,9])
        incrnum += 1
        # if incrnum > 10:
        #     incrnum = 0
        #     rndnum = 1
        # else:
        #     rndnum = 10
        numerornd = random.randint(2, 2)
        if rndnum == 1:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("PULSO_KEYSW", puerto)
        if rndnum == 2:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("STATUS_IO", puerto)
        if rndnum == 3:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("TOGLE_ZONA", puerto)
        if rndnum == 4:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("SETIPD,0a364f24", puerto)
        if rndnum == 5:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("SET_T_TIME,0001", puerto)
        if rndnum == 6:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("PULSO_ZONA1", puerto)
        if rndnum == 7:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("PULSO_ZONA2", puerto)
        if rndnum == 8:
            direccion, puerto = sockarray[numerornd].getsockname()
            # sndsock.sendto(byteSec,(UDP_SND_IP,UDP_SND_PORT))
            sndData2BAP(str(incrnum), puerto)
            # sndsock.sendto(b'\x0112345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', (UDP_SND_IP, UDP_SND_PORT))
            # sndsock.sendto(
            #     b'12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890',
            #     (UDP_SND_IP, UDP_SND_PORT))
        if rndnum == 9:
            byterandom = bytearray(os.urandom(random.randint(1, 255)))
            byterandom.insert(0, 1)
            # print(len(byterandom))
            sndsock.sendto(byterandom, (UDP_SND_IP, UDP_SND_PORT))
        if rndnum == 10:
            direccion, puerto = sockarray[numerornd].getsockname()
            letras = string.printable
            msgEnvio = "".join(random.choice(letras) for i in range(0, random.randint(1, 255)))
            #print(msgEnvio)
            sndData2BAP(msgEnvio, puerto)
        if rndnum == 11:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",ENCENDER," + str(random.randint(1, 5)), puerto)
            secuenciaCmd += 1
        if rndnum == 12:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",ENCENDER," + str(random.randint(1, 5)), puerto)
            secuenciaCmd += 1
        if rndnum == 13:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",APAGAR," + str(random.randint(1, 5)), puerto)
            secuenciaCmd += 1
        if rndnum == 14:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",PULSAR," + str((secuenciaCmd % 5) + 1) + "," + str(random.randint(1, 1)), puerto)
            secuenciaCmd += 1
        if rndnum == 15:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",ESTADOSALIDA," + str(random.randint(1, 5)), puerto)
            secuenciaCmd += 1
        if rndnum == 16:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",POLL" , puerto)
            secuenciaCmd += 1
        if rndnum == 17:
            direccion, puerto = sockarray[numerornd].getsockname()
            sndData2BAP("CMD," + str(secuenciaCmd) + ",ENCENDER," + (''.join(
                random.choice(string.digits) for i in range(random.randint(1, 1)))), puerto)
            secuenciaCmd += 1
        if rndnum == 18:
            direccion, puerto = sockarray[numerornd].getsockname()
            incrSal += 1
            if incrSal > 10:
                incrSal = 1
            if incrSal <= 5:
                sndData2BAP("CMD," + str(secuenciaCmd) + ",APAGAR," + str(incrSal), puerto)
                secuenciaCmd += 1
            else:
                sndData2BAP("CMD," + str(secuenciaCmd) + ",ENCENDER," + str(incrSal-5), puerto)
                secuenciaCmd += 1
        if rndnum == 19:
            accionList[len(accionList)-1] = (''.join(random.choice(string.printable) for i in range(random.randint(1, 5))))
            secList[0] = str(secuenciaCmd)
            secList[1] = (''.join(random.choice(string.printable) for i in range(random.randint(1, 50))))
            secList[2] = str(random.randint(1, 10000000000000000000000000000000000000000000000000000000000))
            salList[0] = str(random.randint(1, 4))
            salList[1] = str(random.randint(1, 50000000000000000000000000000000000000000000000000000000000))
            salList[2] = (''.join(random.choice(string.printable) for i in range(random.randint(1, 50))))

            direccion, puerto = sockarray[numerornd].getsockname()            #sndData2BAP("CMD," + str(secuenciaCmd) + ",ENCENDER," + str(random.randint(1, 100)), puerto)
            sndData2BAP("CMD," + random.choice(secList) + "," + random.choice(accionList) + "," + random.choice(salList),puerto)
            secuenciaCmd += 1