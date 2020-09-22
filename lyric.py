import re
import config
from math import floor

def modifyLyric(str, type = 0):
    regex = r'\[(\d+):(\d+)[.:](\d+)\]'
    modified = []
    lines = str.split('\n')

    for line in lines:
        match = re.search(regex, line)
        if not match:
             continue
        
        time = 0
        if int(match.group(1)) * 60 + int(match.group(2)) + float('0.' + match.group(3)) - 0.05 >= 0:
            time = int(match.group(1)) * 60 + int(match.group(2)) + float('0.' + match.group(3)) - 0.05
        else:
            time = int(match.group(1)) * 60 + int(match.group(2)) + float('0.' + match.group(3))

        modified.append({
            "time" : time,
            "type" : type,
            "content" : line.replace(match.group(0), '').strip()
        })
 
    return modified

def generateLyric(lyricData):
    lyricModified = []
    lyricModified += modifyLyric(lyricData["lrc"]["lyric"])
    if lyricData["tlyric"] and "lyric" in lyricData["tlyric"] and lyricData["tlyric"]["lyric"]:
        lyricModified += modifyLyric(lyricData["tlyric"]["lyric"], 1)
    
    lyricModified.sort(key=lambda x: (x["time"], x["type"]))

    for i, lyric in enumerate(lyricModified):
        if lyric["type"] == 0 or i == 0 or lyricModified[i - 1]["type"] == 1 or lyricModified[i - 1]["time"] != lyric["time"]: 
            continue
    
        if config.parseCfg("mergeTranslation") == "True":
            lyricModified[i - 1]["content"] += ' - ' + lyric["content"]
        elif i == len(lyricModified) - 1:
            if lyric["content"] != '':
                lyric["time"] += 100
        else:
            lyric["time"] = lyricModified[i + 1]["time"]
        
        lyricModified[i] = lyric
    
    if config.parseCfg("mergeTranslation") == "True":
        lyricModified = [lyric for lyric in lyricModified if lyric["type"] == 0]

    lyric = []
    
    for info in lyricModified:
        hour = str(floor(info["time"] / 60))
        if len(hour) == 1:
            hour = '0' + hour
        
        sec = str(floor(info["time"] % 60))
        if len(sec) == 1:
            sec = '0' + sec

        micsec = format(info["time"], '0.2f')
        micsec = micsec.split('.')[-1] or '00'
        if len(micsec) == 1:
            micsec = micsec + '0'
        
        time = "[{}:{}.{}]".format(hour, sec, micsec)
        lyric.append(time + info["content"])
    return "\n".join(lyric)
        

