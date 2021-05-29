import requests
import json
import re
from bs4 import BeautifulSoup

def search_con(query):
    search = "https://www.youtube.com/results?search_query="
    text = query
    text = list(text.split(" "))
    search_query = f"{search}{'+'.join(str(x) for x in text)}"

    source = requests.get(search_query).text



    soup = BeautifulSoup(source, 'lxml')
    script = soup.find_all('script')[32]

    json_text = re.search('var ytInitialData = (.+)[,;]{1}', str(script)).group(1)


    data = json.loads(json_text) #converts json string to dictionary
    meta_data = (data['contents']['twoColumnSearchResultsRenderer']
    ['primaryContents']['sectionListRenderer']
    ['contents'][0]['itemSectionRenderer']
    ['contents'])

    videos = {}
    res = []

    #making global variables to use in the nested loops and conditional statements below
    link, duration, thumbs, title, num, gafla = '','','','', '', ''

    if type(meta_data) is list:

        for data in meta_data:
            if type(data) is dict:

                for key, value in data.items():
                    if type(value) is dict:
                        for k,v in value.items():                       
                            #if (k == 'videoId') or (k == 'thumbnail') or (k == 'title' and 'runs' in v) or (k=='lengthText'): #Checks if the key we need are present
                            if k=='videoId' and type(v) is not dict and len(v) == 11:
                                #count += 1
                                link = "https://www.youtube.com/watch?v="+v

                            if k=='lengthText' and 'simpleText' in v:
                                duration=v['simpleText']
                                num = [int(x) for x in duration.split(":")]
                                if len(num) == 2:
                                    duration=(num[0]*60+num[1])
                                elif len(num) == 2:
                                    duration=(num[0]*3600+num[1]*60+num[0])
                                
                                

                            if type(v) is dict:                       
                                if 'thumbnails' in v:
                                    if not v['thumbnails'][0]['url'].startswith('//'): #This code is written to avoid getting a channel's thumbnail
                                        thumbs = v['thumbnails'][0]['url']
    
                                        
                                if k=='title' and 'runs' in v : 
                                    title = v['runs'][0]['text']
                                    res.append((title, thumbs, link, duration))
                            
    for x in range(len(res)): #Storing the video resources in a dictionary
        videos[x+1] = res[x]
    return videos

print(search_con("mereko toh aisa dhak dhak horela hai"))