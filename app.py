# Python ≥ 3.5
import config
import cm_structure
import lyric
import os, errno
import json
from pathlib import Path
import shutil
import operator
import logging
from ncmdump import dump
import importlib
marker = importlib.import_module('163marker')

LOGGING_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
DATE_FORMAT = '%H:%M:%S'
logging.basicConfig(level=int(config.parseCfg("loggingLevel")),
                    format=LOGGING_FORMAT,
                    datefmt=DATE_FORMAT)
logging.debug("Logging's setting is OK!")

cmPath = os.path.normpath(config.parseCfg("cmPath"))
wmPath = os.path.normpath(config.parseCfg("wmPath"))
playlistPath = os.path.join(wmPath, "MUSIC", "CloudMan_Local")
dataPath = os.path.join(wmPath, "MUSIC", "CloudMan_Local", "MUSIC")

localAppData = os.getenv("LOCALAPPDATA")
lrcPath = os.path.normpath(localAppData + "\\Netease\\CloudMusic\\webdata\\lyric")
playlists = cm_structure.FetchPlaylist()
logging.debug(playlists)
n = 1

try:
    Path(os.path.join(wmPath, "MUSIC", "CloudMan_Local", "MUSIC")).mkdir(parents=True, exist_ok=True)
except OSError as e:
    if e.errno != errno.EEXIST:
        logging.critical("An error happened when creating folder for WalkMan!")
        raise
logging.debug("Creating folder for WalkMan successfully!")

for playlist in playlists:
    logging.info("Processing playlist: {}".format(playlist.playlist["name"]))
    songCount = 0
    skippedCount = 0
    m3u8 = ""
    songs = cm_structure.FetchPlaylistSongs(playlist.pid)
    skippedReasons = []

    if len(songs) == 0:
        continue

    for song in songs:
        detail = cm_structure.FetchSongDetial(song)

        if detail == None:
            skippedReasons.append(cm_structure.FailedRecords(song, "Detail data not found."))
            skippedCount += 1
            logging.debug("{} Detail data not found.".format(song))
            continue

        if detail.relative_path == "":
            skippedReasons.append(cm_structure.FailedRecords(detail.detail["name"], "Relative path is empty."))
            skippedCount += 1
            logging.debug("{} Relative path is empty.".format(detail.detail["name"]))
            continue
        
        if not os.path.isfile(os.path.join(cmPath, detail.relative_path)):
            skippedReasons.append(cm_structure.FailedRecords(detail.detail["name"], "Relative path is not a file."))
            skippedCount += 1
            logging.debug("{} Relative path is not a file.".format(detail.detail["name"]))
            continue

        if detail.relative_path[-3:] == "ncm":
            logging.debug("{} ncm founded!".format(detail.detail["name"]))
            ncmPath = os.path.join(cmPath, detail.relative_path.replace('\\', '/'))
            detail.relative_path = detail.relative_path.replace("ncm", detail.real_suffix)
            dumpPath = os.path.join(cmPath, detail.relative_path.replace('\\', '/'))

            dump(ncmPath, dumpPath)
            logging.debug("{} dump successfully!".format(detail.detail["name"]))
            #logging.info("{} strat to parse!".format(detail.detail["name"]))
            #metadata = marker.parse("https://music.163.com/api/song/detail?id=" + str(song))
            #marker.mark(dumpPath, metadata)
            #logging.info("{} mark successfully!\n".format(detail.detail["name"]))

        wm_songPath = os.path.join(dataPath, detail.relative_path.replace('\\', '/'))
        cm_songPath = os.path.join(cmPath, detail.relative_path.replace('\\', '/'))

        if os.path.isfile(os.path.join(lrcPath, str(song))):
            lrcJson = ""
            f = open(os.path.join(lrcPath, str(song)), encoding='utf-8',mode ="r")
            if f.mode == 'r':
                lrcJson = f.read()
            lrc = json.loads(lrcJson)

            if not('nolyric' in lrc and lrc["nolyric"] == True):
                text = lyric.generateLyric(lrc)
                f = open("".join(wm_songPath.split(".")[:-1])+".lrc", encoding='utf-8', mode ="w+")
                f.write(text)
                f.close()
        
        songCount += 1
        m3u8 += "#EXTINF:" + str(detail.detail["duration"]) + "," + str(detail.detail["name"]) + "\n"
        m3u8 += wm_songPath + "\n\n"

        if not os.path.isfile(wm_songPath):
            shutil.copyfile(cm_songPath, wm_songPath)

    if songCount == 0:
        logging.info("Playlist: {} has 0 songs!\n".format(playlist.playlist["name"]))
        continue

    f = open(os.path.join(playlistPath, str(n).rjust(2,'0') + ". " + cm_structure.GetSafeFilename(playlist.playlist["name"]) + ".m3u8"), encoding='utf-8',mode ="w+")
    f.write(m3u8)
    f.close()
    logging.info("Finish generating playlist: {}, Songs count: {}, Skipped count: {}".format(playlist.playlist["name"], songCount, skippedCount))
    if skippedCount != 0:
        for i in range(skippedCount if skippedCount <= 5 else 5):
            logging.info("Track ID: {}, Reason: {}".format(skippedReasons[i].tid, skippedReasons[i].reason))
    
    n += 1
    logging.info("")

logging.info("Finished!")
