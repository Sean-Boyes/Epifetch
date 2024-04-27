import socket
import time
import yaml
from datetime import datetime
from database import exists2
import codes
import os
import sys

global LOGIN_ATTEMPT
LOGIN_ATTEMPT = 0

DEBUG = False

RELAITED_AID_TYPE: dict = {
     1 : 'sequel',
     2 : 'prequel',
    11 : 'same setting',
    32 : 'alternative version',
    41 : 'music video',
    42 : 'character',
    51 : 'side story',
    52 : 'parent story',
    61 : 'summary',
    62 : 'full story',
   100 : 'other'
}

class config:
    def __init__(self) -> None:
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        config_name = application_path + '/config.yaml'
        with open(config_name) as INCONFIG:
            CONFIGFILE = yaml.safe_load(INCONFIG)

        self.UDP_IP:         str = CONFIGFILE['constants']['UDP_IP']
        self.UDP_PORT:       int = CONFIGFILE["constants"]['UDP_PORT']
        self.LOCAL_IP:       str = CONFIGFILE["constants"]['LOCAL_IP']
        self.LOCAL_PORT:     int = CONFIGFILE["constants"]['LOCAL_PORT']
        self.PROTOVER:       int = CONFIGFILE['constants']['PROTOVER']
        self.CLIENT:         str = CONFIGFILE['constants']['CLIENT']
        self.CLIENT_VERSION: int = CONFIGFILE['constants']['CLIENT_VERSION']
        self.MASK:           str = CONFIGFILE['constants']['MASK']
        self.USERNAME:       str = CONFIGFILE['user']['USERNAME']
        self.PASSWORD:       str = CONFIGFILE['user']['PASSWORD']
        self.SID_TOKEN:      str = CONFIGFILE['session']['SID_TOKEN']

    def update(self) -> None:
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        config_name = application_path + '/config.yaml'
        with open(config_name, 'r') as f:
            CONFIGFILE = yaml.safe_load(f)
        CONFIGFILE['constants']['UDP_IP']         = self.UDP_IP
        CONFIGFILE["constants"]['UDP_PORT']       = self.UDP_PORT
        CONFIGFILE["constants"]['LOCAL_IP']       = self.LOCAL_IP
        CONFIGFILE["constants"]['LOCAL_PORT']     = self.LOCAL_PORT
        CONFIGFILE['constants']['PROTOVER']       = self.PROTOVER
        CONFIGFILE['constants']['CLIENT']         = self.CLIENT
        CONFIGFILE['constants']['CLIENT_VERSION'] = self.CLIENT_VERSION
        CONFIGFILE['constants']['MASK']           = self.MASK
        CONFIGFILE['user']['USERNAME']            = self.USERNAME
        CONFIGFILE['user']['PASSWORD']            = self.PASSWORD
        CONFIGFILE['session']['SID_TOKEN']        = self.SID_TOKEN
        with open("config.yaml", "w") as f:
            yaml.dump(CONFIGFILE, f)

def udp_startup(config: object) -> object:
    print(f"UDP target IP: {config.UDP_IP}")
    print(f"UDP target port: {config.UDP_PORT}")
    sock = socket.socket(socket.AF_INET,    # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((config.LOCAL_IP, config.LOCAL_PORT))
    return(sock)

# TODO: detect packet loss, check return code
def send_command(sock: object, config: object, COMMAND: str) -> str:
    time.sleep(3) # Flood Protection
    COMMAND = str.encode(COMMAND)
    sock.sendto(COMMAND, (config.UDP_IP, config.UDP_PORT))
    DATA, ADDR = sock.recvfrom(1024)
    DATA = bytes.decode(DATA)
    if (DEBUG == True):
        print(f'{COMMAND} | {DATA}')
    returncode = DATA.split(" ")[0]
    print (codes.codes[returncode])
    return(DATA)

def login(sock: object, config: object) -> str:
    COMMAND = f"AUTH user={config.USERNAME}&pass={config.PASSWORD}&protover={str(config.PROTOVER)}&client={config.CLIENT}&clientver={str(config.CLIENT_VERSION)}"
    DATA = send_command(sock, config, COMMAND)
    DATA = DATA.split(" ")
    DATACODE = DATA[0]
    match DATA[0]:
        case "200":
            # print("Login Accepted")
            pass
        case "201":
            # print("Login Accepted, New version avaliable")
            pass
        case "500":
            # print("Login Failed")
            return(DATACODE)
        case "503":
            # print("Client Version Outdated")
            return(DATACODE)
        case "504":
            # print(f"Client Banned")
            return(DATACODE)
        case "505":
            # print("Access Denied")
            return(DATACODE)
        case "555":
            # print("BANNED | too many logins in quick succession, come back later (or use a vpn :3)")
            # print(DATA)
            LOGIN_ATTEMPT = LOGIN_ATTEMPT + 1
            sleep_time = 4 ** LOGIN_ATTEMPT
            print(f"too many logins ({LOGIN_ATTEMPT}), waiting {sleep_time}")
            time.sleep(sleep_time)
            return(DATACODE)
        case "601":
            # print("Database out of Service, Try again later")
            return(DATACODE)
        case _:
            print(f"Error {DATACODE}")
            return(DATACODE)
    return(DATA[1]) # Session Token (SID)

def logout(sock: object, config: object, SID: str) -> None:
    COMMAND = f"LOGOUT s={SID}"
    print("Logging out...")
    send_command(sock, config, COMMAND)
    sock.close()
    # print("Logged out")
    
# TODO: Check when last fetched
def fetch_anime(sock: object, config: object, AID: int, SID: str) -> str:
    # Get Current Date
    now = datetime.now()
    COMMAND = (f"ANIME aid={str(AID)}&amask={config.MASK}&s={SID}")
    print(f"Getting Anime {AID}...")
    return send_command(sock, config, COMMAND)

# TODO: Check when last fetched
def fetch_episode(sock: object, config: object, AID: int, EPISODE: int, SID: str) -> str:
    # Get Current Date
    now = datetime.now()
    COMMAND = (f"EPISODE aid={str(AID)}&epno={str(EPISODE)}&s={SID}")
    print(f"Getting Episode {EPISODE}...")
    return send_command(sock, config, COMMAND)

def fetch_episodes(sock: object, config: object, AID: int, EPISODE_START: int, EPISODE_END: int, SID: str) -> list[str]:
    if (EPISODE_START == 0 and EPISODE_END == 0):
        return 0
    now = datetime.now()
    COMMAND = (f"EPISODE aid={str(AID)}&epno={str(EPISODE_START)}&s={SID}")
    number_of_episodes: int = EPISODE_END - EPISODE_START + 1
    i: int = EPISODE_START
    data: list[str] = []
    while (i <= EPISODE_END):
        if (exists2('EPISODES', 'AID', AID, 'episode_number', i) == False):
            COMMAND = (f"\nEPISODE aid={str(AID)}&epno={str(i)}&s={SID}")
            print(f"Getting Episode {i}...")
            data.append(send_command(sock, config, COMMAND))
        i += 1
    return data

def exit_handler() -> None:
    logout()
    
