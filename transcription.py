import bs4, os, requests

os.chdir(os.path.dirname(os.path.abspath(__file__)))

url = "https://podcasts.apple.com/us/podcast/le-surfeur-sans-limites-the-surfer-without-limits/id1466824259?i=1000445611085"

try:
    res = requests.get(url)
except ConnectionError:
    print('Main Page doesn\'t exist(or connection is to it is refused)!')
    exit()

podcastsAppleSoup = bs4.BeautifulSoup(res.text, 'html.parser')

pElems = podcastsAppleSoup.select('p')

# for pElem in pElems:
#     print(pElem)

# print(pElems[1].getText())

# Split the sentence with link to get link:

linkToTranscription = pElems[1].getText().split()[11].rstrip('.')

# print(linkToTranscription)

try:
    res_transcription = requests.get(linkToTranscription)
except ConnectionError:
    print('Main Page of transcription doesn\'t exist(or connection is to it is refused)!')
    exit()

podcastsTranscriptionSoup = bs4.BeautifulSoup(res_transcription.text, 'html.parser')

pElemsTranscription = podcastsTranscriptionSoup.select('p')

# for pElem in pElemsTranscription:
#     print(pElem.getText())

transcriptionFile = open('transcriptionFile.txt', 'w')

for index, pElem in enumerate(pElemsTranscription):
    if index > 2:
        # print(pElem.getText())
        transcriptionFile.write(pElem.getText())
        transcriptionFile.write('\n\n')

transcriptionFile.close()