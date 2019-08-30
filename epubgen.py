from jinja2 import Environment, FileSystemLoader
from zipfile import ZipFile
import settings
import os
import shutil

def make_epub():

    load_settings()    
    make_meta()
    make_oepbs()
    make_file()

    # finally delete the temp folder 
    shutil.rmtree('epub')

def load_settings():
    if os.path.exists(settings.INFO_PATH):
        with open(settings.INFO_PATH, 'r') as file:
            try:
                data = json.load(file)
                settings.CURL = data['url']
                settings.COUNT = data['count']
            except json.JSONDecodeError as e:
                print(e)
                return
    else:
        raise IOError('info.json couldn\'t be found, maybe the scrapper didn\'t run?')

#mimetype as well 
def make_meta():
    
    if not os.path.exists('epub'):
        os.mkdir('epub')
    with open('epub/mimetype', 'w') as mime:
        mime.write('application/epub+zip')
    if not os.path.exists('epub/META-INF'):
        os.mkdir('epub/META-INF')
    
    shutil.copyfile(r'epub_templates\container.xml',r'epub\META-INF\container.xml')


def make_oepbs():
    pass

def make_file():
    pass

if __name__ == "__main__":
    make_meta()