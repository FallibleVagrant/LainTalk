#!/usr/bin/env python3

import requests
import urllib.request
import re

main_url = "https://laingame.net/index.php?id="
for i in range(830):
    r = requests.get(main_url + str(i))
    match_video = re.search(r"https\://.*?\.mp4", r.text)
    if match_video:
        print(f"Getting video id {i} from {match_video.group(0)}.")
        urllib.request.urlretrieve(match_video.group(0), match_video.group(0)[27:])
    else:
        raise IOError("No video to download.")

    match_subtitles = re.search(r"sub\.php.*?lang=en", r.text)
    if match_subtitles:
        print("Found subtitles!")
        urllib.request.urlretrieve("https://laingame.net/" + match_subtitles.group(0), match_video.group(0)[27:-4] + ".vtt")
    else:
        print("No matching subtitles found for video.")
