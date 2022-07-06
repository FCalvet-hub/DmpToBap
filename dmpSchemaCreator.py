import json
from pathlib import Path

archivo = 'DMPesquema.json'

myfile = Path(archivo)
myfile.touch(exist_ok=True)

data = dict()

data['Za'] = {}
data['Zb'] = {}
data['Zd'] = {}
data['Zf'] = {}
data['Zh'] = {}
data['Zk'] = {}
data['Zr'] = {}
data['Zt'] = {}
data['Zw'] = {}
data['Zx'] = {}
data['Zy'] = {}
data['Zj'] = {}
data['Zl'] = {}
data['Zq'] = {}
data['Zu'] = {}
data['Zg'] = {}
data['Ze'] = {}
data['Zm'] = {}
data['Zn'] = {}
data['Zs'] = {}
data['Zc'] = {}
data['Zi'] = {}
data['Zz'] = {}

data['Za']["name"] = "Zone Alarm"
data['Zb']["name"] = "Zone Force"
data['Zd']["name"] = "Zone Low Battery"
data['Zf']["name"] = "Zone Fail"
data['Zh']["name"] = "Zone Missing"
data['Zk']["name"] = "Zone Verify"
data['Zr']["name"] = "Zone Restore"
data['Zt']["name"] = "Zone Trouble"
data['Zw']["name"] = "Zone Fault"
data['Zx']["name"] = "Zone Bypass"
data['Zy']["name"] = "Zone Reset"
data['Zj']["name"] = "Door Access"
data['Zl']["name"] = "Schedules"
data['Zq']["name"] = "Arming Status"
data['Zu']["name"] = "User Codes"
data['Zg']["name"] = "Holidays"
data['Ze']["name"] = "Equipment"
data['Zm']["name"] = "Service Code"
data['Zn']["name"] = "Lockdown"
data['Zs']["name"] = "System Message"
data['Zc']["name"] = "Device Status"
data['Zi']["name"] = "Zone Tamper"
data['Zz']["name"] = "Reserved"
     
data['Za']["category"] = "Zone_type"
data['Zb']["category"] = "Zone_type"
data['Zd']["category"] = "Zone_type"
data['Zf']["category"] = "Zone_type"
data['Zh']["category"] = "Zone_type"
data['Zk']["category"] = "Zone_type"
data['Zr']["category"] = "Zone_type"
data['Zt']["category"] = "Zone_type"
data['Zw']["category"] = "Zone_type"
data['Zx']["category"] = "Zone_type"
data['Zy']["category"] = "Zone_type"
data['Zj']["category"] = "Status_type"
data['Zl']["category"] = "Schedule_type"
data['Zq']["category"] = "Arming_type"
data['Zu']["category"] = "User_type"
data['Zg']["category"] = "Holiday_type"
data['Ze']["category"] = "Equipment_type"
data['Zm']["category"] = "Service_type"
data['Zn']["category"] = "lockdown_type"
data['Zs']["category"] = "System_type"
data['Zc']["category"] = "Real_time_type"
data['Zi']["category"] = "Tamper_type"
data['Zz']["category"] = "reserved_type"


for key in data:
    if data[key]["category"] == "Zone_type":
        data[key]['type'] = {
      "BL": {"name": "Blank",                                       "CIDEventCode": 140, "enable": True     },
      "FI": {"name": "Fire",                                        "CIDEventCode": 110, "enable": True     },
      "BU": {"name": "Burglary",                                    "CIDEventCode": 130, "enable": True     },
      "SV": {"name": "Supervisory",                                 "CIDEventCode": 150, "enable": True     },
      "PN": {"name": "Panic",                                       "CIDEventCode": 120, "enable": True     },
      "EM": {"name": "Emergency",                                   "CIDEventCode": 100, "enable": True     },
      "A1": {"name": "Auxiliary 1",                                 "CIDEventCode": 140, "enable": True     },
      "A2": {"name": "Auxiliary 2",                                 "CIDEventCode": 140, "enable": True     },
      "CO": {"name": "Carbon Monoxide",                             "CIDEventCode": 140, "enable": True     },
      "VA": {"name": "Video Alarm",                                 "CIDEventCode": 140, "enable": True     }
        }       
    if data[key]["category"] == "Status_type":
        data[key]['type'] = {
            "DA" :{"name": "Door Access Granted"     ,"CIDEventCode": 0, "enable": False     },
            "AA" :{"name": "Denied: Armed Area"      ,"CIDEventCode": 0, "enable": False     },
            "IA" :{"name": "Denied: Invalid Area"    ,"CIDEventCode": 0, "enable": False     },
            "IT" :{"name": "Denied: Invalid Time"    ,"CIDEventCode": 0, "enable": False     },
            "AP" :{"name": "Denied: Previous Access" ,"CIDEventCode": 0, "enable": False     },
            "IC" :{"name": "Denied: Invalid Code"    ,"CIDEventCode": 0, "enable": False     },
            "IL" :{"name": "Denied: Invalid Level"   ,"CIDEventCode": 0, "enable": False     },
            "WP" :{"name": "Denied: Wrong PIN"       ,"CIDEventCode": 0, "enable": False     },
            "IN" :{"name": "Denied: Inactive User"   ,"CIDEventCode": 0, "enable": False     },
            "DO" : {"name": "Door Status: Open",                    "CIDEventCode": 0, "enable": False     },
            "DC" : {"name": "Door Status: Closed",                  "CIDEventCode": 0, "enable": False     },
            "HO" : {"name": "Door Status: Held Open",               "CIDEventCode": 0, "enable": False     },
            "FO" : {"name": "Door Status: Forced Open",             "CIDEventCode": 0, "enable": False     },
            "ON" : {"name": "Output Status: On",                    "CIDEventCode": 0, "enable": False     },
            "OF" : {"name": "Output Status: Off",                   "CIDEventCode": 0, "enable": False     },
            "PL" : {"name": "Output Status: Pulse",                 "CIDEventCode": 0, "enable": False     },
            "TP" : {"name": "Output Status: Temporal",              "CIDEventCode": 0, "enable": False     },
            "MO" : {"name": "Output Status: Momentary",             "CIDEventCode": 0, "enable": False     }
        }
    if data[key]["category"] == "Schedule_type":
        data[key]['type'] = {
            "PE" :   {"name": "Permanent Schedule",                 "CIDEventCode": 0, "enable": False     },
            "TE" :   {"name": "Temporary Schedule",                 "CIDEventCode": 0, "enable": False     },
            "PR" :   {"name": "Primary Schedule",                   "CIDEventCode": 0, "enable": False     },
            "SE" :   {"name": "Secondary Schedule",                 "CIDEventCode": 0, "enable": False     },
            "S1" :   {"name": "Shift One",                          "CIDEventCode": 0, "enable": False     },
            "S2" :   {"name": "Shift Two",                          "CIDEventCode": 0, "enable": False     },
            "S3" :   {"name": "Shift Three",                        "CIDEventCode": 0, "enable": False     },
            "S4" :   {"name": "Shift Four",                         "CIDEventCode": 0, "enable": False     },
            "00-99": {"name": "Numeric,XR150/350/550",              "CIDEventCode": 0, "enable": False     }
       }   
    if data[key]["category"] == "Arming_type":              #son los que hay que mandar con armado/desarmado
        data[key]['type'] = {
            "OP" : {"name": "Area Disarmed",                        "CIDEventCode": 400, "enable": True      },  
            "CL" : {"name": "Area Armed",                           "CIDEventCode": 400, "enable": True      }, 
            "LA" : {"name": "Area Late to Arm",                     "CIDEventCode": 0,   "enable": False     }            
       }
    if data[key]["category"] == "User_type":              
        data[key]['type'] = {
           "AD" : {"name": " User Code Added",                      "CIDEventCode": 0,   "enable": False     },
           "CH" : {"name": " User Code Changed",                    "CIDEventCode": 0,   "enable": False     },                                   
           "DE" : {"name": " User Code Deleted",                    "CIDEventCode": 0,   "enable": False     },
           "IN" : {"name": "User Code Inactive",                   "CIDEventCode": 0,   "enable": False     }                                   
       }   
    if data[key]["category"] == "Holiday_type":              
        data[key]['type'] = {                
            "HA" : {"name" : "Holiday Schedule A",                  "CIDEventCode": 0,   "enable": False     },  
            "HB" : {"name" : "Holiday Schedule B",                  "CIDEventCode": 0,   "enable": False     },
            "HC" : {"name" : "Holiday Schedule C",                  "CIDEventCode": 0,   "enable": False     }
       }   
    if data[key]["category"] == "Equipment_type":              
        data[key]['type'] = {  
            "RP" : {"name": "Repair"                               ,"CIDEventCode": 0,   "enable": False     },
            "RL" : {"name": "Replace"                              ,"CIDEventCode": 0,   "enable": False     },    
            "AD" : {"name": "Add"                                  ,"CIDEventCode": 0,   "enable": False     },
            "RM" : {"name": "Remove"                               ,"CIDEventCode": 0,   "enable": False     },
            "AJ" : {"name": "Adjust"                               ,"CIDEventCode": 0,   "enable": False     },
            "TS" : {"name": "Test"                                 ,"CIDEventCode": 0,   "enable": False     },
            "SO" : {"name": "Receiver EEPROM Error - System Option","CIDEventCode": 0,   "enable": False     },        
            "PR" : {"name": "Receiver EEPROM Error - Printer"      ,"CIDEventCode": 0,   "enable": False     },    
            "LC" : {"name": "Receiver EEPROM Error - Line Card"    ,"CIDEventCode": 0,   "enable": False     },    
            "H1" : {"name": "Receiver EEPROM Error - Host Port"    ,"CIDEventCode": 0,   "enable": False     },    
            "H2" : {"name": "Receiver EEPROM Error - Host Port"    ,"CIDEventCode": 0,   "enable": False     },    
            "SP" : {"name": "Receiver EEPROM Error - Serial Port"  ,"CIDEventCode": 0,   "enable": False     },        
            "LG" : {"name": "Receiver EEPROM Error - Log"          ,"CIDEventCode": 0,   "enable": False     },
            "EE" : {"name": "Receiver EEPROM Error - Entire EEPROM","CIDEventCode": 0,   "enable": False     },        
            "CD" : {"name": "ContactID"                            ,"CIDEventCode": 0,   "enable": False     }
       }  
    if data[key]["category"] == "Service_type":              
        data[key]['type'] = {  
           "ST" : {"name": "Start Service User",                    "CIDEventCode": 0,   "enable": False     },
           "SP" : {"name": "Stop Service User ",                    "CIDEventCode": 0,   "enable": False     }                                                  
       }
    if data[key]["category"] == "lockdown_type":              
        data[key]['type'] = { 
                                                            
       }  
    if data[key]["category"] == "Real_time_type":              #son los que hay que mandar con armado/desarmado
        data[key]['type'] = {
                                           
       }  
    if data[key]["category"] == "Tamper_type":              #son los que hay que mandar con armado/desarmado
        data[key]['type'] = { 
                                                            
       }  
    if data[key]["category"] == "reserved_type":              #son los que hay que mandar con armado/desarmado
        data[key]['type'] = { 
                                                            
       }        
    if data[key]["category"] == "System_type":              #son los que hay que mandar con armado/desarmado
        data[key]['type'] = {  
                                                           
       }                                                                          
         
for key in data:
    for ev in data[key]['type']: 
        if key in['Zr','Zy']:           #restore y reset
            data[key]['type'][ev]['restore'] = True
        else:
            if key in['Zq'] and ev == 'CL':            #en arming status, el que es close
                data[key]['type'][ev]['restore'] = True
            else:
                data[key]['type'][ev]['restore'] = False
            
        
    
with open(archivo,'w') as f:     
    json.dump(data,f,sort_keys=True, indent=4)