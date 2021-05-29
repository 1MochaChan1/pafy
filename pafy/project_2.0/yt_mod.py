import requests
import json
import re
from bs4 import BeautifulSoup

# Allowing the user to search YouTube for desired videos
def search_content(query):
    search = "https://www.youtube.com/results?search_query="
    text = query    #changes made
    text = list(text.split(" ")) #Let's search for any keyword without returning any Assignment error
    search_query = f"{search}{'+'.join(str(x) for x in text)}"

    # Getting the HTML and JSON texts
    source = requests.get(search_query).text

    soup = BeautifulSoup(source, 'lxml')  # Creating a soup instance
    # Getting the 32nd <script> tag and its contents
    results = soup.find_all('script')[32]

    # Idk how the regex work in this line of code. (will check the tutorial later)
    script = re.search('var ytInitialData = (.+)[,;]{1}', str(results)).group(1) 
    data = json.loads(script)

    meta = (data['contents']['twoColumnSearchResultsRenderer']
            ['primaryContents']['sectionListRenderer']
            # [0] is to go down the tree where itemSectionRenderer is located
            ['contents'][0]['itemSectionRenderer']
            ['contents'])

    videos = {}
    res = []

    # Nested for loops to get the video title and link
    if type(meta) is list:
        for data in meta:
            if type(data) is dict:
                for key, value in data.items():
                    if type(value) is dict:

                        for k,v in value.items():                      
                            if (k == 'videoId') or (k == 'thumbnail') or (k == 'title' and 'runs' in v): #Checks if the key we need are present
                                if type(v) is not dict and len(v) == 11:
                                    #count += 1
                                    link = "https://www.youtube.com/watch?v="+v
                                if type(v) is dict:                       
                                    if 'thumbnails' in v:
                                        if not v['thumbnails'][0]['url'].startswith('//'): #This code is written to avoid getting a channel's thumbnail
                                            thumbs = v['thumbnails'][0]['url']
                                            
                                            
                                    if 'title' and 'runs' in v: 
                                        title = v['runs'][0]['text']
                                        res.append((title, thumbs, link))
    for x in range(len(res)): #Storing the video resources in a dictionary
        videos[x+1] = res[x]

    return videos
    #for k,v in videos.items():
        #print(f"{k}:\t{v[0]}\n\t{v[1]}\n\t{v[2]}\n")   In this way you can print the video data

#print(search_content("mereko toh aisa dhak dhak horela hai"))