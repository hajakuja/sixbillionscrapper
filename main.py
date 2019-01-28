from bs4 import BeautifulSoup
import requests
import os
count = 0
def get_chapter(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, features='html.parser')
    nextUrl = soup.select(".navi-next")[0].get('href')
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
        path = os.path.join('images', str(count) + os.path.basename(comicUrl))
        print("Writing image %s..." % (os.path.basename(path)))
        imageFile = open(path, 'wb')
        for chunk in res.iter_content(10000):
            imageFile.write(chunk)
        imageFile.close()
    return nextUrl


def main():
    url = 'https://killsixbilliondemons.com/comic/kill-six-billion-demons-chapter-1/'
    while url is not None:
        url = get_chapter(url)
        global count 
        count += 1

    
    


if __name__ == "__main__":
    main()