import scrapper
import settings
import epubgen


def main():
        scrapper.get_chapter()
        epubgen.make_epub()
         
        
    


if __name__ == "__main__":
    main()
    # CURL = 'https://killsixbilliondemons.com/comic/king-of-swords-4-38/'   
    # COUNT = 400
    # write_info()
    # read_info()