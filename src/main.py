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
            print(f'logging in...')
            # myconfig, mysock, SID = command_login()
            return usrinput
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
        case 'test':
            print("not logged in")
            db.print_lookup(db.search_unwatched())
            pass
        case 'exit':
            exit()
        case 'quit':
            exit()
        case _:
            print(f"{program_name}: Command not found: {com[0]}")
    return 0
            
def online(myconfig: object, mysock:object, SID:str, usrinput):
    # com = input(f"{program_name} % ")
    com = usrinput.split(' ')
    code = com[0]
    
    match code:
        case 'login':
            print(f'logging in...')
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
        case 'test':
            print("logged in")
        case 'exit':
                ani.logout(mysock, myconfig, SID)
                exit()
        case 'quit':
                ani.logout(mysock, myconfig, SID)
                exit()
        case _:
            print(f"{program_name}: Command not found: {com[0]}")
    return myconfig, mysock, SID
    
if (__name__ == '__main__'):
    print("")
    while(1):
        usrinput = input(f"\n{program_name} % ")
        if (offline(usrinput) != 0):
            myconfig, mysock, SID = command_login()
            while(1):
                myconfig, mysock, SID = online(myconfig, mysock, SID, usrinput)
                usrinput = input(f"\n{program_name} % ")
