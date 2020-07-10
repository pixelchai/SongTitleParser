# SongTitleParser
---

I'm trying to make a program that can parse Title/Artist pairs from YouTube song titles (no matter how dodgy the format)

I haven't yet decided if I'm going to use Machine Learning or just normal techniques, but in any case, I'm gathering a dataset right now.

## Dataset Creation
The dataset is created from tagged song files (which already have correct artist and title tags) and YouTube, using `dataset/gen.py`.
- The script searches YouTube for `<artist name> - <song title>` for each input song file presents the user with the search results.
- The user then selects which search results correspond to the song for each file.<br>
- The program records titles (and YouTube ids) of the selected results, alongside the ground truth artist and song title values for each song
- In this way, we create a dataset of YouTube title - Title/Artist pairs

### Screenshot:
![](res/gen_screenshot.png)