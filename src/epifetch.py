import database as db
import anidb as ani
import time
import atexit

program_name: str = 'epifetch'

def fetch_latest_episodes(sock: object, config: object, AID: int, SID: str):
    now = int(time.time())
    end_date = db.db_get('Series', 'end_date', 'aid', AID)
    if (now > int(end_date)):
        print('ended')
        # grab if last grab was before end date
        if ((db.db_get('Series', 'end_date', 'aid', AID)) > db.db_get('Series', 'date_last_accessed', 'aid', AID)):
            db.season_handler(AID, ani.fetch_anime(sock, config, AID, SID))
    else:
        print('ongoing')
        # grab if it was grabbed longer that a day ago
        if ((db.db_get('Series', 'date_last_accessed', 'aid', AID) + 86400) < now):
            db.season_handler(AID, ani.fetch_anime(sock, config, AID, SID))
    db.episodes_handler(AID, 1, ani.fetch_episodes(sock, config, AID, 1, db.db_get('Series', 'highest_episode_number', 'aid', AID), SID))

def mark_episodes(config: object, mark: str, AID: int, EPOS: int, EPOE: int):
    c, connection = db.init()
    i: int = EPOS
    while (i <= EPOE):
        command = (f"UPDATE Episodes SET Status = '{mark}' WHERE AID = {AID} AND episode_number = {i}")
        c.execute(command)
        i = i + 1
    connection.commit()
    connection.close()
    
### Commands ###

def command_login() -> tuple: 
    """Returns: myconfig, mysock, SID"""
    command = 'login'
    myconfig: object = ani.config()
    mysock: object = ani.udp_startup(myconfig)
    SID: str = ani.login(mysock, myconfig)
    # atexit.register(ani.logout(mysock, myconfig, SID))  
    return myconfig, mysock, SID

def command_mark(com: list[str]):
    command = 'mark'
    aid: int = com[1].replace('_',' ')
    try:
        episode: int = com[2]
    except:
        print(f"usage: {command} <show-title or id> <first> <last>")
        return 0
    try:
        episodeEnd: int = com[3]
    except TypeError:
        return 1
    except:
        episodeEnd = episode
    try:
        if (not com[2].isnumeric() and not com[3].isnumeric()):
            raise TypeError
    except:
        print(f"usage: {command} <show-title or id> <first> <last>")
    else:
        print(f'{command}: episodes {episode}-{episodeEnd} from {aid}')
        if (aid.isnumeric()): # user is using aid
            # print(f'{com[1]} is numeric, using aid')
            c, connection = db.init()
            while (int(episode) <= int(episodeEnd)):
                c.execute(f"UPDATE Episodes SET status = 'seen' WHERE AID = '{aid}' and episode_number = '{episode}'")
                episode:int = int(episode) + 1
            print('done')
            connection.commit()
            connection.close()
            return
        else: # user is using name
            title = aid
            # print(f"is not numeric")
            same_aid = True
            result: list[list[str]] = db.search_title(title)
            for entry in result:
                same_aid = entry[2] * same_aid
            if (same_aid):
                print(result)
                com[1] = str(result[0][2])
                command_mark(com)
                print(f'{com[1]}')
                return
            else:
                print(f"{command}: Show title was not specific enough, try using the Search command and use the AID")
        
def command_search(name: str):
    command = 'search'
    name.replace('_', ' ')
    db.print_search(db.search_title(name))

def command_check(mysock: object, myconfig: object, SID):
    command = 'check'
    ongoing = db.db_get_ongoing()
    if (ongoing != 0):
        for i in ongoing:
            db.season_handler(i[1], ani.fetch_anime(mysock, myconfig, i[1], SID))
            latest_episode = db.db_get_one('Series', 'highest_episode_number', 'aid', i[1])
            latest_seen = db.db_get_all('Episodes', 'Episode_number', 'aid', i[1])[-1][0]
            #temp fix for episodes name 'episode x'
            # blah blah blah
            print(f"getting from {latest_seen} to {latest_episode}")
            db.episodes_handler(i[1], latest_seen, ani.fetch_episodes(mysock, myconfig, i[1], latest_seen, latest_episode, SID))
    
    db.print_lookup(db.search_unwatched())

def command_fetch(mysock: object, myconfig: object, SID, com: list[str]):
    AID = com[1]
    command = 'fetch'
    try:
        if(com[2] == 'all'):
            # print(f"fetching all from {AID}")
            db.season_handler(AID, ani.fetch_anime(mysock, myconfig, AID, SID))
            latest_episode = db.db_get_one('Series', 'highest_episode_number', 'aid', AID)
            db.episodes_handler(AID, 1, ani.fetch_episodes(mysock, myconfig, AID, 1, latest_episode, SID))
    except Exception:
        try:
            if(com[2].isnumeric()):
                # print(f"getting {AID}")
                db.season_handler(AID, ani.fetch_anime(mysock, myconfig, AID, SID))
                db.episodes_handler(AID, 1, ani.fetch_episodes(mysock, myconfig, AID, 1, com[2], SID))
        except Exception:
            db.season_handler(AID, ani.fetch_anime(mysock, myconfig, AID, SID))

            

        
        
    
    