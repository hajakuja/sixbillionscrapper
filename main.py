import scrapper
import settings



def main():
    scrapper.read_info()
    while settings.CURL is not None:
        settings.CURL = scrapper.get_chapter()
         
        
    


if __name__ == "__main__":
    main()
    # CURL = 'https://killsixbilliondemons.com/comic/king-of-swords-4-38/'   
    # COUNT = 400
    # write_info()
    # read_info()