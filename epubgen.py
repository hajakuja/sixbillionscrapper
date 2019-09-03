from jinja2 import Environment, PackageLoader
import zipfile
import settings
import os
import shutil
import json

env = Environment(
    loader=PackageLoader('epubgen', 'epub_templates')
    )

chapters = []

def make_epub():
    if not os.path.exists('epub'):
        os.mkdir('epub')
    load_settings()  
    load_chapters()  
    make_meta()
    make_oepbs()
    make_file()

    # finally delete the temp folder 
    # shutil.rmtree('epub')

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

def load_chapters():
    # global chapters
    if not os.path.exists(settings.IMAGES_PATH):
        return 'The images couldn\'t be found!'
    if not os.path.exists(settings.ENTRIES_PATH) and settings.INCLUDE_ENTRIES:
        return 'The entries couldn\'t be found!'
    
    # The first two checks should always be False
    if not os.path.exists('epub'):
        os.mkdir('epub')
    if not os.path.exists('epub/OPS'):
        os.mkdir('epub/OPS')
    if not os.path.exists('epub/OPS/images'):
        os.mkdir('epub/OPS/images')

    # for src in os.listdir(settings.IMAGES_PATH):
    #     shutil.copyfile(settings.IMAGES_PATH+src, 'epub/OPS/images/'+src)



    for i in range(settings.COUNT):
        chapters.append({'link':'page-{}.xhtml'.format(i),
                        'id':'page-{}'.format(i),
                        'play_order':i,
                        'title':'page-{}'.format(i),
                        'image_link':'images/{}.{}'.format(i, 'jpg'), 
                        'img_id':"img-{}".format(i)
                        })

#mimetype as well 
def make_meta():
    
    if not os.path.exists('epub'):
        os.mkdir('epub')
    with open('epub/mimetype', 'w') as mime:
        mime.write('application/epub+zip')
    if not os.path.exists('epub/META-INF'):
        os.mkdir('epub/META-INF')
    
    shutil.copyfile(r'epub_templates\container.xml',r'epub\META-INF\container.xml')
    shutil.copyfile(r'epub_templates\com.apple.ibooks.display-options.xml',r'epub\META-INF\com.apple.ibooks.display-options.xml')

def make_oepbs():  
    if not os.path.exists('epub'):
        os.mkdir('epub')
    if not os.path.exists('epub/OPS'):
        os.mkdir('epub/OPS')
    
    load_chapters()

    make_opf()
    make_pages()
    make_ncx()

def make_opf():
    template = env.get_template('opf.xml')
    with open('epub/OPS/content.opf', 'w') as opf:
        opf.write(template.render(
                    title=settings.TITLE, creator=settings.CREATOR, language = settings.LANGUAGE,
                    uid=settings.UID, chapters=chapters
                ))

def make_ncx():
    template = env.get_template('toc_ncx.xml')
    with open('epub/OPS/content.ncx','w') as ncx:
        ncx.write(template.render(
            name = settings.TITLE,
            chapters=chapters,
        ))

def make_pages():
    if not os.path.exists('epub/OPS/css'):
        os.mkdir('epub/OPS/css')

    shutil.copy('epub_templates/style.css', 'epub/OPS/css')

    position = ('rightspread', 'leftspread')

    entry = ''
    template = env.get_template('page.html')
    for chapter in chapters:
        if settings.INCLUDE_ENTRIES:
            entry = open(settings.ENTRIES_PATH + str(chapter['play_order']) + '.html', 'r', encoding='utf-8').read()

        with open('epub/OPS/{}.xhtml'.format(chapter['id']), 'w') as  page:
            page.write(template.render(
                name  = settings.TITLE,
                page_id = chapter['id'],
                image_link = chapter['image_link'],
                pos = position[chapter['play_order']%2],
                entries = settings.INCLUDE_ENTRIES,
                entry = entry,
            ))
    
def make_file():
    # ziph = zipfile.ZipFile('comic.epub', 'w', zipfile.ZIP_DEFLATED)
    # for root, dirs, files in os.walk('epub'):
    #     for file in files:
    #         ziph.write(os.path.join(root, file))
    shutil.make_archive('comic', 'zip',root_dir='epub',)
    shutil.move('comic.zip', 'comic.epub')
if __name__ == "__main__":
    # temp for test
   make_epub()