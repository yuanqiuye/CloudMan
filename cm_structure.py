import sqlite3
import os
import json
import config
import re

localAppData = os.getenv("LOCALAPPDATA")
dbPath = os.path.normpath(localAppData + '\\Netease\\CloudMusic\\Library\\webdb.dat')
con = sqlite3.connect(dbPath)

class PlayList:
    pid = None
    playlist = None

class SongDetail:
    detail = None
    relative_path = None
    real_suffix = None

class FailedRecords:
    tid = None
    reason = None

    def __init__(self, tid, reason):
        self.tid = tid
        self.reason = reason


def FetchPlaylist():
    onlyUser = config.parseCfg("onlyUserPlaylist")
    userId = config.parseCfg("userId")
    ret = []
    CommandText = "SELECT * FROM web_playlist"
    rows = con.execute(CommandText)

    for row in rows:
        
        elem = PlayList()
        elem.pid = int(row[0])
        elem.playlist = json.loads(row[1])
        if onlyUser == "True" and elem.playlist["creator"]["userId"] != int(userId):
            continue

        ret.append(elem)
    
    return ret


def FetchPlaylistSongs(pid):
    ret = []
    CommandText = "SELECT tid, pid FROM web_playlist_track WHERE pid = " + str(pid) + " ORDER BY `order`"
    rows = con.execute(CommandText)

    for row in rows:
        ret.append(row[0])

    return ret

def FetchSongDetial(tid):
    ret = SongDetail()

    CountText = "SELECT COUNT(*) FROM web_offline_track WHERE track_id =" + str(tid)
    count = con.execute(CountText)
    (number_of_rows,) = count.fetchone()
    if number_of_rows == 0:
        return None

    CommandText = "SELECT detail, relative_path, real_suffix FROM web_offline_track WHERE track_id =" + str(tid)
    rows = con.execute(CommandText)
    
    for row in rows:
        ret.detail = json.loads(row[0])
        ret.relative_path = row[1]
        ret.real_suffix = row[2]
    
    return ret

def GetSafeFilename(filename):
    return re.sub('[^\w\-_\. ]', '_', filename)







