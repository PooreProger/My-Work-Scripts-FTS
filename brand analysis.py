import os
import logging


logging.basicConfig(
    level=logging.DEBUG, 
    filename="brand logz.log", 
    encoding='utf-8', 
    format='%(asctime)s %(levelname)s %(message)s')


PATH_TO_CURRENT_DIR = os.getcwd()
NAME_OF_THE_DATA_DIR = 'brand data dir'
PATH_TO_THE_DATA_DIR = PATH_TO_CURRENT_DIR+'\\'+NAME_OF_THE_DATA_DIR

logging.debug(PATH_TO_CURRENT_DIR)
logging.debug(PATH_TO_THE_DATA_DIR)


def main_algorith():
    pass


if __name__ == '__main__':
    logging.debug("START________________________________________")
    main_algorith
    logging.debug("FINISH_______________________________________")
