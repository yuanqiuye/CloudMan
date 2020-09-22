<h1 align="center">CloudMan_Local</h1>
用來為 Sony WalkMan 產生Playlist的工具

# Credit:

[Original CloudMan by isXiaoLin](https://github.com/isXiaoLin/CloudMan)

[The Netease's m3u8 generator by ntzyz](https://ntzyz.io/post/mingrate-from-cloudmusic-to-walkman)

[Python ncmdump by nondanee](https://github.com/nondanee/ncmdump)

# Need:
- Python >= 3.5
- 網易雲WIndows客戶端 (手上沒MacOS沒辦法開發，求有緣人PR XD)

# Config (cm.ini):

```
[general]

# info = 20, debug = 10
loggingLevel = 20

# Netease download folder
cmPath = C:\CloudMusic

# Walkman folder
wmPath = D:\

# Only generate playlists which created by user
onlyUserPlaylist = True

# User ID (Can be found in Netease's share link, like: http://music.163.com/playlist?id=2862806718&userid=416611804)
userId = 416611804

mergeTranslation = False
```

# How ot use:
1. 在網易雲音樂Windows客戶端下載音樂
2. 編輯cm.ini
3. `pip install -r requirements.txt`
4. `python app.py`

# Features:
- 資料直接從網易雲客戶端抓取，無須外接第三方接口
- 自動將ncm轉換格式
- 享受客戶端下載1000kbps以上的高音質音樂 (需要網易雲VIP)
- 自動將音樂和歌詞複製至Walkman，並產生m3u8
- 完美匹配雲盤音樂
