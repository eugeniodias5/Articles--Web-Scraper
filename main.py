from ACMDL import ACMDL
from IEEE import IEEE
from Springer import Springer
from ScienceDirect import ScienceDirect
import time

if __name__ == '__main__':

    start_time = time.time()
    ieee = ACMDL()
    ieee.return_data()  

    print(time.time() - start_time)  