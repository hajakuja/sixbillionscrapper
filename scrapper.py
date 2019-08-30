from bs4 import BeautifulSoup
import requests
import os
import html
import json
import settings


def get_next_url():
    global soup
    # load_soup()
    return soup.select(".navi-next")[0].get('href')

def load_soup():
    global soup
    #print("Url: {}".format(settings.CURL))
    res = requests.get(settings.CURL)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, features='html.parser')

def get_chapter():
    read_info()
    while settings.CURL is not None:
        global soup
        load_soup()
        get_text()
        get_image()
        # settings.CURL = get_image()

def get_image():
    global soup
    # load_soup()
    comicElem = soup.select('#comic img')
    res =  requests.get(comicElem[0].get('src'))
    if comicElem == []:        
        print('Could not find comic image.')    
    else:
        comicUrl = comicElem[0].get('src')        
        # Download the image.
        print('Downloading image {}...'.format(comicUrl))        
        res = requests.get(comicUrl)        
        res.raise_for_status()
        
        # create the directory
        if not os.path.exists(os.path.split(settings.IMAGES_PATH)[0]):
            os.mkdir(os.path.split(settings.IMAGES_PATH)[0])
            os.mkdir(settings.IMAGES_PATH)
        elif not os.path.exists(settings.IMAGES_PATH):
            os.mkdir(settings.IMAGES_PATH)
        
        # comicPath = html.unescape(os.path.basename(comicUrl))
        path = os.path.join(settings.IMAGES_PATH, str(settings.COUNT)+'.jpg') #+ comicPath)
        print("Writing image {}...".format(os.path.basename(path)))
        try:
            imageFile = open(path, 'wb')
        except OSError as e:
            # if e.args[0] is 22:
            #     # comicPath = comicPath[2:]
            #     path = os.path.join('images', str(settings.COUNT)+'.jpg')# + comicPath)
            #     imageFile = open(path, 'wb')
            # else:
            print(e)
            return
        for chunk in res.iter_content(10000):
            imageFile.write(chunk)
        imageFile.close()
        settings.COUNT += 1
        settings.CURL = get_next_url()
        write_info()

def get_text():
    global soup
    # get the alt and content
    alt = soup.select('#comic img')[0].get('alt')
    t = [a.prettify() for a in soup.find_all('div', {'class':'entry'})[0].select('p')]
    text = '<p>AltText: {}</p> \n\n<div><p>Entry(might be empty):</p> \n{}</div>'.format(alt, '\n'.join(t))
    
    # create directory
    if not os.path.exists(os.path.split(settings.ENTRIES_PATH)[0]):
        os.mkdir(os.path.split(settings.ENTRIES_PATH)[0])
        os.mkdir(settings.ENTRIES_PATH)
    elif not os.path.exists(settings.ENTRIES_PATH):
        os.mkdir(settings.ENTRIES_PATH)

    path = os.path.join(settings.ENTRIES_PATH, str(settings.COUNT)+'.html')
    try:
        with open(path, 'w') as textFile:
            textFile.write(text.encode(encoding='UTF-8').decode())
    except OSError as e:
        print(e)
        return

def write_info():
    data = {'url':settings.CURL,  'count':settings.COUNT}
    with open(settings.INFO_PATH, 'w') as file:
        json.dump(data, file)

def read_info():
    if os.path.exists(settings.INFO_PATH):
        with open(settings.INFO_PATH, 'r') as file:
            try:
                data = json.load(file)
                settings.CURL = data['url']
                settings.COUNT = data['count']
            except json.JSONDecodeError as e:
                print(e)
                return
        # settings.CURL = get_next_url()

if __name__ == "__main__":
    get_chapter()