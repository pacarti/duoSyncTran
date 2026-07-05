# duoSyncTran
Downloads the user-given Duolingo Podcast from https://podcasts.apple.com, syncs the transcription to it and outputs the .mp3 file of podcast with an .srt file with synced transcription.
<br>Works with French podcasts.
<br><br>
Update 2026: Due to the aeneas compbatibility issues, the scipt was upgraded into the Docker solution, so that it uses older version of Python - 3.11.

## Usage
<code>docker build -t aeneas-legacy .</code>


On Linux:
<code>chmod +x sync.sh</code> 


Then:
<code>./sync.sh "<url_to_podcast>"</code>
<br><br><b>Warning: </b>The podcast URL MUST come from https://podcasts.apple.com
<br><br><br>Example:<br>
<code>python3 duosynctran.py https://podcasts.apple.com/us/podcast/le-grand-pari-the-big-gamble/id1466824259?i=1000534510175</code>
<br>
## How it works
1. The MP3 file of Duolingo Podcast is downloaded from https://podcasts.apple.com url given by user in 2nd command-line argument with yt-dlp.
2. For better captions readibility, the Duolingo cover is removed from that MP3 file.
3. The transcription from Duolingo site is fetched from the link available in description of Apple Podcast website. The raw transcription is saved to .txt file with the same name as downloaded Podcast file.
4. Now, with Aeneas module, the transcription is synced so that the proper words are shown in proper time(like subtitles in movies). The SRT file containing the synced transcription is being then created(with the same name as podcast).
5. Done. Now, if you run your file with media player like mpv, you can run the synced transcription as subtitles of the file.
