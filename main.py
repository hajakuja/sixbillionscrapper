from bs4 import BeautifulSoup
import requests
import os
import html
import json


COUNT = 0
CURL = 'https://killsixbilliondemons.com/comic/kill-six-billion-demons-chapter-1/'


def get_next_url():
    global soup
    load_soup()
    return soup.select(".navi-next")[0].get('href')

def load_soup():
    global CURL
    global soup
    print("Url: %s" %(CURL))
    res = requests.get(CURL)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, features='html.parser')

def get_chapter():
    global CURL
    global COUNT
    global soup
    load_soup()
    comicElem = soup.select('#comic img')
    res =  requests.get(comicElem[0].get('src'))
    if comicElem == []:        
        print('Could not find comic image.')    
    else:
        comicUrl = comicElem[0].get('src')        
        # Download the image.
        print('Downloading image %s...' % (comicUrl))        
        res = requests.get(comicUrl)        
        res.raise_for_status()
        if not os.path.exists('images'):
            os.mkdir('images')
        comicPath = html.unescape(os.path.basename(comicUrl))
        path = os.path.join('images', str(COUNT) + comicPath)
        print("Writing image %s..." % (os.path.basename(path)))
        try:
            imageFile = open(path, 'wb')
        except OSError as e:
            if e.args[0] is 22:
                comicPath = comicPath[2:]
                path = os.path.join('images', str(COUNT) + comicPath)
                imageFile = open(path, 'wb')
            else:
                print(e)
        for chunk in res.iter_content(10000):
            imageFile.write(chunk)
        imageFile.close()
        COUNT += 1
        write_info()
    return get_next_url()

def write_info():
    global CURL
    global COUNT
    data = {'url':CURL,  'count':COUNT}
    with open('info.json', 'w') as file:
        json.dump(data, file)

def read_info():
    global CURL
    global COUNT
    if os.path.exists('info.json'):
        with open('info.json', 'r') as file:
            data = json.load(file)
            CURL = data['url']
            COUNT = data['count']
    CURL = get_next_url()



def main():
    read_info()
    global CURL
    while CURL is not None:
        CURL = get_chapter()
        global COUNT 
        
    


if __name__ == "__main__":
    main()
    # CURL = 'https://killsixbilliondemons.com/comic/king-of-swords-4-38/'   
    # COUNT = 400
    # write_info()
    # read_info()