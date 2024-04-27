import sqlite3
import csv
import yaml
import datetime
import time
import sys, os
# import anidb as ani 

DATACOMMAND_ANIME: list[tuple] = [
    # Byte 1
    ('aid', 'integer', True),
    ('date_flags', 'integer', True),
    ('year', 'text', True),
    ('type', 'text', True),
    ('related_aid_list', 'text', True),
    ('relatied_aid_type', 'text', True),
    ('retired_byte1_bit1', 'text', False),
    ('retired_byte1_bit0', 'text', False),
    # Byte 2
    ('romaji_name', 'text', True),
    ('kanji_name', 'text', True),
    ('english_name', 'text', True),
    ('other_name', 'text', False),
    ('short_name_list', 'text', False),
    ('synonym_list', 'text', False),
    ('retired_byte2_bit1', 'text', False),
    ('retired_byte2_bit0', 'text', False),
    # Byte 3
    ('episodes', 'integer', True),
    ('highest_episode_number', 'integer', True),
    ('special_episode_number', 'integer', True),
    ('air_date', 'integer', True),
    ('end_date', 'integer', True),
    ('url', 'text', True),
    ('picname', 'text', True),
    ('retired_byte3_bit0', 'text', False),
    # Byte 4integer
    ('rating', 'integer', True),
    ('vote_count', 'integer', True),
    ('temp_rating', 'integer', True),
    ('temp_vote_count', 'integer', True),
    ('average_review_rating', 'integer', True),
    ('review_count', 'integer', True),
    ('award_list', 'text', False),
    ('is_restricted', 'integer', True),
    # Byte 5
    ('retired_byte5_bit7', 'null', False),
    ('ANN_id', 'text', False),
    ('allcinema_id', 'text', False),
    ('AnimeNfo_id', 'text', False),
    ('tag_name_list', 'text', False),
    ('tag_id_list', 'text', False),
    ('tag_weight_list', 'text', False),
    ('date_record_updated', 'text', False),
    # Byte 6
    ('character_id_list', 'text', False),
    ('retired_byte6_bit6', 'null', False),
    ('retired_byte6_bit5', 'null', False),
    ('retired_byte6_bit4', 'null', False),
    ('unused_byte6_bit3', 'null', False),
    ('unused_byte6_bit2', 'null', False),
    ('unused_byte6_bit1', 'null', False),
    ('unused_byte6_bit0', 'null', False),
    # Byte 7
    ('specials_count', 'integer', True),
    ('credits_count', 'integer', True),
    ('other_count', 'integer', True),
    ('trailer_count', 'integer', True),
    ('parody_count', 'integer', True),
    ('unused_byte7_bit1', 'null', False),
    ('unused_byte7_bit1', 'null', False),
    ('unused_byte7_bit0', 'null', False)
]


REMOVE_UNICODE: bool = True
TITLE_PADDING: int = 50

DAT_DIC: dict = {
    '1' : 'Primary Title',
    '2' : 'Synonyms',
    '3' : 'Short Title',
    '4' : 'Official Title',
    '5' : 'null',
    '6' : 'null'
}

def init() -> tuple:
    # Connect to database
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    database_location = application_path + '/database.db'
    connection = sqlite3.connect(database_location, timeout=10)
    # Create cursor
    c = connection.cursor()
    return c, connection

def drop_table(table: str) -> None:
    try:
        c, connection = init()
        c.execute(f"DROP TABLE {table}")
    except:
        return

def init_series(config: object) -> None:
    c, connection = init()
    # Create Table
    command = "CREATE TABLE Series (title text"
    mask: int = 0
    byte: int = 6
    bit: int = 7
    for i in DATACOMMAND_ANIME:
        if (i[2]):
            command += f", {i[0]} {i[1]}"
            mask += 1 << (byte*8 + bit)
        if (bit == 0):
            byte -= 1
            bit = 7
        else:
            bit -= 1
    command += ",date_last_accessed integer)"
    config.MASK = format(mask, 'x')
    config.update()
    c.execute(command)

class series():
    def __init__(self, DATA: str) -> None:
        out = DATA.replace("\n","|")
        out = out.replace('"',"_")
        out = out.split("|")
        self.title = None
        self.AID = out[1]
        self.dateflags = out[2]
        self.year = out[3]
        self.type = out[4]
        self.related_aid_list = out[5]
        self.related_aid_type = out[6]
        self.romaji_name = out[7]
        self.kanji_name = out[8]
        self.english_name = out[9]
        self.episodes = out[10]
        self.highest_episode = out[11]
        self.special_episodes = out[12]
        self.air_date = out[13]
        self.end_date = out[14]
        self.url = out[15]
        self.pic_name = out[16]
        self.vote_count = out[17]
        self.temp_rating = out[18]
        self.temp_vote_count = out[19]
        self.restricted = out[20]
        self.specials_count = out[21]
        self.credits_count = out[22]
        self.other_count = out[23]
        self.trailer_count = out[24]
        self.parody_count = out[25]
        self.date_last_accessed = int(time.time())

class episode():
    def __init__(self, DATA: str) -> None:
        out = DATA.replace("\n","|")
        out = out.replace('"',"_")
        out = out.split("|")

def init_episodes() -> None:
    c, connection = init()
    # Create Table
    c.execute("""CREATE TABLE Episodes (
                 Series text,
                 Episode text,
                 episode_number integer, 
                 status text,
                 EID integer,
                 AID integer, 
                 length integer, 
                 rating integer, 
                 votes integer, 
                 english_title text, 
                 romaji_title text, 
                 kanji_title text, 
                 aired integer, 
                 type integer
    )""")
    
def init_search() -> None:
    c, connection = init()
    # Create Table
    c.execute("""CREATE TABLE Search (
                 AID integer,
                 type text,
                 language text,
                 title text    
    )""")
    
def exists1(TABLE: str, CATEGORY: str, DATA: str) -> bool:
    COM = f"SELECT {CATEGORY} FROM {TABLE} WHERE {CATEGORY} = {DATA}"
    c, command = init()
    c.execute(COM)
    result = c.fetchall()
    if (result == []):
        return False
    else:
        return True

def exists2(TABLE: str, CATEGORY1: str, DATA1: str, CATEGORY2: str, DATA2: str) -> bool:
    COM = f"SELECT {CATEGORY1} FROM {TABLE} WHERE {CATEGORY1} = {DATA1} AND {CATEGORY2} = {DATA2}"
    c, command = init()
    c.execute(COM)
    result = c.fetchall()
    if (result == []):
        return False
    else:
        return True

def db_get_one(TABLE: str, CATEGORY: str, DATACATEGORY: str, DATA: str) -> str:
    COM = f"SELECT {CATEGORY} FROM {TABLE} WHERE {DATACATEGORY} = {DATA}"
    c, command = init()
    c.execute(COM)
    entry = c.fetchone()
    # if (ani.DEBUG == True):
    #     print(f"entry = {entry}")
    if (entry == []):
        return 0
    return entry[0]

def db_get_all(TABLE: str, CATEGORY: str, DATACATEGORY: str, DATA: str) -> list[list[str]]:
    COM = f"SELECT {CATEGORY} FROM {TABLE} WHERE {DATACATEGORY} = {DATA}"
    c, command = init()
    c.execute(COM)
    entry = c.fetchall()
    # if (ani.DEBUG == True):
    #     print(f"entry = {entry}")
    if (entry == []):
        return [[0]]
    return entry

def db_get_ongoing() -> list[list[str]]:
    now: int = round(time.time(), 0)
    twelve_hours= 43200
    twelve_hours_ago= now - twelve_hours
    # if (ani.DEBUG == True):
    #     print(f'now = {now}')
    COM = f"SELECT title, aid FROM Series WHERE end_date = 0 AND date_last_accessed < {twelve_hours_ago} OR end_date > {now} AND date_last_accessed < {twelve_hours_ago} OR date_last_accessed < end_date AND date_last_accessed < {twelve_hours_ago}"
    c, command = init()
    c.execute(COM)
    entry = c.fetchall()
    # if (ani.DEBUG == True):
    #     print(f"entry = {entry}")
    if (entry == []):
        return 0
    return entry
    
def season_handler(AID: int, DATA: str) -> None:
    c, connection = init()
    out: str = DATA.replace("\n","|")
    out: str = out.replace('"',"_")
    out: list[str] = out.split("|")
    now = int(time.time())
    if (str(out[9]) != ''):
        title = out[9]
    elif (str(out[8]) != ''):
        title = out[8]
    elif (str(out[7]) != ''):
        title = out[7]
    else:
        title = 'null'
    # Create Table
    if (exists1("Series", "AID", AID)):
        command = f'UPDATE Series SET Title = "{title}"'
        ii: int = 1
        for i in DATACOMMAND_ANIME:
            if (i[2]):
                command += f', {i[0]} = "{out[ii]}"'
                ii += 1
        command += f", 'date_last_accessed' = {now} WHERE AID = '{AID}'"
    else:
        command = f'INSERT INTO Series VALUES ("{title}"'
        ii: int = 1
        for i in DATACOMMAND_ANIME:
            if (i[2]):
                command += f', "{out[ii]}"'
                ii += 1
        command += f", {now})"
    command = command.replace('""', '"null"')
    c.execute(command)
    connection.commit()
    connection.close()
    print(f"{AID} pushed to local database")

def episode_handler(AID: int, EPNO: int, DATA:str) -> None:
    c, connection = init()
    out = DATA.replace("\n","|")
    out = out.replace('"',"_")
    out = out.split("|")
    # Find proper title
    if (str(out[7]) != 'null'):
        title = out[7]
    elif (str(out(8) != 'null')):
        title = out[8]
    elif (str(out[9]) != 'null'):
        title = str(out[9])
    else:
        title = 'null'
    series: str = db_get_one('Series','title', 'AID', AID)
    if (int(out[10]) > int(time.time())):
        status = 'unreleased'
    else:
        status = 'unwatched'
    if (exists2('EPISODES', 'AID', AID, 'episode_number', EPNO)):
        print("Updating Database")
        c.execute(f"UPDATE EPISODES SET Series = '{series}', Episode = '{title}', episode_number = '{out[6]}', status = '{status}', EID = '{out[1]}', AID = '{AID}', length = '{out[3]}', rating = '{out[4]}', votes = '{out[5]}', english_title = '{out[7]}', romaji_title = '{out[8]}', kanji_title = '{out[9]}', aired = '{out[10]}', type = '{out[11]}' WHERE EID = '{out[1]}'")
    else:
        print("Adding to Database")
        c.execute(f"INSERT INTO EPISODES VALUES ('{series}', '{title}', '{out[6]}', '{status}', '{out[1]}', '{str(AID)}', '{out[3]}', '{out[4]}', '{out[5]}', '{out[7]}', '{out[8]}', '{out[9]}', '{out[10]}', '{out[11]}')")
    connection.commit()
    connection.close()
    
def episodes_handler(AID: int, EPNO_START: int, DATA: list[str]) -> None:
    if (DATA == 0):
        return 0
    for episode in DATA:
        out = episode.replace("\n","|")
        out = out.replace('"',"_")
        out = out.split("|")
        episode_handler(AID, out[6], episode)
    pass

def dat_handler(file: str) -> None:
    c, connection = init()
    drop_table('SEARCH') # TODO: return newly added entries
    init_search()
    with open(file, newline='') as datfile:
        dat = csv.reader(datfile, delimiter='|')
        for row in dat:
            if (row[0].isnumeric()):
                row[1] = DAT_DIC[row[1]]
                c.execute(f"INSERT INTO SEARCH VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}')")
    connection.commit()
    c.close()

def search_title(partial_title: str) -> list[list[str]]:
    partial_title = partial_title + "%"
    c, connection = init()
    c.execute(f"SELECT title, language, AID FROM SEARCH WHERE title LIKE '{partial_title}' ORDER BY AID")
    data = c.fetchall()
    connection.close()
    return data

def search_AID(AID: int) -> list[list[str]]:
    c, connection = init()
    c.execute(f"SELECT title, language, AID FROM SEARCH WHERE AID = '{str(AID)}' ORDER BY AID")
    data = c.fetchall()
    connection.close()
    return data

def search_unwatched() -> list[list[str]]:
    c, connection = init()
    c.execute(f"SELECT Series, Episode, episode_number, aired, aid FROM Episodes WHERE status = 'unwatched' or status = 'unreleased' ORDER BY aired")
    data = c.fetchall()
    connection.close()
    return data

def print_search(data: list[list[str]]) -> None:
    title = "Title"
    language = "Language"
    aid = "aid"
    nothing = ""
    print(f'| {nothing: ^{TITLE_PADDING}} | {nothing: ^10} | {nothing: ^6} |')
    print(f'| {title: ^{TITLE_PADDING}} | {language: ^10} | {aid: ^6} |')
    print(f'| {nothing:_^{TITLE_PADDING}} | {nothing:_^10} | {nothing:_^6} |')
    for row in data:
        title = row[0]
        if (REMOVE_UNICODE and title.isascii()): # non-ascii characters do not format properly
            title = str(title[:50])
            print(f'| {title: <{TITLE_PADDING}} | {row[1][:10]: <10} | {row[2]: <6} |')
       
def print_lookup(data: list[list[str]]) -> None:
    Series = "Series"
    Episode = "Episode"
    Episode_number = "#"
    Release = "Release Date"
    released = "Released"
    aid = "aid"
    nothing = ""
    print(f'| {nothing: ^6} | {nothing: ^20} | {nothing: ^{TITLE_PADDING}} | {nothing: ^5} | {nothing: ^20} | {nothing: ^5} ')
    print(f'| {aid: ^6} | {Series: ^20} | {Episode: ^{TITLE_PADDING}} | {Episode_number: ^5} | {Release: ^20} | {released: ^5}')
    print(f'| {nothing:_^6} | {nothing:_^20} | {nothing:_^{TITLE_PADDING}} | {nothing:_^5} | {nothing:_^20} | {nothing:_^5}')
    for row in data:
        title = row[0]
        if (REMOVE_UNICODE and title.isascii()): # non-ascii characters do not format properly
            title = str(title[:20])
            episode_name = str(row[1][:TITLE_PADDING])
            # Get date
            # ts_epoch = 1362301382
            ts_epoch = row[3]
            now = int(time.time())
            if (now < ts_epoch):
                avaliable = "no"
            else:
                avaliable = "yes"
            ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%d-%m-%Y %H:%M:%S')

            print(f'| {row[4]: <6} | {title: <20} | {(episode_name): <{TITLE_PADDING}} | {row[2]: ^5} | {ts: <20} | {avaliable: <5}')
     
if (__name__ == '__main__'):
    print_search(search_title(input("Search: ")))
    