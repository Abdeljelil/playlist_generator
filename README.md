# Playlist Generator
**Play List Generator** is a script to make m3u8 playlist from local path,</br>
the Concept is to seek all videos under a given local path and create output as m3u8 file.</br>
*No external Python modules are required to run this script*

### :mag: Looking for all videos for given local path
```
source_dir = "/media/video"
vs = VideoSeeker(source_dir)

video_files = vs.get_videos()
```

### :one: Create play list sorted by the Creation Date
```
m3u8_output = "/tmp/playlist_creation.m3u8"

plg = PlayListGenerator(video_files,SORT_BY_CREATION_DATE)
plg.dump(m3u8_output)
```

### :two: Create play list sorted by the Modification Date
```
m3u8_output = "/tmp/playlist_modification.m3u8"

plg = PlayListGenerator(video_files,SORT_BY_MODIFICATION_DATE)
plg.dump(m3u8_output)
```

### :three: Create play list sorted by the last access date
```
m3u8_output = "/tmp/playlist_access.m3u8"

plg = PlayListGenerator(video_files,SORT_BY_LAST_ACCESS_DATE)
plg.dump(m3u8_output)
```

### :four: Create play list sorted by Size
```
m3u8_output = "/tmp/playlist_size.m3u8"

plg = PlayListGenerator(video_files,SORT_BY_SIZE)
plg.dump(m3u8_output)
```
