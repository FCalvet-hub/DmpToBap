
import json
import logging
import queue

logger = logging.getLogger(__name__)

def calcCidChecksum(cidmsg):
    '''
    (Sum of all message digits + S) MOD 15 = 0
    Note: A 0 shall be transmitted as a 10 and
    valued as a 10 for checksum purposes even
    though it is displayed and printed as 0. It
    uses the same tone pair as the 0 (OPER)
    key on a standard telephone

    a) Add all of the message digits
    together, using 10 for all 0 digits
    (1+2+3+4)+(1+8)+(1+1+3+1)+(1
    0+1)+(10+1+5) = 52
    b) Find the next highest multiple of
    15, in this case 60.
    c) Subtract the sum from this value
    (60-52 = 8)
    d) Use the result for the checksum..
    If the result is 0, use the digit ‘F’
    (15) for the checksum.
    '''    
    suma=0
    resto=0
    for i in cidmsg:
        suma += (int(i, base=16) if (i != '0') else 10)
        resto = 15 - (suma % 15)
    return str(resto)

def queueCIDmsg(account: str, event_code: str, partition: str, zone: str, restore: bool, mType='18'):
    """
    Comprueba y coloca los datos de acuerdo al standard CID
    Ningun parametro debe exceder el largo correspondiente
    y deberan ser numericos los que correspondan.
    De cumplirse las condiciones, colocara el mensaje en cola para ser enviado 
    hacia el BAPMgr.

    El formato del mensaje CID es:
    ACCT MT QXYZ GG CCC S

    En donde
    ACCT: 4 digitos de numero de cuenta (0-9, B-F)
    MT = Tipo de mensaje: Define el formato (en el caso de CID es 18 y en algunos casos puede ser el 98)
    Q = Calificador de evento: 1= Nuevo evento o Apertura, 3 = Restablecimiento o Cierre, 6 = Reporte de Status (normalmente no utilizado)
    XYZ = Código de evento (3 dígitos)
    GG = Partición (2 dígitos): Se usa 00 para indicar que no pertenece a ninguna partición.
    CCC = Zona / Usuario (3 dígitos): Se usa 000 para indicar que no pertenece a ninguna zona/usuario.
    S = Dígito verificador de información o checksum (se usa para validar el evento)

    EJEMPLOs:
    6556 18 3 402 A1 015 D
    Cuenta: "6556"
    "18" identifica al protocolo CID
    Calificador: Cierre ("3")
    Código de evento: GRUPO O/C ("402")
    Partición: "01"
    Usuario: 15 ("015")
    "D" es un código de verificación de datos correctos producto de una sumatoria.

    1234 18 1131 01 015 8
    Cuenta: “1234”
    “18” identifica al protocolo CID
    Calificador: nuevo evento (“1”)
    Código de evento: “131”
    Partición: “01”
    Zona: “15” (015)
    "8" es un código de verificación de datos correctos producto de una sumatoria
    """
    cidMsg = ''

    if len(account) == 4 and account.isnumeric()       \
            and len(event_code) == 3 and event_code.isnumeric() \
            and len(partition) == 2 and partition.isnumeric()   \
            and len(zone) == 3 and zone.isnumeric():
        cidMsg = account + \
                 mType + \
                 ('1' if (restore != True) else '3') + \
                 event_code + \
                 zone
        resto = calcCidChecksum(cidMsg)        
        cidMsg += resto        
        logging.info(f'[CID] Mensaje encolado: {cidMsg}')        
        cola_cid.put(cidMsg)
        
    else:
        logging.error(
            "Problemas en el formado de mensaje CID, revisar mensaje de entrada y condiciones")                    

def analyzeScsvrData(in_str: str):
    
    logging.info(f'[DMP MSG] Mensaje a analizar: {in_str}')
    
    with open(dmpSchema_path) as f:
        dmpSch = json.load(f)
    
    try:
        evento = dict()
        '''Se extrae el numero de cuenta y se separa el resto del mensaje'''
        evento['acct'] = in_str[:in_str.index('Z')].strip(
            ' ')[-4:]  # rescato numero de cuenta y me quedo con los ultimos 4
        in_msg = in_str[in_str.index('Z'):]
        print(in_msg)

        '''Se separa el mensaje delimitado por contrabarra'''
        splt_msg = in_msg.split('\\')

        # se extrae la definicion del tipo de mensaje
        evento['def'] = splt_msg.pop(0)

        evento['size'] = splt_msg.pop(0)  # se extrae el largo

        if len(in_msg) == int(evento['size']):
            for dat in splt_msg:
                if dat[0] == 't':  # event type ----  Number: tqnnn\ or Text: tq"cc\
                    if dat[2] == '\"':  # viene texto
                        evento['type'] = dat[3:]
                    else:
                        evento['type'] = dat[2:]  # viene numero
                # zone  ---- zqnnn"ccccccc...(variable)...ccccccccc
                if dat[0] == 'z':
                    index_comillas = dat.find('\"')
                    if index_comillas > 1:
                        evento['zoneNum'] = dat[2:index_comillas]
                        evento['zoneName'] = dat[index_comillas:]
                    else:
                        evento['zoneNum'] = dat[2:]
                if dat[0] == 'a':  # area  ---- aqnnn"ccccccc...(variable)...ccccccccc\
                    index_comillas = dat.find('\"')
                    if index_comillas > 1:
                        evento['areaNum'] = dat[(index_comillas-2):index_comillas]
                        evento['areaName'] = dat[index_comillas:]
                    else:
                        evento['areaNum'] = dat[-2:]
                if dat[0] == 'v':  # device
                    pass
                if dat[0] == 'n':  # schedule
                    pass
                if dat[0] == 'e':  # qualifier
                    pass
                if dat[0] == 'h':  # holiday
                    pass
                if dat[0] == 'i':  # time/day
                    pass
                if dat[0] == 'd':  # date
                    pass
                if dat[0] == 'u':  # user code
                    pass
                if dat[0] == 's':  # Service
                    pass
                if dat[0] == 'g':  # Equipment
                    pass
                if dat[0] == 'p':  # Programming
                    pass
                if dat[0] == 'c':  # Path
                    pass
                if dat[0] == 'n':  # Call info
                    pass
                if dat[0] == 'b':  # Signal Strenght
                    pass
        else:
            raise LookupError(
                f"Deferencia en largo de mensaje. Largo mensaje {len(in_msg)}, largo recibido {evento['size']}")

        cidParams = dmpSch[evento['def']]['type'][evento['type']]       #intenta buscar 

        evento['evCode'] = '{:03d}'.format(cidParams['CIDEventCode'])
        evento['restore'] = cidParams['restore']

        if cidParams['enable'] == True:
            queueCIDmsg(
                account=evento['acct'],
                event_code=evento['evCode'],
                partition=(evento['areaNum']
                        if 'areaNum' in evento.keys() else '00'),
                zone=(evento['zoneNum'] if 'zoneNum' in evento.keys() else '000'),
                restore=evento['restore']
            )
        else:
            logging.info(
                f'Tipo de mensaje no habilitado en el esquema {dmpSchema_path}')

    except ValueError as e:
        logging.error(f'{e}')
    except KeyError as e:
        logging.error(f'No existe la el parametro {e} en el esquema.')
    # except Exception as e:
    #    print("error: ",e.__class__)




datoentrada = '1-12345 Za\\029\\t "BU\\z ***"BURGLARY\\\r'
datoentrada = '1-12345 Za\\020\\t "BU\\z ***\\\r'
datoentrada = '24545 Zq\\058\\t "OP\\z 051"BURGLARY\\u *****"PARTIAL ARM \\a 003" \\\r'


logging.basicConfig(filename='redirector.log', encoding='utf-8', level=logging.DEBUG, filemode='w', datefmt='%d/%m/%Y %H:%M:%S ', format='%(asctime)s %(message)s')

dmpSchema_path = './DMPesquema.json'

cola_cid =  queue.Queue()    

logger = logging.getLogger('')
formatter = logging.Formatter("%(asctime)s %(levelname)s " + "[%(module)s:%(lineno)d] %(message)s")

logger.setLevel(logging.DEBUG)
conLog = logging.StreamHandler()
conLog.setLevel(logging.DEBUG)

conLog.setFormatter(formatter)
logger.addHandler(conLog)

analyzeScsvrData(in_str= datoentrada)