from Scraper import Scraper
from ScienceDirect import ScienceDirect
from ACMDL import ACMDL
from IEEE import IEEE
from Springer import Springer
from ScienceDirect import ScienceDirect

if __name__ == '__main__':
    iee = ACMDL()
    #print(springer.return_titles())
    for title in iee.return_titles():
        print(title)
