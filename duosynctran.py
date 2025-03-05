import subprocess, os
# from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

url = "https://podcasts.apple.com/us/podcast/le-surfeur-sans-limites-the-surfer-without-limits/id1466824259?i=1000445611085"

# Download the podcast(subprocess, yt-dlp)



result = subprocess.run(["yt-dlp", "--print", "filename", url] ,capture_output=True, text=True)

filename = result.stdout.strip()

print("Downloading the file %s ..." % filename)

subprocess.run("yt-dlp " + url, shell=True)

# print(result)

# print("File " + filename + "downloaded.")

# exit()
# Remove the cover from mp3 file(subprocess ffmpeg
# pFilename = 
outputFileNoExt = filename.split('.mp3')[0]

# print(outputFileNoExt)

# exit()

outputFileNoCover = outputFileNoExt + 'NoCover.mp3'

print('Removing the cover...')

subprocess.run('ffmpeg -i %s -id3v2_version 3 -vn -c:a copy %s' % (filename, outputFileNoCover), shell=True)

# TODO: Take the transcription from the link(web scraping)
# TODO: Apply the transcription to the podcast(aeneas)
# TODO: Apply the output srt to the mp3 file(ffmpeg)