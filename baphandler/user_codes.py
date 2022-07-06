
class UserCodes:
    '''
    Util para saber que codigos ADEMCO llevan el numero de usuario en el CID
    '''
    default_event_code_for_users = [
        121,        126,        313,        400,        401,        402,        403,        404,        405,
        406,        407,        408,        409,        441,        442,        443,        450,        451,
        452,        453,        454,        455,        456,        457,        458,        459,        462,
        463,        464,        466,        411,        412,        413,        414,        415,        421,
        422,        424,        425,        429,        430,        431,        435,        436,        574,
        604,        607,        625,        642,        652,        653,        655,        913,        914,
        915,        916,        920,        921,        928,        929
        ]
    
    def __init__(self) -> None:
        pass
    
    def isUserEventCode(self, evCode) -> bool:        
        '''devuelve si pertenece o no a un codigo de evento que lleva el numero de usuario en el CID'''
        if int(evCode) in self.default_event_code_for_users:
            return True
        
        return False
        