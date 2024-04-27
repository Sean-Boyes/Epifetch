from epifetch import *
import atexit

# TODO:
# + delay for releases
# + rename epsiodes if named "episode #"
# + http fetch the anime-titles.dat

def offline(usrinput):
    com = usrinput.split(' ')
    code = com[0]
    match code:
        case 'login':
            # print(f'logging in...')
            # myconfig, mysock, SID = command_login()
            return 'dummy'
        case 'mark':
            command_mark(com)
        case 'search':
            title = ""
            for i in com[1:]:
                title = title + i + " "
            title = title.rstrip(" ")
            # print(f"|{title}|")
            command_search(title)
        case 'fetch':
            # myconfig, mysock, SID = command_login()
            # online(myconfig, mysock, SID, usrinput) 
            return usrinput
        case 'check':
            # myconfig, mysock, SID = command_login()
            # online(myconfig, mysock, SID, usrinput)
            return usrinput
        #
        case 'clear':
            print("login before clearing your database")
        case 'exit':
            exit()
        case 'quit':
            exit()
        case 'help':
            commands = "\nCommands\n\n"
            commands += "login \n"
            commands += "mark \t usage: mark <show-title or id> <first> <last> \n"
            commands += "search \t usage: search <show-title or partial-title> \n"
            commands += "fetch \t usage: fetch <aid> \n"
            commands += "check \n"
            commands += "clear \n"
            commands += "exit \n"
            commands += "help \n"
            print(commands)
        case _:
            print(f"{program_name}: Command not found: {com[0]}")
    return 0
            
def online(myconfig: object, mysock:object, SID:str, usrinput):
    # com = input(f"{program_name} % ")
    com = usrinput.split(' ')
    code = com[0]
    
    match code:
        case 'login':
            # print(f'logging in...')
            # close socket if there is one in use
            try:
                mysock.close()
            except Exception as e:
                if (ani.DEBUG == True):
                    print(e)
            myconfig, mysock, SID = command_login()
        case 'mark':
            command_mark(com)
        case 'search':
            title = ""
            for i in com[1:]:
                title = title + i + " "
            title = title.rstrip(" ")
            # print(f"|{title}|")
            command_search(title)
        case 'fetch':
            try:
                command_fetch(mysock, myconfig, SID, com)
                pass
            except IndexError:
                print("usage: fetch <show-title or id>")
            except Exception:
                pass
        case 'check':
            try:
                command_check(mysock, myconfig, SID)
                pass
            except Exception as e:
                print(e)
                pass
        #
        case 'clear':
            if (input("Are you sure you want to clear your database? (y/N): ").lower() == 'y'):
                db.drop_table('Episodes')
                db.drop_table('Series')
                db.init_episodes()
                db.init_series(myconfig)
                print("database reset")
        case 'exit':
                ani.logout(mysock, myconfig, SID)
                exit()
        case 'quit':
                ani.logout(mysock, myconfig, SID)
                exit()
        case 'dummy':
            pass
        case 'help':
            commands = "\nCommands\n\n"
            commands += "login \n"
            commands += "mark \t usage: mark <show-title or id> <first> <last> \n"
            commands += "search \t usage: search <show-title or partial-title> \n"
            commands += "fetch \t usage: fetch <aid> \n"
            commands += "check \n"
            commands += "clear \n"
            commands += "exit \n"
            commands += "help \n"
            print(commands)
        case _:
            print(f"{program_name}: Command not found: {com[0]}")
    return myconfig, mysock, SID
    
if (__name__ == '__main__'):
    print("")
    while(1):
        usrinput = input(f"\n{program_name} % ")
        if (offline(usrinput) != 0):
            myconfig, mysock, SID = command_login()
            if (usrinput == 'login'):
                usrinput = 'dummy'
            while(1):
                myconfig, mysock, SID = online(myconfig, mysock, SID, usrinput)
                usrinput = input(f"\n{program_name} % ")
