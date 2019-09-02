# global COUNT
# global CURL 
# global INFO_PATH
# global IMAGES_PATH
# global ENTRIES_PATH
# global INCLUDE_ENTRIES
import datetime 
import random

CREATOR = 'Abbadon'
TITLE = 'Kill Six Billion Demons'
LANGUAGE = 'EN'
UID = 'killsixbilliondemons.com'+str(random.randint(100,10000))
DATE = str(datetime.date.today())
INCLUDE_ENTRIES = True

COUNT = 0
CURL = 'https://killsixbilliondemons.com/comic/kill-six-billion-demons-chapter-1/'

INFO_PATH = r'downloaded/info.json'

#TODO(URAN): make this better 
# MUST BE TWO LEVELS DEEP, SO ./A/B/C IS NOT GOOD NEITHER IS ./A 
IMAGES_PATH = r'./downloaded/images/'
ENTRIES_PATH = r'./downloaded/entries/'