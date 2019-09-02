import settings
import shutil

def make_cbz():
    shutil.make_archive('comic','zip',root_dir=settings.IMAGES_PATH)
    shutil.move('comic.zip','comic.cbz')

if __name__ == "__main__":
    make_cbz()