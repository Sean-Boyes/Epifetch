# Epifetch
A terminal based anime episode/release tracker made for mac and windows built in python

# Overview
This project uses sqlite databases and udp communication with python
- Tracks all shows you are watching with a sqlite database
- Fetches all new episodes from AniDB
- Fetches useful metadate for every series and episode fetch
- Anime series lookup using sql lookups
- UDP server surge protection and error code handling
  
# Planned Features
- Release delay for dubs/regional releases
- Renaming for episodes that do not have a title when they are first confirmed
- Http request for up-to-date ```anime-title.dat```

# Packing
The packfiles are included for Windows as a bash file, and a shell file for Mac/Unix
- Pyinstaller is required (obviously)

# Basic Commands
- ```login``` | logs into anidb thought the ```config.yaml``` and user input username/password
- ```mark <show-title or id> <first> <last>``` | marks ```<show-title or id>``` from ```<first>``` to ```<last>``` episode as watched
- ```mark <show-title or id> <episode-number>``` | marks ```<show-title or id>``` ```<episode-number>``` as watched
- ```search <show-title or partial-title>``` | outputs a table of any series that match the ```<show-title or partial-title>```
- ```fetch <aid> <all>``` | fetches series with ```<aid>```, ```<all>```fetches all episodes in ```<aid>``` series
- ```check``` | outputs a table of episodes that you havent marked as watched, checks for any new releases
- ```clear``` | clears all saved data from your local database
- ```exit``` | exits program, logs out if logged in
- ```help``` | outputs the list of usable commands
