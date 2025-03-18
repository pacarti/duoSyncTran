import subprocess, os, requests, bs4, shutil, sys

def fetchTranscription(url, outputFileNoExt):

    try:
        res = requests.get(url)
    except ConnectionError:
        print('Main Page doesn\'t exist(or connection is to it is refused)!')
        exit()

    podcastsAppleSoup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Get a link to the transcription
    pElems = podcastsAppleSoup.select('p')


    for word in pElems[1].getText().split():
        # print(word)
        if word.startswith('https://bit.ly'):
            linkToTranscription = word.rstrip('.')



    try:
        res_transcription = requests.get(linkToTranscription)
    except ConnectionError:
        print('Main Page of transcription doesn\'t exist(or connection is to it is refused)!')
        exit()

    podcastsTranscriptionSoup = bs4.BeautifulSoup(res_transcription.text, 'html.parser')

    pElemsTranscription = podcastsTranscriptionSoup.select('p')

    transcriptionFile = open(outputFileNoExt + '.txt', 'w')

    for index, pElem in enumerate(pElemsTranscription):
        if index > 2:
            transcriptionFile.write(pElem.getText())
            transcriptionFile.write('\n\n')

    transcriptionFile.close()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

url = sys.argv[1]

# Download the podcast(subprocess, yt-dlp)
# 'stdout=subprocess.PIPE' instead of 'capture_output' because capture_output is incompatible with Python 3.6

result = subprocess.run(["yt-dlp", "--print", "filename", url],
stdout=subprocess.PIPE, 
stderr=subprocess.PIPE,
universal_newlines=True) # Ensure output is str, not bytes


filename = result.stdout.strip()

print("Downloading the file %s ..." % filename)

subprocess.run("yt-dlp " + url, shell=True)


outputFileNoExt = filename.split('.mp3')[0]


# Remove the cover

outputFileNoCover = outputFileNoExt + 'NoCover.mp3'

print('Removing the cover...')


removeCoverCmd = 'ffmpeg -i \'%s\' -id3v2_version 3 -vn -c:a copy \'%s\'' % (filename, outputFileNoCover)


subprocess.run(removeCoverCmd, shell=True)


# Remove the original MP3 and rename the NoCover one to its name

os.unlink(filename)

shutil.move(outputFileNoCover, filename)


# Take the transcription from the link(web scraping)
fetchTranscription(url, outputFileNoExt)


# Sync the transcription to the podcast(aeneas)
subprocess.run([
    "python", "-m", "aeneas.tools.execute_task",
    filename,
    outputFileNoExt + '.txt',
    'task_language=eng|is_text_type=plain|os_task_file_format=srt',
    outputFileNoExt + '.srt'
])

print("Done!")