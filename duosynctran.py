import subprocess, os, requests, bs4, shutil

def fetchTranscription(url, outputFileNoExt):

    try:
        res = requests.get(url)
    except ConnectionError:
        print('Main Page doesn\'t exist(or connection is to it is refused)!')
        exit()

    podcastsAppleSoup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Get a link to the transcription
    pElems = podcastsAppleSoup.select('p')

    '''for p in pElems:
        print(p.getText())
        if p.getText().startswith("A transcript"):
            linkToTranscription = p.getText().split()[11].rstrip('.')
            print(linkToTranscription)
            # print(p.getText())'''
    


    # print(pElems[1].getText())

    for word in pElems[1].getText().split():
        # print(word)
        if word.startswith('https://bit.ly'):
            linkToTranscription = word.rstrip('.')


    # linkToTranscription = pElems[1].getText().split()[11].rstrip('.')
    
    # print(linkToTranscription)

    # exit()


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

url = "https://podcasts.apple.com/us/podcast/la-com%C3%A9dienne-de-balcon-the-balcony-performer-revisited/id1466824259?i=1000642573010"
# url = 'https://podcasts.apple.com/us/podcast/le-surfeur-sans-limites-the-surfer-without-limits/id1466824259?i=1000445611085'

# Download the podcast(subprocess, yt-dlp)


# result = subprocess.run(["yt-dlp", "--print", "filename", url], capture_output=True, text=True)

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
# print(removeCoverCmd)

subprocess.run(removeCoverCmd, shell=True)


# Remove the original MP3 and rename the NoCover one to its name

os.unlink(filename)
# print(filename)
# exit()
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

# TODO: Implement an interactive link instead of rigid(with sys.argv)